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

Generic: point it at any OKF v0.2 bundle, including additive ORF and EMF profiles.
"""
import html
import json
import pathlib
import re
import sys

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
        # Resolve within a bundle AND across bundles in a catalogue.
        # "../other-bundle/index.md" -> other-bundle/index ; "concepts/x.md" -> {BUNDLE}/x
        parts = [x for x in href.replace(".md", "").split("/") if x not in ("", ".")]
        up = parts.count("..")
        parts = [x for x in parts if x != ".."]
        if not parts:
            return text
        # "../learnings/x.md" is a SECTION hop inside one bundle;
        # "../other-bundle/index.md" is a bundle hop. Structurally identical,
        # so disambiguate on the known section names.
        SECTIONS = {"concepts", "evidence", "learnings"}
        if up and len(parts) >= 2 and parts[-2] in SECTIONS:
            slug = "{BUNDLE}/" + parts[-1]
        elif up and len(parts) >= 2:
            slug = f"{parts[-2]}/{parts[-1]}"
        elif up == 1:
            slug = f"{parts[-1]}/index"
        else:
            slug = "{BUNDLE}/" + parts[-1]
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
        if l.strip():
            # Markdown wraps a paragraph across source lines; a blank line ends
            # it. Emitting one <p> per LINE made every wrapped line its own
            # paragraph, so paragraph margin appeared between every line and no
            # amount of CSS tuning could fix it.
            buf = []
            while i < len(lines) and lines[i].strip() \
                    and not re.match(r"^(#{1,4} |[-*] |\d+\. |> |\||```)", lines[i]) \
                    and lines[i].strip() != "---":
                buf.append(lines[i].strip()); i += 1
            out.append("<p>" + inl(" ".join(buf)) + "</p>")
            continue
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

def discover(root: pathlib.Path):
    """Return the bundles under `root`.

    A catalogue is a directory of bundles (root/bundles/<slug>/ or root/<slug>/,
    each with an index.md). A single bundle is its own catalogue of one. OKF says
    nothing about this layer — it is purely how people file bundles on disk.
    """
    if (root / "index.md").is_file():
        return [root]
    for parent in (root / "bundles", root):
        if not parent.is_dir():
            continue
        found = sorted(d for d in parent.iterdir()
                       if d.is_dir() and (d / "index.md").is_file())
        if found:
            return found
    return []


def collect(bundle: pathlib.Path, label: str | None = None):
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
            slug=(f"{label}/{path.stem}" if label else path.stem),
            bundle=label or "",
            # Catalogue view: 18 bundles' concepts in one "Concepts" group is
            # useless. Group by bundle instead; section survives as `section`.
            group=(label or group), section=group,
            file=str(path.relative_to(bundle)),
            title=fm.get("title") or path.stem, type=fm.get("type", "—"),
            status=fm.get("status", ""), tags=fm.get("tags", ""),
            verified=fm.get("verified") or {}, html=md(body), src=body,
        ))

    add(bundle / "index.md", "Bundle")
    add(bundle / "log.md", "Bundle")
    # Every subdirectory holding markdown is a concept group. The old hardcoded
    # (concepts, evidence, learnings) tuple silently dropped facts/ — six fact
    # files, including a pack's founding document, rendered as dead links.
    for d in sorted(p for p in bundle.iterdir() if p.is_dir()):
        for pth in sorted(d.glob("*.md")):
            add(pth, d.name.replace("-", " ").title())
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


def host_home_html(cfg):
    """Optional return link to the host app (not the OKF pack index).

    docs.json:
      "home": { "href": "/boxes/", "label": "Boxes" }
    Also overridable at runtime with ?return= or ?home= query params (see template).
    """
    home = cfg.get("home") or cfg.get("return") or {}
    if isinstance(home, str):
        home = {"href": home}
    href = (home.get("href") or home.get("url") or "").strip()
    label = (home.get("label") or home.get("title") or "Home").strip() or "Home"
    if not href:
        # Placeholder still in DOM so ?return= can enable it at runtime
        return (
            '<a class="host-home" id="host-home" hidden href="/" data-host-home="1">'
            '<span class="hh-arrow" aria-hidden="true">←</span>'
            '<span class="hh-label">Home</span></a>'
        )
    return (
        f'<a class="host-home" id="host-home" href="{html.escape(href)}" data-host-home="1" '
        f'title="Back to {html.escape(label)}">'
        f'<span class="hh-arrow" aria-hidden="true">←</span>'
        f'<span class="hh-label">{html.escape(label)}</span></a>'
    )


_GH_ICON = (
    '<svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor">'
    '<path d="M12 2a10 10 0 0 0-3.16 19.49c.5.09.68-.22.68-.48v-1.7c-2.78.6-3.37-1.34-3.37-1.34'
    "-.45-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.9 1.53 2.36 1.09 "
    "2.94.83.09-.65.35-1.09.63-1.34-2.22-.25-4.555-1.11-4.555-4.94 0-1.09.39-1.98 1.03-2.68-.1-.25"
    "-.45-1.27.1-2.64 0 0 .84-.27 2.75 1.02a9.5 9.5 0 0 1 5 0c1.91-1.29 2.75-1.02 2.75-1.02.55 "
    "1.37.2 2.39.1 2.64.64.7 1.03 1.59 1.03 2.68 0 3.84-2.34 4.69-4.57 4.94.36.31.68.92.68 1.85v2.74"
    'c0 .27.18.58.69.48A10 10 0 0 0 12 2Z"/></svg>'
)


def github_link_html(cfg):
    """Header GitHub control — must not hard-promote okflify when hosted in another product.

    docs.json:
      "github": false                          # hide
      "github": "https://github.com/org/repo"  # custom URL
      "github": { "href": "...", "label": "GitHub", "title": "…" }

    Default: standalone packs (no ``home``) still link to eidos-agi/okflify.
    Hosted packs (``home`` set) omit GitHub unless ``github`` is set explicitly.
    """
    has_home = bool(cfg.get("home") or cfg.get("return"))
    raw = cfg.get("github", "__default__")

    if raw is False or raw is None or raw == "":
        return ""

    if raw == "__default__" or raw is True:
        if has_home:
            return ""  # embedded in a host app — no tool self-promo
        href = "https://github.com/eidos-agi/okflify"
        title = "okflify — converts OKF bundles into HTML"
        label = "GitHub"
    elif isinstance(raw, str):
        href, title, label = raw.strip(), "GitHub", "GitHub"
        if not href:
            return ""
    elif isinstance(raw, dict):
        href = (raw.get("href") or raw.get("url") or "").strip()
        if not href:
            return ""
        label = (raw.get("label") or "GitHub").strip() or "GitHub"
        title = (raw.get("title") or label).strip() or label
    else:
        return ""

    return (
        f'<a class="ib" href="{html.escape(href)}" target="_blank" rel="noopener" '
        f'title="{html.escape(title)}" style="text-decoration:none;gap:.4rem">'
        f"{_GH_ICON}{html.escape(label)}</a>"
    )


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
        "__FORMAT__": " · ".join(
            f"{name.upper()} v{root_fm[key]}"
            for name, key in (("okf", "okf_version"), ("orf", "orf_version"), ("emf", "emf_version"))
            if root_fm.get(key)
        ) or "OKF v0.2",
        "__HOST_HOME__": host_home_html(cfg),
        "__GITHUB_LINK__": github_link_html(cfg),
    }


def build(bundle="." , out=None, template=None):
    """Convert an OKF v0.2 bundle into one self-contained HTML file."""
    bundle = pathlib.Path(bundle)
    if not bundle.is_dir():
        raise SystemExit(f"okflify: not a directory: {bundle}")
    out = pathlib.Path(out or bundle / "okflify.html")

    found = discover(bundle)
    multi = len(found) > 1
    docs = []
    for b in found:
        label = b.name if multi else None
        got = collect(b, label)
        if multi:
            # resolve the same-bundle placeholder now that the label is known
            for d in got:
                d["html"] = d["html"].replace("{BUNDLE}", label)
        else:
            for d in got:
                d["html"] = d["html"].replace("{BUNDLE}/", "")
        docs += got
    if not docs:
        raise SystemExit(
            f"okflify: no OKF documents under {bundle}\n"
            "  expected index.md / log.md / concepts/ / evidence/ / learnings/"
        )
    edges = link_graph(docs)

    idx = (found[0] / "index.md") if found else (bundle / "index.md")
    root_fm, _ = frontmatter(idx.read_text()) if idx.exists() else ({}, "")
    cfg_path = bundle / "docs.json"
    if not cfg_path.exists() and found:
        cfg_path = found[0] / "docs.json"
    cfg = json.loads(cfg_path.read_text()) if cfg_path.exists() else {}

    # bundle-local template wins, else the packaged one
    tpl_path = pathlib.Path(template) if template else (bundle / "template.html")
    if not tpl_path.exists():
        tpl_path = HERE / "template.html"

    html_out = (tpl_path.read_text()
        .replace("__TITLE__", html.escape(str(root_fm.get("title") or bundle.resolve().name)))
        .replace("__STATUS__", str(root_fm.get("status") or "—"))
        .replace("__DOCS__", json.dumps(docs))
        .replace("__EDGES__", json.dumps(edges)))
    for k, v in theme_tokens(cfg, root_fm).items():
        html_out = html_out.replace(k, str(v))

    out.write_text(html_out)
    diagrams = sum(d["html"].count('class="mermaid"') for d in docs)
    return dict(out=out, docs=len(docs), edges=len(edges), diagrams=diagrams)
