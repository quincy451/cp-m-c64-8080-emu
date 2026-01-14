#!/usr/bin/env python3
"""d64_check.py

Quick sanity checks for a D64:
- exact expected size
- md5/sha1/sha256 hashes

Usage:
  py tools\d64_check.py images\original\cpm_emu.d64
"""
from __future__ import annotations
import sys, hashlib
from pathlib import Path

D64_SIZE = 174_848

def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    p = Path(sys.argv[1])
    data = p.read_bytes()
    print(f"File: {p}")
    print(f"Size: {len(data)} bytes")
    if len(data) != D64_SIZE:
        print(f"WARNING: expected {D64_SIZE} bytes for a standard 35-track D64")
    print("MD5   :", hashlib.md5(data).hexdigest())
    print("SHA1  :", hashlib.sha1(data).hexdigest())
    print("SHA256:", hashlib.sha256(data).hexdigest())
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
