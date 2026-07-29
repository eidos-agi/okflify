# Investigation log (append-only)

| When | Who | Event | Concept / learning id |
|------|-----|-------|------------------------|
| 2026-07-29 | human:daniel | Asked for an example bundle shipped inside okflify, reachable from the sidebar | `index` |
| 2026-07-29 | agent:claude | Wrote the docs AS a bundle rather than about one — documentation that cannot drift from the tool | `index` |
| 2026-07-29 | agent:claude | Cross-linked the concepts deliberately, after shipping a real bundle whose every edge left the index | `links-are-the-product` |

---

## Why this bundle exists

Documentation about a format tends to drift from the tool that reads it. This
bundle cannot: it is built by the tool, on every release, and a broken renderer
means a broken page.

It is also the smallest honest test. If okflify cannot make four concepts and a
handful of links legible, it will not survive a hundred.
