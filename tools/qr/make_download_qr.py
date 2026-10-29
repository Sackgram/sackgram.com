#!/usr/bin/env python3
"""Writes the QR code for https://sackgram.com/download/ :

    tools/qr/download.svg        inlined into every home page and /download page
    tools/qr/download-print.svg  for print: same code, mm-sized, scales without loss
    tools/qr/download-print.png  for print: 2400 px square, black on white

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

# The trailing slash since 2026-10-18: /download is a directory, so GitHub
# Pages answers the slashless form with a redirect to /download/. With the
# slash the scan lands in one request. Codes printed before carry the
# slashless form and keep working through that redirect.
URL = 'https://sackgram.com/download/'
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'download.svg')

# Error correction M: survives a smudge or a screen's glare without making the
# code dense. Border 4 is the quiet zone the QR standard requires.
qr = segno.make(URL, error='m', micro=False)
qr.save(OUT, kind='svg', border=4, dark='#111418', light='#FFFFFF',
        xmldecl=False, svgns=True, title=None, desc=None, omitsize=True,
        unit=None, svgclass='qr', lineclass=None)
# Print: pure black on white (a printer renders #111418 as a dithered grey).
# The SVG is 1 mm per module (37 mm square including the quiet zone) — scale it
# freely, but keep it at least 20 mm wide on paper. The PNG is 64 px per module
# (2368 px square: 37 mm at ~1600 dpi). A fractional SVG scale is avoided on
# purpose: segno 1.6.6 then draws the white background one module short.
qr.save(os.path.join(HERE, 'download-print.svg'), kind='svg', border=4, dark='#000000',
        light='#FFFFFF', xmldecl=True, svgns=True, title=URL, desc=None,
        unit='mm', scale=1, svgclass=None, lineclass=None)
qr.save(os.path.join(HERE, 'download-print.png'), kind='png', border=4, dark='#000000',
        light='#FFFFFF', scale=64)
print(f'{OUT}: version {qr.version}, {qr.symbol_size(border=4)[0]} modules incl. quiet zone')
