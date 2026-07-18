# Contributing to Value Map

Value Map separates its public distribution from its canonical research source.

- `value-map/SKILL.md` is projected from `operatorstack/intelligence-flow` and must not be edited directly here.
- `UPSTREAM.json` records the exact source commit and projected-file checksums.
- The README, brand assets, installers, tests, and `.github/workflows` are owned by this repository.

Open ordinary pull requests for distribution, documentation, installation, test, or control-plane changes. Changes to the operator contract belong upstream in Intelligence Flow and arrive here through a generated sync pull request.

Every merged pull request releases a new patch version by default. Apply exactly one of these labels when needed:

- `minor` — release the next minor version;
- `major` — release the next major version;
- `skip-release` — merge without publishing a release.

Before opening a pull request, run:

```bash
python3 -m unittest discover -s tests -v
bash -n install.sh
python3 scripts/project_upstream.py --source ../intelligence-flow --repo . --check
```

By contributing, you agree that your contribution is licensed under Apache-2.0.
