# bisikletsporu.com - static archive

A frozen, static copy of **www.bisikletsporu.com** (Turkish pro-cycling blog, 2012-2016),
made in November 2026 when the site moved off its old WordPress hosting.

- `site/` - the website exactly as visitors saw it, served by Cloudflare Pages.
  Every post, page, category and image keeps its original address.
- **Podcast** - the 33 episodes live in this repository's
  [podcast release](https://github.com/buyruka/bisikletsporu-arsiv/releases/tag/podcast);
  old links under `/dosyalar/podcast/` are redirected there by `site/_redirects`.
- The search box uses Google site search (a static site has no database).

`scripts/` and `.github/workflows/` hold the tools that made the copy. They need the
old server, so they only work until it is switched off; they are kept for the record.
