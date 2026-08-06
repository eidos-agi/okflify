---
okf_version: "0.2"
type: rule
title: "ORF v0.2.0 — the additive OKF profile for auditable research"
tags: [orf, research, approval, findings, evidence]
sources:
  - repo: eidos-agi/eidos-squiddie
verified:
  by: agent:codex
  at: 2026-08-06
  method: "checked against eidos-squiddie/orf/SPEC.md v0.2.0 and its validator examples"
  stale_after: 2026-11-06
---

# ORF v0.2.0 — OKF Research Format

ORF is the OKF face for **investigations**. It records what was asked, whether
research was approved, how it was decomposed, what each arm found, how strong
the evidence is, and what remains unresolved.

It is additive: every ORF document still declares `okf_version: "0.2"` and
remains readable by an OKF-only tool. ORF adds fields and gates; it does not
replace the bundle, links, document types, or trust ladder.

## Why the profile exists

| Observed failure | ORF requirement |
|---|---|
| Greeting or chat noise became a durable pack | A real `question` and `approval: go` are required past intake |
| Parallel research ran without one plan | The face records `brief` and `plan.sub_questions` |
| Confident citations came from one host | Findings carry evidence grades and a distinct-host gate |
| Research was confused with investment diligence | Capital `verdict` is out of scope |
| Findings were confused with durable human memory | Promotion to EMF is separate; agents do not author human intent |

## Pack face

```yaml
---
okf_version: "0.2"
orf_version: "0.2.0"
profile: orf
type: Investigation
title: "Goldfish memory — weeks, not three seconds"
question: "Do goldfish really have only a 3-second memory?"
status: done
approval: go
brief:
  goal: "sanity-check a common claim before citing it"
  scope: "peer-reviewed or strong secondary sources"
  audience: "research consumers"
  success_looks_like: "graded findings with host-independent sources"
plan:
  k: 2
  estimate: quick
  sub_questions:
    - "Where did the three-second claim originate?"
    - "What retention do controlled studies measure?"
verified:
  by: agent:squiddie
  at: 2026-08-03
  method: "approved ORF run; two research arms; gates applied"
---
```

`status` moves through `intake`, `planned`, `running`, and `done`. A durable pack
past intake needs `approval: go`. A `done` pack with no approval or no governing
question is invalid because it claims completed research that was never
authorized or scoped.

The `brief` preserves goal, scope, audience, and success condition. The `plan`
records fan-out count, estimate, and shared sub-questions. This lets a later
reader distinguish a deliberate investigation from an answer assembled after
the fact.

## Layout

```text
investigation/
  index.md          required question, brief, plan, status, answer
  log.md            required append-only research timeline
  findings/*.md     one graded finding per concept
  evidence/         optional extracts and supporting artifacts
  plan.md           optional when the plan is too large for frontmatter
  brief.md          optional when the brief is too large for frontmatter
  emf/              optional promoted memory, never agent-authored human intent
  research.json     optional machine sidecar for spend and session linkage
```

The unit of distribution is one approved research question. Squiddie commonly
writes `.research/<id>/`, but ORF is a format rather than a global warehouse;
packs can be reseated if the index says where they live.

## Findings and evidence grades

```yaml
---
okf_version: "0.2"
orf_version: "0.2.0"
type: claim
title: "Controlled work shows retention measured in weeks"
evidence: CONFIRMED
sub_question: "What retention do controlled studies measure?"
sources:
  - https://example.org/study
  - https://independent.example/report
disconfirmation: "searched for controlled studies supporting a seconds-scale ceiling"
verified:
  by: agent:squiddie
  at: 2026-08-03
  method: "research arm with independence and disconfirmation gates"
---
```

| Grade | Meaning | Gate |
|---|---|---|
| `CONFIRMED` | At least two independent source hosts agree | Fewer than two hosts must downgrade; disconfirmation search is expected |
| `REASONED` | Source-backed but partial or not independently confirmed | The honest middle |
| `UNVERIFIED` | Missing sources, conflict, or failed research arm | Must not be presented as confirmed |

The grade evaluates the evidence set. OKF's `verified.by` evaluates the
producer and method. A finding can have two sources and still be agent-produced;
both facts matter.

## Conformance that bites

- Every ORF document is valid OKF v0.2.
- `orf_version` is `X.Y.Z`; `X.Y` matches `okf_version`.
- A pack claiming ORF carries `orf_version` on its face.
- `done` implies `approval: go` and a non-empty `question`.
- `CONFIRMED` requires at least two distinct source hosts.
- An agent must not author `type: intent`.
- Capital diligence verdicts warn because they belong to a different profile.

```sh
python -m orf.validate --strict /path/to/investigation
```

ORF `0.2.0` means the first ORF revision on OKF `0.2`. ORF-only changes advance
the patch component; moving to OKF `0.3` starts ORF `0.3.0`.

Research becomes durable memory by **promotion**, not by relabelling the whole
pack. See [profile composition](../learnings/profile-composition.md).
