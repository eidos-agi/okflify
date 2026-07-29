---
okf_version: "0.2"
type: evidence-pointer
title: "Build output — what this bundle produces"
tags: [okflify, evidence]
sources:
  - repo: eidos-agi/okflify
verified:
  by: job:okflify-build
  at: 2026-07-29
  method: "captured from `okflify example` on the commit that ships this bundle"
---

## Command

```sh
$ okflify example
okflify → example/okflify.html — 8 documents, 12 edges, 1 diagrams
```

## What that means

| Number | Reading |
|---|---|
| **8 documents** | index + log + 4 concepts + 1 learning + 1 evidence |
| **12 edges** | markdown links between them — **6 of 12 originate outside the index** |
| **density 0.43** | vs 0.19 for the star described in [links-are-the-product](../learnings/links-are-the-product.md) |
| **1 diagram** | the mermaid graph in `graph-not-tree` |

The middle number is the one that matters. A star of 8 documents would show 7
edges, all from the index, and density 0.25. See [links-are-the-product](../learnings/links-are-the-product.md).

## A correction worth keeping

The first draft of this page claimed 7 documents and 12 edges. The build said 8
and 10. Both numbers were wrong, and chasing the gap exposed a real bug: okflify
treated `../learnings/x.md` (a section hop inside one bundle) as a bundle hop,
silently dropping two edges.

Invented numbers on an evidence page would have hidden a renderer bug. That is
the argument for `method:` in one paragraph.

## Reproduce

```sh
git clone https://github.com/eidos-agi/okflify && cd okflify
pip install -e .
okflify example --open
```

If the counts differ from the table above, this page is stale — which is the
point of recording them.
