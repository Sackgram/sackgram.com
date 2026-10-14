# Downloads Google's official "Get it on Google Play" badges, one per site
# language, into assets/google-play/<lang>.png. ADDED 2026-10-09.
#
#   cd C:\Users\rephi\sackgram.com
#   powershell -ExecutionPolicy Bypass -File .\tools\fetch_play_badges.ps1
#   python tools\check_play_badges.py
#
# The files are Google's own artwork (https://play.google.com/intl/en_us/badges/),
# used unmodified. They are committed here so the site never hotlinks Google:
# a hotlinked badge would hand every visitor's IP address to a third party.
# If one download fails, get that language's badge from the page above
# (choose the language, download the PNG) and save it under the same name.
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$out = Join-Path $root 'assets\google-play'
New-Item -ItemType Directory -Force -Path $out | Out-Null
# site language -> Google's badge code
$codes = [ordered]@{
  en = 'en'; ko = 'ko'; de = 'de'; es = 'es'; fr = 'fr'; id = 'id'; it = 'it';
  ja = 'ja'; pt = 'pt-br'; ru = 'ru'; zh = 'zh-cn'; ar = 'ar'
}
$failed = @()
foreach ($lang in $codes.Keys) {
  $url = "https://play.google.com/intl/en_us/badges/static/images/badges/$($codes[$lang])_badge_web_generic.png"
  $dest = Join-Path $out "$lang.png"
  try {
    Invoke-WebRequest -Uri $url -OutFile $dest -UseBasicParsing
    Write-Host "OK   $lang  <- $url"
  } catch {
    Write-Host "FAIL $lang  <- $url"
    $failed += $lang
  }
}
if ($failed.Count -gt 0) { Write-Host "Failed: $($failed -join ', ')"; exit 1 }
