from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "project_upstream", ROOT / "scripts/project_upstream.py"
)
assert SPEC and SPEC.loader
PROJECT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROJECT)


class DistributionTests(unittest.TestCase):
    def test_manifest_matches_projected_skill(self) -> None:
        manifest = json.loads((ROOT / "UPSTREAM.json").read_text())
        skill = ROOT / "value-map/SKILL.md"
        self.assertEqual(manifest["generator"], PROJECT.GENERATOR)
        self.assertEqual(
            manifest["files"]["value-map/SKILL.md"],
            hashlib.sha256(skill.read_bytes()).hexdigest(),
        )

    def test_projection_refuses_downstream_collision(self) -> None:
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as repo_dir:
            source = Path(source_dir)
            repo = Path(repo_dir)
            canonical = source / PROJECT.SOURCE_PATH
            canonical.parent.mkdir(parents=True)
            canonical.write_text("canonical\n")
            target = repo / PROJECT.DESTINATION
            target.parent.mkdir(parents=True)
            target.write_text("downstream edit\n")
            files = PROJECT.projected_files(source, "a" * 40)
            self.assertEqual(PROJECT.write(repo, files, adopt=False), 2)
            self.assertEqual(target.read_text(), "downstream edit\n")

    def test_public_surface_is_downstream_owned(self) -> None:
        manifest = json.loads((ROOT / "UPSTREAM.json").read_text())
        self.assertNotIn("README.md", manifest["files"])
        self.assertNotIn("assets/value-map-mark.svg", manifest["files"])
        self.assertNotIn("install.sh", manifest["files"])
        self.assertNotIn(".github/workflows/release.yml", manifest["files"])

    def test_skill_contract_is_read_only_and_conversational(self) -> None:
        skill = (ROOT / "value-map/SKILL.md").read_text()
        normalized = re.sub(r"\s+", " ", skill)
        self.assertIn("Keep repository access read-only", normalized)
        self.assertIn("opening move in a conversation", skill)
        self.assertIn("`PROPOSED`", skill)
        self.assertIn("Do not include a full claim/evidence table", skill)


if __name__ == "__main__":
    unittest.main()
