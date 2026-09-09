#!/usr/bin/env python3
"""Mechanical build checks for a torsor document (tier 1 of the publication pass).

Run from the document root (the directory holding Makefile and latex/):

    python3 check-build.py [--root DIR] [--log PATH]

Verifies, without trusting any tool's exit code:
  - latex/main.pdf exists and is newer than every .tex source
  - the LaTeX log carries no errors and no undefined references/citations
  - overfull hboxes, itemized with pt overrun and source lines
  - no non-ASCII characters inside lstlisting environments
  - HTML math fallback spans have a MathJax loader if present
  - EPUB and Markdown outputs exist (informational)

Prints an evidence report. Exit 1 on hard failures (missing/stale PDF, LaTeX
errors, undefined references); exit 0 otherwise — warnings still deserve reading.
No dependencies beyond the standard library.
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


def fmt_mtime(p: Path) -> str:
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(p.stat().st_mtime))


def check_pdf(root: Path, failures: list[str]) -> None:
    pdf = root / "latex" / "main.pdf"
    if not pdf.exists():
        failures.append("PDF missing: latex/main.pdf")
        print("PDF: MISSING (latex/main.pdf)")
        return
    sources = list((root / "latex").rglob("*.tex"))
    newer = [s for s in sources if s.stat().st_mtime > pdf.stat().st_mtime]
    fresh = not newer
    print(f"PDF: latex/main.pdf, built {fmt_mtime(pdf)}, fresh against sources: {'yes' if fresh else 'NO'}")
    if not fresh:
        failures.append("PDF stale — sources newer than PDF")
        for s in newer:
            print(f"  newer source: {s.relative_to(root)} ({fmt_mtime(s)})")


def find_log(root: Path, explicit: str | None) -> Path | None:
    if explicit:
        p = Path(explicit)
        return p if p.exists() else None
    for cand in ("latex/main.log", "latex/build/main.log", "build/main.log"):
        p = root / cand
        if p.exists():
            return p
    return None


def check_log(log: Path | None, failures: list[str]) -> None:
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
        worst = max(pt for pt, _ in overfull)
        print(f"Overfull hboxes: {len(overfull)} (worst {worst}pt)")
        for pt, where in sorted(overfull, reverse=True)[:15]:
            print(f"  {pt}pt {where}")
    else:
        print("Overfull hboxes: none")


def check_listings_ascii(root: Path, warnings: list[str]) -> None:
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
        warnings.append("non-ASCII inside lstlisting")
        print(f"lstlisting non-ASCII: {len(hits)} line(s)")
        for h in hits[:10]:
            print(f"  {h}")
    else:
        print("lstlisting non-ASCII: none")


def check_html(root: Path, warnings: list[str]) -> None:
    html = root / "html" / "manual.html"
    if not html.exists():
        print("HTML: not built")
        return
    text = html.read_text(errors="replace")
    spans = text.count('class="math')
    loader = "MathJax-script" in text
    print(f"HTML math: {spans} fallback span(s), MathJax loader present: {'yes' if loader else 'no'}")
    if spans and not loader:
        warnings.append("HTML has raw TeX math spans but no MathJax loader (see commons/lessons.md)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=".", help="document root (default: cwd)")
    ap.add_argument("--log", default=None, help="path to the LaTeX log if not latex/main.log")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    if not (root / "latex").is_dir():
        print(f"error: no latex/ directory under {root}", file=sys.stderr)
        return 2

    failures: list[str] = []
    warnings: list[str] = []
    print(f"== check-build report — {root.name} ==")
    check_pdf(root, failures)
    check_log(find_log(root, args.log), failures)
    check_listings_ascii(root, warnings)
    check_html(root, warnings)
    for out, label in (("epub/manual.epub", "EPUB"), ("markdown/manual.md", "Markdown")):
        print(f"{label}: {'present' if (root / out).exists() else 'not built'}")

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
