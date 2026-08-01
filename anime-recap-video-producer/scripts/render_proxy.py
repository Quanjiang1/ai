Exit code: 0
Wall time: 0.2 seconds
Output:
"""Render one low-resolution proxy directly from the source edit list."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

from build_recap_assets import clips_json_bytes
from validate_project import validate_project


def verify_clips_derivative(job_root: Path) -> None:
    """Require clips.json to be the byte-exact deterministic plan derivative."""
    plan = json.loads((job_root / "recap-plan.json").read_text(encoding="utf-8"))
    clips_path = job_root / "clips.json"
    if clips_path.read_bytes() != clips_json_bytes(plan):
        raise ValueError("clips.json is not the exact deterministic derivative of recap-plan.json")


def source_identity(job_root: Path) -> dict:
    """Return the render source's resolved path and cheap filesystem identity."""
    project = json.loads((job_root / "project.json").read_text(encoding="utf-8"))
    source = Path(project["source"]).expanduser()
    if not source.is_absolute():
        source = job_root / source
    source = source.resolve()
    stat = source.stat()
    return {"path": str(source), "size": stat.st_size, "mtime_ns": stat.st_mtime_ns}


def plan_fingerprint(job_root: Path) -> str:
    """Hash the approved edit inputs that affect the proxy or final render."""
    verify_clips_derivative(job_root)
    digest = hashlib.sha256()
    for relative in (
        "project.json",
        "recap-plan.json",
        "clips.json",
        "build/captions.ass",
        "build/voiceover.mp3",
    ):
        path = job_root / relative
        digest.update(relative.encode())
        digest.update(path.read_bytes())
    digest.update(b"source_identity")
    digest.update(
        json.dumps(source_identity(job_root), sort_keys=True, separators=(",", ":")).encode("utf-8")
    )
    return digest.hexdigest()


def sha256_file(path: Path) -> str:
    with path.open("rb") as file:
        return hashlib.file_digest(file, "sha256").hexdigest()


def proxy_render_record(proxy: Path, input_fingerprint: str) -> dict:
    """Describe the exact proxy bytes produced from one stable input state."""
    return {
        "plan_fingerprint": input_fingerprint,
        "proxy_path": str(proxy.resolve()),
        "proxy_size": proxy.stat().st_size,
        "proxy_sha256": sha256_file(proxy),
    }


def atomic_write_json(path: Path, value: dict) -> None:
    """Atomically publish JSON within its destination directory."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as file:
            json.dump(value, file, indent=2)
            file.write("\n")
            temporary_path = Path(file.name)
        os.replace(temporary_path, path)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def ffmpeg_filter_path(path: Path) -> str:
    return str(path.resolve()).replace("\\", "/").replace(":", r"\:").replace("'", r"\'")


def build_timeline_graph(clips: list[dict], width: int, height: int, bed_gain_db: str) -> str:
    count = len(clips)
    video_labels = "".join(f"[vs{index}]" for index in range(count))
    audio_labels = "".join(f"[as{index}]" for index in range(count))
    graph = [
        f"[0:v]split={count}{video_labels}",
        f"[0:a]asplit={count}{audio_labels}",
    ]
    joined = []
    for index, clip in enumerate(clips):
        source_in = float(clip["source_in"])
        duration = float(clip.get("target_seconds", float(clip["source_out"]) - source_in))
        graph.append(
            f"[vs{index}]trim=start={source_in:.3f}:duration={duration:.3f},"
            f"setpts=PTS-STARTPTS,scale={width}:{height}:flags=lanczos,setsar=1[v{index}]"
        )
        graph.append(
            f"[as{index}]atrim=start={source_in:.3f}:duration={duration:.3f},"
            f"asetpts=PTS-STARTPTS,aresample=48000[a{index}]"
        )
        joined.append(f"[v{index}][a{index}]")
    graph.append("".join(joined) + f"concat=n={count}:v=1:a=1[vcat][acat]")
    graph.append(f"[acat]volume={bed_gain_db}[aout]")
    return ";".join(graph)


def build_proxy_command(project_path: Path, fps: str | None = None) -> list[str]:
    if project_path.is_file():
        report = validate_project(project_path)
        project, clips, media = report["project"], report["clips"], report["media"]
        source = Path(project["source"])
        output = project_path.parent / "build" / "proxy.mp4"
        width, height = project["proxy"]["width"], project["proxy"]["height"]
        gain = f"{project['audio']['source_bed_gain_db']}dB"
        fps = fps or media["fps"]
        voice = project_path.parent / "build" / "voiceover.mp3"
        captions = project_path.parent / "build" / "captions.ass"
    else:
        source, output = Path("episode.mp4"), Path("proxy.mp4")
        clips = [{"source_in": 0.0, "source_out": 1.0, "target_seconds": 1.0}]
        width, height, gain, fps = 960, 540, "-22dB", fps or "24000/1001"
        voice, captions = Path("build/voiceover.mp3"), Path("build/captions.ass")
    graph = build_timeline_graph(clips, width, height, gain)
    total_duration = sum(
        float(clip.get("target_seconds", float(clip["source_out"]) - float(clip["source_in"])))
        for clip in clips
    )
    subtitle_filter = f"subtitles=filename='{ffmpeg_filter_path(captions)}'"
    graph += (
        f";[vcat]{subtitle_filter}[vout]"
        ";[1:a]aresample=48000,highpass=f=80,lowpass=f=15000[voice]"
        ";[aout][voice]amix=inputs=2:duration=longest:dropout_transition=0,"
        f"atrim=duration={total_duration:.3f},asetpts=PTS-STARTPTS[mix]"
    )
    return [
        "ffmpeg", "-hide_banner", "-loglevel", "warning", "-y",
        "-i", str(source), "-i", str(voice), "-filter_complex", graph,
        "-map", "[vout]", "-map", "[mix]", "-sn", "-r", fps,
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "28", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "96k", "-ar", "48000", "-movflags", "+faststart",
        str(output),
    ]


def render_proxy(project_path: Path) -> Path:
    project_path = project_path.resolve()
    job_root = project_path.parent
    manifest_path = job_root / "build" / "proxy-render.json"
    manifest_path.unlink(missing_ok=True)
    build_fingerprint = plan_fingerprint(job_root)
    command = build_proxy_command(project_path)
    output = Path(command[-1])
    output.parent.mkdir(parents=True, exist_ok=True)
    input_fingerprint = plan_fingerprint(job_root)
    if input_fingerprint != build_fingerprint:
        raise ValueError("inputs changed while preparing proxy render")
    subprocess.run(command, check=True)
    try:
        completed_fingerprint = plan_fingerprint(job_root)
    except (FileNotFoundError, ValueError, KeyError, json.JSONDecodeError) as error:
        raise ValueError("inputs changed during proxy render") from error
    if completed_fingerprint != input_fingerprint:
        raise ValueError("inputs changed during proxy render")
    atomic_write_json(manifest_path, proxy_render_record(output, input_fingerprint))
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    args = parser.parse_args()
    print(render_proxy(args.project))


if __name__ == "__main__":
    main()

