#!/usr/bin/env python3
"""Fetches Apple's "Download on the App Store" badges into assets/app-store/.

    python3 tools/fetch_appstore_badges.py

ADDED 2026-10-18. The source is Apple's Marketing Resources toolbox
(toolbox.marketingtools.apple.com), the black badge, one localized SVG per
site language. The files are committed and served from this site — never
hotlinked, so a visitor's browser contacts nobody but sackgram.com. Apple's
guidelines forbid altering the artwork, so this script refuses a file that
does not look like a plain SVG and never edits one.
"""
import os
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'app-store')
API = 'https://toolbox.marketingtools.apple.com/api/v2/badges/download-on-the-app-store/black/{}'

# Site language -> Apple's badge locale. Arabic is ar-ar (ar-sa returns 404).
LOCALES = {'en': 'en-us', 'ko': 'ko-kr', 'ja': 'ja-jp', 'zh': 'zh-cn', 'de': 'de-de',
           'fr': 'fr-fr', 'es': 'es-es', 'it': 'it-it', 'pt': 'pt-br', 'ru': 'ru-ru',
           'ar': 'ar-ar', 'id': 'id-id'}

os.makedirs(OUT, exist_ok=True)
for lang, loc in LOCALES.items():
    with urllib.request.urlopen(API.format(loc), timeout=30) as r:
        data = r.read()
    text = data.decode('utf-8')
    if '<svg' not in text or '<script' in text.lower() or 'foreignobject' in text.lower():
        raise SystemExit(f'{lang} ({loc}): not a plain SVG — refusing to save it')
    with open(os.path.join(OUT, f'{lang}.svg'), 'wb') as f:
        f.write(data)
    print(f'{lang}: {loc}, {len(data)} bytes')
