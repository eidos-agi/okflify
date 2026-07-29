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

    def test_output_is_self_contained(self, tmp_path):
        out = tmp_path / "out.html"
        build(EXAMPLE, out)
        html = out.read_text()
        assert html.startswith("<!doctype html>")
        assert "__DOCS__" not in html and "__PRIMARY__" not in html   # all placeholders filled
        assert 'id="treehost"' in html and 'data-nav="tree"' in html  # tree view present
        assert "human:daniel" in html  # trust tiers rendered                                  # trust tiers rendered

    def test_empty_directory_fails_loudly(self, tmp_path):
        try:
            build(tmp_path, tmp_path / "o.html")
        except SystemExit as e:
            assert "no OKF documents" in str(e)
        else:
            raise AssertionError("an empty directory must not build silently")
