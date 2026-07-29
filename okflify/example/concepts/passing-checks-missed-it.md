---
okf_version: "0.2"
type: claim
title: "Four checks passed and the page was unreadable"
tags: [verification, testing, method]
sources:
  - repo: eidos-agi/okflify
verified:
  by: agent:claude
  at: 2026-07-29
  method: "reconstructed from the session's own tool history — an honest account, but self-reported and not independently reviewed"
  stale_after: 2026-11-01
---

## The claim

Every check in place reported success while the output was unusable:

| Check | Said | Missed |
|---|---|---|
| Build exit code | ✅ | Legibility is not an exit code |
| Diagram count | ✅ 9 of 9 rendered | Rendered ≠ readable |
| No console errors | ✅ | Nothing threw. Nothing was wrong *to the machine* |
| DOM assertions | ✅ elements present, correctly positioned | Never measured **effective font size** |

The gap: every check verified **presence and structure**. None verified the
property a reader actually cares about — *can this be read.*

> **Agent-verified.** This is a self-account of my own mistake, written by the
> party responsible for it. Under OKF weighting, treat it as the weakest tier —
> it has an obvious motive to be generous.

## Why the DOM assertions were the most misleading

They *felt* like real verification. `getBoundingClientRect`, computed styles,
element counts — objective numbers, all passing.

But I only measured what I had just changed. That is confirmation with extra
steps: it can prove a change took effect and still say nothing about whether the
result is any good.

## What actually caught it

A person looked at a screenshot.

The durable fix was not more DOM assertions — it was **rendering to an image and
looking at it**, then measuring the one number that encodes the complaint:
effective font size after scaling.

## Counter-cases

- Screenshot diffing catches regressions but not a *first* bad render. Something
  has to define "good" once.
- Some qualities genuinely resist automation. Naming them as unautomated beats
  a proxy metric that passes while the thing is broken.

## Next

[measure-what-the-eye-judges](../learnings/measure-what-the-eye-judges.md)
