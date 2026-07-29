# Investigation log (append-only)

| When | Who | Event | Concept / learning id |
|------|-----|-------|------------------------|
| 2026-07-29 | human:daniel | "poor rendering quality" — with a screenshot | — |
| 2026-07-29 | agent:claude | Measured rather than guessed: label 7.2px effective, scale 0.51 | `evidence/measurements` |
| 2026-07-29 | agent:claude | Cause: `width:100%` shrinks a diagram wider than its column, text with it | `fit-to-width-shrinks-text` |
| 2026-07-29 | job:okflify-build | Fix verified: 7.2px → 14px, scale 0.51 → 1.00 | `evidence/measurements` |
| 2026-07-29 | human:daniel | Confirmed readable on screen — the check that actually decided it | `measure-what-the-eye-judges` |

---

## Why this is the example bundle

It is small, real, and every number in it was measured. Nothing here is
illustrative or invented — which matters, because a bundle demonstrating a
format built around verification cannot itself be fabricated.
