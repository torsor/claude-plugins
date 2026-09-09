#!/usr/bin/env bash
# Inspect working files and the index; --history also checks every local ref.
# Provenance needs manual review. See docs/PUBLICATION.md.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$HERE/audit_public.py" "$@"
