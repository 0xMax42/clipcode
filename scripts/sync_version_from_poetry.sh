#!/usr/bin/env bash

set -euo pipefail

# Stelle sicher, dass wir im Projektverzeichnis sind
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PYPROJECT="pyproject.toml"
VERSION_FILE="VERSION"

# Extrahiere die Version mit grep + sed (keine externen Abhängigkeiten nötig)
VERSION=$(grep -E '^version\s*=' "$PYPROJECT" | head -n1 | sed -E 's/.*=\s*"([^"]+)".*/\1/')

if [[ -z "$VERSION" ]]; then
  echo "❌ Version konnte nicht aus $PYPROJECT gelesen werden."
  exit 1
fi

printf "%s" "$VERSION" > "$VERSION_FILE"
echo "✅ Version synchronisiert: $VERSION → $VERSION_FILE"
