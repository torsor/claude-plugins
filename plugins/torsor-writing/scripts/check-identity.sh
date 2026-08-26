#!/usr/bin/env bash
# Backstop: refuse to ship content that carries maintainer identity.
#
# sync-assets.sh rewrites the vendored snapshots under assets/, but skills/ and
# docs/ are hand-authored and are never rewritten — which is exactly where a name
# gets typed by accident. This check covers the whole repo regardless of how the
# content got there, so it catches what the sanitizer structurally cannot.
#
# Patterns live OUTSIDE the repo in scripts/identity.local (gitignored): one
# extended regex per line; blank lines and #-comments ignored.
#
# Usage:  scripts/check-identity.sh
# Exit:   0 = clean · 1 = hits found, or patterns missing
set -euo pipefail

PLUGIN="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO="$(cd "$PLUGIN/../.." && pwd)"
PATTERNS="$PLUGIN/scripts/identity.local"

if [ ! -f "$PATTERNS" ]; then
  echo "check-identity: patterns file not found: scripts/identity.local" >&2
  echo "  Create it (one extended regex per line) before sharing this repo." >&2
  echo "  It is gitignored on purpose — see scripts/sync-assets.sh." >&2
  exit 1
fi

CLEANED="$(mktemp)"
trap 'rm -f "$CLEANED"' EXIT
grep -vE '^[[:space:]]*(#|$)' "$PATTERNS" > "$CLEANED" || true

if [ ! -s "$CLEANED" ]; then
  echo "check-identity: scripts/identity.local has no usable patterns." >&2
  exit 1
fi

cd "$REPO"
HITS="$(grep -rEnI -f "$CLEANED" . \
          --exclude-dir=.git --exclude-dir=__pycache__ \
          --exclude='*.local' 2>/dev/null || true)"

if [ -n "$HITS" ]; then
  echo "check-identity: FAIL — maintainer identity in shippable content:" >&2
  printf '%s\n' "$HITS" | sed 's/^/  /' >&2
  echo "" >&2
  echo "  Fix the content (or widen scripts/sanitize.local) before committing." >&2
  exit 1
fi

echo "check-identity: clean — no maintainer identity in shippable content."
