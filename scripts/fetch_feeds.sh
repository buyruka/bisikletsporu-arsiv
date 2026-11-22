#!/usr/bin/env bash
# Save the site's real RSS feeds into a folder (the crawl folder or site/).
# The old site sends ordinary visitors to a FeedBurner copy of /feed/, but lets
# FeedBurner's own robot through, so these requests identify as FeedBurner.
# /category/podcast/feed/ is the real podcast feed (episodes as MP3 enclosures).
set -euo pipefail
DEST="${1:?usage: fetch_feeds.sh <folder>, e.g. site or crawl/www.bisikletsporu.com}"
UA="FeedBurner/1.1 (http://www.FeedBurner.com)"

fetch() {
  local path="$1" out tmp
  out="$DEST${path}index.html"
  tmp=$(mktemp)
  if curl -sS --fail -A "$UA" -o "$tmp" "https://www.bisikletsporu.com$path" \
     && head -c 200 "$tmp" | grep -q '<?xml' && grep -q '<channel>' "$tmp"; then
    mkdir -p "$(dirname "$out")"
    mv "$tmp" "$out"
    echo "saved $path: $(wc -c < "$out") bytes, $(grep -o '<item>' "$out" | wc -l) items, $(grep -o '<enclosure ' "$out" | wc -l) audio files"
  else
    echo "WARNING: $path did not come back as an RSS feed; left unchanged"
    rm -f "$tmp"
  fi
}

fetch /feed/
fetch /comments/feed/
fetch /category/podcast/feed/
