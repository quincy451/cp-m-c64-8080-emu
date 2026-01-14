#!/usr/bin/env python3
"""d64_diff.py

Compare two D64 images and report which track/sector pairs differ.

Usage:
  py tools\d64_diff.py images\original\cpm_emu.d64 images\work\variant.d64
"""
from __future__ import annotations
import sys
from pathlib import Path

SECTORS_PER_TRACK = {**{t:21 for t in range(1,18)},
                     **{t:19 for t in range(18,25)},
                     **{t:18 for t in range(25,31)},
                     **{t:17 for t in range(31,36)}}

def ts_offset(track: int, sector: int) -> int:
    sectors_before = sum(SECTORS_PER_TRACK[t] for t in range(1, track))
    return (sectors_before + sector) * 256

def read_sector(img: bytes, track: int, sector: int) -> bytes:
    off = ts_offset(track, sector)
    return img[off:off+256]

def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    a = Path(sys.argv[1]).read_bytes()
    b = Path(sys.argv[2]).read_bytes()
    if len(a) != len(b):
        print(f"Different sizes: {len(a)} vs {len(b)}")
        return 1

    diffs = []
    for track in range(1, 36):
        for sector in range(SECTORS_PER_TRACK[track]):
            if read_sector(a, track, sector) != read_sector(b, track, sector):
                diffs.append((track, sector))

    if not diffs:
        print("No differences.")
        return 0

    print(f"Differences: {len(diffs)} sector(s)")
    for t,s in diffs[:200]:
        print(f"  T{t:02d} S{s:02d}")
    if len(diffs) > 200:
        print(f"  ... ({len(diffs)-200} more)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
