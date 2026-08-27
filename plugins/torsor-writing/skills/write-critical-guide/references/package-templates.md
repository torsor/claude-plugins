# Package templates

Drop-in files for the `critical-guide/` directory. All four are proven on real packages; adapt the
marked fields and leave the rest alone.

---

## `Makefile`

Rebuilds everything from the ledger. `regen` runs first so the annotated sources are always
current with `issues.yaml` — never edit an `annotated-*.tex` by hand, since the next `make`
overwrites it.

```makefile
# Critical-guide package for <IDENTIFIER>

DOCS := $(basename $(notdir $(wildcard annotated-*.tex)))
PDFS := $(addsuffix .pdf,$(DOCS))
MD   := 01-summary.md 02-issues.md

.PHONY: all clean distclean regen guide check

all: regen guide annotated

# --- anchors must resolve before anything else is built ---
check:
	python3 annotate_tex.py check -v

# --- generated from the ledger: issue list + annotated sources ---
regen:
	python3 annotate_tex.py all --clean-aux -l issues.yaml -o .

# --- the guide: the two markdown documents as one PDF ---
guide: 00-guide.pdf

00-guide.pdf: $(MD) guide-meta.yaml guide-preamble.tex
	{ cat guide-meta.yaml; echo; cat 01-summary.md; \
	  printf '\n\n\\clearpage\n\n'; cat 02-issues.md; } > .guide-combined.md
	pandoc .guide-combined.md \
	  --pdf-engine=pdflatex \
	  --include-in-header=guide-preamble.tex \
	  -o $@
	@rm -f .guide-combined.md
	@echo "built $@"

# --- the annotated copies of the paper ---
# Delegated to the tool, which runs the pass sequence that converges and then
# verifies the result. A bare `pdflatex` rule here would report success on a PDF
# whose every cross-reference reads `??`.
annotated:
	python3 annotate_tex.py build -l issues.yaml -o .

clean:
	rm -f *.aux *.log *.out *.toc *.bbl *.blg *.tdo *.brf *.fls *.fdb_latexmk
	rm -f *.build.log .guide-combined.md
	rm -rf __pycache__

distclean: clean
	rm -f $(PDFS) 00-guide.pdf annotated-*.tex 02-issues.md
```

The `annotated` target defers to `annotate_tex.py build`, which runs `pdflatex` three times
with `bibtex` between and then checks the log, the note count, and the timestamps. That is not
superstition: one pass leaves every cross-reference as `??`, and both `make` and `latexd` exit
0 on a failed run. If the paper ships a `.bib`, copy it in beside the annotated sources.

---

## `guide-preamble.tex`

Pandoc header for `00-guide.pdf`. Change only the running-head title.

```latex
% Preamble for the combined critical guide (pandoc -> pdflatex).
\usepackage{amsmath,amssymb}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{array}
\usepackage{ragged2e}
\usepackage{xcolor}
\usepackage{titlesec}
\usepackage{fancyhdr}
\usepackage{etoolbox}

\definecolor{rule}{HTML}{B8B0A0}
\definecolor{head}{HTML}{2A2620}
\definecolor{soft}{HTML}{5A5348}

% Headings
\titleformat{\section}{\normalfont\Large\bfseries\color{head}}{\thesection}{0.6em}{}
  [\vspace{-0.4em}{\color{rule}\titlerule[0.5pt]}]
\titleformat{\subsection}{\normalfont\large\bfseries\color{head}}{\thesubsection}{0.6em}{}
\titleformat{\subsubsection}{\normalfont\normalsize\bfseries\color{soft}}{\thesubsubsection}{0.6em}{}
\titlespacing*{\section}{0pt}{2.4ex plus 1ex minus .2ex}{1.2ex}

% Running head  <-- CHANGE THE TITLE (keep the "guide to" wording)
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\itshape\color{soft} A critical guide to \emph{<SHORT TITLE>}}
\fancyhead[R]{\small\color{soft}\thepage}
\renewcommand{\headrulewidth}{0pt}
\fancypagestyle{plain}{\fancyhf{}\fancyfoot[C]{\small\color{soft}\thepage}%
  \renewcommand{\headrulewidth}{0pt}}

% Tables: let long cells wrap, and keep them inside the text block
\setlength{\tabcolsep}{5pt}
\renewcommand{\arraystretch}{1.15}
\AtBeginEnvironment{longtable}{\small\RaggedRight}

% Block quotes a little tighter and set off
\renewenvironment{quote}
  {\begin{list}{}{\leftmargin1.2em\rightmargin1.2em\topsep0.6em}\item\relax\itshape\color{soft}}
  {\end{list}}
```

`\AtBeginEnvironment{longtable}{\small\RaggedRight}` is what keeps a typographical table with
long "suggested wording" cells inside the text block. Without it the table overflows the
margin, which the log does not report.

---

## `guide-meta.yaml`

```yaml
---
title: "A critical guide to *<PAPER TITLE>*"
subtitle: "<IDENTIFIER> --- <AUTHORS>"
date: "<DATE>"
lang: en
geometry:
  - top=1.1in
  - bottom=1.1in
  - left=1.2in
  - right=1.2in
fontsize: 11pt
linestretch: 1.06
colorlinks: true
linkcolor: black
urlcolor: "[HTML]{9A5230}"
toc: true
toc-depth: 2
numbersections: false
---
```

No `mainfont` / `sansfont` / `monofont` keys — those are XeTeX and LuaTeX only, and this builds
with `pdflatex`.

Because the metadata carries the title, `01-summary.md` must not repeat it as its own first
heading. Open it with the section heading instead — "Summary, context, and significance".

---

## `README.md`

```markdown
# A critical guide to *<TITLE>* (<IDENTIFIER>)

Working material for assessing and evaluating this paper. It is **not a formal evaluation**: it carries no
recommendation and reaches no disposition. It is the examination — the paper read closely, its
context established, everything questionable found, located, and verified, with repairs where
they exist — for a critical reader to work from in writing their own report and reaching their own
judgment.

| File | What it is |
|---|---|
| `00-guide.pdf` | **The guide itself** — `01-summary.md` and `02-issues.md` set as one typeset document. Start here. |
| `01-summary.md` | The work, its context, and an assessment of the contribution, ending with the findings and the scope of what was checked. |
| `02-issues.md` | Every issue, point by point, grouped **A. Mathematical**, **B. References**, **C. Typographical/editorial**, each graded *major / minor / trivial*. This is the master list; the tags used here are the tags used everywhere. |
| `03-repairs.md` | Repairs for the issues that have a clear route. |
| `issues.yaml` | The ledger. `02-issues.md` and the annotated sources are generated from it — edit here, not there. |
| `annotated-mathematical.pdf` | The paper's own source with the <N> mathematical notes inserted as `\todo[inline]` (pink). |
| `annotated-references.pdf` | Same, with the <N> reference notes (green). |
| `annotated-typographical.pdf` | Same, with the <N> typographical and editorial notes (blue). |

Each annotated document opens with an index of its own notes, in tag order, and is otherwise
**byte-for-byte the authors' source** apart from the inserted notes and one changed
`todonotes` option.

## Rebuilding

    make          # everything
    make check    # verify every annotation anchor still matches the source
    make guide    # just 00-guide.pdf
    make clean    # remove build artifacts
    make distclean # also remove generated PDFs, .tex, and 02-issues.md

Two constraints if you edit the Markdown: bare LaTeX macros outside math (a `\Cref{...}`
quoted from the paper) must be wrapped in backticks, or pandoc hands them to an engine that
has never heard of them; and the build uses `pdflatex` rather than `lualatex`, which is an
order of magnitude faster here and handles every non-ASCII character the guide uses.

<!-- CASE B ONLY — delete if the annotation base is the submitted text -->
## A note on the source

The submission supplied here is a PDF rather than the authors' `.tex`. For the annotated
copies, the corresponding public source (<SOURCE>) was used as the base text. Each
`\todo[inline]` is placed directly after the passage it applies to, after checking that the
same statement, formula, or reference occurs in the submitted PDF. <DESCRIBE ANY DIFFERENCE
BETWEEN THE TWO VERSIONS>; no comment relies on that difference.

Page and line locations in the Markdown documents refer to the submitted PDF. The inline notes
instead follow the actual source passage, as is appropriate for a copy intended for revision.
<!-- END CASE B -->
```

Where a cover sheet is prepended by the submission system, say which numbering you used:
"manuscript p. N" is the printed page; "PDF p. N" includes the cover sheet and is one greater.
