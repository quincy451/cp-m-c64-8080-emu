\
param(
  [Parameter(Mandatory=$true)][string]$ViceExe,
  [Parameter(Mandatory=$true)][string]$D64,
  [int]$WaitSeconds = 12,
  [string]$OutDir = "out"
)

$ErrorActionPreference = "Stop"

if (!(Test-Path $ViceExe)) { throw "VICE exe not found: $ViceExe" }
if (!(Test-Path $D64)) { throw "D64 not found: $D64" }

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$shot  = Join-Path $OutDir ("smoke_" + $stamp + ".png")
$log   = Join-Path $OutDir ("smoke_" + $stamp + ".log")

# Key buffer: load and run CP/M, then USER 0 and DIR.
# VICE manual: -keybuf accepts C-style hex escapes like \x0d for RETURN.
$keybuf = 'LOAD"CP/M",8,1\x0dRUN\x0dUSER 0\x0dDIR\x0d'

$args = @(
  "-logtostdout",
  "-logfile", $log,
  "-8", $D64,
  "-keybuf", $keybuf,
  "-exitscreenshot", $shot
)

Write-Host "Launching VICE:"
Write-Host "  $ViceExe $($args -join ' ')"
Write-Host "Waiting $WaitSeconds second(s)..."

$p = Start-Process -FilePath $ViceExe -ArgumentList $args -PassThru
Start-Sleep -Seconds $WaitSeconds

# Ask VICE to close so it can write the exit screenshot.
$null = $p.CloseMainWindow()
$p.WaitForExit(5000) | Out-Null

if (!$p.HasExited) {
  Write-Warning "VICE did not exit; killing process."
  $p.Kill()
}

if (Test-Path $shot) {
  Write-Host "Wrote screenshot: $shot"
} else {
  Write-Warning "No screenshot produced (VICE may not have exited cleanly)."
}

if (Test-Path $log) {
  Write-Host "Wrote log: $log"
}
