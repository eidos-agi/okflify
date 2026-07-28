#!/usr/bin/env python3
"""
okflify — an app for reading Open Knowledge Format v0.2 bundles.

    python3 okflify.py [bundle_dir] [out.html]

OKF is a GRAPH, not a tree: directories are storage, and the real structure is
the markdown links documents make to each other. okflify reads a bundle, parses
the frontmatter, extracts that link graph, and emits ONE self-contained HTML
file — no server, no build step, no dependencies.

What it renders:
  · sidebar navigation grouped by bundle section
  · a force-directed knowledge graph of the actual links
  · OKF v0.2 trust signals per document (human: > job: > agent:), with an
    explicit warning when a document is only agent-verified
  · backlinks and forward links as cards
  · mermaid diagrams, bound to the page palette so they stay legible in both
    light and dark
  · full-text sidebar search, on-this-page rail, and a print layout

Theming is Mintlify-shaped and lives in docs.json — colours, fonts, background
decoration, eyebrows. Never edit template.html to restyle.

Generic: point it at any OKF v0.2 bundle.
"""
import json, html, pathlib, re, sys

HERE = pathlib.Path(__file__).parent

# ── markdown ────────────────────────────────────────────────────────────────

def inl(s: str) -> str:
    s = html.escape(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    # internal bundle links become in-app navigation
    def link(m):
        text, href = m.group(1), m.group(2)
        if re.match(r"^https?://", href):
            return f'<a href="{href}" target="_blank" rel="noopener">{text}</a>'
        slug = href.split("/")[-1].replace(".md", "")
        return f'<a href="#{slug}" data-nav="{slug}">{text}</a>'
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, s)

def md(text: str) -> str:
    out, i, lines = [], 0, text.split("\n")
    while i < len(lines):
        l = lines[i]
        if l.startswith("```mermaid"):
            b = []; i += 1
            while i < len(lines) and not lines[i].startswith("```"): b.append(lines[i]); i += 1
            out.append('<pre class="mermaid">' + html.escape("\n".join(b)) + "</pre>"); i += 1; continue
        if l.startswith("```"):
            b = []; i += 1
            while i < len(lines) and not lines[i].startswith("```"): b.append(lines[i]); i += 1
            out.append("<pre><code>" + html.escape("\n".join(b)) + "</code></pre>"); i += 1; continue
        if l.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s\-:|]+\|$", lines[i + 1]):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip("|").split("|")]); i += 1
            hdr, body = rows[0], rows[2:]
            t = "<div class='tw'><table><thead><tr>" + "".join(f"<th>{inl(c)}</th>" for c in hdr) + "</tr></thead><tbody>"
            for r in body: t += "<tr>" + "".join(f"<td>{inl(c)}</td>" for c in r) + "</tr>"
            out.append(t + "</tbody></table></div>"); continue
        m = re.match(r"^(#{1,4})\s+(.*)", l)
        if m:
            lv = len(m.group(1)); out.append(f"<h{lv}>{inl(m.group(2))}</h{lv}>"); i += 1; continue
        if l.startswith(">"):
            b = []
            while i < len(lines) and lines[i].startswith(">"):
                b.append(re.sub(r"^>\s?", "", lines[i])); i += 1
            txt = "\n".join(b).strip()
            kind, icon = "note", "info"
            probe = re.sub(r"[*_`]", "", txt)[:6]
            if "🔴" in probe or "STOP" in probe.upper(): kind, icon = "danger", "octagon-alert"
            elif "⚠" in probe: kind, icon = "warn", "triangle-alert"
            elif "✅" in probe or "🟢" in probe: kind, icon = "check", "circle-check"
            elif "❓" in probe or "🟡" in probe: kind, icon = "info", "circle-help"
            elif "💡" in probe: kind, icon = "tip", "lightbulb"
            body = re.sub(r"^\s*[🔴⚠️✅🟢❓🟡💡]+\s*", "", txt)
            paras = "".join(f"<p>{inl(x)}</p>" for x in body.split("\n") if x.strip())
            out.append(f'<div class="cal cal-{kind}"><span class="ci" data-i="{icon}"></span><div>{paras}</div></div>')
            continue
        if re.match(r"^[-*]\s+", l):
            it = []
            while i < len(lines) and re.match(r"^[-*]\s+", lines[i]):
                it.append(inl(re.sub(r"^[-*]\s+", "", lines[i]))); i += 1
            out.append("<ul>" + "".join(f"<li>{x}</li>" for x in it) + "</ul>"); continue
        if re.match(r"^\d+\.\s+", l):
            it = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i]):
                it.append(inl(re.sub(r"^\d+\.\s+", "", lines[i]))); i += 1
            out.append("<ol>" + "".join(f"<li>{x}</li>" for x in it) + "</ol>"); continue
        if l.strip() == "---": out.append("<hr/>"); i += 1; continue
        if l.strip(): out.append(f"<p>{inl(l)}</p>")
        i += 1
    return "\n".join(out)

# ── frontmatter (minimal YAML — enough for OKF) ─────────────────────────────

def frontmatter(text: str):
    if not text.startswith("---"):
        return {}, text
    _, fm, body = text.split("---", 2)
    data = {}
    stack = [(0, data)]
    for raw in fm.split("\n"):
        if not raw.strip() or raw.lstrip().startswith("#"): continue
        indent = len(raw) - len(raw.lstrip())
        line = raw.strip()
        if line.startswith("- "):
            item = line[2:]
            parent = stack[-1][1]
            key = parent.setdefault("_list", [])
            if ":" in item:
                k, v = item.split(":", 1); key.append({k.strip(): v.strip()})
            else: key.append(item)
            continue
        while len(stack) > 1 and indent <= stack[-1][0]: stack.pop()
        if ":" not in line: continue
        k, v = line.split(":", 1); k, v = k.strip(), v.strip()
        cur = stack[-1][1]
        if v == "":
            nd = {}; cur[k] = nd; stack.append((indent, nd))
        else:
            cur[k] = v.strip('"')
    # flatten list holders
    def clean(d):
        if isinstance(d, dict):
            if set(d.keys()) == {"_list"}: return d["_list"]
            return {k: clean(v) for k, v in d.items() if k != "_list"}
        return d
    return clean(data), body.lstrip("\n")

# ── collect ─────────────────────────────────────────────────────────────────

def collect(bundle: pathlib.Path):
    """Walk an OKF bundle. Directories are storage, nothing more."""
    docs = []

    def add(path, group):
        if not path.exists():
            return
        fm, body = frontmatter(path.read_text())
        # The frontmatter title is what the sidebar, breadcrumb and graph use.
        # If the body opens with its own h1 it competes — the OKF template ships
        # a generic "# Investigation" — so drop it and render the real title.
        if fm.get("title"):
            body = re.sub(r"\A\s*#\s+[^\n]*\n+", "", body, count=1)
        docs.append(dict(
            slug=path.stem, group=group, file=str(path.relative_to(bundle)),
            title=fm.get("title") or path.stem, type=fm.get("type", "—"),
            status=fm.get("status", ""), tags=fm.get("tags", ""),
            verified=fm.get("verified") or {}, html=md(body), src=body,
        ))

    add(bundle / "index.md", "Bundle")
    add(bundle / "log.md", "Bundle")
    for g, d in (("Concepts", "concepts"), ("Evidence", "evidence"), ("Learnings", "learnings")):
        for pth in sorted((bundle / d).glob("*.md")):
            add(pth, g)
    return docs


def link_graph(docs):
    """
    OKF is a GRAPH, not a tree. The edges are whatever the documents actually
    reference in markdown — the folder layout says nothing about structure.
    """
    slugs = {d["slug"] for d in docs}
    edges, seen = [], set()
    for d in docs:
        for tgt in re.findall(r'data-nav="([^"]+)"', d["html"]):
            if tgt in slugs and tgt != d["slug"] and (d["slug"], tgt) not in seen:
                seen.add((d["slug"], tgt))
                edges.append({"s": d["slug"], "t": tgt})
    for d in docs:
        d["out"] = sorted({e["t"] for e in edges if e["s"] == d["slug"]})
        d["in"] = sorted({e["s"] for e in edges if e["t"] == d["slug"]})
    return edges


def theme_tokens(cfg, root_fm):
    """Mintlify-shaped docs.json → template substitutions."""
    col, fon = cfg.get("colors", {}), cfg.get("fonts", {})
    fam = fon.get("family", "Inter")
    head_f = fon.get("heading", fam)
    wts = fon.get("weights", "400;500;600;700")
    fams = "&family=".join(sorted({f"{f.replace(' ', '+')}:wght@{wts}" for f in (fam, head_f)}))
    return {
        "__FONT_LINK__": (
            '<link rel="preconnect" href="https://fonts.googleapis.com">'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={fams}&display=swap">'
        ),
        "__FONT_BODY__": f'"{fam}"',
        "__FONT_HEAD__": f'"{head_f}"',
        "__PRIMARY__": col.get("primary", "#9F3232"),
        "__LIGHT__": col.get("light", "#E08A8A"),
        "__DARK__": col.get("dark", "#7A2424"),
        "__DECOR__": cfg.get("background", {}).get("decoration", "none"),
        "__EYEBROW__": cfg.get("styling", {}).get("eyebrows", "breadcrumbs"),
        "__DEFAULTMODE__": cfg.get("appearance", {}).get("default", "system"),
        "__BRANDNAME__": cfg.get("name", str(root_fm.get("title") or "")),
    }


def build(bundle="." , out=None, template=None):
    """Convert an OKF v0.2 bundle into one self-contained HTML file."""
    bundle = pathlib.Path(bundle)
    if not bundle.is_dir():
        raise SystemExit(f"okflify: not a directory: {bundle}")
    out = pathlib.Path(out or bundle / "okflify.html")

    docs = collect(bundle)
    if not docs:
        raise SystemExit(
            f"okflify: no OKF documents under {bundle}\n"
            "  expected index.md / log.md / concepts/ / evidence/ / learnings/"
        )
    edges = link_graph(docs)

    idx = bundle / "index.md"
    root_fm, _ = frontmatter(idx.read_text()) if idx.exists() else ({}, "")
    cfg_path = bundle / "docs.json"
    cfg = json.loads(cfg_path.read_text()) if cfg_path.exists() else {}

    # bundle-local template wins, else the packaged one
    tpl_path = pathlib.Path(template) if template else (bundle / "template.html")
    if not tpl_path.exists():
        tpl_path = HERE / "template.html"

    html_out = (tpl_path.read_text()
        .replace("__TITLE__", html.escape(str(root_fm.get("title") or bundle.resolve().name)))
        .replace("__OKFV__", str(root_fm.get("okf_version") or "0.2"))
        .replace("__STATUS__", str(root_fm.get("status") or "—"))
        .replace("__DOCS__", json.dumps(docs))
        .replace("__EDGES__", json.dumps(edges)))
    for k, v in theme_tokens(cfg, root_fm).items():
        html_out = html_out.replace(k, str(v))

    out.write_text(html_out)
    diagrams = sum(d["html"].count('class="mermaid"') for d in docs)
    return dict(out=out, docs=len(docs), edges=len(edges), diagrams=diagrams)
