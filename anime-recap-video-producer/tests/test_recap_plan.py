Exit code: 0
Wall time: 0.2 seconds
Output:
import csv
import json
import math
from pathlib import Path
import sys

import pytest


SCRIPTS = Path(__file__).parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from build_recap_assets import derive_assets, validate_recap_plan


def valid_plan():
    return {
        "segments": [{
            "id": "hook-01",
            "narration": "浠栦互涓烘垬鏂楀凡缁忕粨鏉燂紝鐪熸鐨勬晫浜哄嵈鍒氬垰鐜拌韩銆?,
            "story_function": "hook",
            "evidence_ranges": [[10.0, 18.0]],
            "visual_beats": ["涓昏鍥炲ご鐪嬭鏁屼汉"],
            "clip_ranges": [[10.0, 18.0]],
            "target_seconds": 8.0,
            "spoiler_level": "minor",
        }]
    }


def test_derive_assets_keeps_script_csv_and_clips_in_sync(tmp_path: Path):
    plan_path = tmp_path / "recap-plan.json"
    plan_path.write_text(json.dumps(valid_plan(), ensure_ascii=False), encoding="utf-8")

    outputs = derive_assets(plan_path)

    clips = json.loads(outputs["clips"].read_text(encoding="utf-8"))
    assert clips == [{
        "source_in": 10.0,
        "source_out": 18.0,
        "target_seconds": 8.0,
        "purpose": "hook-01:涓昏鍥炲ご鐪嬭鏁屼汉",
    }]
    assert "鐪熸鐨勬晫浜? in outputs["voiceover"].read_text(encoding="utf-8")
    with outputs["shot_list"].open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    assert rows[0]["segment_id"] == "hook-01"
    assert rows[0]["visual_beats"] == "涓昏鍥炲ご鐪嬭鏁屼汉"


def test_derive_assets_is_deterministic(tmp_path: Path):
    plan_path = tmp_path / "recap-plan.json"
    plan_path.write_text(json.dumps(valid_plan(), ensure_ascii=False), encoding="utf-8")

    first = {name: path.read_bytes() for name, path in derive_assets(plan_path).items()}
    second = {name: path.read_bytes() for name, path in derive_assets(plan_path).items()}

    assert second == first


@pytest.mark.parametrize(
    ("mutate", "message", "excluded"),
    [
        (lambda plan: plan["segments"][0].update(target_seconds=7.0), "target_seconds", []),
        (lambda plan: plan["segments"][0].update(narration=""), "narration", []),
        (lambda plan: plan["segments"][0].update(evidence_ranges=[]), "evidence_ranges", []),
        (lambda plan: plan["segments"][0].update(visual_beats=[]), "visual_beats", []),
        (lambda plan: plan["segments"][0].update(clip_ranges=[]), "clip_ranges", []),
        (lambda plan: plan["segments"][0].update(clip_ranges=[[1439.0, 1441.0]]), "media duration", []),
        (lambda plan: plan["segments"][0].update(clip_ranges=[[14.0, 18.0]], target_seconds=4.0), "excluded", [[12.0, 15.0]]),
    ],
)
def test_validate_plan_rejects_invalid_segments(mutate, message, excluded):
    plan = valid_plan()
    mutate(plan)
    with pytest.raises(ValueError, match=message):
        validate_recap_plan(plan, {"excluded_ranges": excluded}, {"duration": 1440.0})


def test_validate_plan_requires_every_segment_field():
    plan = valid_plan()
    del plan["segments"][0]["spoiler_level"]
    with pytest.raises(ValueError, match="spoiler_level"):
        validate_recap_plan(plan, {"excluded_ranges": []}, {"duration": 1440.0})


def test_validate_plan_rejects_duplicate_segment_ids():
    plan = valid_plan()
    duplicate = dict(plan["segments"][0])
    duplicate["clip_ranges"] = [[20.0, 28.0]]
    duplicate["evidence_ranges"] = [[20.0, 28.0]]
    plan["segments"].append(duplicate)

    with pytest.raises(ValueError, match="duplicate segment id.*hook-01"):
        validate_recap_plan(plan, {"excluded_ranges": []}, {"duration": 1440.0})


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
def test_validate_plan_rejects_non_finite_target_seconds(value):
    plan = valid_plan()
    plan["segments"][0]["target_seconds"] = value

    with pytest.raises(ValueError, match="target_seconds"):
        validate_recap_plan(plan, {"excluded_ranges": []}, {"duration": 1440.0})


@pytest.mark.parametrize("field", ["evidence_ranges", "clip_ranges"])
@pytest.mark.parametrize("endpoint", [math.nan, math.inf, -math.inf])
@pytest.mark.parametrize("endpoint_index", [0, 1])
def test_validate_plan_rejects_non_finite_range_endpoints(field, endpoint, endpoint_index):
    plan = valid_plan()
    endpoint_values = [10.0, 18.0]
    endpoint_values[endpoint_index] = endpoint
    plan["segments"][0][field] = [endpoint_values]

    with pytest.raises(ValueError, match=field):
        validate_recap_plan(plan, {"excluded_ranges": []}, {"duration": 1440.0})

