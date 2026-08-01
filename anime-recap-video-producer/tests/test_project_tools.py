Exit code: 0
Wall time: 0.2 seconds
Output:
from pathlib import Path
import json
import sys

import pytest


SCRIPTS = Path(__file__).parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from init_project import create_project
from validate_project import load_project, validate_contract


def media(duration=1440.0, width=1920, height=1080, fps="24000/1001"):
    return {"duration": duration, "width": width, "height": height, "fps": fps}


def test_create_project_uses_bilibili_horizontal_defaults(tmp_path: Path):
    source = tmp_path / "episode.mp4"
    source.touch()
    project_path = create_project(source, tmp_path / "job", "绀轰緥浣滃搧")
    data = json.loads(project_path.read_text(encoding="utf-8"))

    assert data["authorized_for_public_editing"] is False
    assert data["source_audio_authorized"] is False
    assert data["platform"] == "bilibili"
    assert data["output"] == {
        "width": 1920,
        "height": 1080,
        "min_seconds": 240,
        "target_seconds": 300,
        "max_seconds": 360,
    }
    assert data["proxy"] == {"width": 960, "height": 540}
    assert (tmp_path / "job" / "clips.json").is_file()
    assert (tmp_path / "job" / "copy" / "voiceover.txt").is_file()


def test_load_project_reads_project_json(tmp_path: Path):
    project_path = tmp_path / "project.json"
    expected = {"source": "episode.mp4", "output": {"min_seconds": 240}}
    project_path.write_text(json.dumps(expected), encoding="utf-8")

    assert load_project(project_path) == expected


def valid_project():
    return {
        "authorized_for_public_editing": True,
        "source_audio_authorized": True,
        "output": {
            "width": 1920,
            "height": 1080,
            "min_seconds": 240,
            "target_seconds": 300,
            "max_seconds": 360,
        },
    }


def valid_clips():
    return [
        {"source_in": 10.0, "source_out": 160.0, "target_seconds": 150.0},
        {"source_in": 200.0, "source_out": 350.0, "target_seconds": 150.0},
    ]


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (lambda p, c, m: p.update(authorized_for_public_editing=False), "authorization"),
        (lambda p, c, m: p["output"].update(width=1080), "1920x1080"),
        (lambda p, c, m: c[1].update(source_in=5.0), "ordered"),
        (lambda p, c, m: c[1].update(source_out=1500.0), "source duration"),
        (lambda p, c, m: c[0].update(target_seconds=10.0), "240-360"),
        (lambda p, c, m: m.update(fps="0/0"), "frame rate"),
    ],
)
def test_validate_contract_rejects_invalid_projects(mutate, message):
    project, clips, probed = valid_project(), valid_clips(), media()
    mutate(project, clips, probed)
    with pytest.raises(ValueError, match=message):
        validate_contract(project, clips, probed)


def test_validate_contract_accepts_valid_project():
    validate_contract(valid_project(), valid_clips(), media())


def test_validate_contract_accepts_anamorphic_source_with_16_by_9_display_aspect():
    probed = media(width=720, height=480)
    probed["display_aspect_ratio"] = 16 / 9

    validate_contract(valid_project(), valid_clips(), probed)


@pytest.mark.parametrize(
    ("width", "height"),
    [
        (1920, 1200),
        (2560, 1080),
    ],
)
def test_validate_contract_rejects_non_16_by_9_display_aspect(width, height):
    with pytest.raises(ValueError, match="16:9"):
        validate_contract(valid_project(), valid_clips(), media(width=width, height=height))


def test_validate_contract_reports_configured_duration_bounds():
    project, clips, probed = valid_project(), valid_clips(), media()
    clips[1]["target_seconds"] = 10.0
    with pytest.raises(ValueError, match="240-360"):
        validate_contract(project, clips, probed)

