Exit code: 0
Wall time: 0.2 seconds
Output:
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest


SCRIPTS = Path(__file__).parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from approve_proxy import approve_proxy
from build_recap_assets import derive_assets
import render_final as render_final_module
from render_proxy import render_proxy


MISSING_TOOLS = [name for name in ("ffmpeg", "ffprobe") if shutil.which(name) is None]
pytestmark = pytest.mark.skipif(
    bool(MISSING_TOOLS),
    reason=(
        "real FFmpeg integration test requires ffmpeg and ffprobe on PATH; missing: "
        + ", ".join(MISSING_TOOLS)
    ),
)


def run(command: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def probe(path: Path) -> dict:
    result = run([
        "ffprobe", "-v", "error",
        "-show_entries", "stream=codec_type,width,height,r_frame_rate:format=duration",
        "-of", "json", str(path),
    ])
    return json.loads(result.stdout)


def write_ass(path: Path) -> None:
    path.write_text(
        "[Script Info]\n"
        "ScriptType: v4.00+\n"
        "PlayResX: 1920\n"
        "PlayResY: 1080\n"
        "\n"
        "[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
        "OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
        "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
        "Alignment, MarginL, MarginR, MarginV, Encoding\n"
        "Style: Default,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,"
        "0,0,0,0,100,100,0,0,1,2,0,2,40,40,60,1\n"
        "\n"
        "[Events]\n"
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, "
        "Effect, Text\n"
        "Dialogue: 0,0:00:00.00,0:00:00.90,Default,,0,0,0,,Recap caption\n",
        encoding="utf-8",
    )


def test_real_proxy_approval_and_final_pipeline(tmp_path: Path, monkeypatch):
    source = tmp_path / "episode.mp4"
    voice = tmp_path / "build" / "voiceover.mp3"
    captions = tmp_path / "build" / "captions.ass"
    voice.parent.mkdir()
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "lavfi", "-i", "testsrc2=size=320x180:rate=24:duration=1.2",
        "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000:duration=1.2",
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-ar", "48000", "-shortest", str(source),
    ])
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "lavfi", "-i", "sine=frequency=880:sample_rate=48000:duration=1.6",
        "-c:a", "libmp3lame", "-q:a", "5", str(voice),
    ])
    write_ass(captions)

    plan = {
        "segments": [{
            "id": "hook-01",
            "narration": "Recap caption",
            "story_function": "hook",
            "evidence_ranges": [[0.0, 1.0]],
            "visual_beats": ["Test pattern"],
            "clip_ranges": [[0.0, 1.0]],
            "target_seconds": 1.0,
            "spoiler_level": "minor",
        }]
    }
    project = {
        "source": str(source.resolve()),
        "authorized_for_public_editing": True,
        "source_audio_authorized": True,
        "output": {
            "width": 1920,
            "height": 1080,
            "min_seconds": 1,
            "target_seconds": 1,
            "max_seconds": 2,
        },
        "proxy": {"width": 160, "height": 90},
        "audio": {"source_bed_gain_db": -22},
        "excluded_ranges": [],
    }
    project_path = tmp_path / "project.json"
    project_path.write_text(json.dumps(project), encoding="utf-8")
    plan_path = tmp_path / "recap-plan.json"
    plan_path.write_text(json.dumps(plan), encoding="utf-8")
    derive_assets(plan_path)

    proxy_path = render_proxy(project_path)
    manifest_path = tmp_path / "build" / "proxy-render.json"
    approval_path = approve_proxy(tmp_path)
    assert json.loads(approval_path.read_text(encoding="utf-8")) == json.loads(
        manifest_path.read_text(encoding="utf-8")
    )

    def stage_test_fonts(destination: Path) -> Path:
        destination.mkdir(parents=True, exist_ok=True)
        return destination

    monkeypatch.setattr(render_final_module, "stage_fonts", stage_test_fonts)
    final_path = render_final_module.render_final(project_path)

    for path, dimensions in ((proxy_path, (160, 90)), (final_path, (1920, 1080))):
        data = probe(path)
        stream_types = [stream["codec_type"] for stream in data["streams"]]
        video = next(stream for stream in data["streams"] if stream["codec_type"] == "video")
        assert stream_types == ["video", "audio"]
        assert (video["width"], video["height"]) == dimensions
        assert video["r_frame_rate"] == "24/1"
        assert 0.9 <= float(data["format"]["duration"]) <= 1.2

