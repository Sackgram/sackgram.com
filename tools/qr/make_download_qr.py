#!/usr/bin/env python3
"""Writes tools/qr/download.svg — the QR code for https://sackgram.com/download

    pip install segno==1.6.6
    python3 tools/qr/make_download_qr.py

ADDED 2026-10-09 (Eric). Run only when the address changes; the SVG is
committed, and tools/build_pages.py inlines it into every home page and
/download page, so the build itself needs nothing beyond the standard library
and the page makes no request for it.

⚠ THE ADDRESS CARRIES NO TRACKING PARAMETER, ON PURPOSE. No utm_*, no
referrer: a person who scans it lands on the plain /download page.
"""
import os

import segno

URL = 'https://sackgram.com/download'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'download.svg')

# Error correction M: survives a smudge or a screen's glare without making the
# code dense. Border 4 is the quiet zone the QR standard requires.
qr = segno.make(URL, error='m', micro=False)
qr.save(OUT, kind='svg', border=4, dark='#111418', light='#FFFFFF',
        xmldecl=False, svgns=True, title=None, desc=None, omitsize=True,
        unit=None, svgclass='qr', lineclass=None)
print(f'{OUT}: version {qr.version}, {qr.symbol_size(border=4)[0]} modules incl. quiet zone')
