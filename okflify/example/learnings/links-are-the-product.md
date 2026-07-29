---
okf_version: "0.2"
type: learning
title: "A renderer cannot fix a bundle with nothing to render"
tags: [okf, graph, method]
sources:
  - repo: eidos-agi/okflify
verified:
  by: human:daniel
  at: 2026-07-29
  method: "observed directly: the first real bundle rendered a star, and Daniel said the graph tool was bad before the bundle was diagnosed"
  stale_after: 2027-01-01
---

## The learning

**The graph view is only as good as the links the author wrote.**

okflify's first real bundle — nine documents about a platform architecture —
rendered as a **star**: all seven edges leaving `index.md`, no concept linking to
any other, one document orphaned entirely. Density 0.19.

The reasonable reaction was *"this is a bad graph tool."* It was not. It was an
honest picture of a bundle written as **chapters** — 00, 01, 02 — rather than as
claims that depend on each other.

The next bundle, written with cross-links deliberately, came out at **18 edges
across 8 documents, density 0.64, 12 of 18 originating outside the index**. Same
renderer. Different authoring.

## Why it generalises

Any visualisation inherits its subject's quality. A force-directed layout of a
hierarchy is strictly worse than a list: same information, plus jitter.

The tempting fix is renderer features — arrowheads, clustering, better physics.
None of them create a relationship that the author did not write down.

## What to do instead

- Write concepts that **cite each other**: a rule should link the claim it rests on
- Link **counter-cases across bundles** — that is where the real edges live
- Treat okflify's zero-edge warning as a **content** signal, not a bug report
- Judge a bundle by whether edges originate **outside the index**

## Counter-cases

- Small bundles are legitimately star-shaped; four documents owe you nothing.
- Density can be gamed. Links added to look connected are worse than absent ones,
  because the picture then lies with confidence.
- Some knowledge really is hierarchical — a runbook is a sequence. Use the tree.

## Re-verify

When a catalogue passes ~50 documents. If density has fallen while document count
rose, bundles are being written in isolation again.
