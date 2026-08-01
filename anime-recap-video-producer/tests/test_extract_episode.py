Exit code: 0
Wall time: 0.2 seconds
Output:
from pathlib import Path
import json
import subprocess
import sys

import pytest


SCRIPTS = Path(__file__).parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from extract_episode import (
    build_contact_sheet_command,
    build_scene_command,
    build_subtitle_command,
    extract_episode,
    source_fingerprint,
)


def test_fingerprint_changes_with_stream_or_analysis_parameters(tmp_path: Path):
    source = tmp_path / "episode.mp4"
    source.write_bytes(b"media")
    first = source_fingerprint(source, 3, 0.35, 12)
    assert first != source_fingerprint(source, 4, 0.35, 12)
    assert first != source_fingerprint(source, 3, 0.40, 12)


def test_subtitle_extraction_maps_only_selected_stream():
    command = build_subtitle_command(Path("episode.mp4"), 3, Path("source.srt"))
    assert command[command.index("-map") + 1] == "0:3"
    assert command[command.index("-c:s") + 1] == "srt"


def test_scene_command_uses_source_directly_and_scales_only_frames():
    command = build_scene_command(
        Path("episode.mp4"), Path("frames/frame-%05d.jpg"), 0.35
    )
    assert command.count("-i") == 1
    graph = command[command.index("-vf") + 1]
    assert "gt(scene\\,0.350)" in graph
    assert "scale=480:-2" in graph


def test_contact_sheet_uses_portable_numbered_sequence_not_glob(tmp_path: Path):
    pattern = tmp_path / "staged" / "frame-%05d.jpg"
    command = build_contact_sheet_command(pattern, tmp_path / "sheet.jpg")

    assert "-pattern_type" not in command
    assert "glob" not in command
    assert command[command.index("-i") + 1] == str(pattern)
    assert command[command.index("-start_number") + 1] == "1"


def test_interrupted_rebuild_invalidates_stale_cache_before_next_run(tmp_path, monkeypatch):
    source = tmp_path / "episode.mp4"
    source.write_bytes(b"media")
    job = tmp_path / "job"
    analysis = job / "build" / "analysis"
    frames = analysis / "frames"
    frames.mkdir(parents=True)
    (job / "project.json").write_text(json.dumps({
        "source": str(source),
        "analysis": {"scene_threshold": 0.35, "fallback_interval_seconds": 12},
    }), encoding="utf-8")
    (analysis / "episode.json").write_text(
        json.dumps({"subtitle_stream_index": 3}), encoding="utf-8"
    )
    for name in ("source.srt", "scenes.json", "contact-sheet.jpg"):
        (analysis / name).write_bytes(b"stale")
    fingerprint = source_fingerprint(source, 3, 0.35, 12)
    (analysis / "cache.json").write_text(json.dumps({"fingerprint": fingerprint}))

    def interrupted_run(command, **kwargs):
        if "scene-%05d.jpg" in str(command[-1]):
            (frames / "scene-00001.jpg").write_bytes(b"partial")
            return type("Result", (), {"stderr": "pts_time:1.0"})()
        if "fallback-%05d.jpg" in str(command[-1]):
            raise subprocess.CalledProcessError(1, command)
        return type("Result", (), {"stderr": ""})()

    monkeypatch.setattr("extract_episode.subprocess.run", interrupted_run)
    with pytest.raises(subprocess.CalledProcessError):
        extract_episode(job)
    assert not (analysis / "cache.json").exists()

    def successful_run(command, **kwargs):
        output = str(command[-1])
        if "scene-%05d.jpg" in output:
            (frames / "scene-00001.jpg").write_bytes(b"scene")
            return type("Result", (), {"stderr": "pts_time:1.0"})()
        if "fallback-%05d.jpg" in output:
            for index in range(2, 13):
                (frames / f"fallback-{index:05d}.jpg").write_bytes(b"frame")
        if output.endswith("contact-sheet.jpg"):
            Path(output).write_bytes(b"sheet")
        return type("Result", (), {"stderr": ""})()

    monkeypatch.setattr("extract_episode.subprocess.run", successful_run)
    assert extract_episode(job)["cached"] is False

