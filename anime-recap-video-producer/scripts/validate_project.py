Exit code: 0
Wall time: 0.2 seconds
Output:
"""Validate authorization, media and edit-list invariants before rendering."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess


TARGET_DISPLAY_ASPECT = 16 / 9
DISPLAY_ASPECT_RELATIVE_TOLERANCE = 0.01


def load_project(project_path: Path) -> dict:
    """Load the project configuration from its canonical JSON file."""
    return json.loads(Path(project_path).read_text(encoding="utf-8"))


def probe_source(path: Path) -> dict:
    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries",
            "stream=codec_type,width,height,r_frame_rate,sample_aspect_ratio,display_aspect_ratio:"
            "format=duration",
            "-of", "json", str(path),
        ],
        check=True, capture_output=True, text=True, encoding="utf-8",
    )
    data = json.loads(result.stdout)
    video = next(stream for stream in data["streams"] if stream["codec_type"] == "video")
    display_aspect = _display_aspect_ratio(video)
    return {
        "duration": float(data["format"]["duration"]),
        "width": int(video["width"]),
        "height": int(video["height"]),
        "display_aspect_ratio": display_aspect,
        "fps": video["r_frame_rate"],
    }


def _parse_ratio(value: object) -> float | None:
    if isinstance(value, (int, float)):
        return float(value) if float(value) > 0 else None
    if not isinstance(value, str):
        return None
    separator = ":" if ":" in value else "/"
    try:
        numerator, denominator = value.split(separator, 1)
        ratio = float(numerator) / float(denominator)
    except (ValueError, ZeroDivisionError):
        return None
    return ratio if ratio > 0 else None


def _display_aspect_ratio(video: dict) -> float:
    display_aspect = _parse_ratio(video.get("display_aspect_ratio"))
    if display_aspect is not None:
        return display_aspect
    sample_aspect = _parse_ratio(video.get("sample_aspect_ratio")) or 1.0
    return int(video["width"]) * sample_aspect / int(video["height"])


def validate_contract(project: dict, clips: list[dict], media: dict) -> None:
    if not project.get("authorized_for_public_editing") or not project.get("source_audio_authorized"):
        raise ValueError("authorization: public editing and source audio must be confirmed")
    output = project["output"]
    if (output["width"], output["height"]) != (1920, 1080):
        raise ValueError("output must be 1920x1080")
    display_aspect = float(
        media.get("display_aspect_ratio", media["width"] / media["height"])
    )
    relative_error = abs(display_aspect - TARGET_DISPLAY_ASPECT) / TARGET_DISPLAY_ASPECT
    if relative_error > DISPLAY_ASPECT_RELATIVE_TOLERANCE:
        raise ValueError("source display aspect ratio must be 16:9 within 1% tolerance")
    if media["fps"] in {"0/0", ""}:
        raise ValueError("frame rate is invalid")
    if not clips:
        raise ValueError("clips list is empty")
    previous_in = -1.0
    total = 0.0
    excluded = project.get("excluded_ranges", [])
    for clip in clips:
        source_in = float(clip["source_in"])
        source_out = float(clip["source_out"])
        target = float(clip.get("target_seconds", source_out - source_in))
        if source_in < previous_in:
            raise ValueError("clips must be ordered by source_in")
        if source_out <= source_in or source_out > media["duration"]:
            raise ValueError("clip exceeds source duration")
        if target <= 0 or target > source_out - source_in + 0.001:
            raise ValueError("target_seconds must fit source range")
        if any(source_in < float(end) and source_out > float(start) for start, end in excluded):
            raise ValueError("clip overlaps an excluded range")
        total += target
        previous_in = source_in
    minimum = float(output["min_seconds"])
    maximum = float(output["max_seconds"])
    if not minimum <= total <= maximum:
        raise ValueError(f"total target duration must be {minimum:g}-{maximum:g} seconds")


def validate_project(project_path: Path) -> dict:
    project_path = project_path.resolve()
    project = load_project(project_path)
    source = Path(project["source"])
    if not source.is_file():
        raise FileNotFoundError(source)
    clips = json.loads((project_path.parent / "clips.json").read_text(encoding="utf-8"))
    media = probe_source(source)
    validate_contract(project, clips, media)
    return {"project": project, "clips": clips, "media": media}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    args = parser.parse_args()
    report = validate_project(args.project)
    print(json.dumps(report["media"], ensure_ascii=False))
    print("PROJECT_OK")


if __name__ == "__main__":
    main()

