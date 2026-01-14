#!/usr/bin/env python3
"""cpm_dir.py

Print a DIR-style listing of the CP/M filesystem stored in a C64 CP/M D64.

Assumptions (matches common C64 CP/M 2.2-on-1541 layouts):
- CP/M uses only the first 17 *256-byte* sectors (0..16) of each physical track.
- Physical track 18 is skipped (CBM directory/BAM live there).
- CP/M has 2 reserved system tracks (OFF=2).
- CP/M block size is 1KiB (4 host sectors).
- Directory consumes 2 blocks = 2KiB = 64 entries.

Usage:
  py tools\cpm_dir.py images\original\cpm_emu.d64
"""
from __future__ import annotations
import sys
from pathlib import Path

SECTORS_PER_TRACK = {**{t:21 for t in range(1,18)},
                     **{t:19 for t in range(18,25)},
                     **{t:18 for t in range(25,31)},
                     **{t:17 for t in range(31,36)}}

D64_SIZE = 174_848
HOST_SECTORS_PER_TRACK = 17  # sectors 0..16 only
CPM_OFF = 2                  # system track offset
DIR_HOST_SECTORS = 8         # 2 blocks * 4 sectors/block

def ts_offset(track: int, sector: int) -> int:
    sectors_before = sum(SECTORS_PER_TRACK[t] for t in range(1, track))
    return (sectors_before + sector) * 256

def read_sector(d64: bytes, track: int, sector: int) -> bytes:
    off = ts_offset(track, sector)
    return d64[off:off+256]

def host_to_phys_track(host_track: int) -> int:
    # host 0..16 -> physical 1..17 ; host 17..33 -> physical 19..35
    return host_track + 1 if host_track <= 16 else host_track + 2

def get_host_sector(d64: bytes, host_track: int, host_sector: int) -> bytes:
    pt = host_to_phys_track(host_track)
    return read_sector(d64, pt, host_sector)

def parse_dir(d64: bytes):
    # Directory is the first 8 host sectors starting at host track CPM_OFF
    raw = b''.join(get_host_sector(d64, CPM_OFF, s) for s in range(DIR_HOST_SECTORS))
    entries = []
    for i in range(0, len(raw), 32):
        e = raw[i:i+32]
        user = e[0]
        if user == 0xE5:
            continue
        name = e[1:9].decode('ascii', errors='replace').rstrip()
        ext  = e[9:12].decode('ascii', errors='replace').rstrip()
        entries.append((user, name, ext))
    return entries

def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    p = Path(sys.argv[1])
    d64 = p.read_bytes()
    if len(d64) != D64_SIZE:
        raise SystemExit(f"Unexpected size {len(d64)} bytes (expected {D64_SIZE})")

    entries = parse_dir(d64)
    if not entries:
        print("(no CP/M directory entries found in first 64 entries)")
        return 0

    by_user = {}
    for user, name, ext in entries:
        by_user.setdefault(user, []).append((name, ext))

    for user in sorted(by_user.keys()):
        files = sorted(by_user[user], key=lambda t:(t[0], t[1]))
        print(f"USER {user}")
        for name, ext in files:
            print(f"  {name:<8} {ext:<3}")
        print()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
