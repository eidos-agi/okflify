---
okf_version: "0.2"
type: rule
title: "EMF v0.1 — the additive OKF profile for durable memory and intent"
tags: [emf, memory, intent, altitude, sensors, conflicts]
sources:
  - repo: eidos-agi/emf
verified:
  by: agent:codex
  at: 2026-08-06
  method: "checked against eidos-agi/emf SPEC.md v0.1, validator, and current examples"
  stale_after: 2026-11-06
---

# EMF v0.1 — Eidos Memory Format

EMF is the OKF profile for memory that must preserve **human direction,
authority, attachment to work, machine provenance, and disagreement**. It is a
protocol and validator, not an organization-wide memory warehouse.

Every EMF document remains valid OKF v0.2. EMF adds the axes that base OKF does
not express strongly enough for long-lived operational memory.

## 1. Human intent and altitude

```yaml
---
okf_version: "0.2"
emf_version: "0.1"
type: intent
title: "linear is where tasks will live"
altitude: strategic
concerns: [armada]
verified:
  by: human:daniel
  at: 2026-07-31
  method: "stated directly in session"
  stale_after: 2027-07-31
---
```

Intent is not true or false. It is honored or violated. The title of an intent
record is therefore the person's words verbatim, not an agent's cleaner
paraphrase. `by` must be `human:*`; an agent can transcribe human intent but
cannot manufacture it.

Human instructions have different governing ranges:

| Altitude | Governs | Default shelf life |
|---|---|---|
| `strategic` | What the thing is for | 365 days |
| `tactical` | Sequencing and approach | 90 days |
| `operational` | Immediate mechanics | 7 days |

Altitude applies only inside the human tier and must be human-assigned. A quiet
sentence can set an entire storage model; emphasis-based agent heuristics have
measurably downgraded strategic intent and shortened its authority.

## 2. Concerns and supersession

OKF Markdown links connect documents. EMF also connects memory to the systems
it governs:

```yaml
concerns: [EID-1039, armada, okflify]
supersedes: [emf:2026-06-01-old-rule]
```

`concerns` lets an issue, repo, service, or product retrieve relevant memory.
`supersedes` makes replacement explicit. A reader must not render superseded
evidence as current or rank it above a live record.

## 3. Machine sensors

Base OKF `job:` means a machine measured something. EMF requires the machine
claim to identify the validated sensor:

```yaml
verified:
  by: job:count_user_turns
  sensor:
    id: count_user_turns
    validated_by: E-11
    validated_at: 2026-08-01
```

Without a validated sensor, readers must treat the document as `agent:` tier.
This rule exists because repeatable automation can be consistently wrong. One
measured turn counter treated tool-result blocks as human turns: 345 markers
were only 47 real turns. Reproducibility did not make the sensor valid.

## 4. Unresolved contradictions

```yaml
---
okf_version: "0.2"
emf_version: "0.1"
type: unresolved
sources:
  - by: human:daniel
    claims: "tasks live in Linear"
  - by: job:git
    claims: "the work has no issue key"
contested: "whether this work was meant to be tracked"
---
```

A smooth synthesis is sometimes data loss. `type: unresolved` preserves both
accounts when the resolution rules cannot pick a legitimate winner.

## Resolution order

When two live EMF documents conflict:

1. **Tier:** `human:` > `job:` > `agent:`.
2. **Altitude inside human:** strategic > tactical > operational.
3. **Staleness:** an expired record does not govern.
4. **Recency:** newer wins; a gap of at least 30 days is itself recorded as evidence of change.
5. **Otherwise unresolved:** surface both and invent no resolution.

The first rung is load-bearing. Evidence can correct a factual claim; it cannot
reason its way out of the owner's direction.

## Placement and conformance

The default home is `docs/emf/` inside the repo the memory concerns. Reseating
is allowed when the pack says where it went. The `eidos-agi/emf` repository owns
the spec, validator, and dogfood—not all organizational memory.

- Every EMF document is valid OKF v0.2.
- `altitude` is absent unless `by` is human.
- `sensor` is required for `job:` memory.
- `type: intent` carries verbatim human words and a human author.
- Stale and superseded documents do not outrank live documents.
- Omitted human `stale_after` derives from altitude.

```sh
python -m emf.validate /path/to/repo/docs/emf
```

See [profile composition](../learnings/profile-composition.md) for the boundary
between an ORF investigation and promoted EMF memory.
