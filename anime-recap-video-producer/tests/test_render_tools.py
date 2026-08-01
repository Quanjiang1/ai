Exit code: 0
Wall time: 0.2 seconds
Output:
from pathlib import Path
import hashlib
import json
import os
import re
import sys

import pytest


SCRIPTS = Path(__file__).parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from render_proxy import build_timeline_graph, build_proxy_command
from render_final import build_final_command, require_current_proxy_approval
from render_proxy import plan_fingerprint
from approve_proxy import approve_proxy
import render_final as render_final_module
import render_proxy as render_proxy_module
from vtt_to_ass import convert_vtt


CLIPS = [
    {"source_in": 10.0, "source_out": 14.0, "target_seconds": 4.0},
    {"source_in": 20.0, "source_out": 25.0, "target_seconds": 5.0},
]


def populate_approval_job(job_root: Path) -> Path:
    source = job_root / "episode.mp4"
    source.write_bytes(b"episode")
    (job_root / "project.json").write_text(
        json.dumps({"title": "recap", "source": str(source)}),
        encoding="utf-8",
    )
    plan = {
        "segments": [{
            "id": "hook-01",
            "narration": "Narration",
            "story_function": "hook",
            "evidence_ranges": [[0.0, 1.0]],
            "visual_beats": ["Action"],
            "clip_ranges": [[0.0, 1.0]],
            "target_seconds": 1.0,
            "spoiler_level": "minor",
        }]
    }
    (job_root / "recap-plan.json").write_text(json.dumps(plan), encoding="utf-8")
    clips = [{
        "source_in": 0.0,
        "source_out": 1.0,
        "target_seconds": 1.0,
        "purpose": "hook-01:Action",
    }]
    (job_root / "clips.json").write_bytes(
        (json.dumps(clips, ensure_ascii=False, indent=2) + "\n").encode("utf-8"),
    )
    build = job_root / "build"
    build.mkdir()
    (build / "captions.ass").write_text("[Script Info]", encoding="utf-8")
    (build / "voiceover.mp3").write_bytes(b"voice")
    proxy = build / "proxy.mp4"
    proxy.write_bytes(b"proxy")
    manifest = {
        "plan_fingerprint": plan_fingerprint(job_root),
        "proxy_path": str(proxy.resolve()),
        "proxy_size": proxy.stat().st_size,
        "proxy_sha256": hashlib.sha256(proxy.read_bytes()).hexdigest(),
    }
    (build / "proxy-render.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    return proxy


def render_proxy_with_fake_ffmpeg(
    job_root: Path,
    monkeypatch,
    proxy_bytes: bytes = b"rendered-proxy",
) -> Path:
    proxy = job_root / "build" / "proxy.mp4"
    monkeypatch.setattr(
        render_proxy_module,
        "build_proxy_command",
        lambda _: ["ffmpeg", str(proxy)],
    )

    def fake_run(command, check):
        proxy.write_bytes(proxy_bytes)

    monkeypatch.setattr(render_proxy_module.subprocess, "run", fake_run)
    return render_proxy_module.render_proxy(job_root / "project.json")


def test_timeline_graph_is_single_input_horizontal_concat():
    graph = build_timeline_graph(CLIPS, 960, 540, "-22dB")

    assert "split=2" in graph and "asplit=2" in graph
    assert "concat=n=2:v=1:a=1" in graph
    assert "scale=960:540" in graph
    assert graph.count("volume=-22dB") == 1
    assert "crop=" not in graph and "gblur" not in graph


def test_proxy_command_is_fast_and_preserves_source_fps():
    command = build_proxy_command(Path("project.json"), "24000/1001")

    assert command.count("-i") == 2
    assert ["-preset", "ultrafast"] == command[command.index("-preset"):command.index("-preset") + 2]
    assert command[command.index("-r") + 1] == "24000/1001"
    assert "960:540" in command[command.index("-filter_complex") + 1]


def test_proxy_includes_voice_and_burned_recap_captions():
    command = build_proxy_command(Path("project.json"), "24000/1001")
    graph = command[command.index("-filter_complex") + 1]

    assert command.count("-i") == 2
    assert "subtitles=" in graph
    assert "amix=inputs=2" in graph
    assert "-sn" in command


def test_final_rejects_stale_proxy_approval(tmp_path: Path):
    populate_approval_job(tmp_path)
    approve_proxy(tmp_path)
    (tmp_path / "build" / "captions.ass").write_text("[Script Info]\nchanged", encoding="utf-8")

    with pytest.raises(ValueError, match="proxy approval is stale"):
        require_current_proxy_approval(tmp_path)


def test_approval_records_current_fingerprint_and_proxy_metadata(tmp_path: Path):
    proxy = populate_approval_job(tmp_path)

    approval_path = approve_proxy(tmp_path)
    approval = json.loads(approval_path.read_text(encoding="utf-8"))

    assert approval == {
        "plan_fingerprint": plan_fingerprint(tmp_path),
        "proxy_path": str(proxy.resolve()),
        "proxy_size": proxy.stat().st_size,
        "proxy_sha256": hashlib.sha256(proxy.read_bytes()).hexdigest(),
    }


def test_current_proxy_approval_passes(tmp_path: Path):
    populate_approval_job(tmp_path)
    approve_proxy(tmp_path)

    require_current_proxy_approval(tmp_path)


def test_approval_rejects_proxy_without_render_manifest(tmp_path: Path):
    populate_approval_job(tmp_path)
    (tmp_path / "build" / "proxy-render.json").unlink()

    with pytest.raises(ValueError, match="proxy render manifest"):
        approve_proxy(tmp_path)


def test_approval_rejects_input_changed_after_manifested_render(
    tmp_path: Path,
    monkeypatch,
):
    populate_approval_job(tmp_path)
    render_proxy_with_fake_ffmpeg(tmp_path, monkeypatch)
    plan_path = tmp_path / "recap-plan.json"
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    plan["segments"][0]["narration"] = "Valid deterministic input B"
    plan_path.write_text(json.dumps(plan), encoding="utf-8")

    with pytest.raises(ValueError, match="proxy render manifest"):
        approve_proxy(tmp_path)


def test_approval_rejects_same_size_proxy_replacement_after_render(
    tmp_path: Path,
    monkeypatch,
):
    proxy = populate_approval_job(tmp_path)
    render_proxy_with_fake_ffmpeg(tmp_path, monkeypatch, b"proxy-A")
    proxy.write_bytes(b"proxy-B")

    with pytest.raises(ValueError, match="proxy render manifest"):
        approve_proxy(tmp_path)


def test_current_render_manifest_can_be_approved(tmp_path: Path, monkeypatch):
    proxy = populate_approval_job(tmp_path)
    render_proxy_with_fake_ffmpeg(tmp_path, monkeypatch)
    manifest_path = tmp_path / "build" / "proxy-render.json"

    assert manifest_path.is_file()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    approval_path = approve_proxy(tmp_path)

    assert json.loads(approval_path.read_text(encoding="utf-8")) == manifest
    assert manifest["proxy_path"] == str(proxy.resolve())


def test_render_rejects_mid_render_input_change_and_invalidates_old_manifest(
    tmp_path: Path,
    monkeypatch,
):
    proxy = populate_approval_job(tmp_path)
    manifest_path = tmp_path / "build" / "proxy-render.json"
    manifest_path.write_text('{"old":true}', encoding="utf-8")
    manifest_seen_by_ffmpeg = []
    monkeypatch.setattr(
        render_proxy_module,
        "build_proxy_command",
        lambda _: ["ffmpeg", str(proxy)],
    )

    def fake_run(command, check):
        manifest_seen_by_ffmpeg.append(manifest_path.exists())
        proxy.write_bytes(b"new-proxy")
        (tmp_path / "build" / "captions.ass").write_text(
            "[Script Info]\nchanged during render",
            encoding="utf-8",
        )

    monkeypatch.setattr(render_proxy_module.subprocess, "run", fake_run)

    with pytest.raises(ValueError, match="inputs changed during proxy render"):
        render_proxy_module.render_proxy(tmp_path / "project.json")

    assert manifest_seen_by_ffmpeg == [False]
    assert not manifest_path.exists()


def test_approval_rejects_clips_that_are_not_the_exact_plan_derivative(tmp_path: Path):
    populate_approval_job(tmp_path)
    clips_path = tmp_path / "clips.json"
    clips_path.write_text("[]\n", encoding="utf-8")

    with pytest.raises(ValueError, match="clips.json.*deterministic derivative"):
        approve_proxy(tmp_path)


def test_clips_mutation_invalidates_approval(tmp_path: Path):
    populate_approval_job(tmp_path)
    approve_proxy(tmp_path)
    clips_path = tmp_path / "clips.json"
    clips_path.write_text(clips_path.read_text(encoding="utf-8") + " ", encoding="utf-8")

    with pytest.raises(ValueError, match="proxy approval"):
        require_current_proxy_approval(tmp_path)


def test_source_identity_mutation_invalidates_approval(tmp_path: Path):
    populate_approval_job(tmp_path)
    approve_proxy(tmp_path)
    source = tmp_path / "episode.mp4"
    stat = source.stat()
    os.utime(source, ns=(stat.st_atime_ns, stat.st_mtime_ns + 1_000_000))

    with pytest.raises(ValueError, match="proxy approval"):
        require_current_proxy_approval(tmp_path)


@pytest.mark.parametrize("replacement", [b"replacement", b"PROXY"])
def test_proxy_replacement_invalidates_approval(tmp_path: Path, replacement: bytes):
    proxy = populate_approval_job(tmp_path)
    approve_proxy(tmp_path)
    proxy.write_bytes(replacement)

    with pytest.raises(ValueError, match="proxy approval"):
        require_current_proxy_approval(tmp_path)


def test_missing_approved_proxy_is_rejected(tmp_path: Path):
    proxy = populate_approval_job(tmp_path)
    approve_proxy(tmp_path)
    proxy.unlink()

    with pytest.raises(ValueError, match="proxy approval"):
        require_current_proxy_approval(tmp_path)


def test_final_requires_proxy_approval_before_audio_preflight(tmp_path: Path, monkeypatch):
    (tmp_path / "project.json").write_text('{"title":"recap"}', encoding="utf-8")
    (tmp_path / "recap-plan.json").write_text('{"segments":[]}', encoding="utf-8")
    build = tmp_path / "build"
    build.mkdir()
    (build / "captions.ass").write_text("[Script Info]", encoding="utf-8")
    (build / "voiceover.mp3").write_bytes(b"voice")
    (build / "proxy.mp4").write_bytes(b"proxy")
    monkeypatch.setattr(render_final_module, "validate_project", lambda _: {
        "project": {"source": str(tmp_path / "episode.mp4"), "audio": {"source_bed_gain_db": -22}},
        "clips": CLIPS,
        "media": {"fps": "24000/1001"},
    })
    monkeypatch.setattr(render_final_module, "stage_fonts", lambda _: tmp_path / "fonts")
    monkeypatch.setattr(
        render_final_module,
        "measure_loudnorm",
        lambda *_: pytest.fail("audio preflight must not run before proxy approval"),
    )

    with pytest.raises(ValueError, match="proxy approval is missing"):
        render_final_module.render_final(tmp_path / "project.json")


def test_final_revalidates_clips_before_project_probe(tmp_path: Path, monkeypatch):
    populate_approval_job(tmp_path)
    approve_proxy(tmp_path)
    (tmp_path / "clips.json").write_text("[]\n", encoding="utf-8")
    monkeypatch.setattr(
        render_final_module,
        "validate_project",
        lambda _: pytest.fail("project probing must not run before approval revalidation"),
    )

    with pytest.raises(ValueError, match="proxy approval"):
        render_final_module.render_final(tmp_path / "project.json")


def test_final_command_has_one_high_quality_video_encode_and_audio_preflight_chain():
    command = build_final_command(
        source=Path("episode.mp4"),
        voice=Path("voice.mp3"),
        captions=Path("captions.ass"),
        output=Path("final.mp4"),
        clips=CLIPS,
        fps="24000/1001",
        loudnorm_filter="loudnorm=I=-14:TP=-1.5:LRA=9",
    )
    graph = command[command.index("-filter_complex") + 1]

    assert command.count("-i") == 2
    assert command.count("libx264") == 1
    assert ["-preset", "medium"] == command[command.index("-preset"):command.index("-preset") + 2]
    assert "aresample=48000,highpass=f=80,lowpass=f=15000" in graph
    assert graph.count("volume=-22dB") == 1
    assert "concat=n=2:v=1:a=1" in graph
    assert "subtitles=" in graph
    assert (
        "amix=inputs=2:duration=longest:dropout_transition=0,"
        "atrim=duration=9.000,asetpts=PTS-STARTPTS,"
        "loudnorm=I=-14:TP=-1.5:LRA=9[mix]"
    ) in graph


def test_loudness_measurement_trims_to_selected_edit_before_loudnorm(monkeypatch):
    commands = []

    class Result:
        stderr = (
            '{"input_i":"-20.0","input_tp":"-3.0","input_lra":"2.0",'
            '"input_thresh":"-30.0","target_offset":"1.0"\n}'
        )

    def fake_run(command, **kwargs):
        commands.append(command)
        return Result()

    monkeypatch.setattr(render_final_module.subprocess, "run", fake_run)

    render_final_module.measure_loudnorm(
        Path("episode.mp4"),
        Path("narration-longer-than-edit.mp3"),
        CLIPS,
        "-22dB",
    )
    graph = commands[0][commands[0].index("-filter_complex") + 1]

    assert (
        "amix=inputs=2:duration=longest:dropout_transition=0,"
        "atrim=duration=9.000,asetpts=PTS-STARTPTS,"
        "loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json[mix]"
    ) in graph


def test_vtt_converter_limits_horizontal_captions_to_two_nonoverlapping_lines(tmp_path: Path):
    vtt = tmp_path / "voice.vtt"
    ass = tmp_path / "captions.ass"
    vtt.write_text(
        "WEBVTT\n\n00:00:00,000 --> 00:00:04,000\n"
        + "鐢? * 60
        + "\n\n00:00:03,950 --> 00:00:05,000\n闆跺ぉ璧嬩篃鑳藉彉寮恒€俓n",
        encoding="utf-8",
    )

    count = convert_vtt(vtt, ass, keywords=["闆跺ぉ璧?])
    text = ass.read_text(encoding="utf-8-sig")
    events = [line.split(",", 9) for line in text.splitlines() if line.startswith("Dialogue:")]

    assert count >= 3
    assert "PlayResX: 1920" in text and "PlayResY: 1080" in text
    assert "MarginV=140" not in text
    assert all(len(fields[9].split(r"\N")) <= 2 for fields in events)
    assert all(_cs(left[2]) <= _cs(right[1]) for left, right in zip(events, events[1:]))
    assert r"{\c&H00FFFF&}闆跺ぉ璧媨\c&HFFFFFF&}" in text


def _cs(value: str) -> int:
    h, m, rest = value.split(":")
    s, cs = rest.split(".")
    return (int(h) * 3600 + int(m) * 60 + int(s)) * 100 + int(cs)

