Exit code: 0
Wall time: 0.2 seconds
Output:
from pathlib import Path
import sys

import pytest


SCRIPTS = Path(__file__).parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from inspect_episode import choose_subtitle_stream, inspect_probe


def test_choose_subtitle_prefers_explicit_then_chinese_then_default():
    streams = [
        {"index": 2, "codec_type": "subtitle", "codec_name": "ass",
         "tags": {"language": "eng"}, "disposition": {"default": 1}},
        {"index": 3, "codec_type": "subtitle", "codec_name": "ass",
         "tags": {"language": "chi"}, "disposition": {"default": 0}},
    ]
    assert choose_subtitle_stream(streams, 2)["index"] == 2
    assert choose_subtitle_stream(streams, None)["index"] == 3


def test_choose_subtitle_rejects_invalid_explicit_index_with_actionable_error():
    streams = [
        {"index": 2, "codec_type": "subtitle", "codec_name": "ass"},
        {"index": 3, "codec_type": "subtitle", "codec_name": "subrip"},
    ]

    with pytest.raises(ValueError, match=r"99.*available.*2, 3"):
        choose_subtitle_stream(streams, 99)


def test_inspect_probe_preserves_source_fps_and_lists_streams():
    raw = {
        "format": {"duration": "1440.0"},
        "streams": [
            {"index": 0, "codec_type": "video", "codec_name": "h264",
             "width": 1920, "height": 1080, "r_frame_rate": "24000/1001"},
            {"index": 1, "codec_type": "audio", "codec_name": "aac"},
            {"index": 3, "codec_type": "subtitle", "codec_name": "ass",
             "tags": {"language": "chi"}, "disposition": {"default": 1}},
        ],
    }
    result = inspect_probe(raw)
    assert result["fps"] == "24000/1001"
    assert result["subtitle_streams"][0]["index"] == 3

