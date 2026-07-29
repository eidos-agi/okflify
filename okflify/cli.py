"""okflify CLI — converts OKF bundles into HTML."""
import argparse, pathlib, sys
from . import __version__
from .build import build


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="okflify",
        description="Convert an Open Knowledge Format v0.2 bundle into one self-contained HTML file.",
        epilog="OKF is a graph, not a tree: directories are storage, the structure is the links.",
    )
    ap.add_argument("bundle", nargs="?", default=".", help="bundle directory (default: .)")
    ap.add_argument("--example", action="store_true",
                    help="render the bundle that documents okflify (ships in this repo)")
    ap.add_argument("-o", "--out", help="output file (default: <bundle>/okflify.html)")
    ap.add_argument("-t", "--template", help="override the HTML template")
    ap.add_argument("--open", action="store_true", help="open the result when done")
    ap.add_argument("--version", action="version", version=f"okflify {__version__}")
    a = ap.parse_args(argv)

    if a.example:
        import okflify
        a.bundle = str(pathlib.Path(okflify.__file__).parent / "example")
    r = build(a.bundle, a.out, a.template)
    print(f"okflify → {r['out']} — {r['docs']} documents, {r['edges']} edges, {r['diagrams']} diagrams")
    if r["edges"] == 0 and r["docs"] > 1:
        print("  note: no links between documents — the graph view will be empty.", file=sys.stderr)
    if a.open:
        import subprocess, shutil
        for cmd in ("open", "xdg-open"):
            if shutil.which(cmd):
                subprocess.run([cmd, str(r["out"])]); break
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
