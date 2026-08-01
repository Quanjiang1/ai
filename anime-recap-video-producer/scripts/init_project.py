Exit code: 0
Wall time: 0.2 seconds
Output:
"""Create a reusable horizontal anime-recap project."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def create_project(source: Path, output_dir: Path, title: str) -> Path:
    source = source.expanduser().resolve()
    if not source.is_file():
        raise FileNotFoundError(source)
    output_dir = output_dir.expanduser().resolve()
    (output_dir / "copy").mkdir(parents=True, exist_ok=True)
    (output_dir / "build").mkdir(parents=True, exist_ok=True)
    project = {
        "source": str(source),
        "title": title,
        "authorized_for_public_editing": False,
        "source_audio_authorized": False,
        "platform": "bilibili",
        "output": {
            "width": 1920,
            "height": 1080,
            "min_seconds": 240,
            "target_seconds": 300,
            "max_seconds": 360,
        },
        "proxy": {"width": 960, "height": 540},
        "voice": {"name": "zh-CN-YunxiNeural", "rate": "+10%", "pitch": "-2Hz"},
        "audio": {
            "source_bed_gain_db": -22,
            "target_integrated_lufs": -14,
            "true_peak_db": -1.5,
        },
        "captions": {"keywords": [], "font": "Microsoft YaHei", "margin_v": 140},
        "analysis": {
            "subtitle_stream_index": None,
            "scene_threshold": 0.35,
            "fallback_interval_seconds": 12,
        },
        "excluded_ranges": [],
    }
    project_path = output_dir / "project.json"
    project_path.write_text(json.dumps(project, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "clips.json").write_text("[]\n", encoding="utf-8")
    (output_dir / "copy" / "voiceover.txt").write_text("", encoding="utf-8")
    return project_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--title", required=True)
    args = parser.parse_args()
    print(create_project(args.source, args.output_dir, args.title))


if __name__ == "__main__":
    main()

