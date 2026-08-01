Exit code: 0
Wall time: 0.2 seconds
Output:
"""Inspect an episode and choose its text subtitle stream for analysis."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess


TEXT_SUBTITLE_CODECS = {"ass", "ssa", "subrip", "webvtt", "mov_text"}
CHINESE_TAGS = {"chi", "zho", "zh", "zh-cn", "zh-hans"}


def inspect_probe(raw: dict) -> dict:
    """Shape ffprobe's full response into the episode metadata we need."""
    video = next(stream for stream in raw["streams"] if stream["codec_type"] == "video")
    subtitles = [
        stream
        for stream in raw["streams"]
        if stream["codec_type"] == "subtitle"
        and stream.get("codec_name") in TEXT_SUBTITLE_CODECS
    ]
    return {
        "duration": float(raw["format"]["duration"]),
        "width": int(video["width"]),
        "height": int(video["height"]),
        "fps": video["r_frame_rate"],
        "video_stream_index": int(video["index"]),
        "audio_streams": [
            stream for stream in raw["streams"] if stream["codec_type"] == "audio"
        ],
        "subtitle_streams": subtitles,
    }


def choose_subtitle_stream(streams: list[dict], preferred_index: int | None) -> dict:
    """Choose an explicit, Chinese, default, or first text subtitle stream."""
    if preferred_index is not None:
        for stream in streams:
            if int(stream["index"]) == preferred_index:
                return stream
        available = ", ".join(str(stream["index"]) for stream in streams) or "none"
        raise ValueError(
            f"invalid subtitle stream index {preferred_index}; "
            f"available extractable text subtitle indices: {available}"
        )
    chinese = [
        stream
        for stream in streams
        if stream.get("tags", {}).get("language", "").lower() in CHINESE_TAGS
    ]
    if chinese:
        return chinese[0]
    defaults = [
        stream
        for stream in streams
        if stream.get("disposition", {}).get("default") == 1
    ]
    if defaults:
        return defaults[0]
    if streams:
        return streams[0]
    raise ValueError("no extractable text subtitle stream; run local speech recognition")


def probe_source(source: Path) -> dict:
    """Run ffprobe with all stream data needed for source analysis."""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(source)],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return json.loads(result.stdout)


def inspect_episode(job_dir: Path, preferred_index: int | None = None) -> dict:
    """Probe the initialized job's source and persist its analysis metadata."""
    job_dir = job_dir.expanduser().resolve()
    project = json.loads((job_dir / "project.json").read_text(encoding="utf-8"))
    if preferred_index is None:
        preferred_index = project.get("analysis", {}).get("subtitle_stream_index")
    episode = inspect_probe(probe_source(Path(project["source"])))
    selected = choose_subtitle_stream(episode["subtitle_streams"], preferred_index)
    episode["subtitle_stream_index"] = int(selected["index"])
    analysis_path = job_dir / "build" / "analysis" / "episode.json"
    analysis_path.parent.mkdir(parents=True, exist_ok=True)
    analysis_path.write_text(json.dumps(episode, ensure_ascii=False, indent=2), encoding="utf-8")
    return episode


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("job_dir", type=Path)
    parser.add_argument("--subtitle-stream-index", type=int)
    args = parser.parse_args()
    episode = inspect_episode(args.job_dir, args.subtitle_stream_index)
    print(episode["subtitle_stream_index"])


if __name__ == "__main__":
    main()

