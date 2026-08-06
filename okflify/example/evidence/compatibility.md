---
okf_version: "0.2"
type: evidence-pointer
title: "Compatibility proof — OKF manual, ORF pack, EMF pack, and mobile Hostkey site"
tags: [evidence, build, orf, emf, mobile, release]
sources:
  - repo: eidos-agi/okflify
  - repo: eidos-agi/eidos-squiddie
  - repo: eidos-agi/emf
verified:
  by: job:okflify-build
  at: 2026-08-06
  method: "pytest, canonical pack renders, public HTTPS requests, and Mafia Chromium at 390x844"
  stale_after: 2026-09-06
---

# Compatibility proof

This page names the concrete checks behind the compatibility claim. It is not a
promise that every future profile field has semantic UI; it proves that current
OKF, ORF, and EMF documents render without a format fork and that their versions
are visible.

## Inputs

| Format | Canonical input | Expected header |
|---|---|---|
| OKF | Packaged detailed guide in `okflify/example/` | `OKF v0.2` |
| ORF | `eidos-squiddie/examples/orf-minimal/` | `OKF v0.2 · ORF v0.2.0` |
| EMF | `emf/examples/` | `OKF v0.2 · EMF v0.1` |

## Commands

```sh
python -m pytest -q
python -m okflify --example -o /tmp/okflify-guide.html
python -m okflify ../eidos-squiddie/examples/orf-minimal -o /tmp/orf.html
python -m okflify ../emf/examples -o /tmp/emf.html
```

The release suite checks link resolution, nested verification frontmatter,
bundle and catalogue discovery, host return links, GitHub link configuration,
self-contained output placeholders, mobile drawer structure, ORF/EMF version
labels, loud empty-directory failure, and single-sourced package versioning.

## Browser proof

The public guide is tested with Mafia against
`https://okflify.eidosagi.com/` at a 390 × 844 viewport.

| Check | Required result |
|---|---|
| Document width | `clientWidth == scrollWidth == 390` |
| Closed navigation | Sidebar off canvas; `aria-expanded=false` |
| Open navigation | Sidebar at x=0, 320px wide; `aria-expanded=true` |
| Main content | Starts below the 60px mobile header |
| HTTPS | Caddy serves the Hostkey static artifact with a valid certificate |

## What the proof means

- The same executable renders base OKF, ORF, and EMF.
- ORF and EMF version stamps survive to visible output.
- The detailed manual ships inside the wheel, so `okflify --example` works after installation.
- The public site is a static artifact produced by OKFlify, not a separate hand-built marketing page.
- Mobile usability is measured against the deployed URL rather than inferred from CSS.

Return to [the guide](../index.md) or read [how profiles compose](../learnings/profile-composition.md).
