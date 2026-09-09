#!/usr/bin/env bash
# Validate and sanitize a staged snapshot before replacing vendored assets.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$HERE/sync_assets.py" "$@"
