#!/usr/bin/env bash
set -euo pipefail

repository="operator-stack/value-map"
version="${VALUE_MAP_VERSION:-latest}"
host="${VALUE_MAP_HOST:-}"
target_repo="${VALUE_MAP_REPO:-$PWD}"

case "$host" in
  codex|cursor|claude) ;;
  *) echo "BLOCKED: set VALUE_MAP_HOST to codex, cursor, or claude" >&2; exit 2 ;;
esac

command -v curl >/dev/null 2>&1 || { echo "BLOCKED: curl is required" >&2; exit 2; }

if [ "$version" = "latest" ]; then
  base="https://github.com/${repository}/releases/latest/download"
else
  base="https://github.com/${repository}/releases/download/${version}"
fi

temporary="$(mktemp -d 2>/dev/null || mktemp -d -t value-map)"
trap 'rm -rf "$temporary"' EXIT
skill="$temporary/value-map-SKILL.md"
checksum="$temporary/value-map-SKILL.md.sha256"

curl -fsSL "$base/value-map-SKILL.md" -o "$skill"
curl -fsSL "$base/value-map-SKILL.md.sha256" -o "$checksum"
expected="$(awk '{print $1}' "$checksum")"
if command -v shasum >/dev/null 2>&1; then
  actual="$(shasum -a 256 "$skill" | awk '{print $1}')"
elif command -v sha256sum >/dev/null 2>&1; then
  actual="$(sha256sum "$skill" | awk '{print $1}')"
else
  echo "BLOCKED: shasum or sha256sum is required" >&2
  exit 2
fi
[ "$expected" = "$actual" ] || { echo "BLOCKED: Value Map checksum mismatch" >&2; exit 2; }

case "$host" in
  codex)
    destination="${CODEX_HOME:-$HOME/.codex}/skills/value-map/SKILL.md"
    ;;
  claude)
    destination="$HOME/.claude/skills/value-map/SKILL.md"
    ;;
  cursor)
    [ -d "$target_repo" ] || { echo "BLOCKED: Cursor repository does not exist: $target_repo" >&2; exit 2; }
    destination="$target_repo/.cursor/commands/value-map.md"
    ;;
esac

mkdir -p "$(dirname "$destination")"
cp "$skill" "$destination"
echo "Installed Value Map for $host at $destination"

