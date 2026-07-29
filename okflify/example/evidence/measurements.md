---
okf_version: "0.2"
type: evidence-pointer
title: "Measurements — before and after"
tags: [evidence, rendering]
sources:
  - repo: eidos-agi/okflify
verified:
  by: job:okflify-build
  at: 2026-07-29
  method: "headless Chromium via playwright against the built page; commands below are reproducible"
---

## The probe

```js
const svg = document.querySelector('.mermaid svg');
const vb  = svg.viewBox.baseVal;
const rect = svg.getBoundingClientRect();
const label = svg.querySelector('.nodeLabel');
const scale = rect.width / vb.width;

({ scale,
   css_font: getComputedStyle(label).fontSize,
   effective_px: parseFloat(getComputedStyle(label).fontSize) * scale })
```

## Result

| | Before | After |
|---|---|---|
| Container | 702px | 702px |
| Diagram natural width | 1280px | 1280px |
| Rendered width | 654px | 1280px (scrolls) |
| **Scale** | **0.51** | **1.00** |
| Label CSS size | 14px | 14px |
| **Label effective** | **7.2px** | **14.0px** |

The CSS font size never changed. Only the scale factor did — which is the whole
point of [fit-to-width-shrinks-text](../concepts/fit-to-width-shrinks-text.md).

## Reproduce

```sh
pip install -e . && okflify --example -o /tmp/x.html
# then run the probe above against /tmp/x.html in any browser console
```

If your numbers differ from this table, this page is stale — which is what
`stale_after` and a recorded `method` are for.
