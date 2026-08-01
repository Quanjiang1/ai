Exit code: 0
Wall time: 0.2 seconds
Output:
# Horizontal recap workflow

## Contents

1. Timing and story design
2. Subtitle and visual analysis
3. Audio and captions
4. Proxy review and approval
5. Publishing disclosure
6. Troubleshooting paths

## Timing and story design

Use 300 seconds as the planning goal. A valid selected-clip total may be any value from 240 through 360 seconds; use these guideposts:

| Target | Use |
|---|---|
| 240 seconds | Lean episode, one main conflict |
| 300 seconds | Default, balanced setup/escalation/result |
| 360 seconds | Dense episode that needs more causal context |

Treat 300 as a goal, not an equality requirement. Build a fast hook, only the setup needed to understand the conflict, escalating cause-and-effect beats, the episode result, and a brief forward-looking close. Measure generated narration audio; do not estimate timing from character count.

`recap-plan.json` is the shared source for narration and clips. Every segment needs subtitle-supported evidence and selectively inspected visuals. `build_recap_assets.py` validates that each segment's `target_seconds` equals the exact sum of its `clip_ranges`, so playback speed never changes. Preserve source FPS and 16:9 framing. Validate display aspect within 1% of 16:9 before scaling; reject 16:10 and ultrawide sources. Do not crop, track, blur-fill, or create per-clip masters.

## Subtitle and visual analysis

`inspect_episode.py` selects text subtitles in this order: explicit global stream index, first Chinese-language track, default track, then first supported text track. Supported codecs are ASS/SSA, SubRip, WebVTT, and mov_text. The selected subtitle is extracted to `build\analysis\source.srt` for analysis only.

If inspection raises `no extractable text subtitle stream; run local speech recognition`:

1. Run an approved local ASR tool and save a time-coded UTF-8 SRT outside the job.
2. Remux a local analysis/render working source without re-encoding video or audio:

```powershell
ffmpeg -i "<episode>" -i "<local-asr.srt>" -map 0:v:0 -map 0:a:0? -map 1:0 `
  -c:v copy -c:a copy -c:s srt "<analysis-source.mkv>"
```

3. Update `project.json.source` to the absolute working-source path, rerun `inspect_episode.py`, then run `extract_episode.py`. The remuxed subtitle remains analysis-only because proxy/final rendering maps only composed video/audio; proxy also uses `-sn`.

Analyze text first: mark story turns and candidate evidence ranges from `source.srt`. Review the extraction contact sheet and scene timestamps next. Open only nearby 480-pixel scene frames needed to verify character, action, location, continuity, and safe cut points. Do not perform dense full-episode frame analysis or transcode a full-episode proxy.

## Audio and captions

Keep the licensed episode audio as a low source bed under narration. The renderer trims and concatenates only selected source ranges, applies `audio.source_bed_gain_db` once, resamples to 48 kHz, mixes narration, then runs two-pass loudness normalization for the single final encode. Targets are -14 LUFS integrated and no higher than -1.5 dBTP.

Generate VTT from the same derived `copy\voiceover.txt`, then convert it to ASS. The ASS is the only burned caption source. Final delivery must contain zero selectable subtitle streams.

## Proxy review and approval

The proxy is a 960脳540 ultrafast render of only the chosen clips with narration, source bed, and burned recap captions. Watch it end to end. Reject it for:

- weak opening or unclear causal progression;
- OP/ED/credits, excluded material, long black fades, or repeated shots;
- source sound masking narration or abrupt bed transitions;
- captions over faces, unreadable two-line breaks, overlaps, or mistimed emphasis;
- crop, speed, frame-rate, aspect-ratio, or obvious compression/artifact problems.

Revise only `recap-plan.json` for narration/edit decisions, regenerate derivatives, rerender, and review again. `render_proxy.py` removes any old `build\proxy-render.json`, fingerprints all inputs immediately before FFmpeg, rejects input changes during rendering, then atomically records the stable fingerprint and proxy path, size, and SHA-256. Run `approve_proxy.py` only after a human accepts that proxy. Approval requires `clips.json` to be the byte-exact deterministic plan derivative and requires current inputs and proxy metadata to exactly equal the render manifest; missing, stale, or manually substituted proxy provenance is rejected. The final gate repeats its approval checks before probing or rendering; any change requires proxy review and approval again.

## Publishing disclosure

Name the title accurately, state that the upload is a recap/derivative commentary, credit authorized sources as required, and use the platform's AI-generated/synthetic-content label. Suggested Chinese disclosure:

`鏈棰戞梺鐧戒娇鐢?AI 璇煶鍚堟垚锛屽彂甯冩椂涓诲姩閫夋嫨骞冲彴鎻愪緵鐨?AI 鐢熸垚/鍚堟垚鏍囪瘑銆俙

## Troubleshooting paths

| Symptom | Exact path |
|---|---|
| Wrong subtitle selected | Rerun `inspect_episode.py "$job" --subtitle-stream-index <global-index>` 鈫?`extract_episode.py` 鈫?reanalyze. |
| No selectable text subtitle | Run local ASR 鈫?losslessly remux the SRT as above 鈫?update `project.json.source` 鈫?inspect 鈫?extract. |
| Extraction unexpectedly reused | Check `build\analysis\cache.json`; source path/size/mtime, subtitle index, scene threshold, or fallback interval must change the fingerprint. Delete only incomplete analysis outputs, never the source. |
| Too few scene frames | Lower `analysis.scene_threshold` or reduce `fallback_interval_seconds` 鈫?rerun extract; the fallback activates below 12 detected frames. |
| Subtitle overflow/overlap | Shorten the segment narration in `recap-plan.json` 鈫?derive 鈫?TTS/VTT 鈫?ASS 鈫?proxy review. Never edit VTT/ASS as the fix. |
| Low-pass/filter error | Ensure narration is decoded/resampled to 48 kHz before `lowpass=f=15000`; rerun TTS if its media is corrupt. |
| Font failure | Verify Microsoft YaHei (`msyh.ttc`, `msyhbd.ttc`) exists in `C:\Windows\Fonts`; final render stages only those fonts. |
| Wrong FPS or geometry | Use `build\analysis\episode.json.fps`; preserve 16:9, original speed, and source FPS. Do not add crop or speed filters. |
| Source bed masks voice | Change `audio.source_bed_gain_db` once in `project.json` 鈫?validate 鈫?proxy 鈫?review 鈫?approve. Do not stack gain filters. |
| Approval missing/stale | Rerender and manually review the proxy, then run `approve_proxy.py`; never edit `proxy-approval.json`. |
| Loudness/true-peak miss | Confirm -14 LUFS/-1.5 dBTP configuration, rerun the audio-only measurement and single final encode, then QA. |
| A/V end delta over 0.5 s | Fix plan/TTS timing, regenerate derivatives, proxy-review/approve again, render final once, then rerun QA. |
| Selectable subtitle in final | Treat as delivery failure. Render through the provided mapped video/audio graph and verify zero subtitle streams with QA. |
| QA visual sample fails | Fix the owning plan/caption/audio input, repeat its cache row, and inspect all 12 regenerated contact-sheet frames. |

