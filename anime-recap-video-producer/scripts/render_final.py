Exit code: 0
Wall time: 0.2 seconds
Output:
"""Render a single high-quality 1080p master after proxy approval."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess

from render_proxy import build_timeline_graph, plan_fingerprint, sha256_file
from validate_project import validate_project


def ffmpeg_filter_path(path: Path) -> str:
    return str(path.resolve()).replace("\\", "/").replace(":", r"\:").replace("'", r"\'")


def stage_fonts(destination: Path) -> Path:
    destination.mkdir(parents=True, exist_ok=True)
    for name in ("msyh.ttc", "msyhbd.ttc"):
        source = Path(r"C:\Windows\Fonts") / name
        if not source.is_file():
            raise FileNotFoundError(source)
        target = destination / name
        if not target.is_file() or target.stat().st_size != source.stat().st_size:
            shutil.copy2(source, target)
    return destination


def build_audio_graph(clips: list[dict], bed_gain_db: str) -> str:
    count = len(clips)
    labels = "".join(f"[as{index}]" for index in range(count))
    graph = [f"[0:a]asplit={count}{labels}"]
    outputs = []
    for index, clip in enumerate(clips):
        source_in = float(clip["source_in"])
        duration = float(clip.get("target_seconds", float(clip["source_out"]) - source_in))
        graph.append(
            f"[as{index}]atrim=start={source_in:.3f}:duration={duration:.3f},"
            f"asetpts=PTS-STARTPTS,aresample=48000[a{index}]"
        )
        outputs.append(f"[a{index}]")
    graph.append("".join(outputs) + f"concat=n={count}:v=0:a=1[acat]")
    graph.append(f"[acat]volume={bed_gain_db}[aout]")
    return ";".join(graph)


def selected_duration(clips: list[dict]) -> float:
    return sum(
        float(clip.get("target_seconds", float(clip["source_out"]) - float(clip["source_in"])))
        for clip in clips
    )


def build_loudness_mix_graph(total_duration: float, loudnorm_filter: str) -> str:
    """Build the shared voice/mix/trim chain used by both loudness passes."""
    return (
        ";[1:a]aresample=48000,highpass=f=80,lowpass=f=15000,"
        "acompressor=threshold=-18dB:ratio=3:attack=5:release=80[voice]"
        ";[aout][voice]amix=inputs=2:duration=longest:dropout_transition=0,"
        f"atrim=duration={total_duration:.3f},asetpts=PTS-STARTPTS,"
        f"{loudnorm_filter}[mix]"
    )


def build_final_command(
    source: Path,
    voice: Path,
    captions: Path,
    output: Path,
    clips: list[dict],
    fps: str,
    loudnorm_filter: str,
    bed_gain_db: str = "-22dB",
    fontsdir: Path | None = None,
) -> list[str]:
    timeline = build_timeline_graph(clips, 1920, 1080, bed_gain_db)
    total_duration = selected_duration(clips)
    fontsdir = fontsdir or captions.parent / "ass-fonts"
    subtitle_filter = (
        f"subtitles=filename='{ffmpeg_filter_path(captions)}':"
        f"fontsdir='{ffmpeg_filter_path(fontsdir)}'"
    )
    graph = (
        timeline
        + f";[vcat]{subtitle_filter}[vout]"
        + build_loudness_mix_graph(total_duration, loudnorm_filter)
    )
    return [
        "ffmpeg", "-hide_banner", "-loglevel", "warning", "-y",
        "-i", str(source), "-i", str(voice),
        "-filter_complex", graph, "-map", "[vout]", "-map", "[mix]", "-r", fps,
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart",
        str(output),
    ]


def measure_loudnorm(source: Path, voice: Path, clips: list[dict], bed_gain_db: str) -> dict:
    graph = build_audio_graph(clips, bed_gain_db)
    graph += build_loudness_mix_graph(
        selected_duration(clips),
        "loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json",
    )
    result = subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "info", "-i", str(source), "-i", str(voice),
         "-filter_complex", graph, "-map", "[mix]", "-f", "null", "NUL"],
        check=True, capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    match = re.search(r'\{\s*"input_i".*?\n\}', result.stderr, re.DOTALL)
    if not match:
        raise RuntimeError("loudnorm analysis did not return JSON")
    return json.loads(match.group(0))


def second_pass(stats: dict) -> str:
    return (
        "loudnorm=I=-14:TP=-1.5:LRA=9:"
        f"measured_I={stats['input_i']}:measured_TP={stats['input_tp']}:"
        f"measured_LRA={stats['input_lra']}:measured_thresh={stats['input_thresh']}:"
        f"offset={stats['target_offset']}:linear=true"
    )


def require_current_proxy_approval(job_root: Path) -> None:
    approval_path = job_root / "build" / "proxy-approval.json"
    if not approval_path.is_file():
        raise ValueError("proxy approval is missing")
    approval = json.loads(approval_path.read_text(encoding="utf-8"))
    try:
        current_fingerprint = plan_fingerprint(job_root)
    except (FileNotFoundError, ValueError, KeyError, json.JSONDecodeError) as error:
        raise ValueError("proxy approval is stale for the current plan") from error
    if approval.get("plan_fingerprint") != current_fingerprint:
        raise ValueError("proxy approval is stale for the current plan")
    proxy = job_root / "build" / "proxy.mp4"
    if not proxy.is_file():
        raise ValueError("proxy approval is invalid: build/proxy.mp4 is missing")
    if approval.get("proxy_path") != str(proxy.resolve()):
        raise ValueError("proxy approval is invalid for build/proxy.mp4")
    if approval.get("proxy_size") != proxy.stat().st_size:
        raise ValueError("proxy approval is stale for the current proxy")
    if approval.get("proxy_sha256") != sha256_file(proxy):
        raise ValueError("proxy approval is stale for the current proxy")


def render_final(project_path: Path) -> Path:
    project_path = project_path.resolve()
    root = project_path.parent
    require_current_proxy_approval(root)
    report = validate_project(project_path)
    project, clips, media = report["project"], report["clips"], report["media"]
    source = Path(project["source"])
    voice = root / "build" / "voiceover.mp3"
    captions = root / "build" / "captions.ass"
    proxy = root / "build" / "proxy.mp4"
    if not proxy.is_file():
        raise FileNotFoundError("proxy approval gate: build/proxy.mp4 is missing")
    for path in (voice, captions):
        if not path.is_file():
            raise FileNotFoundError(path)
    gain = f"{project['audio']['source_bed_gain_db']}dB"
    fontsdir = stage_fonts(root / "build" / "ass-fonts")
    stats = measure_loudnorm(source, voice, clips, gain)
    output = root / "build" / "final.mp4"
    command = build_final_command(
        source, voice, captions, output, clips, media["fps"], second_pass(stats), gain, fontsdir
    )
    subprocess.run(command, check=True)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    args = parser.parse_args()
    print(render_final(args.project))


if __name__ == "__main__":
    main()

