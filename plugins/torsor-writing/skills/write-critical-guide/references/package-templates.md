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

.PHONY: all clean distclean regen guide check annotated
.NOTPARALLEL:

all: regen guide annotated

# --- anchors must resolve before anything else is built ---
check:
	python3 annotate_tex.py check -v

# --- generated from the ledger: issue list + annotated sources ---
# `annotate` and `issues-md`, not `all`: `all` would also run a three-pass
# pdflatex that the `annotated` target below has to redo from scratch, and
# three passes do not always converge (see that target's comment).
regen:
	python3 annotate_tex.py check -l issues.yaml -o .
	python3 annotate_tex.py annotate -l issues.yaml -o .
	python3 annotate_tex.py issues-md -l issues.yaml -o .

# --- the guide: the markdown documents as one PDF ---
#
# Four steps, not one. The guide quotes the paper, so it inherits the paper's
# citations: quoted passages carry the author's own \cite calls. Resolving them
# needs a bibliography, and a bibliography needs bibtex between pdflatex passes
# -- which `pandoc --pdf-engine` cannot do, since it invokes the engine once.
# So pandoc writes 00-guide.tex and the same sequence annotate_tex.py runs for
# the annotated copies is run here, against the same .bib.
guide: 00-guide.pdf

00-guide.pdf: 01-summary.md 02-issues.md guide-meta.yaml guide-preamble.tex \
              guide-bibliography.tex <BIB>.bib
	{ cat guide-meta.yaml; echo; cat 01-summary.md; \
	  printf '\n\n\\clearpage\n\n'; cat 02-issues.md; } > .guide-combined.md
	pandoc .guide-combined.md --standalone \
	  --pdf-engine=pdflatex \
	  --include-in-header=guide-preamble.tex \
	  --include-after-body=guide-bibliography.tex \
	  -o 00-guide.tex
	pdflatex -interaction=nonstopmode 00-guide.tex >/dev/null 2>&1 || true
	bibtex  00-guide                 >/dev/null 2>&1 || true
	pdflatex -interaction=nonstopmode 00-guide.tex >/dev/null 2>&1 || true
	pdflatex -interaction=nonstopmode 00-guide.tex >/dev/null 2>&1 || true
	@python3 check_guide.py

# --- the annotated copies of the paper ---
# Delegated to the tool, which runs the pass sequence and then verifies the
# result. A bare `pdflatex` rule here would report success on a PDF whose every
# cross-reference reads `??`.
#
# Run `build` twice where the paper's numbering is self-referential -- mathtools
# `showonlyrefs` with keytheorems `sharenumber=equation` is the case in hand,
# where statement numbers depend on which equations the previous pass referenced
# and six passes are needed, not three. Each `build` runs three. Drop the second
# line when a single `build` reports no undefined references.
annotated: regen
	python3 annotate_tex.py build --clean-aux -l issues.yaml -o .
	python3 annotate_tex.py build -l issues.yaml -o .

clean:
	rm -f *.aux *.log *.out *.toc *.bbl *.blg *.tdo *.brf *.fls *.fdb_latexmk
	rm -f *.build.log .guide-combined.md 00-guide.tex
	rm -rf __pycache__

distclean: clean
	rm -f $(PDFS) 00-guide.pdf 00-guide.tex annotated-*.tex 02-issues.md
```

Both build paths verify their output rather than trusting an exit status, and both apply the
same rule: **a defect in the package fails the build; a defect in the paper does not.** An
undefined citation in the guide is the guide's own, since the guide cites what it cites, so it
fails. A cross-reference the paper itself leaves dangling is reported as a note and passes —
it prints `??` in the author's PDF too, and it is a finding, not a build error. Getting this
backwards is how a `make` that has never once run to completion ships as a package's
documented rebuild path.

---

## `guide-bibliography.tex`

Fed to pandoc with `--include-after-body`, so it lands just before `\end{document}`. Match the
paper's own `\bibliographystyle` — read it out of the source — so a quoted citation prints the
label the paper prints.

```latex
\bibliographystyle{<THE PAPER'S STYLE, e.g. amsalpha>}
\bibliography{<BIB>,guide-extra}
```

`<BIB>.bib` is the paper's bibliography. If the folder does not supply one, reconstruct it from
the References of the submitted PDF and say so in the README: the labels in every built
document derive from that reconstruction, and it is build support, not the author's file.

`guide-extra.bib` holds works the **guide** cites that the paper's bibliography does not, kept
separate so the reconstruction stays what it claims to be. The case that puts entries here is
worth knowing in advance: quoting another paper's prose brings that paper's citation keys with
it, and they will not resolve against this paper's bibliography.

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

Two more blocks belong in this file, and both exist because the guide sets quoted manuscript
prose as **real LaTeX** rather than as a code span — that is deliberate, so the mathematics
inside a quotation typesets, and it is what makes the rest of this necessary.

**A compatibility block for the paper's own macros.** Every macro that can reach a quoted
passage needs a definition here: the paper's own where it gives one, a faithful stand-in where
it builds the macro with a package this document does not load. Build it by compiling and
fixing what errors — but do not stop when the errors stop. Macros that *warn* rather than
error, `\cite` above all, will pass straight through that loop and print as `[?]` in a
document nobody rereads at ninety pages. Grep the built PDF's text, which is what
`check_guide.py` does.

```latex
% every manuscript macro that can appear inside a quotation
\providecommand{\kk}{\Bbbk}
\providecommand{\vac}{\mathbf{1}}
\DeclareMathOperator{\Aut}{Aut}
% ... and stand-ins for what cannot be reproduced, rendered as what they print
\providecommand{\zcref}[2][]{\textup{(ref)}}
\providecommand{\<AUTHOR MARKER MACRO>}[1]{\textup{[<NAME>: #1]}}
```

**Bibliography support the article class does not supply.** `amsalpha` and its relatives emit
these; without them the four-step build fails in the bibliography rather than in the body,
which is a confusing place to land.

```latex
\providecommand{\bysame}{\leavevmode\hbox to3em{\hrulefill}\thinspace}
\providecommand{\MR}[1]{}
\providecommand{\MRhref}[2]{#2}
```

`\bysame` is not optional whenever two cited works share an author list, which in a guide to a
paper with a series behind it is the normal case.

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
# A critical guide to *<TITLE>*

<AUTHORS>, <IDENTIFIER>, <N> pp.

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

## What is in evidence

**The compiled PDF is the artifact.** Every finding here is about the paper as it prints. The
LaTeX source is used for exact quotation, for line locations, and to carry the annotations; it
is not a source of findings in its own right, and material that does not reach the compiled
page is out of scope. An author marker that a macro *renders* is a different matter — it
prints, so it is in evidence.

Locations give the source line, the paper's own section and statement numbers, and the PDF page.

## Rebuilding

    make          # everything
    make check    # verify every annotation anchor still matches the source
    make guide    # just 00-guide.pdf
    make clean    # remove build artifacts
    make distclean # also remove generated PDFs, .tex, and 02-issues.md

`make` must exit 0. If it does not, the package is not finished — a red gate is a bug to fix,
never a symptom to document in this README.

Three constraints if you edit the Markdown. Bare LaTeX macros outside math (a `\Cref{...}`
quoted from the paper) must be wrapped in backticks, or pandoc hands them to an engine that
has never heard of them. Quoted passages set as prose are the exception and are handled by the
compatibility block instead, since their mathematics has to typeset. And the build uses
`pdflatex` rather than `lualatex`, which is an order of magnitude faster here and handles
every non-ASCII character the guide uses.

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
