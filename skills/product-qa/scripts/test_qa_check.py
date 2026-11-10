#!/usr/bin/env python3
"""Tests for qa_check.py. Run from this folder:  python test_qa_check.py"""
import io
import os
import sys
import tempfile
import unittest
import zipfile
from contextlib import redirect_stdout, redirect_stderr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qa_check as qa  # noqa: E402


def make(folder, files):
    for rel, data in files.items():
        full = os.path.join(folder, *rel.split("/"))
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "wb") as fh:
            fh.write(data if isinstance(data, bytes) else data.encode("utf-8"))


GOOD = {
    "pack/README.md": "# Pack\nSee [the guide](docs/guide.md) and https://example.com/help\n",
    "pack/LICENSE.txt": "Personal use.",
    "pack/docs/guide.md": "Step one.",
}


def run_cli(*args):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = qa.main(list(args))
    return code, out.getvalue(), err.getvalue()


class Checks(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.report = os.path.join(self.dir, "qa-report.md")

    def read_report(self):
        with open(self.report, encoding="utf-8") as fh:
            return fh.read()

    def test_clean_folder(self):
        src = os.path.join(self.dir, "src")
        make(src, GOOD)
        code, out, _ = run_cli(src, "--out", self.report)
        self.assertEqual(code, 0)
        rep = self.read_report()
        self.assertIn("READY AFTER MANUAL PASS - 0 blocker(s)", rep)
        self.assertIn("https://example.com/help", rep)  # listed, not checked

    def test_planted_problems(self):
        src = os.path.join(self.dir, "bad")
        make(src, {
            "pack/notes.md": "TODO finish. See [missing](nope.md). Path C:\\Users\\someone\\file\n",
            "pack/empty.txt": b"",
            "pack/Thumbs.db": b"x",
            "pack/__pycache__/x.pyc": b"x",
            # built at runtime so this test file itself doesn't look like it ships a secret
            "pack/key.txt": "api_" + "key = 'abcdefghijklmnop'",
            "pack/final_v2.pdf": b"%PDF",
        })
        code, _, _ = run_cli(src, "--out", self.report)
        self.assertEqual(code, 1)
        rep = self.read_report()
        for want in ("No README", "No LICENSE", "Empty file", "Junk/system file shipped: `pack/Thumbs.db`",
                     "Junk/system file shipped: `pack/__pycache__/x.pyc`", "Broken local link", "Possible API key",
                     "Placeholder `TODO`", "Personal local path", "Messy file name"):
            self.assertIn(want, rep, want)

    def test_zip_and_listing_crosscheck(self):
        z = os.path.join(self.dir, "p.zip")
        with zipfile.ZipFile(z, "w") as zf:
            for rel, data in GOOD.items():
                zf.writestr(rel, data)
        listing = os.path.join(self.dir, "listing.md")
        with open(listing, "w", encoding="utf-8-sig") as fh:  # BOM on purpose
            fh.write("Inside: `guide.md` and `bonus.pdf`.\n")
        code, _, _ = run_cli(z, "--out", self.report, "--listing", listing)
        self.assertEqual(code, 1)
        rep = self.read_report()
        self.assertIn("Listing mentions `bonus.pdf`", rep)
        self.assertNotIn("Listing mentions `guide.md`", rep)

    def test_skip_content(self):
        src = os.path.join(self.dir, "skip")
        make(src, dict(GOOD, **{"pack/templates/t.md": "Fill {{ name }} and [ASK USER: x]"}))
        run_cli(src, "--out", self.report)
        self.assertIn("Placeholder", self.read_report())
        code, _, _ = run_cli(src, "--out", self.report, "--skip-content", "pack/templates/*")
        self.assertEqual(code, 0)
        self.assertNotIn("Placeholder", self.read_report())

    def test_link_like_text_in_code_is_not_a_link(self):
        src = os.path.join(self.dir, "code")
        make(src, dict(GOOD, **{"pack/tool.py": "LINK = r'href=[\"\\']([^\"\\']+)'  # [x](not/a/file.md)\n"}))
        code, _, _ = run_cli(src, "--out", self.report)
        self.assertEqual(code, 0)
        self.assertNotIn("Broken local link", self.read_report())

    def test_path_placeholders_are_not_personal_paths(self):
        src = os.path.join(self.dir, "ph")
        make(src, dict(GOOD, **{"pack/docs/install.md":
                                "Copy to C:\\Users\\<you>\\.claude\\skills or /home/<user>/.claude/skills\n"}))
        run_cli(src, "--out", self.report)
        self.assertNotIn("Personal local path", self.read_report())
        make(src, {"pack/docs/real.md": "Saved in C:\\Users\\" + "jdoe\\Desktop\n"})
        run_cli(src, "--out", self.report)
        self.assertIn("Personal local path in `pack/docs/real.md`", self.read_report())

    def test_urls_are_cleaned(self):
        self.assertEqual(qa.clean_url("https://example.com/help\\n"), "https://example.com/help")
        self.assertEqual(qa.clean_url("https://example.com/a."), "https://example.com/a")
        src = os.path.join(self.dir, "urls")
        make(src, dict(GOOD, **{"pack/tool.py": 'print("see https://example.com/help\\n")\n'}))
        run_cli(src, "--out", self.report)
        rep = self.read_report()
        self.assertIn("- https://example.com/help\n", rep)
        self.assertNotIn("help\\n", rep)

    def test_bad_input(self):
        self.assertEqual(run_cli(os.path.join(self.dir, "nope"), "--out", self.report)[0], 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
