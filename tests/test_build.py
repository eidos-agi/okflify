"""
Regression tests for okflify.

Every case here is a bug that actually shipped or nearly shipped — shipr's
release model named `pytest` as a proof command and nothing existed to run.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from okflify.build import frontmatter, inl, discover, build

ROOT = pathlib.Path(__file__).parent.parent
EXAMPLE = ROOT / "okflify" / "example"


def nav(md_link):
    """Extract the data-nav target okflify would emit for a markdown link."""
    out = inl(f"[x]({md_link})")
    return out.split('data-nav="')[1].split('"')[0] if "data-nav=" in out else None


class TestLinkResolution:
    def test_same_section(self):
        assert nav("trust-tiers.md") == "{BUNDLE}/trust-tiers"

    def test_subdirectory(self):
        assert nav("concepts/trust-tiers.md") == "{BUNDLE}/trust-tiers"

    def test_section_hop_is_not_a_bundle_hop(self):
        # THE BUG: "../learnings/x.md" is a section hop INSIDE one bundle, but is
        # structurally identical to "../other-bundle/index.md". Treating it as a
        # bundle hop silently dropped edges — caught only by a count mismatch.
        assert nav("../learnings/links-are-the-product.md") == "{BUNDLE}/links-are-the-product"
        assert nav("../evidence/build-output.md") == "{BUNDLE}/build-output"

    def test_bundle_hop_still_works(self):
        assert nav("../redash-security-baseline/index.md") == "redash-security-baseline/index"

    def test_external_links_untouched(self):
        assert nav("https://example.com") is None


class TestFrontmatter:
    def test_nested_verified_block(self):
        fm, body = frontmatter(
            '---\nokf_version: "0.2"\ntype: rule\ntitle: "T"\n'
            'verified:\n  by: human:daniel\n  at: 2026-07-29\n  method: "m"\n---\n\nbody\n')
        assert fm["type"] == "rule"
        assert fm["verified"]["by"] == "human:daniel"
        assert body.strip() == "body"

    def test_missing_frontmatter_is_not_fatal(self):
        fm, body = frontmatter("# log\n\nno frontmatter by convention\n")
        assert fm == {}
        assert "log" in body


class TestDiscover:
    def test_single_bundle(self):
        assert discover(EXAMPLE) == [EXAMPLE]

    def test_catalogue(self, tmp_path):
        for name in ("alpha", "beta"):
            d = tmp_path / "bundles" / name
            d.mkdir(parents=True)
            (d / "index.md").write_text('---\ntitle: "T"\n---\n\nx\n')
        assert sorted(p.name for p in discover(tmp_path)) == ["alpha", "beta"]


class TestBuild:
    def test_example_bundle(self, tmp_path):
        r = build(EXAMPLE, tmp_path / "out.html")
        assert r["docs"] == 6
        # A drop below this means the section-hop resolver bug is back.
        assert r["edges"] == 7
        assert r["out"].is_file()

    def test_host_home_from_docs_json(self, tmp_path):
        # Host app return is optional; when set, header must leave the pack.
        b = tmp_path / "bundle"
        b.mkdir()
        (b / "index.md").write_text(
            '---\nokf_version: "0.2"\ntype: claim\ntitle: "T"\n---\n\nbody\n'
        )
        (b / "docs.json").write_text(
            '{"name":"Demo","home":{"href":"/app/","label":"App"}}'
        )
        out = tmp_path / "out.html"
        build(b, out)
        html_out = out.read_text()
        assert 'id="host-home"' in html_out
        assert 'href="/app/"' in html_out
        assert "App" in html_out
        assert "←" in html_out
        # Hosted pack: no hard-coded okflify GitHub promo
        assert "github.com/eidos-agi/okflify" not in html_out

    def test_github_false_hides_link(self, tmp_path):
        b = tmp_path / "bundle"
        b.mkdir()
        (b / "index.md").write_text(
            '---\nokf_version: "0.2"\ntype: claim\ntitle: "T"\n---\n\nbody\n'
        )
        (b / "docs.json").write_text('{"name":"Demo","github":false}')
        out = tmp_path / "out.html"
        build(b, out)
        assert "github.com" not in out.read_text()

    def test_github_custom_repo(self, tmp_path):
        b = tmp_path / "bundle"
        b.mkdir()
        (b / "index.md").write_text(
            '---\nokf_version: "0.2"\ntype: claim\ntitle: "T"\n---\n\nbody\n'
        )
        (b / "docs.json").write_text(
            '{"name":"Demo","github":{"href":"https://github.com/org/product","label":"Source"}}'
        )
        html_out = build(b, tmp_path / "out.html")["out"].read_text()
        assert "github.com/org/product" in html_out
        assert "Source" in html_out
        assert "github.com/eidos-agi/okflify" not in html_out

    def test_output_is_self_contained(self, tmp_path):
        out = tmp_path / "out.html"
        build(EXAMPLE, out)
        html = out.read_text()
        assert html.startswith("<!doctype html>")
        assert "__DOCS__" not in html and "__PRIMARY__" not in html   # all placeholders filled
        assert 'id="treehost"' in html and 'data-nav="tree"' in html  # tree view present
        assert "human:daniel" in html  # trust tiers rendered                                  # trust tiers rendered

    def test_mobile_navigation_is_a_drawer(self, tmp_path):
        html = build(EXAMPLE, tmp_path / "out.html")["out"].read_text()
        assert 'id="navtoggle"' in html
        assert 'aria-controls="nav"' in html
        assert "aside.open{transform:none}" in html
        assert "mobileNav(false)" in html

    def test_orf_and_emf_profiles_render(self, tmp_path):
        for name, version in (("orf", "0.2.0"), ("emf", "0.1")):
            bundle = tmp_path / name
            bundle.mkdir()
            (bundle / "index.md").write_text(
                f'---\nokf_version: "0.2"\n{name}_version: "{version}"\n'
                f'type: claim\ntitle: "{name.upper()} example"\n---\n\nbody\n'
            )
            rendered = build(bundle, tmp_path / f"{name}.html")["out"].read_text()
            assert "OKF v0.2" in rendered
            assert f"{name.upper()} v{version}" in rendered

    def test_empty_directory_fails_loudly(self, tmp_path):
        try:
            build(tmp_path, tmp_path / "o.html")
        except SystemExit as e:
            assert "no OKF documents" in str(e)
        else:
            raise AssertionError("an empty directory must not build silently")


class TestVersioning:
    def test_version_is_single_sourced(self):
        """__init__ must not hard-code a number that can drift from pyproject."""
        import re
        src = (ROOT / "okflify" / "__init__.py").read_text()
        assert "importlib.metadata" in src, "version must come from package metadata"
        # a literal is fine ONLY as the not-installed sentinel
        for lit in re.findall(r'__version__ = "([^"]+)"', src):
            assert lit.endswith("+source"), f"hard-coded release version: {lit}"

    def test_pyproject_has_a_version(self):
        import re
        txt = (ROOT / "pyproject.toml").read_text()
        m = re.search(r'^version = "(\d+\.\d+\.\d+)"', txt, re.M)
        assert m, "pyproject version missing or malformed"
