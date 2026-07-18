#!/usr/bin/env python3
"""Project the canonical Value Map skill from Intelligence Flow."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


GENERATOR = "operator-stack/value-map:project-upstream"
SOURCE_REPOSITORY = "operatorstack/intelligence-flow"
SOURCE_PATH = Path("labs/14-product-value-projection/value-map/SKILL.md")
MANIFEST = Path("UPSTREAM.json")
DESTINATION = Path("value-map/SKILL.md")


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def projected_files(source: Path, commit: str) -> dict[Path, bytes]:
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("commit must be a full 40-character lowercase Git SHA")
    skill = (source / SOURCE_PATH).read_bytes()
    manifest = {
        "schema_version": 1,
        "generator": GENERATOR,
        "source": {
            "repository": SOURCE_REPOSITORY,
            "commit": commit,
            "path": str(SOURCE_PATH.parent),
        },
        "files": {str(DESTINATION): sha256(skill)},
    }
    return {
        DESTINATION: skill,
        MANIFEST: (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode(),
    }


def previous_manifest(repo: Path) -> dict:
    path = repo / MANIFEST
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text())
    except (OSError, ValueError, TypeError):
        return {}
    return value if value.get("generator") == GENERATOR else {}


def collisions(repo: Path, files: dict[Path, bytes], adopt: bool) -> list[str]:
    if adopt:
        return []
    previous = previous_manifest(repo)
    owned = previous.get("files", {})
    problems: list[str] = []
    for relative, content in files.items():
        target = repo / relative
        if not target.exists() or target.read_bytes() == content:
            continue
        if relative == MANIFEST and previous:
            continue
        old_hash = owned.get(str(relative))
        if not old_hash or sha256(target.read_bytes()) != old_hash:
            problems.append(str(relative))
    return problems


def write(repo: Path, files: dict[Path, bytes], adopt: bool) -> int:
    problems = collisions(repo, files, adopt)
    if problems:
        print("BLOCKED: refusing to overwrite downstream-owned files:")
        for problem in problems:
            print(f"  {problem}")
        return 2
    for relative, content in files.items():
        target = repo / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    print(f"wrote {len(files)} projected files")
    return 0


def check(repo: Path, files: dict[Path, bytes]) -> int:
    problems = []
    for relative, content in files.items():
        target = repo / relative
        if not target.is_file():
            problems.append(f"missing {relative}")
        elif target.read_bytes() != content:
            problems.append(f"drift {relative}")
    if problems:
        print("BLOCKED: projection drift detected:")
        for problem in problems:
            print(f"  {problem}")
        return 1
    print("PASS: Value Map matches the selected Intelligence Flow commit")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--commit", required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--adopt", action="store_true")
    args = parser.parse_args()
    files = projected_files(args.source.resolve(), args.commit)
    if args.check:
        return check(args.repo.resolve(), files)
    return write(args.repo.resolve(), files, args.adopt)


if __name__ == "__main__":
    raise SystemExit(main())
