---
okf_version: "0.2"
type: rule
title: "human > job > agent — and an agent-only claim says so, loudly"
tags: [okf, trust, verification]
sources:
  - spec: "https://cloud.google.com/blog/products/data-analytics/okf-v0-2-adds-trust-signals"
verified:
  by: human:daniel
  at: 2026-07-29
  method: "the weighting is Daniel's operating rule for the ARP catalogue and is enforced in okflify's renderer"
---

## The rule

| Tier | Means | Weight |
|------|-------|--------|
| `human:daniel` | A person checked it against reality | Highest |
| `job:pytest` | A repeatable check passed | Middle |
| `agent:claude` | A model asserted it | **Lowest** |

okflify renders the tier at the top of every document, colours the graph node by
it, and prints a warning on agent-only pages:

> **Agent-verified.** Under OKF v0.2 weighting treat as unverified for
> gate-shaped decisions.

## Why this is the whole point

Knowledge bases fail in one specific way: everything in them **looks equally
true**. A confident paragraph an agent produced in four seconds renders exactly
like a number a human checked against a bank statement.

Trust tiers make the difference visible without anyone opening frontmatter. That
is the entire feature. A renderer that shows agent output as confidently as human
verification is not a neutral choice — it is a bug.

## What good `method` looks like

| Weak | Strong |
|---|---|
| "reviewed" | "reverted the fix and confirmed the test fails against the original" |
| "checked the docs" | "unauthenticated HEAD returned 200 with a private-bucket control returning 400" |
| "verified" | "`vercel projects ls --scope …` lists it; the ingestor is absent" |

The strong column shares a property: **someone else could run it and disagree.**

## Counter-cases

- `job:` outranking `agent:` assumes the job asserts something real. A test that
  cannot fail is agent-tier wearing a badge.
- `human:` is not infallible — it is accountable. Different thing, still better.
- Tiers describe **how** a claim was checked, never how important it is.

## Next

`stale_after` is the unglamorous companion. A human-verified claim about a live
system decays; the date says when to look again.
