# okflify

**Converts OKF bundles into HTML.**

One command, one self-contained file. No server, no build pipeline, no dependencies — Python standard library only.

```sh
pip install -e .
okflify --example --open   # see it work: okflify's own docs, as a bundle
okflify ~/path/to/bundle --open
```

**[See it live →](https://eidos-agi.github.io/okflify/)** — the rendered example, no install.
Rebuilt from source by CI on every push to `master`, so the demo cannot drift from the renderer.

**Start with `--example`.** The [`example/`](example/) bundle *is* okflify's
documentation — written as an OKF bundle, rendered by the tool it documents. If
the renderer breaks, that page does not build, so the docs cannot drift.

```
okflify → bundle/okflify.html — 9 documents, 7 edges, 13 diagrams
```

---

## OKF is a graph, not a tree

[Open Knowledge Format](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing) v0.2 bundles are stored as directories, but the directory is **not** the structure. Concepts connect through ordinary markdown links, which makes a bundle a network rather than a hierarchy.

Most renderers throw that away and print a folder tree. okflify extracts the link graph and puts it first.

## What it renders

| | |
|---|---|
| **Knowledge graph** | force-directed, drag to rearrange, click to open. Node size = inbound links, colour = trust tier |
| **Trust signals** | OKF v0.2 `verified.by/at/method` per document. `human: > job: > agent:` — an agent-only document is labelled **unverified for gate-shaped decisions**, because that is what it is |
| **Backlinks** | "links to" / "linked from" cards on every page |
| **Diagram surfing** | click any mermaid or image → lightbox. Scroll zooms at the cursor, drag or <kbd>space</kbd>+drag pans, <kbd>+</kbd>/<kbd>−</kbd>, <kbd>0</kbd> fit, <kbd>1</kbd> actual size, arrows nudge, <kbd>esc</kbd> closes |
| **Also** | sidebar search, on-this-page rail, light/dark, print layout, typed callouts |

## Bundle layout it expects

```
bundle/
  index.md          # type: investigation — the root
  log.md            # append-only, no frontmatter by convention
  concepts/*.md     # claims, rules — ANY md-bearing subdirectory becomes a group
  facts/*.md        # (facts/, architecture/, runtime/… all scanned since 28a8cf3)
  evidence/*.md     # evidence pointers
  learnings/*.md    # promoted, re-verified
  docs.json         # optional theming
  template.html     # optional override
```

Everything is optional except having at least one document. Missing directories are skipped.

## Theming

`docs.json` follows the Mintlify shape. **Never edit the template to restyle.**

```json
{
  "name": "My Bundle",
  "colors": { "primary": "#9F3232", "light": "#E08A8A", "dark": "#7A2424" },
  "fonts": { "family": "Inter", "heading": "Inter" },
  "appearance": { "default": "system" },
  "background": { "decoration": "gradient" },
  "styling": { "eyebrows": "section" }
}
```

Any Google Font name loads automatically. `background.decoration` takes `gradient`, `grid`, or `none`.

## Notes from building it

Two things that cost real time, recorded so nobody repeats them:

**Mermaid's built-in themes fight the page.** `neutral` and `dark` render dark subgraph fills with dark labels — unreadable. okflify uses `theme: "base"` with `themeVariables` bound to the CSS palette instead.

**`mermaid.run()` is a no-op on an already-rendered block.** Mermaid stamps `data-processed="true"` and replaces the content with SVG, so the first theme rendered wins permanently. okflify keeps each block's pristine source and restores it before re-running on a theme change. Without this, a light page keeps dark diagrams forever.

## Status

v0.1.0. Known gaps, honestly:

- The graph is only as good as the bundle's cross-links. A bundle where every edge leaves `index.md` renders a **star**, and a star is worse than a list. okflify warns on stderr when a multi-document bundle has zero edges.
- No arrowheads yet, so edge direction is invisible.
- Layout is re-seeded per visit rather than stable.
- Single bundle only — no catalogue view across sibling bundles, which is where a graph would actually earn its keep.

## Related

Sibling of [mafia](https://github.com/eidos-agi/mafia) (Chromium for agents). Same house, same conventions.
