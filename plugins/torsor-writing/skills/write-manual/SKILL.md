---
name: write-manual
description: Create a styled user's manual for a project — LaTeX source with HTML, PDF, and EPUB output — following the torsor design and Scalzi-influenced prose style used in the thing manual.
argument-hint: [path or description of the project to document]
---

You are helping the user write a user's manual for a project. The manual will be a LaTeX book with matching HTML, PDF, and EPUB output, following the design and voice established in the *thing: A User's Manual*.

The user has said: $ARGUMENTS

If no project was specified, ask before proceeding.

---

## Reference materials — read these first

Before doing anything else, read:

1. **Style — base mechanics + the chosen voice.** A manual's style is composed from the
   torsor prose library: format mechanics plus one selectable voice. Read both, plus the
   voice catalog in the README:
   ```
   ${CLAUDE_PLUGIN_ROOT}/assets/prose/base-manual.md
   ${CLAUDE_PLUGIN_ROOT}/assets/prose/voices/01-direct.md
   ${CLAUDE_PLUGIN_ROOT}/assets/prose/README.md
   ```
   `01-direct` is the default, proven voice. Use it unless the user asks for another.

2. **Canonical manual template** — a snapshot of the shelf manual as the definitive worked
   example for layout and preamble. Read both:
   ```
   ${CLAUDE_PLUGIN_ROOT}/assets/reference/shelf-main.tex
   ${CLAUDE_PLUGIN_ROOT}/assets/reference/shelf-00-preface.tex
   ```
   `shelf-main.tex` is the full preamble + main matter; `shelf-00-preface.tex` is one chapter
   for prose rhythm. The canonical Makefile pattern is reproduced verbatim in Step 4 below.

3. **Visual style reference** — the artifacts document's LaTeX preamble establishes the
   Solarized Cézanne color palette and Garamond/Cabin typography used in all manuals:
   ```
   ${CLAUDE_PLUGIN_ROOT}/assets/reference/artifacts.tex
   ```
   (Read lines 1–110 — that's the whole preamble.)

4. **tex2torsor** — the LaTeX→HTML converter. Lives here:
   ```
   ${CLAUDE_PLUGIN_ROOT}/tools/tex2torsor/
   ```

---

## Step 1 — Understand the project

From the argument and by reading the project directory, identify:

- What the project *does* — its primary purpose, core concept, and main interface
- Who the audience is — power user? newcomer? general reader?
- What the key features or concepts are that need explaining
- What already exists as documentation (README, doc/ directory, inline --help text, existing guides)

Run:
```
ls <project-dir>
cat <project-dir>/README.md 2>/dev/null
ls <project-dir>/doc/ 2>/dev/null
```

If there's a `thing.yaml`, read it for the project description and tags.

---

## Step 2 — Find or confirm the manual location

Propose where the manual should live. The default is a `manual/` subdirectory of the project root. Confirm with the user before creating anything.

If a `manual/` directory already exists, inspect it and ask whether to work alongside existing content or start fresh.

---

## Step 3 — Propose a chapter outline

Design a chapter structure appropriate to the project. Every manual should have:

- **Preface** — Why does this exist? What problem does it solve? What's the honest pitch?
- **One "big idea" chapter** — The core concept in one clean explanation. Grounds the reader before details.
- **2–6 feature/workflow chapters** — One chapter per major area. Not a feature list; a narrative walk through each area.
- **Quick reference appendix** — Commands, flags, config fields — the exhaustive table the prose chapters deliberately avoid.
- **Afterword** (optional) — A short closing note in the same voice as the preface.

Adapt to the project. A small tool might need only three chapters. A complex system might need eight.

Present the proposed outline to the user and confirm before writing a word. Confirm the
**voice** at the same time — default to `01-direct`; if the user wants a different register
(e.g. the more digressive `02-wandering`), read that voice file in its place.

---

## Step 4 — Scaffold the directory

Once the outline is confirmed, create the manual directory structure:

```
manual/
  .gitignore
  Makefile
  latex/
    main.tex
    STYLE.md          ← base-manual + chosen voice, assembled (records the voice)
    chapters/
      00-preface.tex
      01-<chapter>.tex
      ...
      99-quick-reference.tex
  tex2torsor/         ← symlink to the envtools manual's tex2torsor
  html/               ← build output, not created yet
  epub/               ← build output, not created yet
```

### .gitignore

Create this file at `manual/.gitignore`:

```gitignore
# Built outputs
html/
epub/

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

### Makefile

Use this exact pattern — `latexd` for PDF, tex2torsor for HTML, pandoc for EPUB, `lab-view` for preview:

```makefile
# <project> manual
#
# PDF:  latexd (wrapper around latexmk — keeps build artifacts out of source tree)
# HTML: tex2torsor (Python converter)
# EPUB: pandoc (directly from LaTeX source)
#
# tex2torsor resolve order:
#   1. TEX2TORSOR_ROOT=/path/to/dir
#   2. ./tex2torsor  (symlink or copy inside this manual/ directory)
#   3. ../tex2torsor  (sibling of this directory)
#   4. ../../tex2torsor

PYTHON    ?= python3
LATEX_DIR := latex
HTML_DIR  := html
EPUB_DIR  := epub
EPUB_OUT  := $(EPUB_DIR)/manual.epub

.PHONY: html pdf epub view clean help

help:
	@echo "Targets:"
	@echo "  make pdf    — build latex/main.pdf via latexd"
	@echo "  make html   — build html/manual.html via tex2torsor"
	@echo "  make epub   — build epub/manual.epub via pandoc"
	@echo "  make view   — build html (if needed) and open in lab-view"
	@echo "  make clean  — remove html/ and epub/ output"

pdf:
	latexd $(LATEX_DIR)/main.tex

epub:
	mkdir -p $(EPUB_DIR)
	cd $(LATEX_DIR) && pandoc main.tex \
	  --toc \
	  --split-level=1 \
	  --metadata title="<Project Title>" \
	  --metadata author="torsor lab" \
	  -o ../$(EPUB_OUT)

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

view: html
	lab-view $(HTML_DIR)/manual.html &

clean:
	rm -rf $(HTML_DIR) $(EPUB_DIR)
```

**EPUB note:** pandoc resolves `\input` relative to its working directory, not the source file, so the epub target must `cd $(LATEX_DIR)` before invoking pandoc and use `../$(EPUB_OUT)` as the output path.

### main.tex preamble

Use the **shelf manual's `main.tex`** as the verbatim template for the preamble
(`${CLAUDE_PLUGIN_ROOT}/assets/reference/shelf-main.tex`).
It embeds the full Solarized Cézanne palette, Garamond/Cabin fonts, titlesec chapter/section/part
formatting, fancyhdr setup, mdframed callout boxes, and lstlisting style — all calibrated together.

Replace only these project-specific fields:
- `pdftitle` in `\hypersetup`; set `pdfauthor` to `torsor lab`
- The title-page content inside `\begin{titlepage}...\end{titlepage}`
- The `\input{chapters/...}` lines in the main matter
- `\part{...}` labels if the book uses parts

**Keep the colophon page verbatim.** Immediately after `\end{titlepage}`, the template
carries the inner-cover (colophon) page — `torsor lab` over the terracotta `torsor.org`
link, bottom-aligned on an otherwise blank page. This is a fixed family element: do **not**
edit the attribution or the URL, and do not move it. Every manual carries the same one.

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

Do **not** alter the color palette, fonts, titlesec definitions, box styles, or `\code{}` macro
without the user's agreement — these are the family-wide design constants.

### STYLE.md

Assemble the manual's effective style guide into `latex/STYLE.md` by concatenating the base
mechanics and the chosen voice, with a header recording which voice was used. From the
prose library:
```
PROSE=${CLAUDE_PLUGIN_ROOT}/assets/prose
{ echo "<!-- Voice: 01-direct (manual). Assembled from torsor-style/prose. -->"; echo; \
  cat "$PROSE/base-manual.md"; echo; cat "$PROSE/voices/01-direct.md"; } \
  > manual/latex/STYLE.md
```
Substitute the chosen voice file if it isn't `01-direct`. This keeps the manual
self-contained and records which voice it was written in.

### tex2torsor

The converter is vendored in this plugin. **Copy** it into the manual (don't symlink) so the
manual stays a self-contained deliverable that survives plugin updates or uninstalls:

```bash
cp -R ${CLAUDE_PLUGIN_ROOT}/tools/tex2torsor manual/tex2torsor
```

The Makefile's `html` target also accepts `make TEX2TORSOR_ROOT=${CLAUDE_PLUGIN_ROOT}/tools/tex2torsor html`
if you'd rather not copy it in.

---

## Step 5 — Write the preface first

The preface sets the voice for everything that follows. Write it before the other chapters. It should:

- Open with "Let's be honest with each other." or a similar direct acknowledgment of the reader's situation
- Name the actual problem the project solves in concrete terms
- Introduce the project in one clear sentence
- Briefly sketch what the manual covers and in what order
- End without a flourish — just the setup for Chapter 1

Show the user the draft. Revise before moving on.

---

## Step 6 — Write chapters one at a time

Work through the outline chapter by chapter. For each:

1. **Read relevant source material** — the actual code, config, existing docs, --help output — so the chapter reflects how the tool actually works
2. **Write the chapter** following STYLE.md conventions:
   - Open with a grounding sentence or short paragraph — what does this chapter solve?
   - One idea per paragraph
   - Lead with the point
   - `\code{}` for inline code; `lstlisting` for multi-line blocks
   - `notebox` for things readers might genuinely miss; `warnbox` for data-loss risks
   - No throat-clearing, no "In this section we will discuss"
3. **Show the user** the draft chapter; revise before moving on

Do not write all chapters in one pass without review. Manuals benefit from course-correction mid-stream.

---

## Step 7 — Write the quick reference appendix last

The quick-reference chapter is exhaustive. It can use tables, dense lists, and one-line summaries. Prose style is relaxed here — this is the part readers search, not read. Write it after the narrative chapters so you know what needs covering.

---

## Step 8 — Verify the build

Once at least the preface and one chapter exist, test the build:

```
cd manual && make pdf
cd manual && make html
cd manual && make epub
```

If any target fails, diagnose and fix before continuing. Common issues:
- `latexd` not installed or not on PATH — it's a Python tool in the lab software suite
- Missing LaTeX packages (install via tlmgr)
- Unicode characters inside `lstlisting` blocks — the listings package rejects non-ASCII;
  replace any non-ASCII arrows or special characters with ASCII equivalents (`->` not `→`)
- Pandoc not installed (needed by tex2torsor for HTML and directly for EPUB)
- Path issues in Makefile — remember the epub target must `cd` into `latex/` before calling pandoc

---

## Voice reminders (from the prose library — base-manual + 01-direct)

- **Friendly and direct.** Not corporate, not performed-quirky.
- **Concrete over abstract.** Name the actual scenario, not "you may find that..."
- **Short sentences for emphasis; longer for flow.**
- **Use "you."** Not "the user," not "one."
- **Contractions are fine.**
- **Dry humor welcome; jokes not required.** One well-placed observation beats three strained quips.
- **No:** "seamless," "robust," "powerful," "simple," "easy," "straightforward," "utilize," "leverage."
- **No throat-clearing:** "In this section, we will discuss..." — cut it.
- **Explain the *why* before the *how*.**

---

## What makes these manuals a family

All manuals in this set share:
- The same LaTeX preamble (Solarized Cézanne palette, Garamond/Cabin fonts, box styles, `\code{}` macro)
- The same base mechanics, plus a chosen voice, from the torsor prose library
- The same tex2torsor converter and HTML design
- The same build toolchain: `latexd` for PDF, pandoc for EPUB, `lab-view` for HTML preview
- The same author credit: `torsor lab` (in `pdfauthor`, the epub `--metadata author`, and the colophon page)
- The same colophon page on the title page's verso: `torsor lab` over the `torsor.org` link
- The same structural rhythm: preface → big idea → features → quick reference

This means a reader moving between manuals for different projects will feel at home. Don't deviate from the design without a strong reason and the user's agreement.
