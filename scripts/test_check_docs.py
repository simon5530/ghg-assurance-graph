#!/usr/bin/env python3
"""Negative tests of the Phase 0 documentation oracle, not domain tests."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("check_docs", ROOT / "scripts/check_docs.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class CheckDocsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "repo"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(".git", ".venv", ".pytest_cache", ".ruff_cache", "__pycache__", "artifacts", "dist", "build"))
    def tearDown(self):
        self.temp.cleanup()
    def test_valid_tree(self):
        self.assertEqual(module.check(self.root)[0], [])
    def test_ignored_environment(self):
        path = self.root / ".venv/vendor/README.md"
        path.parent.mkdir(parents=True)
        path.write_text("[vendor-only](not-bundled.md)")
        self.assertEqual(module.check(self.root)[0], [])
    def test_missing_required(self):
        (self.root / "docs/GATE_A.md").unlink()
        self.assertTrue(module.check(self.root)[0])
    def test_broken_link(self):
        with (self.root / "README.md").open("a") as f:
            f.write("\n[broken](missing.md)\n")
        self.assertTrue(module.check(self.root)[0])
    def test_escaping_link(self):
        with (self.root / "README.md").open("a") as f:
            f.write("\n[escape](../outside.md)\n")
        self.assertTrue(module.check(self.root)[0])
    def test_cycle(self):
        p = self.root / ".github/roadmap.json"
        data = json.loads(p.read_text())
        data["issues"][0]["depends_on"] = [2]
        p.write_text(json.dumps(data))
        self.assertTrue(module.check(self.root)[0])
    def test_missing_contract(self):
        p = self.root / ".github/roadmap.json"
        data = json.loads(p.read_text())
        del data["issues"][0]["verification"]
        p.write_text(json.dumps(data))
        self.assertTrue(module.check(self.root)[0])

if __name__ == "__main__":
    unittest.main()
