Exit code: 0
Wall time: 0.2 seconds
Output:
"""Convert Edge TTS WebVTT to safe two-line 1920x1080 ASS captions."""

from __future__ import annotations

import argparse
from pathlib import Path
import re


MAX_CHARS_PER_LINE = 26
HIGHLIGHT = r"{\c&H00FFFF&}"
WHITE = r"{\c&HFFFFFF&}"


def _cs(value: str) -> int:
    hours, minutes, seconds = value.split(":")
    whole, millis = re.split(r"[.,]", seconds)
    return (int(hours) * 3600 + int(minutes) * 60 + int(whole)) * 100 + int(millis[:2])


def _ass_time(value: int) -> str:
    hours, remainder = divmod(value, 360000)
    minutes, remainder = divmod(remainder, 6000)
    seconds, centis = divmod(remainder, 100)
    return f"{hours}:{minutes:02}:{seconds:02}.{centis:02}"


def _events(text: str) -> list[tuple[int, int, str]]:
    parsed = []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        timing = next((index for index, line in enumerate(lines) if "-->" in line), None)
        if timing is None:
            continue
        start, end = (part.strip().split()[0] for part in lines[timing].split("-->"))
        caption = "".join(lines[timing + 1:])
        if caption:
            parsed.append((_cs(start), _cs(end), caption))
    return parsed


def _parts(text: str) -> list[tuple[str, int]]:
    lines = [text[index:index + MAX_CHARS_PER_LINE] for index in range(0, len(text), MAX_CHARS_PER_LINE)]
    return [(r"\N".join(lines[index:index + 2]), sum(len(x) for x in lines[index:index + 2]))
            for index in range(0, len(lines), 2)]


def _style(text: str, keywords: list[str]) -> str:
    for keyword in sorted(filter(None, keywords), key=len, reverse=True):
        text = text.replace(keyword, f"{HIGHLIGHT}{keyword}{WHITE}")
    return text


def convert_vtt(source: Path, target: Path, keywords: list[str] | None = None) -> int:
    keywords = keywords or []
    output = []
    previous_end = 0
    for raw_start, raw_end, caption in _events(source.read_text(encoding="utf-8-sig")):
        start = max(raw_start, previous_end)
        end = raw_end
        if end <= start:
            continue
        parts = _parts(caption)
        total = sum(length for _, length in parts)
        consumed = 0
        part_start = start
        for index, (part, length) in enumerate(parts):
            consumed += length
            part_end = end if index == len(parts) - 1 else start + round((end - start) * consumed / total)
            output.append(
                f"Dialogue: 0,{_ass_time(part_start)},{_ass_time(part_end)},Main,,0,0,0,,{_style(part, keywords)}"
            )
            part_start = part_end
        previous_end = end
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Main,Microsoft YaHei,58,&H00FFFFFF,&H0000FFFF,&H00000000,&H60000000,-1,0,0,0,100,100,0,0,1,4,1,2,130,130,140,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(header + "\n".join(output) + "\n", encoding="utf-8-sig")
    return len(output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("target", type=Path)
    parser.add_argument("--keyword", action="append", default=[])
    args = parser.parse_args()
    print(f"ASS_EVENTS={convert_vtt(args.source, args.target, args.keyword)}")


if __name__ == "__main__":
    main()

