#!/usr/bin/env python3
"""Checks that assets/google-play/<lang>.png exists for every site language
and is a real PNG of badge proportions. ADDED 2026-10-09.

    python3 tools/check_play_badges.py

The home pages and /download reference these files; a missing one shows as a
broken image. Exit status 1 names every missing or wrong file.
"""
import os
import struct
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ['en', 'ko', 'de', 'es', 'fr', 'id', 'it', 'ja', 'pt', 'ru', 'zh', 'ar']

bad = []
for lang in LANGS:
    p = os.path.join(ROOT, 'assets', 'google-play', f'{lang}.png')
    if not os.path.exists(p):
        bad.append(f'{lang}: missing ({p})')
        continue
    with open(p, 'rb') as f:
        head = f.read(24)
    if head[:8] != b'\x89PNG\r\n\x1a\n':
        bad.append(f'{lang}: not a PNG (an HTML error page saved as .png?)')
        continue
    w, h = struct.unpack('>II', head[16:24])
    ratio = w / h if h else 0
    # Google's generic web badges are about 2.3–3.9 : 1 across languages.
    status = 'OK' if 2.0 <= ratio <= 4.5 else 'ODD RATIO'
    print(f'{status:9} {lang}: {w}x{h}')
    if status != 'OK':
        bad.append(f'{lang}: {w}x{h} does not look like a badge')
if bad:
    print('\n'.join(['', 'PROBLEMS:'] + bad))
    sys.exit(1)
print('all 12 badges present')
