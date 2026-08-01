Exit code: 0
Wall time: 0.2 seconds
Output:
# Project and artifact schemas

`recap-plan.json` is the only hand-edited narration/edit source. `copy\voiceover.txt`, `shot-list.csv`, and `clips.json` are deterministic derivatives and must not be edited.

## `project.json`

| Field | Type | Contract |
|---|---|---|
| `source` | absolute path string | Authorized source whose display aspect is within 1% of 16:9; may be a lossless local-ASR remux. |
| `title` | string | Accurate work/episode title. |
| `authorized_for_public_editing` | boolean | Hard public-derivative gate; must be `true`. |
| `source_audio_authorized` | boolean | Hard source-bed gate; must be `true`. |
| `platform` | string | Default `bilibili`. |
| `output.width`, `output.height` | integers | Fixed `1920`, `1080`. |
| `output.min_seconds` | number | `240`. |
| `output.target_seconds` | number | Planning goal `300`; it is not an exact selected-clip-duration requirement. |
| `output.max_seconds` | number | `360`. |
| `proxy.width`, `proxy.height` | integers | Fixed `960`, `540`. |
| `voice.name` | string | Edge TTS voice, default `zh-CN-YunxiNeural`. |
| `voice.rate` | string | Tested Edge TTS rate, default `+10%`. |
| `voice.pitch` | string | Tested Edge TTS pitch, default `-2Hz`. |
| `audio.source_bed_gain_db` | number | Gain applied exactly once to selected source audio, default `-22`. |
| `audio.target_integrated_lufs` | number | Delivery target `-14`. |
| `audio.true_peak_db` | number | Ceiling `-1.5`. |
| `captions.keywords` | string array | Phrases passed as repeated ASS `--keyword` values. |
| `captions.font` | string | Expected CJK font, default `Microsoft YaHei`. |
| `captions.margin_v` | integer | Bottom-safe vertical margin, default `140`. |
| `analysis.subtitle_stream_index` | integer or null | Optional global ffprobe stream index override. |
| `analysis.scene_threshold` | number | FFmpeg scene-change threshold, default `0.35`. |
| `analysis.fallback_interval_seconds` | positive integer | Even-frame interval when fewer than 12 scene frames are found, default `12`. |
| `excluded_ranges` | array of `[start,end]` number pairs | OP, ED, credits, or forbidden source-time ranges. |

## Analysis artifacts

### `build\analysis\episode.json`

| Field | Type | Meaning |
|---|---|---|
| `duration` | number | Source seconds from ffprobe. |
| `width`, `height` | integers | Source video dimensions. |
| `fps` | rational string | Source `r_frame_rate`, such as `24000/1001`. |
| `video_stream_index` | integer | Global ffprobe index of chosen video stream. |
| `audio_streams` | object array | Full ffprobe records for source audio streams. |
| `subtitle_streams` | object array | Supported text-subtitle ffprobe records. |
| `subtitle_stream_index` | integer | Selected global subtitle stream index. |

Each subtitle-stream record may include `index`, `codec_name`, `tags.language`, and `disposition.default`; the selector uses those fields. `build\analysis\source.srt` is analysis-only.

### `build\analysis\scenes.json`

| Field | Type | Meaning |
|---|---|---|
| `scene_times` | number array | FFmpeg-detected scene-change timestamps. |
| `fallback_used` | boolean | Whether evenly spaced frames supplemented sparse detection. |

`build\analysis\frames\*.jpg` contains compact 480-pixel references. `contact-sheet.jpg` is the first selective overview.

### `build\analysis\cache.json`

| Field | Type | Meaning |
|---|---|---|
| `fingerprint` | SHA-256 string | Hash of absolute source path, size, nanosecond mtime, selected subtitle index, rounded scene threshold, and fallback interval. |
| `frame_manifest` | object array | Completeness check for cached frames. |
| `frame_manifest[].name` | string | Frame filename. |
| `frame_manifest[].size` | integer | Frame byte size. |

The cache is reusable only when the fingerprint matches and source SRT, scenes JSON, contact sheet, and the complete frame manifest all exist.

## `recap-plan.json`

Top-level field:

| Field | Type | Contract |
|---|---|---|
| `segments` | non-empty ordered array | Story order and single source for narration/edit decisions. |

Every segment contains:

| Field | Type | Contract |
|---|---|---|
| `id` | non-empty string | Stable unique production identifier, e.g. `hook-01`. |
| `narration` | non-empty string | Chinese voiceover grounded in evidence. |
| `story_function` | non-empty string | Hook, setup, escalation, reversal, result, or close. |
| `evidence_ranges` | non-empty array of `[start,end]` pairs | Subtitle/source ranges supporting narration. |
| `visual_beats` | non-empty string array | Selectively frame-verified on-screen actions/details. |
| `clip_ranges` | non-empty array of `[start,end]` pairs | Exact source ranges, in seconds, at original speed. |
| `target_seconds` | finite number | Must equal the sum of all `clip_ranges` durations. |
| `spoiler_level` | non-empty string | Editorial disclosure/control label such as `minor`, `major`, or `ending`. |

All ranges must be finite, positive, within source duration, and outside `excluded_ranges`. The total of segment targets may be any value within 240鈥?60 seconds; `output.target_seconds=300` is the planning goal, not an equality constraint.

Example:

```json
{
  "segments": [
    {
      "id": "hook-01",
      "narration": "浠栦互涓烘垬鏂楀凡缁忕粨鏉燂紝鐪熸鐨勬晫浜哄嵈鍒氬垰鐜拌韩銆?,
      "story_function": "hook",
      "evidence_ranges": [[10.0, 18.0]],
      "visual_beats": ["涓昏鍥炲ご鐪嬭鏁屼汉"],
      "clip_ranges": [[10.0, 18.0]],
      "target_seconds": 8.0,
      "spoiler_level": "minor"
    }
  ]
}
```

## Derived assets

### `clips.json`

An ordered array generated from plan clip ranges:

| Field | Type | Meaning |
|---|---|---|
| `source_in` | number | Inclusive source start in seconds. |
| `source_out` | number | Source end in seconds. |
| `target_seconds` | number | `source_out - source_in`; no speed change. |
| `purpose` | string | Generated `<segment-id>:<visual beats>` trace. |

`copy\voiceover.txt` joins segment narration in order. `shot-list.csv` has `segment_id`, `story_function`, `source_in`, `source_out`, `target_seconds`, `visual_beats`, `narration`, and `spoiler_level`.

## `build\proxy-render.json`

`render_proxy.py` invalidates any old manifest before FFmpeg and atomically writes this file only after the input fingerprint is unchanged across a successful render:

| Field | Type | Meaning |
|---|---|---|
| `plan_fingerprint` | SHA-256 string | Hash of `project.json`, `recap-plan.json`, byte-exact `clips.json`, `build\captions.ass`, `build\voiceover.mp3`, and source identity (resolved path, byte size, nanosecond mtime). |
| `proxy_path` | absolute path string | Rendered `build\proxy.mp4`. |
| `proxy_size` | integer | Rendered proxy byte size. |
| `proxy_sha256` | SHA-256 string | Digest of the rendered proxy bytes. |

## `build\proxy-approval.json`

`approve_proxy.py` writes this file only when the current input fingerprint and current proxy path, size, and SHA-256 exactly equal `proxy-render.json`. A missing, invalid, or stale render manifest blocks approval. The approval file uses the same four fields above and is never hand-edited.

Before approval and again before final project probing, `clips.json` must exactly match the deterministic `recap-plan.json` derivative. The final gate verifies the approval fingerprint and requires the proxy at the exact resolved `build\proxy.mp4` path with the approved byte size and SHA-256. Any mismatch, missing field, or missing proxy makes approval invalid or stale.

## QA report

`qa_output.py` prints this JSON:

| Field | Type | Meaning |
|---|---|---|
| `delivery_ready` | boolean | `true` only when no automated failures remain. |
| `failures` | string array | Possible gates include `resolution`, `video_codec`, `audio_codec`, `pixel_format`, `audio_sample_rate`, `frame_rate`, `duration`, `subtitle_stream`, `av_end_delta`, `integrated_loudness`, and `true_peak`. |
| `duration` | number | Final format duration; must be 240鈥?60 seconds. |
| `av_end_delta_seconds` | number | Absolute video/audio stream-end delta. |
| `one_frame_seconds` | number | Diagnostic duration of one expected-FPS frame. |
| `av_tolerance_seconds` | number | Fixed `0.5`. |
| `sample_times` | number array | Twelve representative visual-QA timestamps. |
| `loudness.integrated_lufs` | number | Measured integrated loudness; accepted range is -15 to -13 around the -14 target. |
| `loudness.true_peak_db` | number | Measured true peak; must be at or below -1.5 dBTP. |
| `contact_sheet` | path string, optional | Generated 12-sample contact sheet when requested. |

QA also requires H.264, AAC, 1920脳1080, yuv420p, 48 kHz audio, exact source FPS, zero selectable subtitle streams, and manual inspection of every contact-sheet sample.

