Exit code: 0
Wall time: 0.2 seconds
Output:
from pathlib import Path
import sys


SCRIPTS = Path(__file__).parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import qa_output
from qa_output import evaluate_probe, sample_times


def valid_probe():
    return {
        "format_duration": 300.0,
        "video": {
            "codec_name": "h264",
            "width": 1920,
            "height": 1080,
            "pix_fmt": "yuv420p",
            "r_frame_rate": "24000/1001",
            "duration": 300.0,
        },
        "audio": {"codec_name": "aac", "sample_rate": "48000", "duration": 300.02},
        "subtitle_stream_count": 0,
    }


def test_evaluate_probe_accepts_delivery_contract():
    report = evaluate_probe(valid_probe(), "24000/1001")
    assert report["delivery_ready"] is True
    assert report["av_end_delta_seconds"] <= 0.5


def test_evaluate_probe_accepts_av_delta_up_to_half_a_second():
    data = valid_probe()
    data["audio"]["duration"] = 300.5
    report = evaluate_probe(data, "24000/1001")
    assert report["delivery_ready"] is True


def test_evaluate_probe_rejects_av_delta_above_half_a_second():
    data = valid_probe()
    data["audio"]["duration"] = 300.5005
    report = evaluate_probe(data, "24000/1001")
    assert report["delivery_ready"] is False
    assert "av_end_delta" in report["failures"]


def test_evaluate_probe_rejects_bad_dimensions_and_av_delta():
    data = valid_probe()
    data["video"]["width"] = 1080
    data["audio"]["duration"] = 300.6
    report = evaluate_probe(data, "24000/1001")
    assert report["delivery_ready"] is False
    assert "resolution" in report["failures"]
    assert "av_end_delta" in report["failures"]


def test_evaluate_probe_rejects_selectable_subtitles_and_loudness_miss():
    data = valid_probe()
    data["subtitle_stream_count"] = 1
    report = evaluate_probe(data, "24000/1001", {"integrated_lufs": -11.0, "true_peak_db": -1.0})
    assert {"subtitle_stream", "integrated_loudness", "true_peak"} <= set(report["failures"])


def test_sample_times_returns_twelve_representative_points():
    values = sample_times(300.0)
    assert len(values) == 12
    assert values[0] == 0.0
    assert values[-1] < 300.0


def test_measure_loudness_parses_final_loudnorm_json(monkeypatch, tmp_path):
    class Result:
        stderr = "[Parsed_loudnorm_0 @ 0] {\"input_i\": \"-14.2\", \"input_tp\": \"-1.7\"}"

    commands = []

    def fake_run(command, **kwargs):
        commands.append(command)
        return Result()

    monkeypatch.setattr("qa_output.subprocess.run", fake_run)
    loudness = qa_output.measure_loudness(tmp_path / "final.mp4")
    assert loudness == {"integrated_lufs": -14.2, "true_peak_db": -1.7}
    assert commands[0][-2:] == ["-f", "null"] or commands[0][-1] == "-"


def test_contact_sheet_uses_exact_reported_sample_schedule(monkeypatch, tmp_path):
    commands = []
    monkeypatch.setattr(qa_output, "measure_loudness", lambda _: {
        "integrated_lufs": -14.0,
        "true_peak_db": -2.0,
    })
    monkeypatch.setattr(qa_output, "probe", lambda _: valid_probe())
    monkeypatch.setattr(qa_output.subprocess, "run", lambda command, **_: commands.append(command))

    report = qa_output.qa_output(
        tmp_path / "final.mp4",
        "24000/1001",
        tmp_path / "contact-sheet.jpg",
    )
    command = commands[0]
    graph_flag = "-filter_complex" if "-filter_complex" in command else "-vf"
    graph = command[command.index(graph_flag) + 1]

    assert report["sample_times"][-1] == 299.95
    assert all(f"start={timestamp:.3f}" in graph for timestamp in report["sample_times"])
    assert "tile=4x3" in graph

