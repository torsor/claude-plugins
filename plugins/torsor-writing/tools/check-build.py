#!/usr/bin/env python3
"""Mechanical build checks for a torsor document (tier 1 of the publication pass).

Run from the document root (the directory holding Makefile and latex/):

    python3 check-build.py [--root DIR] [--stem NAME] [--log PATH]
                           [--overfull-threshold PT]

The output stem defaults to the document directory's name (the unified builder
names outputs <stem>.pdf/.html/.epub/-svg.epub/.md). Override with --stem.

Verifies, without trusting any tool's exit code:
  - the deliverable PDF exists and is newer than every .tex source
  - the LaTeX log carries no errors and no undefined references/citations
  - overfull hboxes, itemized with pt overrun and source lines
  - no non-ASCII characters inside lstlisting environments
  - HTML math fallback spans have a MathJax loader if present
  - both EPUBs (MathML + SVG math) and the Markdown output exist

Exit 1 on mechanical failures: missing/stale PDF, LaTeX errors, undefined
references, overfull hboxes over the threshold, non-ASCII listings, or any
missing expected output. Overfull hboxes at or below --overfull-threshold pt are
reported but not fatal (they are the residue no rewrap can fix). Exit 0
otherwise. No dependencies beyond the standard library.
"""
from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

OVERFULL_RE = re.compile(r"Overfull \\hbox \((\d+(?:\.\d+)?)pt too wide\)(.*)")
UNDEF_RE = re.compile(r"LaTeX Warning: (Reference|Citation) [`']([^']*)' .*undefined")
PAGES_RE = re.compile(r"Output written on .*\((\d+) pages?")

DEFAULT_OVERFULL_THRESHOLD = 2.0


def fmt_mtime(p: Path) -> str:
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(p.stat().st_mtime))


def find_pdf(root: Path, stem: str) -> Path | None:
    """Prefer the stem-named deliverable; fall back to the raw latexmk output."""
    for cand in (f"latex/{stem}.pdf", "latex/main.pdf"):
        p = root / cand
        if p.exists():
            return p
    return None


def check_pdf(root: Path, stem: str, failures: list[str]) -> None:
    pdf = find_pdf(root, stem)
    if pdf is None:
        failures.append(f"PDF missing: latex/{stem}.pdf")
        print(f"PDF: MISSING (latex/{stem}.pdf)")
        return
    sources = list((root / "latex").rglob("*.tex"))
    newer = [s for s in sources if s.stat().st_mtime > pdf.stat().st_mtime]
    fresh = not newer
    print(f"PDF: {pdf.relative_to(root)}, built {fmt_mtime(pdf)}, fresh against sources: {'yes' if fresh else 'NO'}")
    if not fresh:
        failures.append("PDF stale — sources newer than PDF")
        for s in newer:
            print(f"  newer source: {s.relative_to(root)} ({fmt_mtime(s)})")


def find_log(root: Path, stem: str, explicit: str | None) -> Path | None:
    if explicit:
        p = Path(explicit)
        return p if p.exists() else None
    for cand in (f"latex/{stem}.log", "latex/main.log", "latex/build/main.log", "build/main.log"):
        p = root / cand
        if p.exists():
            return p
    return None


def check_log(log: Path | None, threshold: float, failures: list[str]) -> None:
    if log is None:
        print("Log: NOT FOUND — latexd may keep it elsewhere; pass --log PATH. "
              "Errors/undefined refs/overfull NOT checked.")
        failures.append("LaTeX log not found — log-based checks did not run")
        return
    text = log.read_text(errors="replace")
    lines = text.splitlines()

    m = PAGES_RE.search(text)
    print(f"Pages: {m.group(1) if m else 'not stated in log'}")

    errors = [ln for ln in lines if ln.startswith("! ")]
    if errors:
        failures.append(f"{len(errors)} LaTeX error(s) in log")
        print(f"LaTeX errors: {len(errors)}")
        for ln in errors[:10]:
            print(f"  {ln}")
    else:
        print("LaTeX errors: none")

    undef = UNDEF_RE.findall(text)
    if "There were undefined references" in text or undef:
        failures.append("undefined references/citations")
        print(f"Undefined refs/citations: {len(undef)}")
        for kind, name in undef[:20]:
            print(f"  {kind}: {name}")
    else:
        print("Undefined refs/citations: none")

    overfull = [(float(m.group(1)), m.group(2).strip()) for m in map(OVERFULL_RE.match, lines) if m]
    if overfull:
        over = [(pt, where) for pt, where in overfull if pt > threshold]
        under = len(overfull) - len(over)
        worst = max(pt for pt, _ in overfull)
        note = f" ({under} at or below {threshold}pt, not fatal)" if under else ""
        print(f"Overfull hboxes: {len(overfull)} (worst {worst}pt){note}")
        if over:
            failures.append(f"{len(over)} overfull hbox(es) over {threshold}pt")
        for pt, where in sorted(over, reverse=True)[:15]:
            print(f"  {pt}pt {where}")
    else:
        print("Overfull hboxes: none")


def check_listings_ascii(root: Path, failures: list[str]) -> None:
    hits: list[str] = []
    for tex in (root / "latex").rglob("*.tex"):
        inside = False
        for i, ln in enumerate(tex.read_text(errors="replace").splitlines(), 1):
            if "\\begin{lstlisting}" in ln:
                inside = True
            if inside and any(ord(c) > 127 for c in ln):
                hits.append(f"{tex.relative_to(root)}:{i}")
            if "\\end{lstlisting}" in ln:
                inside = False
    if hits:
        failures.append("non-ASCII inside lstlisting")
        print(f"lstlisting non-ASCII: {len(hits)} line(s)")
        for h in hits[:10]:
            print(f"  {h}")
    else:
        print("lstlisting non-ASCII: none")


def check_html(root: Path, stem: str, warnings: list[str]) -> None:
    html = root / "html" / f"{stem}.html"
    if not html.exists():
        print("HTML: not built")
        return
    text = html.read_text(errors="replace")
    spans = text.count('class="math')
    loader = "MathJax-script" in text
    print(f"HTML math: {spans} fallback span(s), MathJax loader present: {'yes' if loader else 'no'}")
    if spans and not loader:
        warnings.append("HTML has raw TeX math spans but no MathJax loader")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".", help="document root (default: cwd)")
    ap.add_argument("--stem", default=None, help="output stem (default: document directory name)")
    ap.add_argument("--log", default=None, help="path to the LaTeX log if not latex/<stem>.log or latex/main.log")
    ap.add_argument("--overfull-threshold", type=float, default=DEFAULT_OVERFULL_THRESHOLD,
                    help=f"overfull hboxes at or below this many pt are not fatal (default: {DEFAULT_OVERFULL_THRESHOLD})")
    ap.add_argument("--require", nargs="*", default=None, metavar="PATH",
                    help="output files that must exist (the Makefile passes the registered "
                         "formats' + features' declared outputs). If omitted, defaults to "
                         "epub/<stem>.epub and markdown/<stem>.md.")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    if not (root / "latex").is_dir():
        print(f"error: no latex/ directory under {root}", file=sys.stderr)
        return 2
    stem = args.stem or root.name

    failures: list[str] = []
    warnings: list[str] = []
    print(f"== check-build report — {root.name} (stem: {stem}) ==")
    check_pdf(root, stem, failures)
    check_log(find_log(root, stem, args.log), args.overfull_threshold, failures)
    check_listings_ascii(root, failures)
    check_html(root, stem, warnings)
    required = args.require if args.require is not None else [f"epub/{stem}.epub", f"markdown/{stem}.md"]
    for rel in required:
        present = (root / rel).exists()
        print(f"output {rel}: {'present' if present else 'MISSING'}")
        if not present:
            failures.append(f"missing output: {rel}")

    print()
    if failures:
        print("FAIL: " + "; ".join(failures))
        return 1
    if warnings:
        print("PASS with warnings: " + "; ".join(warnings))
    else:
        print("PASS: all mechanical checks clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
