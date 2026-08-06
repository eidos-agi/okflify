---
okf_version: "0.2"
type: claim
title: "OKFlify — what the renderer does from input to portable output"
tags: [okflify, renderer, cli, html, mobile]
sources:
  - repo: eidos-agi/okflify
verified:
  by: job:okflify-build
  at: 2026-08-06
  method: "19 regression tests plus a 390x844 Mafia browser run against the live Hostkey build"
  stale_after: 2026-11-06
---

# The OKFlify renderer

OKFlify performs one bounded transformation:

```text
OKF bundle directory → discover → parse → link graph → render → one HTML file
```

It uses the Python standard library. There is no framework runtime, asset
pipeline, search service, or database. The generated page can be opened from
`file://`, attached to a message, archived with a release, or served by any
static host.

## Command line

```sh
okflify bundle/                       # writes bundle/okflify.html
okflify bundle/ -o /tmp/site.html     # explicit output
okflify --example --open              # this packaged guide
okflify catalogue/ -o catalogue.html  # multiple sibling bundles
okflify --version
```

The CLI fails when the input is not a directory or no OKF documents are found.
It reports document, edge, and diagram counts so an empty or thinned build is
visible in automation.

## Discovery and parsing

For one bundle, OKFlify reads `index.md`, `log.md`, and Markdown documents under
the conventional sections. For a catalogue it discovers sibling bundles and
namespaces their document slugs. A deliberately small frontmatter parser reads
the OKF fields needed for identity and trust. Unknown keys remain harmless,
which is why ORF and EMF can add profile fields without an OKFlify fork.

Markdown links become graph edges and in-app navigation. Relative links across
sections stay inside the bundle; links to another bundle's `index.md` become
catalogue edges; external HTTP links remain normal browser links.

## Four reading modes

1. **Document view** shows one page with its type, verification actor, date,
   method, freshness, prose, diagrams, outgoing links, and backlinks.
2. **Knowledge graph** lays out the actual document links. Node color reflects
   trust tier; inbound links influence node size; selecting a node opens it.
3. **Tree view** groups bundle → section → document for predictable scanning,
   especially in catalogues with many files.
4. **Whole bundle** places every document in reading order for end-to-end review,
   browser find, copying, and printing.

The graph and tree are complements. The tree is a storage-oriented index; the
graph shows the authored relationships.

## Trust presentation

Verification appears above the document, not buried in a footer. Agent-only
content receives an explicit warning that OKF v0.2 treats it as the weakest tier
for gate-shaped decisions. Graph nodes use the same tier, so weakly supported
regions can be seen before every page is read.

OKFlify does not reinterpret ORF evidence grades or EMF resolution rules. Those
profiles define conformance; the renderer faithfully exposes their OKF trust
base and profile version.

## Navigation and copying

The sidebar groups documents by section. `⌘K` searches document titles and
headings. The page rail follows headings. Copy actions produce Markdown for the
current page or whole bundle; external “open in” helpers attach the page rather
than pretending a model saw it.

On mobile, the sidebar becomes an accessible off-canvas drawer. The menu button
tracks `aria-expanded`, Escape closes it, navigation closes it, header controls
stay within the viewport, and the reading column uses the full device width.

## Diagrams and images

Mermaid blocks render in the browser with palette variables derived from the
page theme. Theme changes restore the pristine Mermaid source before rerendering
because Mermaid marks processed nodes and otherwise silently keeps the first
theme. Images and diagrams open in a lightbox with cursor-centered zoom, pan,
fit, actual size, keyboard nudge, and Escape close.

Wide diagrams keep a readable natural size and scroll instead of shrinking text
until technically present but functionally unreadable.

## Theming and host integration

Presentation belongs in `docs.json`, not the renderer template:

```json
{
  "name": "My Knowledge",
  "colors": { "primary": "#2E6F5E", "light": "#6FC7AC", "dark": "#1F5044" },
  "fonts": { "family": "Inter", "heading": "Inter" },
  "appearance": { "default": "system" },
  "background": { "decoration": "gradient" },
  "home": { "href": "/product/", "label": "Product" },
  "github": false
}
```

`home` adds a return control when the page lives inside another product. A
same-origin `?return=` or `?home=` query can override it at runtime. Hosted
packs hide OKFlify self-promotion by default; standalone packs may link to the
tool or their own source repository.

## Self-contained has a precise boundary

The generated document data, HTML, CSS, and application JavaScript are inline.
Google Fonts, Mermaid, Cytoscape, and icons are browser-fetched enhancements.
The prose and trust record remain readable when those enhancements are
unavailable; graph layout, web fonts, and Mermaid rendering require network
access unless a host supplies them locally.

## Honest limits

- It is a reader, not an editor.
- Search covers titles and headings rather than every body token.
- Graph layout is not stable across reloads and does not cluster bundles.
- It displays ORF and EMF but does not replace their validators.
- A bundle with few cross-links produces a thin graph; OKFlify reports the content as written.

Next: [ORF for research](orf-research.md) and [EMF for memory](emf-memory.md).
