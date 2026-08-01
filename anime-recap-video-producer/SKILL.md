Exit code: 0
Wall time: 0.2 seconds
Output:
---
name: anime-recap-video-producer
description: Use when turning an authorized anime episode with selectable subtitles or completed local-ASR recovery into a 4鈥? minute horizontal Chinese recap for Bilibili or another 16:9 platform, especially with episode analysis, narration, shot lists, FFmpeg proxy review, Edge TTS, burned captions, source-audio mixing, or delivery QA.
---

# Anime Recap Video Producer

## Contract and gates

Create a 1920脳1080 recap at original speed, source FPS, and 16:9. Reject source display aspect outside 1% of 16:9 before scaling. `recap-plan.json` is the sole editable story/edit source; derive `copy\voiceover.txt`, `shot-list.csv`, and `clips.json`. Source subtitles are analysis-only; output has no subtitle stream, only burned recap ASS.

Confirm public-edit and source-audio authorization; set both `project.json` gates to `true` or stop. Require a local episode with video/audio, FFmpeg/ffprobe, title, and either selectable text subtitles or completed [local-ASR recovery](references/workflow.md). `output.target_seconds=300` is the planning goal; validation accepts selected-clip totals from 240 through 360 seconds.

## Exact workflow

Set `$skill` to the skill directory and `$job` to the job directory.

1. Initialize; edit only authorization/configuration in `project.json`.

```powershell
python "$skill\scripts\init_project.py" "<episode>" "$job" --title "<浣滃搧鍚?"
```

2. Inspect; override only a wrongly selected global subtitle index.

```powershell
python "$skill\scripts\inspect_episode.py" "$job"
python "$skill\scripts\inspect_episode.py" "$job" --subtitle-stream-index <index>
```

3. Extract subtitles and compact scene references.

```powershell
python "$skill\scripts\extract_episode.py" "$job"
```

4. Analyze `source.srt`, then inspect only frames near candidate evidence/clip ranges.
5. Author `recap-plan.json` from subtitle evidence and verified visuals. Keep selected clips within 240鈥?60 seconds; target 300.
6. Validate and derive narration, shot list, and clips.

```powershell
python "$skill\scripts\build_recap_assets.py" "$job\recap-plan.json"
```

7. Generate TTS, VTT, ASS, then validate.

```powershell
uvx --from edge-tts edge-tts --voice zh-CN-YunxiNeural --rate=+10% --pitch=-2Hz `
  --file "$job\copy\voiceover.txt" --write-media "$job\build\voiceover.mp3" `
  --write-subtitles "$job\build\voiceover.vtt"
python "$skill\scripts\vtt_to_ass.py" "$job\build\voiceover.vtt" "$job\build\captions.ass"
python "$skill\scripts\validate_project.py" "$job\project.json"
```

8. Render only selected clips; manually review the entire proxy.

```powershell
python "$skill\scripts\render_proxy.py" "$job\project.json"
```

Revise only `recap-plan.json`, re-derive, and rebuild affected assets until accepted.

9. Record approval after review.

```powershell
python "$skill\scripts\approve_proxy.py" "$job"
```

10. Render final once. Approval must match the plan, exact clips derivative, source resolved path/size/mtime, and proxy path/size/SHA-256.

```powershell
python "$skill\scripts\render_final.py" "$job\project.json"
```

11. Run QA with probed source FPS.

```powershell
python "$skill\scripts\qa_output.py" "$job\build\final.mp4" --fps <source-fps> `
  --contact-sheet "$job\build\qa\contact-sheet.jpg"
```

Deliver only with `delivery_ready=true` and manual approval of all 12 samples.

## Cache/rebuild reference

| Change | Rebuild from |
|---|---|
| Source/subtitle/analysis settings | inspect 鈫?extract 鈫?analyze 鈫?plan |
| Any `recap-plan.json` field | derive 鈫?TTS/VTT/ASS 鈫?proxy 鈫?approve |
| Voice/caption settings | TTS/VTT/ASS 鈫?proxy 鈫?approve |
| Source bed/render settings | validate 鈫?proxy 鈫?approve |
| Plan or proxy after approval | proxy review 鈫?approve; final gate is stale |

Cache only complete matching outputs; never edit derivatives. Keep -14 LUFS, -1.5 dBTP, and 鈮?.5-second A/V delta.

## References

- Read [project-schema.md](references/project-schema.md) for every project, analysis, plan, cache, approval, clip, and QA field.
- Read [workflow.md](references/workflow.md) for ASR, selective inspection, timing, audio, proxy review, publishing, and troubleshooting.