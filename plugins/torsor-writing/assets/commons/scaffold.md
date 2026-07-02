# Shared scaffold — directory, Makefile, preamble, build

Every torsor book — manual, paper guide, topic guide, study guide — is scaffolded the
same way. This file is the single source for the mechanics; the per-genre SKILL.md
supplies only what varies (chapter list, title page, EPUB title). When a skill says
"scaffold per the commons," it means this file, followed exactly.

Placeholders used below: `<doc-dir>` (the manual/ or guide/ directory), `<Title>` (the
EPUB/PDF title the skill specifies), `<genre comment>` (one line for the Makefile
header, e.g. "thing manual" or "Gross–Zagier reading guide").

## Directory layout

```
<doc-dir>/
  .gitignore
  Makefile
  check-build.py      ← copied from the plugin (see "Vendored tools" below)
  latex/
    main.tex
    STYLE.md          ← base + chosen voice, assembled (records the voice)
    chapters/         ← per-genre chapter files, from the skill
  tex2torsor/         ← copied from the plugin
  html/               ← build output, not created yet
  epub/               ← build output, not created yet
  markdown/           ← build output, not created yet
```

Genre additions (the skill says when): `latex/reader-profile.md` for calibrated guides,
`source-notes/` beside `latex/` for topic guides.

## .gitignore

Create this file at `<doc-dir>/.gitignore`:

```gitignore
# Built outputs
html/
epub/
markdown/

# LaTeX PDF output
latex/main.pdf

# LaTeX intermediate artifacts (if built without latexd)
latex/*.aux
latex/*.log
latex/*.out
latex/*.toc
latex/*.fls
latex/*.fdb_latexmk
latex/*.synctex.gz
latex/chapters/*.aux

# macOS
.DS_Store
```

## Makefile

Use this exact pattern — `latexd` for PDF, tex2torsor for HTML, pandoc for EPUB and
Markdown, `lab-view` for preview, `check-build.py` for verification:

```makefile
# <genre comment>
#
# PDF:  latexd (wrapper around latexmk — keeps build artifacts out of source tree;
#         falls back to plain latexmk when latexd isn't on PATH)
# HTML: tex2torsor (Python converter)
# EPUB: pandoc (directly from LaTeX source)
# MD:   pandoc → GitHub-Flavored Markdown (directly from LaTeX source)
#
# tex2torsor resolve order:
#   1. TEX2TORSOR_ROOT=/path/to/dir
#   2. ./tex2torsor  (symlink or copy inside this directory)
#   3. ../tex2torsor  (sibling of this directory)
#   4. ../../tex2torsor

PYTHON    ?= python3
LATEX_DIR := latex
HTML_DIR  := html
EPUB_DIR  := epub
EPUB_OUT  := $(EPUB_DIR)/manual.epub
MD_DIR    := markdown
MD_OUT    := $(MD_DIR)/manual.md

.PHONY: html pdf epub md check view clean help

help:
	@echo "Targets:"
	@echo "  make pdf    — build latex/main.pdf via latexd (or latexmk if latexd absent)"
	@echo "  make html   — build html/manual.html via tex2torsor"
	@echo "  make epub   — build epub/manual.epub via pandoc"
	@echo "  make md     — build markdown/manual.md via pandoc (GitHub-Flavored Markdown)"
	@echo "  make check  — run check-build.py (log scan, freshness, format checks)"
	@echo "  make view   — build html (if needed) and open in lab-view"
	@echo "  make clean  — remove html/, epub/, and markdown/ output"

# latexd keeps build artifacts out of the source tree. On hosts without it,
# fall back to plain latexmk (leaves aux files in latex/ — already gitignored).
pdf:
	@if command -v latexd >/dev/null 2>&1; then \
	  latexd $(LATEX_DIR)/main.tex; \
	else \
	  echo "latexd not on PATH — falling back to latexmk"; \
	  latexmk -pdf -interaction=nonstopmode -halt-on-error -cd $(LATEX_DIR)/main.tex; \
	fi

epub:
	mkdir -p $(EPUB_DIR)
	cd $(LATEX_DIR) && pandoc main.tex \
	  --toc \
	  --split-level=1 \
	  --metadata title="<Title>" \
	  --metadata author="torsor lab" \
	  -o ../$(EPUB_OUT)

md:
	mkdir -p $(MD_DIR)
	cd $(LATEX_DIR) && pandoc main.tex \
	  --toc \
	  -t gfm \
	  -o ../$(MD_OUT)

html:
	@set -e; \
	MANUAL="$(CURDIR)"; \
	REPO="$$(cd "$$MANUAL/.." && pwd)"; \
	PARENT="$$(cd "$$MANUAL/../.." && pwd)"; \
	if [ -n "$(strip $(TEX2TORSOR_ROOT))" ]; then \
	  T2T_ROOT="$(TEX2TORSOR_ROOT)"; \
	elif [ -f "$$MANUAL/tex2torsor/tex2torsor.py" ]; then \
	  T2T_ROOT="$$MANUAL/tex2torsor"; \
	elif [ -f "$$REPO/tex2torsor/tex2torsor.py" ]; then \
	  T2T_ROOT="$$REPO/tex2torsor"; \
	elif [ -f "$$PARENT/tex2torsor/tex2torsor.py" ]; then \
	  T2T_ROOT="$$PARENT/tex2torsor"; \
	else \
	  echo >&2 "tex2torsor not found."; \
	  echo >&2 "Pass the directory containing tex2torsor.py:"; \
	  echo >&2 "  make TEX2TORSOR_ROOT=/path/to/tex2torsor html"; \
	  exit 1; \
	fi; \
	T2T="$$T2T_ROOT/tex2torsor.py"; \
	CSS_DIR="$$T2T_ROOT/css"; \
	mkdir -p $(HTML_DIR); \
	$(PYTHON) "$$T2T" $(LATEX_DIR)/main.tex \
	  -o $(HTML_DIR)/manual.html \
	  --css tokens.css \
	  --css manual.css; \
	cp "$$CSS_DIR/tokens.css" $(HTML_DIR)/tokens.css; \
	cp "$$CSS_DIR/manual.css" $(HTML_DIR)/manual.css

check:
	$(PYTHON) check-build.py

view: html
	lab-view $(HTML_DIR)/manual.html &

clean:
	rm -rf $(HTML_DIR) $(EPUB_DIR) $(MD_DIR)
```

**EPUB/MD note:** pandoc resolves `\input` relative to its working directory, not the
source file, so the `epub` and `md` targets must `cd $(LATEX_DIR)` before invoking
pandoc and use `../$(EPUB_OUT)` / `../$(MD_OUT)` as the output path.

**PDF note:** `latexd` is a local lab tool and isn't on most systems. The `pdf` target
checks for it and falls back to plain `latexmk`, so the build works out of the box; the
fallback leaves aux files in `latex/` (already gitignored).

## main.tex preamble

Use the **shelf manual's `main.tex`** as the verbatim template for the preamble
(`${CLAUDE_PLUGIN_ROOT}/assets/reference/shelf-main.tex`). It embeds the full Solarized
Cézanne palette, Garamond/Cabin fonts, titlesec part/chapter/section formatting,
fancyhdr setup, mdframed `notebox`/`warnbox`, the `\code{}` macro, and the `lstlisting`
style — all calibrated together.

Replace only these document-specific fields:

- `pdftitle` in `\hypersetup`; keep `pdfauthor` as `torsor lab`
- the content inside `\begin{titlepage}...\end{titlepage}` (the skill supplies the
  genre's title page)
- the `\input{chapters/...}` lines in the main matter, and `\part{...}` labels if used

Do **not** alter the color palette, fonts, titlesec definitions, box styles, or
`\code{}` macro without the user's agreement — these are the family-wide design
constants.

### Colophon — keep verbatim

Immediately after `\end{titlepage}`, every document in the family carries the
inner-cover (colophon) page — `torsor lab` over the terracotta `torsor.org` link,
bottom-aligned on an otherwise blank page. Do **not** edit the attribution or the URL,
and do not move it:

```latex
% Colophon — inner cover (verso of the title page)
\thispagestyle{empty}
\null\vfill
\begin{center}
  {\small\color{inkmuted} torsor lab\par}
  \vspace{0.4em}
  {\small\href{https://torsor.org}{\color{terracotta} torsor.org}}
\end{center}
\clearpage
```

### Math block (documents about mathematics)

Paper guides, topic guides, and study guides — and any manual that needs real
mathematics — add this to the preamble after the existing packages, removing nothing:

```latex
% --- Mathematics ---
\usepackage{amsmath}
\usepackage{amsthm}
\usepackage{mathtools}

% Theorem-like environments, styled to match the palette.
% Used to restate a source's results faithfully — always cite the source's own number.
\newtheoremstyle{guide}%
  {\topsep}{\topsep}%
  {\itshape}%            body font
  {0pt}%                 indent
  {\sffamily\color{inkdark}\bfseries}% head font
  {.}%                   punctuation after head
  {.5em}%                space after head
  {}%
\theoremstyle{guide}
\newtheorem*{paperthm}{Theorem}      % restate as: \begin{paperthm}[Thm 4.2 of the paper] ...
\newtheorem*{paperdefn}{Definition}
\newtheorem*{paperlem}{Lemma}
\newtheorem*{paperprop}{Proposition}

% A callout for the subtlety that actually trips readers — the unstated hypothesis,
% the index that shifts, the "obvious" step that isn't. Terracotta like warnbox,
% but semantically "read carefully," not "data loss."
\newmdenv[
  backgroundcolor=warnbg,
  linecolor=terracotta,
  linewidth=1.5pt,
  innerleftmargin=10pt,
  innerrightmargin=10pt,
  innertopmargin=8pt,
  innerbottommargin=8pt,
  skipabove=10pt,
  skipbelow=10pt,
]{pitfallbox}
```

When restating a source's result, carry its own number in the optional argument
(`\begin{paperthm}[Theorem 4.2, slightly informally]`) so the reader can always
cross-check against the source. If `pitfallbox` is used, HTML needs the callout mapping
— see `${CLAUDE_PLUGIN_ROOT}/assets/commons/lessons.md`.

## STYLE.md

Assemble the document's effective style guide into `latex/STYLE.md` by concatenating
the base mechanics and the chosen voice, with a header recording which voice was used.
The skill names the base file (`base-manual.md` or `base-paper-guide.md`); the default
voice is `01-direct`:

```
PROSE=${CLAUDE_PLUGIN_ROOT}/assets/prose
{ echo "<!-- Voice: 01-direct. Assembled from torsor-style/prose. -->"; echo; \
  cat "$PROSE/<base>.md"; echo; cat "$PROSE/voices/01-direct.md"; } \
  > <doc-dir>/latex/STYLE.md
```

Substitute the chosen voice file if it isn't `01-direct`. This keeps the document
self-contained and records which voice it was written in.

## Vendored tools

**Copy** both tools into the document directory (don't symlink) so it stays a
self-contained deliverable that survives plugin updates or uninstalls:

```bash
cp -R ${CLAUDE_PLUGIN_ROOT}/tools/tex2torsor <doc-dir>/tex2torsor
cp ${CLAUDE_PLUGIN_ROOT}/tools/check-build.py <doc-dir>/check-build.py
```

The Makefile's `html` target also accepts
`make TEX2TORSOR_ROOT=${CLAUDE_PLUGIN_ROOT}/tools/tex2torsor html` if you'd rather not
copy tex2torsor in.

## Verifying the build

Once the preface and at least one chapter exist, build all four formats — the Markdown
export is part of the standard deliverable, not an optional extra:

```
cd <doc-dir> && make pdf && make html && make epub && make md
```

Then run `make check` and fix what it reports. Common issues:

- `latexd` not installed or not on PATH — it's a lab tool, absent on most systems; the
  `pdf` target falls back to `latexmk`, so this only bites if `latexmk` is also missing.
- **`latexd` exits 0 even when LaTeX fails** — never trust the exit code; `make check`
  verifies the PDF is real and fresh. On failure, read `latex/main.log`.
- Missing LaTeX packages (install via tlmgr); the math block needs `amsmath`, `amsthm`,
  `mathtools`.
- Non-ASCII characters inside `lstlisting` blocks — the listings package rejects them;
  use ASCII equivalents (`->` not `→`). Display/inline math is unaffected.
- tex2torsor / pandoc math handling — heavy math needs the workarounds in
  `${CLAUDE_PLUGIN_ROOT}/assets/commons/lessons.md` (MathML for EPUB, MathJax injection
  for HTML, renderable-notation substitutions).
- Pandoc not installed (needed by tex2torsor for HTML, and directly for EPUB/Markdown).
- Path issues — the epub and md targets must `cd` into `latex/` before calling pandoc.

The build is not done until the **publication pass** has run — see
`${CLAUDE_PLUGIN_ROOT}/assets/commons/publication.md`.
