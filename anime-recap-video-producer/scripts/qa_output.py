Exit code: 0
Wall time: 0.2 seconds
Output:
"""Probe a final video and gate delivery on the horizontal recap contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess


def _fps_value(value: str) -> float:
    numerator, denominator = value.split("/")
    return float(numerator) / float(denominator)


def sample_times(duration: float, count: int = 12) -> list[float]:
    if duration <= 0 or count <= 0:
        return []
    if count == 1:
        return [0.0]
    return [
        round(min(duration - 0.05, duration * index / (count - 1)), 3)
        for index in range(count)
    ]


def evaluate_probe(data: dict, expected_fps: str, loudness: dict | None = None) -> dict:
    failures = []
    video, audio = data["video"], data["audio"]
    duration = float(data["format_duration"])
    if (video["width"], video["height"]) != (1920, 1080):
        failures.append("resolution")
    if video["codec_name"] != "h264":
        failures.append("video_codec")
    if audio["codec_name"] != "aac":
        failures.append("audio_codec")
    if video.get("pix_fmt") != "yuv420p":
        failures.append("pixel_format")
    if audio.get("sample_rate") != "48000":
        failures.append("audio_sample_rate")
    if video["r_frame_rate"] != expected_fps:
        failures.append("frame_rate")
    if not 240 <= duration <= 360:
        failures.append("duration")
    if data.get("subtitle_stream_count", 0):
        failures.append("subtitle_stream")
    frame = 1.0 / _fps_value(expected_fps)
    tolerance = 0.5
    delta = abs(float(video["duration"]) - float(audio["duration"]))
    if delta > tolerance:
        failures.append("av_end_delta")
    if loudness is not None:
        if not -15.0 <= float(loudness["integrated_lufs"]) <= -13.0:
            failures.append("integrated_loudness")
        if float(loudness["true_peak_db"]) > -1.5:
            failures.append("true_peak")
    return {
        "delivery_ready": not failures,
        "failures": failures,
        "duration": duration,
        "av_end_delta_seconds": round(delta, 6),
        "one_frame_seconds": round(frame, 6),
        "av_tolerance_seconds": tolerance,
        "sample_times": sample_times(duration),
    }


def probe(path: Path) -> dict:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "stream=codec_type,codec_name,width,height,pix_fmt,r_frame_rate,sample_rate,duration:format=duration",
         "-of", "json", str(path)],
        check=True, capture_output=True, text=True, encoding="utf-8",
    )
    raw = json.loads(result.stdout)
    video = next(stream for stream in raw["streams"] if stream["codec_type"] == "video")
    audio = next(stream for stream in raw["streams"] if stream["codec_type"] == "audio")
    return {
        "format_duration": float(raw["format"]["duration"]),
        "video": video,
        "audio": audio,
        "subtitle_stream_count": sum(
            stream["codec_type"] == "subtitle" for stream in raw["streams"]
        ),
    }


def measure_loudness(path: Path) -> dict:
    result = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
         "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
        check=True, capture_output=True, text=True, encoding="utf-8",
    )
    match = re.search(r"\{\s*\"input_i\".*?\}", result.stderr, re.DOTALL)
    if match is None:
        raise ValueError("ffmpeg loudnorm measurement JSON was not found")
    measured = json.loads(match.group())
    return {
        "integrated_lufs": float(measured["input_i"]),
        "true_peak_db": float(measured["input_tp"]),
    }


def build_contact_sheet_command(path: Path, contact_sheet: Path, duration: float) -> list[str]:
    """Select the exact sample_times schedule and arrange it as a 4x3 sheet."""
    times = sample_times(duration)
    split_labels = "".join(f"[sample{index}]" for index in range(len(times)))
    graph = [f"[0:v]split={len(times)}{split_labels}"]
    frame_labels = []
    for index, timestamp in enumerate(times):
        graph.append(
            f"[sample{index}]trim=start={timestamp:.3f}:duration=0.500,"
            f"setpts=PTS-STARTPTS,select=eq(n\\,0),scale=480:-2[frame{index}]"
        )
        frame_labels.append(f"[frame{index}]")
    graph.append(
        "".join(frame_labels)
        + f"concat=n={len(times)}:v=1:a=0,"
          "tile=4x3:padding=4:margin=4[sheet]"
    )
    return [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(path),
        "-filter_complex", ";".join(graph), "-map", "[sheet]",
        "-frames:v", "1", str(contact_sheet),
    ]


def qa_output(path: Path, expected_fps: str, contact_sheet: Path | None = None) -> dict:
    loudness = measure_loudness(path)
    report = evaluate_probe(probe(path), expected_fps, loudness)
    report["loudness"] = loudness
    if contact_sheet is not None:
        contact_sheet.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(build_contact_sheet_command(path, contact_sheet, report["duration"]), check=True)
        report["contact_sheet"] = str(contact_sheet)
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path)
    parser.add_argument("--fps", required=True)
    parser.add_argument("--contact-sheet", type=Path)
    args = parser.parse_args()
    report = qa_output(args.video, args.fps, args.contact_sheet)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["delivery_ready"] else 2)


if __name__ == "__main__":
    main()

