# okflify — Telos

## Philosophy

**okflify converts OKF bundles into HTML.** That is the whole job. It is not a
docs platform, not a wiki, not a static-site generator with an OKF plugin.

One command in, one file out. The output opens from `file://` with no server,
survives being emailed, and prints. If it ever needs a build step or a runtime,
something has gone wrong.

## The one idea

**OKF is a graph, not a tree.**

Bundles live in directories, so every renderer reaches for a folder tree. That
throws away the actual structure: concepts connect through markdown links, and
the network is richer than any parent-child path. okflify extracts that link
graph and renders it first.

A corollary worth stating, because it is uncomfortable: **if a bundle has no
cross-links, okflify will show you that.** A star — every edge leaving the
index — is not a graph, and no amount of force-directed physics makes it one.
The renderer should be honest about a thin bundle rather than flattering it.

## Trust is a first-class citizen

OKF v0.2 added trust signals and they are the reason to use OKF at all.
`human: > job: > agent:` is not decoration — it is the difference between a
claim you can gate a decision on and a claim you cannot.

okflify therefore:

- shows `verified.by / at / method` at the top of every document, not in a footer
- **states plainly** when a document is agent-verified only
- colours graph nodes by tier, so thin evidence is visible at a glance

An agent-written bundle that renders as confidently as a human-verified one is
a bug, not a style choice.

## Non-goals

- Editing. okflify reads; something else writes.
- Search backends, comments, analytics, auth.
- Being a general markdown renderer. It renders what OKF bundles contain.
- Dependencies. Standard library, plus mermaid from a CDN at view time.

## What "done" looks like

1. Point it at any OKF v0.2 bundle and get a usable document — ✅
2. Trust tiers legible without reading frontmatter — ✅
3. The link graph, not the folder tree, as the primary structure — ⚠️ renders, but needs arrows, stable layout, neighbour highlighting
4. A **catalogue** view across sibling bundles — ❌ not started, and the place a graph genuinely earns its keep
5. Never lies about how well-verified something is — ✅ and non-negotiable
