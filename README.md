# cp-m-c64-8080-emu

Commodore 64 CP/M 2.2 (8080 emulation) playground: **tools + repeatable tests** for inspecting and rebuilding CP/M-on-C64 D64 images.

This repo is intentionally set up so you can:
- Keep your **original disk image** pristine
- Run **deterministic analysis** (directory listing from raw sectors, checksums, diffs)
- Run an **automated VICE smoke test** that boots CP/M and runs `DIR`
- Make changes as **patches**, so you don't have to publish copyrighted disk contents publicly

## ⚠️ Legal / licensing note

Many CP/M system disks and utilities are still copyrighted. If you keep this repo public, it's usually safer to:
- **NOT commit disk images** (`.d64`) themselves
- Commit **patches** (e.g., `xdelta3` output) and scripts that apply them to a user-provided base image

If you want to commit `.d64` files anyway, consider making the repo private.

## Repo layout

```text
images/
  original/           # keep your base D64s here (ignored by default)
  work/               # generated variants (ignored by default)
  patches/            # binary patches you can publish
tools/                # Python helpers (dir listing, hashing, diffs)
scripts/              # VICE smoke test / helper scripts
notes/                # disassembly notes, offsets, experiments
out/                  # logs/screenshots (ignored)
```

## Quick start

1. Put your base disk image here (not committed):
   - `images/original/cpm_emu.d64`

2. Check image size + hashes:
   ```powershell
   py tools\d64_check.py images\original\cpm_emu.d64
   ```

3. List the CP/M directory **from raw sectors**:
   ```powershell
   py tools\cpm_dir.py images\original\cpm_emu.d64
   ```

4. Run a VICE smoke test (boots + runs DIR):
   ```powershell
   powershell -ExecutionPolicy Bypass -File scripts\vice_smoketest.ps1 `
     -ViceExe "C:\Path\To\x64sc.exe" `
     -D64 "images\original\cpm_emu.d64"
   ```

## Notes

- The smoke test uses VICE's `-keybuf` option to inject keystrokes (load CP/M, run, `USER 0`, `DIR`).
- If you want a true non-interactive test, we can extend the script to capture screenshots and logs for CI.
