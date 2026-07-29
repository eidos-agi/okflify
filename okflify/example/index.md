---
okf_version: "0.2"
type: investigation
title: "Why were the diagrams unreadable?"
status: closed
slug: example
started: 2026-07-29
tags: [rendering, mermaid, typography, example]
sources:
  - repo: eidos-agi/okflify
verified:
  by: job:okflify-build
  at: 2026-07-29
  method: "every number below was measured in a headless browser; the commands are in the evidence page"
---

# Investigation

## Question

Diagrams on a documentation site were technically rendering — no errors, correct
shapes — and nobody could read the labels. Why?

## Why it matters

The failure was invisible to every check we had. The build passed. The DOM
assertions passed. A human looked at a screenshot and said *"this is unreadable,"*
which is the only test that caught it.

This bundle is a real, small investigation, kept as okflify's example because it
shows the format doing its actual job: separating **what we measured** from
**what we assumed**.

## Answer

**7.2 pixels.** Labels were rendering at 7.2px effective size — a 1280px-wide
diagram forced into a 702px column at 0.51 scale, with 14px text scaled down
with it.

The CSS said `width: 100%`. That reads like *"make it fit"* and it does — by
shrinking a diagram that was already too wide, along with every label on it.

## Concepts

| Read | For |
|------|-----|
| [fit-to-width-shrinks-text](concepts/fit-to-width-shrinks-text.md) | The mechanism, and when `width:100%` is wrong |
| [passing-checks-missed-it](concepts/passing-checks-missed-it.md) | Why four green checks said nothing |

## Learnings

- [measure-what-the-eye-judges](learnings/measure-what-the-eye-judges.md)

## Evidence

- [measurements](evidence/measurements.md) — the browser commands and their output

## Citations

- [Mermaid](https://mermaid.js.org) sizing behaviour
- [OKF v0.2 trust signals](https://cloud.google.com/blog/products/data-analytics/okf-v0-2-adds-trust-signals)
