#!/usr/bin/env bash
# Refresh the vendored assets from their canonical sources, then strip maintainer
# identifiers so the shipped snapshots stay shareable. The canonical originals are NOT
# modified — only the copies under this plugin.
#
# This is maintainer tooling: it only works on a machine that has the private source tree
# (the torsor prose library, the shelf manual, the artifacts document, and tex2torsor).
#
# Usage:  LAB=/path/to/source-tree scripts/sync-assets.sh
#   LAB must contain:
#     design/torsor-style/prose
#     software/shelf/refactor/manual
#     research/artifacts/src/artifacts.tex
#     software/environs/envtools/manual/tex2torsor
set -euo pipefail

LAB="${LAB:-$HOME/lab}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"   # plugin root

if [ ! -d "$LAB/design/torsor-style/prose" ]; then
  echo "Source tree not found under LAB=$LAB" >&2
  echo "Set LAB=/path/to/your/source-tree and re-run." >&2
  exit 1
fi

echo "Syncing assets from $LAB ..."

# --- prose library (whole tree) ---
rm -rf "$HERE/assets/prose"; mkdir -p "$HERE/assets/prose"
cp -R "$LAB/design/torsor-style/prose/." "$HERE/assets/prose/"

# --- reference snapshots ---
cp "$LAB/software/shelf/refactor/manual/latex/main.tex"                "$HERE/assets/reference/shelf-main.tex"
cp "$LAB/software/shelf/refactor/manual/latex/chapters/00-preface.tex" "$HERE/assets/reference/shelf-00-preface.tex"
# artifacts.tex is only used as a *style* reference — ship the preamble (lines 1-110),
# not the essay body that follows it.
head -n 110 "$LAB/research/artifacts/src/artifacts.tex" > "$HERE/assets/reference/artifacts.tex"

# --- tex2torsor build tool ---
rm -rf "$HERE/tools/tex2torsor"
cp -R "$LAB/software/environs/envtools/manual/tex2torsor" "$HERE/tools/tex2torsor"
find "$HERE/tools/tex2torsor" -name __pycache__ -type d -prune -exec rm -rf {} + 2>/dev/null || true

# --- de-identify the snapshots ---
# Replacement rules live OUTSIDE the repo, in an untracked (gitignored) file, so the
# maintainer's real name never appears in shared content. Create scripts/sanitize.local
# with one or more perl substitutions, e.g.:
#     s/Real Name/torsor lab/g; s/\bRealFirst\b/the author/g;
# Without it this script REFUSES to run — silently shipping un-de-identified snapshots
# is the failure this whole step exists to prevent.
RULES_FILE="$HERE/scripts/sanitize.local"
if [ ! -f "$RULES_FILE" ]; then
  echo "ERROR: scripts/sanitize.local not found — refusing to leave snapshots" >&2
  echo "       un-de-identified. Create it before syncing (see comments above)." >&2
  exit 1
fi

RULES="$(cat "$RULES_FILE")"
# Scope is the whole plugin, not just assets/: skills/ is hand-authored, and that is
# where a name is most likely to be typed rather than imported.
while IFS= read -r f; do
  perl -i -pe "$RULES" "$f"
done < <(find "$HERE" -type f \( -name '*.md' -o -name '*.tex' \) \
           -not -path '*/__pycache__/*' -not -name '*.local')
echo "Sanitized using scripts/sanitize.local (whole plugin)."

# Backstop. Substitution only fixes what its rules anticipate, and it never reaches
# docs/ at the repo root. This fails the sync on anything that slipped through.
"$HERE/scripts/check-identity.sh"

echo "Done. Review with 'git status' / 'git diff', then commit and push."
