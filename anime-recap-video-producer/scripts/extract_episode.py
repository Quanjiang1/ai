Exit code: 0
Wall time: 0.1 seconds
Output:
"""Extract searchable subtitles and a compact set of episode reference frames."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


def source_fingerprint(
    source: Path, subtitle_index: int, scene_threshold: float, interval: int
) -> str:
    """Return a cheap cache key for the source and extraction configuration."""
    stat = source.resolve().stat()
    payload = {
        "path": str(source.resolve()),
        "size": stat.st_size,
        "mtime_ns": stat.st_mtime_ns,
        "subtitle_index": subtitle_index,
        "scene_threshold": round(scene_threshold, 3),
        "fallback_interval_seconds": interval,
    }
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def build_subtitle_command(source: Path, stream_index: int, target: Path) -> list[str]:
    return [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(source), "-map", f"0:{stream_index}", "-c:s", "srt", str(target),
    ]


def build_scene_command(source: Path, pattern: Path, threshold: float) -> list[str]:
    vf = f"select='gt(scene\\,{threshold:.3f})',showinfo,scale=480:-2"
    return [
        "ffmpeg", "-hide_banner", "-loglevel", "info", "-y",
        "-i", str(source), "-an", "-sn", "-vf", vf, "-vsync", "vfr", str(pattern),
    ]


def build_fallback_command(source: Path, pattern: Path, interval: int) -> list[str]:
    """Build the evenly-spaced frame fallback without affecting source media."""
    return [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source),
        "-an", "-sn", "-vf", f"fps=1/{interval},scale=480:-2", str(pattern),
    ]


def _scene_times(log: str) -> list[float]:
    return [float(value) for value in re.findall(r"pts_time:([\-0-9.]+)", log)]


def _frame_manifest(frames: Path) -> list[dict[str, int | str]]:
    return [
        {"name": frame.name, "size": frame.stat().st_size}
        for frame in sorted(frames.glob("*.jpg"))
    ]


def _outputs_exist(
    subtitle: Path, scenes: Path, frames: Path, contact_sheet: Path, cache: dict
) -> bool:
    manifest = cache.get("frame_manifest")
    return (
        subtitle.is_file()
        and scenes.is_file()
        and contact_sheet.is_file()
        and bool(manifest)
        and _frame_manifest(frames) == manifest
    )


def build_contact_sheet_command(pattern: Path, target: Path) -> list[str]:
    return [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-framerate", "1", "-start_number", "1", "-i", str(pattern),
        "-frames:v", "1", "-vf", "scale=240:-2,tile=4x3", str(target),
    ]


def _representative_frames(frames: Path, count: int = 12) -> list[Path]:
    available = sorted(frames.glob("*.jpg"))
    if not available:
        raise ValueError("no extracted frames available for contact sheet")
    if count == 1:
        return [available[0]]
    return [
        available[round(index * (len(available) - 1) / (count - 1))]
        for index in range(count)
    ]


def _write_contact_sheet(frames: Path, target: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="contact-sheet-", dir=frames.parent) as staging:
        staging_dir = Path(staging)
        for index, source in enumerate(_representative_frames(frames), start=1):
            shutil.copy2(source, staging_dir / f"frame-{index:05d}.jpg")
        subprocess.run(
            build_contact_sheet_command(staging_dir / "frame-%05d.jpg", target),
            check=True,
        )


def extract_episode(job_dir: Path) -> dict:
    """Extract analysis assets, reusing a complete matching cached extraction."""
    job_dir = job_dir.expanduser().resolve()
    project = json.loads((job_dir / "project.json").read_text(encoding="utf-8"))
    analysis_dir = job_dir / "build" / "analysis"
    episode = json.loads((analysis_dir / "episode.json").read_text(encoding="utf-8"))
    analysis = project["analysis"]
    source = Path(project["source"])
    subtitle_index = int(episode["subtitle_stream_index"])
    threshold = float(analysis["scene_threshold"])
    interval = int(analysis["fallback_interval_seconds"])
    fingerprint = source_fingerprint(source, subtitle_index, threshold, interval)

    subtitle = analysis_dir / "source.srt"
    scenes = analysis_dir / "scenes.json"
    frames = analysis_dir / "frames"
    contact_sheet = analysis_dir / "contact-sheet.jpg"
    cache_path = analysis_dir / "cache.json"
    if cache_path.is_file():
        cache = json.loads(cache_path.read_text(encoding="utf-8"))
        if cache.get("fingerprint") == fingerprint and _outputs_exist(
            subtitle, scenes, frames, contact_sheet, cache
        ):
            return {"fingerprint": fingerprint, "cached": True}

    analysis_dir.mkdir(parents=True, exist_ok=True)
    cache_path.unlink(missing_ok=True)
    if frames.exists():
        shutil.rmtree(frames)
    frames.mkdir()
    subprocess.run(build_subtitle_command(source, subtitle_index, subtitle), check=True)
    scene_result = subprocess.run(
        build_scene_command(source, frames / "scene-%05d.jpg", threshold),
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    times = _scene_times(scene_result.stderr)
    fallback_used = len(list(frames.glob("*.jpg"))) < 12
    if fallback_used:
        subprocess.run(
            build_fallback_command(source, frames / "fallback-%05d.jpg", interval), check=True
        )
    scenes.write_text(
        json.dumps(
            {"scene_times": times, "fallback_used": fallback_used},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    _write_contact_sheet(frames, contact_sheet)
    cache_path.write_text(
        json.dumps(
            {"fingerprint": fingerprint, "frame_manifest": _frame_manifest(frames)},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return {"fingerprint": fingerprint, "cached": False}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("job_dir", type=Path)
    args = parser.parse_args()
    result = extract_episode(args.job_dir)
    print("cached" if result["cached"] else "extracted")


if __name__ == "__main__":
    main()

