---
okf_version: "0.2"
type: claim
title: "A bundle is five parts, and three of them are optional"
tags: [okf, structure]
sources:
  - spec: "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md"
verified:
  by: job:okflify-build
  at: 2026-07-29
  method: "the layout below is what okflify's discover() and collect() actually walk; if it were wrong this page would not render"
---

## The layout

```
bundle/
  index.md          # required — the root: question, why, status, links
  log.md            # append-only diary (no frontmatter by convention)
  concepts/*.md     # claims, rules, questions — the substance
  evidence/*.md     # pointers to what was actually observed
  learnings/*.md    # promoted, re-verified, generalisable
  docs.json         # optional theming
```

Only `index.md` is required. okflify skips what is absent — a bundle with one
file is a valid bundle.

## Frontmatter that matters

```yaml
---
okf_version: "0.2"
type: claim          # claim | rule | learning | question | evidence-pointer | investigation
title: "One sentence someone could disagree with"
verified:
  by: human:daniel   # human: > job: > agent:
  at: 2026-07-29
  method: "how you checked — the part people skip"
  stale_after: 2026-10-01
---
```

`method` is the field that does the work. "Verified" without a method is a
feeling. See [trust-tiers](trust-tiers.md).

## Body shape that holds up

Not enforced, but earned: **claim → evidence → counter-cases → open questions →
next experiment.** The counter-cases section is the one that separates a note from
a claim. If you cannot name a case where you would be wrong, you have written an
opinion.

## Counter-cases

- A registry — "where does X live?" — is *not* a bundle. Trust tiers on a URL are
  noise. Keep catalogs as structured data with a schema.
- A bundle per meeting produces sprawl. One bundle per **question you expect to
  re-learn in 30 days**.

## Next

Read [graph-not-tree](graph-not-tree.md) — the layout above is storage, not structure.
