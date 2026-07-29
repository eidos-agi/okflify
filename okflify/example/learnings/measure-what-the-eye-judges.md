---
okf_version: "0.2"
type: learning
title: "If a human judges it by looking, verify it by looking — then measure that"
tags: [verification, method, ui]
sources:
  - repo: eidos-agi/okflify
verified:
  by: human:daniel
  at: 2026-07-29
  method: "confirmed on screen after the fix; the original defect was reported by a human from a screenshot, not by any automated check"
  stale_after: 2027-01-01
---

## The learning

For anything judged visually, a check that never produces an **image** is not
verification. It is a structural assertion wearing verification's clothes.

The sequence that works:

1. **Render it and look.** A screenshot, in the real engine, at a real size.
2. **Name the number** behind the complaint. "Unreadable" became *effective font
   size after scaling* — 7.2px.
3. **Assert that number**, so the regression is caught next time without eyes.

Step 2 is the one people skip. Without it you have an opinion; with it you have
a threshold.

## Why this generalises past CSS

Any property a human evaluates holistically — readability, tone, whether a
summary is faithful — has the same shape. Automated checks drift toward what is
*easy* to assert (it exists, it did not throw) and away from what is *meant*
(it is usable).

The failure is not the missing test. It is **believing the passing tests covered
it.**

## Counter-cases

- Not everything deserves a pixel budget. This was worth it because a person had
  already complained twice.
- Screenshots-as-tests are brittle; assert the derived *number*, not the image.
- A human eye is not a regression suite. It defines the threshold once; the
  number enforces it thereafter.

## Re-verify

When the layout, the font stack, or the default column width changes — each
moves the scale factor this claim rests on.
