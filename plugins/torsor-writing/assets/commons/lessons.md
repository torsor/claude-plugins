# Family lessons — apply only when a document needs them

Situational fixes learned from real manuals and guides, family-wide. The per-genre
SKILL.md files stay generic; reach for these when the specific document or toolchain
hits the problem they solve. Not every document needs them.

---

## General gotcha (applies always, every genre)

**`latexd` exits 0 even when LaTeX fails.** `make pdf && echo ok` can lie. `make check`
(check-build.py) automates the detection — it verifies the PDF exists, is newer than the
sources, and that the log is free of errors and undefined references. If you're on a
tree without check-build.py, verify by hand:

- `pdfinfo latex/main.pdf` → page count should be sane (not 1 when you wrote 40).
- The PDF's mtime should be newer than `main.tex`.
- If either is off, the build failed silently — read `latex/main.log` for the real error.

**A long document written in one message is lost entirely.** An agent that composes a whole
chapter, report, or sweep in a single reply and writes it at the end hits the output cap
mid-message and dies having written **nothing** — not a truncated file, no file. The work is
gone and the run has to start over.

Write incrementally instead: create the file early, then append a section at a time. A run cut
short then still leaves everything produced up to that point, and the next pass continues
rather than restarts. This matters most for the pieces with no natural break — a long prose
chapter, a subagent's sweep over a big paper, a summary written straight through — and it
applies to any subagent you dispatch, so put it in the brief rather than assuming it.

**You have no clock, and a number in your context is not a measurement.** Asked how long a
run took, an agent cannot observe the answer and will supply a plausible one. The observed
failure is sharper than invention: a report said "about two hours" because the document's own
README recorded `2 h 7 m` for an *earlier, different* run, that string sat in context all
session, and it came back out as a self-measurement. File mtimes giving the true answer — 41
minutes — were available the whole time and were never consulted.

So: **measure, or say you did not.** Stamp `date -Is` into the log at each phase boundary as
you pass it, or read the mtimes of your own outputs at the end. Never report a duration, a
token count, or a cost you did not read off something. If a figure comes from elsewhere, name
where — "the guide's README records 2 h 7 m for that run" is useful; the same number offered as
your own is not.

**An append to a file that isn't there is silent, and the shell's directory can move under
you.** The incremental-write rule above has one failure mode, and it is nasty. Some tool calls
reset the working directory without saying so. The next `cat >> notes.md` then creates a
*second* `notes.md` one level up, reports nothing, and exits 0 — and reading the file back
looks exactly like having lost six hundred lines of work. Nothing is lost; it is in the other
file.

Two habits prevent it: **append by absolute path**, and check that a file you are appending to
already exists rather than trusting `>>` to tell you. If a file you have been writing to
suddenly looks truncated, look one directory up before concluding anything.

**Verify numbering from `.aux`, not from extracted text.** Comparing two builds of the same
document by scraping `pdftotext` output produces false divergences: a repair that changes a
sentence's length reflows the paragraph, so which statements begin a line differs between
builds even when every number is identical. `\newlabel` entries in the `.aux` files are the
reliable comparison — they carry the actual values.

**Shares of effort are not shares of the clock, and a table implies a partition.** Where work
runs in parallel — a fan-out of subagents while the main thread drafts — wall time and effort
diverge, and the categories overlap. Rows that sum to 100% in a table read as a decomposition
of elapsed time. If they are neither exhaustive nor disjoint, say so in the caption, or do not
use a table.

---

## Heavy-math documents: HTML/EPUB rendering

**The PDF is the source of truth.** The HTML/EPUB math path (tex2torsor + pandoc's
built-in converter) cannot render: over-accents (`\widetilde`, `\overline`), `\frac`,
extensible/labelled arrows (`\xrightarrow`, `\varinjlim`), or `array`/`aligned` (so:
commutative diagrams). The PDF via `latexd` renders everything; the other two formats
need help.

Handle it **without changing the shared `tex2torsor`** — keep the workaround local to
the document:

### 1. EPUB → pandoc `--mathml`

Add `--mathml` to the `epub` target's pandoc call. Produces native, clean MathML.

```makefile
	cd $(LATEX_DIR) && pandoc main.tex \
	  --toc \
	  --split-level=1 \
	  --mathml \
	  --metadata title="..." \
	  --metadata author="torsor lab" \
	  -o ../$(EPUB_OUT)
```

### 2. HTML → inject MathJax to render the converter's TeX fallback

tex2torsor emits raw TeX in `<span class="math …">$…$</span>` for anything it can't
convert. MathJax renders exactly those. Add a post-step to the `html` target:

```makefile
	$(PYTHON) inject-mathjax.py $(HTML_DIR)/manual.html
```

`inject-mathjax.py` (drop at the document root — idempotent, no external deps at build
time):

```python
#!/usr/bin/env python3
"""Inject a MathJax loader into a tex2torsor-generated HTML file.

tex2torsor falls back to raw TeX in <span class="math ...">$...$</span> for math it
can't convert (commutative diagrams, fractions, over-accents). MathJax renders those
fallback spans so HTML matches the PDF/EPUB. Idempotent; safe to run repeatedly.
"""
import sys

SCRIPT = (
    '<script>window.MathJax={tex:{'
    'inlineMath:[["$","$"],["\\\\(","\\\\)"]],'
    'displayMath:[["$$","$$"],["\\\\[","\\\\]"]]}};</script>\n'
    '<script id="MathJax-script" async '
    'src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>\n'
)


def main(path: str) -> None:
    with open(path, encoding="utf-8") as f:
        html = f.read()
    if "MathJax-script" in html:
        return
    html = html.replace("</head>", SCRIPT + "</head>", 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    main(sys.argv[1])
```

### 3. Prefer renderable notation in the source

Where even MathJax/MathML would be awkward, write a renderable equivalent in the LaTeX
and note the source's own glyph at first mention and in the appendix:

- absolute integral closure → a plain macro like `\mathcal{O}^{\mathrm{ic}}` (source: `\widetilde{\mathcal{O}}`)
- filtered colimit/limit → `\operatorname{colim}` / `\lim` (not `\varinjlim`/`\varprojlim`)
- isomorphism → `\cong` (not `\xrightarrow{\sim}`)

This keeps all three formats identical and dependency-free, at the cost of restating
the source's exact glyphs once in prose.

---

## Math preamble additions (when the document needs them)

The commons math block already adds `amsmath`, `amsthm`, `mathtools`, theorem
environments, and `pitfallbox` (see `scaffold.md`). Add these when the source material
calls for them:

```latex
\usepackage{mathrsfs}   % \mathscr — sheaf/script notation
\usepackage{array}      % wrapping table columns (if the preamble doesn't already load it)
\newtheorem*{papercor}{Corollary}   % if the source has corollaries to restate
```

---

## HTML callout mapping for `pitfallbox`

If the document uses `pitfallbox` (or any non-default callout), tex2torsor needs to be
told how to render it, or it's dropped in HTML. Pass a mappings file to the `html`
target with `-c $(LATEX_DIR)/tex2torsor-mappings.yaml`:

```yaml
# Extends the shared default with the document's extra callout.
mappings:
  environments:
    notebox:
      classes: [callout, callout-note]
      label: "Note"
    warnbox:
      classes: [callout, callout-warn]
      label: "Warning"
    pitfallbox:
      classes: [callout, callout-warn]
      label: "Watch out"
  macros:
    code:
      html_tag: code
      classes: []
css: []
```
