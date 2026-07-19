#!/usr/bin/env python3
"""Audit VERBATIM blocks in an interview cut script against a source transcript."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


BLOCK_RE = re.compile(
    r"<!--\s*VERBATIM:(?P<id>[A-Za-z0-9_-]+)\s*-->"
    r"(?P<text>.*?)"
    r"<!--\s*/VERBATIM\s*-->",
    re.DOTALL,
)
HAN_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
WORD_RE = re.compile(r"[A-Za-z]+(?:['’-][A-Za-z]+)*|\d+(?:[.,]\d+)*")


def normalize_for_match(text: str) -> str:
    """Ignore layout whitespace only; keep wording and punctuation exact."""
    return re.sub(r"\s+", "", text)


def clean_block(text: str) -> str:
    lines = [line.strip() for line in text.strip().splitlines()]
    return "\n".join(line for line in lines if line)


def content_units(text: str) -> tuple[int, int, int]:
    han = len(HAN_RE.findall(text))
    words = len(WORD_RE.findall(text))
    return han, words, han + words


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Verify that every marked VERBATIM block exists in the source transcript, "
            "then count spoken-content units."
        )
    )
    parser.add_argument("--source", required=True, type=Path, help="Source TXT transcript")
    parser.add_argument("--cut", required=True, type=Path, help="Markdown cut script")
    parser.add_argument(
        "--target-units",
        type=int,
        default=None,
        help="Optional target for Chinese Han characters plus English/number tokens",
    )
    parser.add_argument(
        "--pure-out",
        type=Path,
        default=None,
        help="Write only the VERBATIM block text to this UTF-8 file",
    )
    return parser.parse_args()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        raise SystemExit(f"ERROR: file not found: {path}")
    except UnicodeDecodeError as exc:
        raise SystemExit(f"ERROR: expected UTF-8 text: {path}: {exc}")


def main() -> int:
    args = parse_args()
    source = read_text(args.source)
    cut = read_text(args.cut)
    blocks = [(m.group("id"), clean_block(m.group("text"))) for m in BLOCK_RE.finditer(cut)]

    if not blocks:
        print("ERROR: no VERBATIM blocks found", file=sys.stderr)
        return 2

    source_normalized = normalize_for_match(source)
    missing: list[str] = []
    empty: list[str] = []
    duplicate_ids: list[str] = []
    seen_ids: set[str] = set()
    reused_text: list[str] = []
    seen_text: dict[str, str] = {}

    for block_id, text in blocks:
        if block_id in seen_ids:
            duplicate_ids.append(block_id)
        seen_ids.add(block_id)

        normalized = normalize_for_match(text)
        if not normalized:
            empty.append(block_id)
            continue
        if normalized not in source_normalized:
            missing.append(block_id)
        if normalized in seen_text:
            reused_text.append(f"{block_id}={seen_text[normalized]}")
        else:
            seen_text[normalized] = block_id

    pure_text = "\n\n".join(text for _, text in blocks if text)
    han, words, units = content_units(pure_text)
    minutes_fast = units / 300 if units else 0.0
    minutes_slow = units / 280 if units else 0.0

    print(f"verbatim_blocks: {len(blocks)}")
    print(f"missing_verbatim_blocks: {len(missing)}")
    print(f"empty_verbatim_blocks: {len(empty)}")
    print(f"duplicate_block_ids: {len(duplicate_ids)}")
    print(f"reused_verbatim_blocks: {len(reused_text)}")
    print(f"han_characters: {han}")
    print(f"english_number_tokens: {words}")
    print(f"content_units: {units}")
    print(f"estimated_minutes_at_300_per_min: {minutes_fast:.2f}")
    print(f"estimated_minutes_at_280_per_min: {minutes_slow:.2f}")

    if args.target_units is not None:
        delta = units - args.target_units
        percent = (delta / args.target_units * 100) if args.target_units else 0.0
        print(f"target_units: {args.target_units}")
        print(f"target_delta: {delta:+d} ({percent:+.1f}%)")

    if missing:
        print("missing_ids: " + ", ".join(missing))
    if empty:
        print("empty_ids: " + ", ".join(empty))
    if duplicate_ids:
        print("duplicate_ids: " + ", ".join(duplicate_ids))
    if reused_text:
        print("reused_text: " + ", ".join(reused_text))

    if args.pure_out is not None:
        args.pure_out.parent.mkdir(parents=True, exist_ok=True)
        args.pure_out.write_text(pure_text + "\n", encoding="utf-8")
        print(f"pure_text_written: {args.pure_out}")

    if missing or empty or duplicate_ids:
        print("result: FAIL")
        return 2

    print("result: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
