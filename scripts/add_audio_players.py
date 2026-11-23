#!/usr/bin/env python3
"""Add an in-page audio player under each podcast episode's download link.

The episode files now live on GitHub, which makes browsers download them when the link is
clicked instead of playing them. A player on the page streams the same file, so every episode
can still be listened to on the site. Running this twice does not add a second player.

Settings (environment variables): SITE (default: site), AUDIO_PREFIX (default: /dosyalar/podcast/).
"""
import os
import re
from pathlib import Path

SITE = Path(os.environ.get('SITE', 'site'))
PREFIX = os.environ.get('AUDIO_PREFIX', '/dosyalar/podcast/')
LINK = re.compile(r'<a\b[^>]*\bhref="(' + re.escape(PREFIX) + r'[^"]+\.mp3)"[^>]*>.*?</a>', re.S | re.I)
PLAYER = ('<p class="archive-audio"><audio controls preload="none" src="{src}" '
          'style="width:100%;max-width:520px"></audio></p>')

pages = players = 0
for p in sorted(SITE.rglob('*.html')):
    h = p.read_text(encoding='utf-8', errors='surrogateescape')
    if PREFIX not in h:
        continue
    done, out, pos = set(), [], 0
    for m in LINK.finditer(h):
        src = m.group(1)
        if src in done or f'<audio controls preload="none" src="{src}"' in h:
            continue
        done.add(src)
        end = h.find('</p>', m.end())
        nxt = h.find('<p', m.end())
        # after the paragraph that holds the link, if the link is inside one; otherwise right after the link
        at = end + 4 if end != -1 and end - m.end() < 800 and (nxt == -1 or nxt > end) else m.end()
        out.append(h[pos:at] + PLAYER.format(src=src))
        pos = at
    if done:
        out.append(h[pos:])
        p.write_text(''.join(out), encoding='utf-8', errors='surrogateescape')
        pages += 1
        players += len(done)

print(f'added {players} audio players on {pages} pages')
