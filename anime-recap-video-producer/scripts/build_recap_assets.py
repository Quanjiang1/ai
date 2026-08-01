Exit code: 0
Wall time: 0.2 seconds
Output:
"""Validate a recap plan and derive its render inputs deterministically."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

from validate_project import load_project, probe_source, validate_project


SEGMENT_FIELDS = (
    "id",
    "narration",
    "story_function",
    "evidence_ranges",
    "visual_beats",
    "clip_ranges",
    "target_seconds",
    "spoiler_level",
)
CSV_FIELDS = (
    "segment_id",
    "story_function",
    "source_in",
    "source_out",
    "target_seconds",
    "visual_beats",
    "narration",
    "spoiler_level",
)


def _ranges(value: object, name: str, segment_id: str, duration: float, excluded: list) -> list[tuple[float, float]]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{segment_id}: {name} must not be empty")
    ranges: list[tuple[float, float]] = []
    for item in value:
        if not isinstance(item, (list, tuple)) or len(item) != 2:
            raise ValueError(f"{segment_id}: {name} entries must be [start, end]")
        start, end = float(item[0]), float(item[1])
        if not math.isfinite(start) or not math.isfinite(end):
            raise ValueError(f"{segment_id}: {name} values must be finite")
        if start < 0 or end <= start or end > duration:
            raise ValueError(f"{segment_id}: {name} exceeds media duration")
        if any(start < float(excluded_end) and end > float(excluded_start) for excluded_start, excluded_end in excluded):
            raise ValueError(f"{segment_id}: {name} overlaps an excluded range")
        ranges.append((start, end))
    return ranges


def validate_recap_plan(plan: dict, project: dict, media: dict) -> None:
    """Validate that a recap plan is complete and safe for its source media."""
    if not isinstance(plan, dict) or not isinstance(plan.get("segments"), list) or not plan["segments"]:
        raise ValueError("segments must not be empty")
    duration = float(media["duration"])
    excluded = project.get("excluded_ranges", [])
    segment_ids: set[str] = set()
    for segment in plan["segments"]:
        if not isinstance(segment, dict):
            raise ValueError("segment must be an object")
        segment_id = str(segment.get("id", "<unknown>"))
        for field in SEGMENT_FIELDS:
            if field not in segment:
                raise ValueError(f"{segment_id}: {field} is required")
        if not isinstance(segment["id"], str) or not segment["id"].strip():
            raise ValueError("id must not be empty")
        if segment["id"] in segment_ids:
            raise ValueError(f"duplicate segment id: {segment['id']}")
        segment_ids.add(segment["id"])
        if not isinstance(segment["narration"], str) or not segment["narration"].strip():
            raise ValueError(f"{segment_id}: narration must not be empty")
        if not isinstance(segment["story_function"], str) or not segment["story_function"].strip():
            raise ValueError(f"{segment_id}: story_function must not be empty")
        if not isinstance(segment["spoiler_level"], str) or not segment["spoiler_level"].strip():
            raise ValueError(f"{segment_id}: spoiler_level must not be empty")
        if not isinstance(segment["visual_beats"], list) or not segment["visual_beats"] or not all(
            isinstance(beat, str) and beat.strip() for beat in segment["visual_beats"]
        ):
            raise ValueError(f"{segment_id}: visual_beats must not be empty")
        _ranges(segment["evidence_ranges"], "evidence_ranges", segment_id, duration, excluded)
        clip_ranges = _ranges(segment["clip_ranges"], "clip_ranges", segment_id, duration, excluded)
        clip_total = sum(end - start for start, end in clip_ranges)
        target_seconds = float(segment["target_seconds"])
        if not math.isfinite(target_seconds):
            raise ValueError(f"{segment['id']}: target_seconds must be finite")
        if abs(target_seconds - clip_total) > 0.001:
            raise ValueError(f"{segment['id']}: target_seconds must equal clip range duration")


def derive_clips(plan: dict) -> list[dict]:
    """Return the canonical clips derivative for a recap plan."""
    clips = []
    for segment in plan["segments"]:
        visual_beats = " / ".join(segment["visual_beats"])
        for start, end in segment["clip_ranges"]:
            start, end = float(start), float(end)
            clips.append({
                "source_in": start,
                "source_out": end,
                "target_seconds": end - start,
                "purpose": f"{segment['id']}:{visual_beats}",
            })
    return clips


def clips_json_bytes(plan: dict) -> bytes:
    """Serialize clips exactly as derive_assets writes clips.json."""
    return (json.dumps(derive_clips(plan), ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def derive_assets(plan_path: Path) -> dict[str, Path]:
    """Create voiceover, shot-list, and clips derivatives without probing media."""
    plan_path = Path(plan_path)
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    job_dir = plan_path.parent
    copy_dir = job_dir / "copy"
    copy_dir.mkdir(parents=True, exist_ok=True)
    voiceover_path = copy_dir / "voiceover.txt"
    shot_list_path = job_dir / "shot-list.csv"
    clips_path = job_dir / "clips.json"
    segments = plan["segments"]

    voiceover_path.write_text("\n".join(segment["narration"] for segment in segments) + "\n", encoding="utf-8")
    with shot_list_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for segment in segments:
            visual_beats = " / ".join(segment["visual_beats"])
            for start, end in segment["clip_ranges"]:
                start, end = float(start), float(end)
                target_seconds = end - start
                writer.writerow({
                    "segment_id": segment["id"],
                    "story_function": segment["story_function"],
                    "source_in": start,
                    "source_out": end,
                    "target_seconds": target_seconds,
                    "visual_beats": visual_beats,
                    "narration": segment["narration"],
                    "spoiler_level": segment["spoiler_level"],
                })
    clips_path.write_bytes(clips_json_bytes(plan))
    return {"voiceover": voiceover_path, "shot_list": shot_list_path, "clips": clips_path}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path, help="Path to <job-dir>/recap-plan.json")
    args = parser.parse_args()
    plan_path = args.plan.resolve()
    project_path = plan_path.parent / "project.json"
    project = load_project(project_path)
    media = probe_source(Path(project["source"]))
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    validate_recap_plan(plan, project, media)
    outputs = derive_assets(plan_path)
    validate_project(project_path)
    print(json.dumps({name: str(path) for name, path in outputs.items()}, ensure_ascii=False))
    print("RECAP_PLAN_OK")


if __name__ == "__main__":
    main()

