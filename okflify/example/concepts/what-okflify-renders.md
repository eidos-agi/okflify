---
okf_version: "0.2"
type: claim
title: "What okflify renders, and how to reach each part"
tags: [okflify, features]
sources:
  - repo: eidos-agi/okflify
verified:
  by: job:okflify-build
  at: 2026-07-29
  method: "every row below is exercised by the page you are reading; a broken feature breaks this page"
---

## One command

```sh
okflify <bundle-or-catalogue> --open
```

Output is **one self-contained HTML file**. No server, no build step, no
dependencies — it opens from `file://`, survives email, and prints.

## What you get

| Feature | Where | Note |
|---|---|---|
| **Trust card** | top of every document | tier, date, method, staleness, agent warning |
| **Knowledge graph** | sidebar → Overview | drag nodes, click to open; size = inbound links, colour = tier |
| **Tree** | sidebar → Overview | bundle → section → document, collapsible |
| **Backlinks** | foot of each document | "links to" / "linked from" as cards |
| **⌘K palette** | anywhere | indexes documents **and** every h2/h3 |
| **Copy page** | title row | Markdown for LLMs · open in Claude/ChatGPT · copy whole bundle |
| **Diagram surfing** | click any diagram | scroll zooms at cursor, drag or space+drag pans, `0` fit, `1` actual, `esc` |
| **Theme** | header | light/dark; diagrams re-render to match |
| **Print** | header | every document, page-broken |

## Catalogues

Point it at a directory of bundles — `root/bundles/<slug>/` or `root/<slug>/` —
and it renders them as one site. Slugs are namespaced `<bundle>/<doc>`, so
`../other-bundle/index.md` becomes a real cross-bundle edge, and the sidebar
groups by bundle.

The ARP catalogue it was built for: **18 bundles, 102 documents, 88 edges.**

## Theming

`docs.json`, Mintlify-shaped. Never edit the template to restyle.

```json
{ "name": "My Knowledge",
  "colors": { "primary": "#2E6F5E", "light": "#6FC7AC", "dark": "#1F5044" },
  "fonts": { "family": "Inter" },
  "background": { "decoration": "gradient" } }
```

Any Google Font name loads automatically.

## Counter-cases

- Not an editor. okflify reads; something else writes.
- Not a general markdown renderer — it renders what bundles contain.
- Mermaid loads from a CDN at view time, so diagrams need network on first paint.

## Known gaps

Stated because [trust-tiers](trust-tiers.md) makes overselling a bug:

- No arrowheads on graph edges — direction is invisible
- Layout re-seeds per visit rather than staying stable
- No full-text search across document *bodies* (titles and headings only)
