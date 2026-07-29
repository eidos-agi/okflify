---
okf_version: "0.2"
type: investigation
title: "How okflify works — a bundle that is its own documentation"
status: open
slug: example
started: 2026-07-29
tags: [okf, okflify, example, documentation]
sources:
  - repo: eidos-agi/okflify
  - spec: "https://cloud.google.com/blog/products/data-analytics/okf-v0-2-adds-trust-signals"
verified:
  by: job:okflify-build
  at: 2026-07-29
  method: "this page is rendered by the tool it documents — if okflify breaks, this page does not build"
---

# Investigation

## Question

What does an Open Knowledge Format v0.2 bundle look like, and what does okflify do with one?

## Why it matters

OKF is easy to describe and hard to picture. Reading a spec tells you a bundle is
"markdown files with YAML frontmatter"; it does not tell you what a **trust tier**
buys you, or why the folder tree is the least interesting thing about it.

So this bundle documents okflify **by being** an okflify bundle. Everything you see
— the sidebar, the trust card above this text, the graph, the tree — is this
directory, rendered by the tool. There is no separate documentation to drift.

## Scope

| In | Out |
|----|-----|
| What a bundle is, what okflify renders | The full OKF spec — linked, not restated |
| The trust model, because it is the point | Authoring advice — write what is true |

## Status

- **Now:** ships inside the repo at `example/`. Build it yourself in one command.
- **Next experiment:** point okflify at your own notes and see how thin the link graph is. That number is usually a surprise.

## Concepts

| Read | For |
|------|-----|
| [what-is-a-bundle](concepts/what-is-a-bundle.md) | The five parts, and which are optional |
| [trust-tiers](concepts/trust-tiers.md) | `human: > job: > agent:` and why it is the whole point |
| [graph-not-tree](concepts/graph-not-tree.md) | Why directories lie about structure |
| [what-okflify-renders](concepts/what-okflify-renders.md) | Every feature, and how to reach it |

## Learnings

- [links-are-the-product](learnings/links-are-the-product.md) — the lesson that cost the most to learn

## Evidence index

| Artifact | Path | Role |
|----------|------|------|
| This page | you are reading it | The tool renders its own documentation |
| Build output | [`evidence/build-output.md`](evidence/build-output.md) | Counts from a real run |

## Citations

- Google [OKF spec](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
- [OKF v0.2 trust signals](https://cloud.google.com/blog/products/data-analytics/okf-v0-2-adds-trust-signals)
