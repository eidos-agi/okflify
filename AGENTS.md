# okflify — instructions for AI operators

## What this is

`okflify` converts OKF bundles into HTML. One bundle directory in, one
self-contained file out.

```sh
okflify <bundle> -o out.html      # or: python3 -m okflify <bundle>
```

## Rules

**Never edit `okflify/template.html` to restyle.** Theming lives in the
bundle's `docs.json` (Mintlify shape: `colors`, `fonts`, `appearance`,
`background.decoration`, `styling.eyebrows`). Editing the template to change a
colour is how the config stops being the source of truth.

**Never soften trust signals.** If a document is `agent:`-verified, the output
says so and warns that it is unverified for gate-shaped decisions. Do not make
that subtler because it looks untidy — it is the point of OKF v0.2.

**Do not add dependencies.** Standard library only. Mermaid arrives from a CDN
at view time, not at build time.

## Verifying changes

Rendering bugs here are visual and will not raise. `tsc`-equivalent confidence
does not exist. **Check the rendered DOM in a real browser** — [mafia](https://github.com/eidos-agi/mafia)
is the sibling tool:

```sh
printf '%s\n' '{"op":"session_open"}' \
  '{"op":"navigate","url":"file:///path/okflify.html#01-topology"}' \
  '{"op":"wait","ms":4000}' \
  '{"op":"eval","expr":"document.querySelectorAll(\".doc.on .mermaid svg\").length"}' \
  '{"op":"quit"}' | mafia api
```

Specifically, after any theme or mermaid change, **toggle the theme and
re-measure**. Configuring mermaid with the right colours is not the same as
those colours reaching the screen — see the `data-processed` note in README.

## Known traps

| Trap | Reality |
|---|---|
| `mermaid.run()` on a rendered block | Silent no-op. Restore the pristine source and strip `data-processed` first. |
| Mermaid `neutral` / `dark` themes | Dark fills, dark labels. Use `theme:"base"` + `themeVariables`. |
| A bundle with no cross-links | Renders a star. That is the bundle's problem, not the renderer's — say so rather than papering over it. |
| `file://` in Chrome extensions | Blocked. Use mafia, or serve over `http.server`. |
