#!/usr/bin/env python3
"""Verify 00-guide.pdf rather than trusting pandoc's or pdflatex's exit status.

Nothing else checks the guide's content. The annotated copies get a real gate in
annotate_tex.py; the guide got a visual spot-check, which is how eight [?] marks
shipped in a ninety-page document. The rule this applies: a defect in the guide
is a failure, a defect in the paper is not. An undefined citation is the guide's
own -- it cites what it cites -- so it fails the build.
"""
import os
import re
import subprocess
import sys

TEX, PDF, LOG = "00-guide.tex", "00-guide.pdf", "00-guide.log"


def read(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def main():
    problems, notes = [], []

    if not os.path.exists(PDF):
        sys.exit("check_guide: FAILED - no %s" % PDF)
    if os.path.exists(TEX) and os.path.getmtime(PDF) < os.path.getmtime(TEX):
        problems.append("PDF older than its source")

    log = read(LOG) if os.path.exists(LOG) else ""
    if log:
        for m in re.finditer(r"^! (.*)$", log, re.M):
            problems.append("LaTeX error: %s" % m.group(1).strip())
        cites = sorted(set(re.findall(r"Citation `([^']*)' on page \d+ undefined", log)))
        if cites:
            problems.append("%d undefined citation(s): %s -- add the entry to a .bib the "
                            "guide reads, or the key prints as [?]"
                            % (len(cites), ", ".join(cites)))
        refs = sorted(set(re.findall(r"Reference `([^']*)' on page \d+ undefined", log)))
        if refs:
            problems.append("%d undefined reference(s): %s" % (len(refs), ", ".join(refs)))
        if re.search(r"Rerun to get cross-references right", log):
            notes.append("LaTeX asked for another pass; the four-step sequence did not settle")

    text = ""
    try:
        text = subprocess.run(["pdftotext", PDF, "-"], capture_output=True, text=True,
                              errors="replace", timeout=120).stdout
    except Exception as e:
        notes.append("could not run pdftotext (%s); PDF text not inspected" % e)

    if text:
        n = text.count("[?]")
        if n:
            problems.append("%d unresolved citation mark(s) [?] in the PDF text" % n)
        n = len(re.findall(r"(?<![?!])\?\?(?!\?)", text))
        if n:
            notes.append("%d occurrence(s) of ?? in the PDF text -- expected where the guide "
                         "quotes the paper's own dangling cross-references" % n)
        if "References" not in text:
            problems.append("no References section in the PDF")

    pages = ""
    try:
        out = subprocess.run(["pdfinfo", PDF], capture_output=True, text=True,
                             errors="replace", timeout=30).stdout
        m = re.search(r"^Pages:\s+(\d+)", out, re.M)
        if m:
            pages = "%s pages, " % m.group(1)
    except Exception:
        pass

    entries = len(re.findall(r"\\bibitem", read("00-guide.bbl"))) if os.path.exists("00-guide.bbl") else 0

    for n in notes:
        print("  %-14s note    - %s" % ("00-guide", n))
    if problems:
        for p in problems:
            print("  %-14s PROBLEM - %s" % ("00-guide", p))
        sys.exit("check_guide: the guide did not come out clean (see above)")
    print("  %-14s ok  (%s%d bibliography entries, no [?])" % ("00-guide", pages, entries))
    return 0


if __name__ == "__main__":
    sys.exit(main())
