---
name: write-paper-guide
description: Create a styled reading guide to a single mathematical paper — LaTeX source with HTML, PDF, and EPUB output — following the torsor design and prose style of the thing/shelf manuals. A two-part guide (Part I overview, Part II detailed walk-through) calibrated to a specific reader, written about the paper in the third person.
argument-hint: [path, arXiv id/URL, or description of the paper to guide]
---

You are helping the user write a reading guide to a mathematical paper. The guide is a
LaTeX book with matching HTML, PDF, and EPUB output, sharing the design and voice of the
*thing* and *shelf* manuals — but its job is different. It is a **reading companion** to
one paper: it orients the reader, then walks them through the paper itself.

The user has said: $ARGUMENTS

If no paper was specified, ask for one (a PDF path, an arXiv id or URL, or enough of a
citation to locate it) before proceeding.

Two framing rules that govern everything below:

1. **Write about the paper in the third person.** The authors prove, introduce, assume;
   Section 3 establishes; Theorem 4.2 states. Never "we prove" or "our construction."
2. **The guide is a guide, not a contribution.** It must never read as original work or
   as a survey. It explains, contextualizes, and signposts a paper that already exists.

---

## Reference materials — read these first

Before doing anything else, read:

1. **Style — base mechanics + the chosen voice.** A guide's style is composed from the
   torsor prose library: format mechanics plus one selectable voice. Read both:
   ```
   ${CLAUDE_PLUGIN_ROOT}/assets/prose/base-paper-guide.md
   ${CLAUDE_PLUGIN_ROOT}/assets/prose/voices/01-direct.md
   ```

2. **Voice catalog** — the available voices and how base+voice compose. `01-direct` is the
   default, proven voice; use it unless the user asks for another:
   ```
   ${CLAUDE_PLUGIN_ROOT}/assets/prose/README.md
   ```

3. **Canonical preamble + layout** — the shelf manual is the definitive worked example
   for preamble, title page, part/chapter structure, and Makefile. Read `main.tex`:
   ```
   ${CLAUDE_PLUGIN_ROOT}/assets/reference/shelf-main.tex
   ```
   and at least one chapter for prose rhythm:
   ```
   ${CLAUDE_PLUGIN_ROOT}/assets/reference/shelf-00-preface.tex
   ```

4. **Visual style reference** — the artifacts preamble establishes the Solarized Cézanne
   palette and Garamond/Cabin typography used family-wide (read lines 1–110):
   ```
   ${CLAUDE_PLUGIN_ROOT}/assets/reference/artifacts.tex
   ```

5. **tex2torsor** — the LaTeX→HTML converter:
   ```
   ${CLAUDE_PLUGIN_ROOT}/tools/tex2torsor/
   ```

If the paper has heavy math or you hit a toolchain limit (HTML/EPUB math not rendering,
`latexd` reporting success on a failed build), check `lessons.md` next to this skill first —
it has the proven, situational workarounds so you don't rediscover them.

---

## Step 1 — Get and read the paper

You cannot guide a paper you have not read. Locate the source and read it closely:

- If given a **PDF path**, read it with the Read tool.
- If given an **arXiv id or URL**, fetch the abstract/source (WebFetch) and, if a local
  PDF exists, read that; otherwise work from the arXiv HTML/source and abstract.
- If given only a **citation or description**, find it first and confirm with the user that
  you have the right paper before investing in a full read.

As you read, build a working understanding of: the main results and where they live; the
central definitions and constructions; the spine of the argument (which lemma is the
engine, which are bookkeeping); the prerequisites the paper assumes; and how it sits
relative to prior work it cites.

Do not start writing until you can state, in one paragraph, what the paper proves and how.

---

## Step 2 — Establish the target reader (interactive)

Every guide is calibrated to a specific reader. Ask the user about that reader before
outlining anything. If the guide is for the user themselves, they can say so and answer from
their own perspective; if it is for a student, a collaborator, or a general audience, the
answers change the whole guide.

Ask, in your own words and as a short batch (not one question at a time):

- **Field and subfield**, and roughly how close it is to the paper's area.
- **What they already know** vs. what needs explaining — which prerequisites are safe to
  assume, which should be developed in Part I.
- **Why they're reading** — refereeing, building on it, teaching from it, a seminar,
  general interest? This sets the depth and what counts as "the point."
- **Desired depth** — intuition and structure only, full proof-level detail, or
  somewhere between.
- **Length tolerance** — a tight orientation or an exhaustive companion.

If the user already has a background document handy, they can point you to it instead of
answering live; read it and confirm your reading of it.

Record the answers verbatim into `latex/reader-profile.md` inside the guide directory
(once it exists). This file is **not** compiled — it is a reference the prose is
calibrated against and a record for the next time. Re-read it whenever you are unsure how
much to explain.

**Voice.** Default to `01-direct`. If the user wants a different register for this guide (e.g.
the more digressive `02-wandering`), confirm it now and read that voice file in place of
`01-direct`. Record the chosen voice in `reader-profile.md`.

---

## Step 3 — Find or confirm the guide location

Propose where the guide should live. Unlike a manual, a paper often has no project
directory of its own, so confirm explicitly. Reasonable defaults:

- A `guide/` subdirectory beside the PDF, if the paper lives in its own folder.
- Otherwise a new directory named for the paper (e.g. `<author>-<short-title>-guide/`)
  in a location the user chooses.

Confirm the path with the user before creating anything. If a guide directory already
exists there, inspect it and ask whether to extend it or start fresh.

---

## Step 4 — Propose the outline

The guide always has **two parts**. Present this outline to the user, adapted to the paper,
and confirm before writing a word.

### Part I — Overview

This part answers six questions. The default grouping is two chapters; split or merge to
fit the paper, but cover all six:

- **What it is about.** Potentially the longest section: conceptual framing, the problem,
  the essential definitions and objects the reader needs, the lay of the land. This is
  where prerequisites the reader lacks (per the reader profile) get developed.
- **Why it is interesting.** Context, history, stakes — what its existence changes, who
  has wanted this and why.
- **Why it is plausible.** The intuition and evidence that the result *should* be true —
  special cases, analogies, heuristics, prior partial results.
- **Why it is hard.** Where the originality and technical difficulty actually live — what
  makes the naive approaches fail.
- **Why it is new.** How and why it goes beyond the prior literature; what was missing
  before.
- **Why the authors were able to pull it off.** The new perspective, technique, or
  sustained effort that made the difference.

A natural default: **Chapter 1 "What this paper is about"** (the long, definitional one)
and **Chapter 2 "The shape of the contribution"** with one section per remaining
question. Adjust freely.

### Part II — The guide to the paper

A detailed, faithful walk-through, written about the paper in the third person. Typical
shape:

- A short **roadmap** chapter: the paper's structure at a glance, what depends on what,
  and a reading order (including what to skim on a first pass).
- **One chapter per major section or result cluster** of the paper, following its spine.
  Each states what that part accomplishes, presents the key definitions/results by the
  paper's own numbering, explains the argument's structure, and flags where the
  difficulty lives.
- An optional closing chapter on **consequences, limitations, and open questions** if the
  paper has them.

### Appendix

A **notation and reference card** — the paper's notation collected in one place, plus a
table mapping the guide's chapters to the paper's sections. This is the dense reference
the prose chapters deliberately avoid.

---

## Step 5 — Scaffold the directory

Once the outline is confirmed, create the structure (identical to the manual family, with
a guide-shaped chapter list):

```
<guide-dir>/
  .gitignore
  Makefile
  latex/
    main.tex
    STYLE.md               ← base-paper-guide + chosen voice, assembled (records the voice)
    reader-profile.md      ← from Step 2; not compiled
    chapters/
      00-preface.tex
      01-what-its-about.tex
      02-shape-of-the-contribution.tex
      03-roadmap.tex
      04-...                ← one per major section of the paper
      99-notation-and-reference.tex
  tex2torsor/              ← symlink to the envtools manual's tex2torsor
  html/                    ← build output, not created yet
  epub/                    ← build output, not created yet
```

### .gitignore

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

Use the manual family's exact Makefile, changing only the EPUB title metadata. The
pattern (latexd for PDF, tex2torsor for HTML, pandoc for EPUB, lab-view for preview):

```makefile
# <paper> reading guide
#
# PDF:  latexd (wrapper around latexmk — keeps build artifacts out of source tree)
# HTML: tex2torsor (Python converter)
# EPUB: pandoc (directly from LaTeX source)
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
	  --metadata title="A Reading Guide to <Paper Title>" \
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

**EPUB note:** pandoc resolves `\input` relative to its working directory, not the source
file, so the epub target must `cd $(LATEX_DIR)` before invoking pandoc and use
`../$(EPUB_OUT)` as the output path.

### main.tex preamble

Take the **shelf manual's `main.tex` preamble verbatim** — it carries the full Solarized
Cézanne palette, Garamond/Cabin fonts, titlesec part/chapter/section formatting, fancyhdr
setup, mdframed `notebox`/`warnbox`, the `\code{}` macro, and `lstlisting` style, all
calibrated together. Replace only:

- `pdftitle` in `\hypersetup` (e.g. `A Reading Guide to <Paper Title>`); keep
  `pdfauthor` as `torsor lab`
- the `\begin{titlepage}...\end{titlepage}` content (see below)
- the `\input{chapters/...}` lines and the two `\part{...}` labels

Do **not** alter the palette, fonts, titlesec definitions, box styles, or `\code{}` macro
— these are the family-wide design constants.

**Two additions specific to a math guide** — add these to the preamble, after the
existing packages, and do not remove anything:

```latex
% --- Mathematics ---
\usepackage{amsmath}
\usepackage{amsthm}
\usepackage{mathtools}

% Theorem-like environments, styled to match the palette.
% Used to restate the paper's results faithfully — always cite the paper's own number.
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

When restating one of the paper's results, use the theorem environment with the paper's
own number in the optional argument, e.g.:

```latex
\begin{paperthm}[Theorem 4.2, slightly informally]
  ...
\end{paperthm}
```

so the reader can always cross-check the guide against the paper.

### Title page

Adapt the shelf title page. Credit the **paper's** title and authors as the subject, and
mark the document as a guide:

```latex
\begin{titlepage}
  \centering
  \vspace*{3cm}
  {\Large\sffamily\color{inkmuted} A Reading Guide to\par}
  \vspace{0.5cm}
  {\huge\rmfamily\color{inkdark} <Paper Title>\par}
  \vspace{0.5cm}
  {\normalsize\itshape\color{inkmuted} <Authors of the paper>\par}
  \vspace{3cm}
  {\normalsize\color{inkbody} <one-line orientation: what the paper does, for whom this guide is written>\par}
  \vfill
  {\small\color{inkdim} Last revised: \today}
\end{titlepage}
```

**Keep the colophon page verbatim.** Immediately after `\end{titlepage}`, carry the
inner-cover (colophon) page from the template unchanged — `torsor lab` over the terracotta
`torsor.org` link, bottom-aligned on an otherwise blank page. This is a fixed family
element (the guide credits the *paper's* authors on the title page; `torsor lab` is the
author of the guide and belongs only here, in the metadata, and in the epub). Do not edit
the attribution or the URL.

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

### STYLE and reader-profile files

Assemble the guide's effective style guide into `latex/STYLE.md` by concatenating the base
mechanics and the chosen voice, with a header recording which voice was used. From the
prose library:
```
PROSE=${CLAUDE_PLUGIN_ROOT}/assets/prose
{ echo "<!-- Voice: 01-direct (paper guide). Assembled from torsor-style/prose. -->"; echo; \
  cat "$PROSE/base-paper-guide.md"; echo; cat "$PROSE/voices/01-direct.md"; } \
  > <guide-dir>/latex/STYLE.md
```
Substitute the chosen voice file if it isn't `01-direct`. This keeps the guide
self-contained and records which voice it was written in.
Write `reader-profile.md` from the Step 2 answers.

### tex2torsor

The converter is vendored in this plugin. **Copy** it into the guide (don't symlink) so the
guide stays a self-contained deliverable that survives plugin updates or uninstalls:

```bash
cp -R ${CLAUDE_PLUGIN_ROOT}/tools/tex2torsor <guide-dir>/tex2torsor
```

The Makefile's `html` target also accepts `make TEX2TORSOR_ROOT=${CLAUDE_PLUGIN_ROOT}/tools/tex2torsor html`
if you'd rather not copy it in.

---

## Step 6 — Write Part I first

Part I sets the voice and the calibration. Write it before Part II.

- Open the **preface** by orienting the reader honestly: what this paper is, who this
  guide is for (name the reader profile's reader), and how to use the guide — Part I to
  orient, Part II to navigate, the appendix to look things up. End without flourish.
- Write **"What it is about"** as the substantial chapter: the problem, the essential
  definitions and objects, and the prerequisites the reader profile says are missing.
  This is where you do the patient setup so the rest can move quickly.
- Write **"The shape of the contribution"** covering, in turn: why it is interesting, why
  it is plausible, why it is hard, why it is new, and why the authors pulled it off. Keep
  these honest and specific — generic praise is the failure mode here.

Show the user Part I. Revise before moving on. Do not draft Part II until the overview's
framing and depth are right, because Part II inherits both.

---

## Step 7 — Write Part II, chapter by chapter

Work through the paper's spine one chapter at a time. For each:

1. **Re-read the relevant part of the paper** so the chapter is faithful to what the
   paper actually does — its statements, its numbering, its argument structure.
2. **Write the chapter** in the paper-guide style:
   - Open by orienting: what does this part of the paper accomplish, and why care?
   - Third person throughout: the authors do this, Section N does that.
   - Restate key results with `paperthm`/`paperdefn`/etc., always carrying the paper's
     own number; mark any paraphrase as a paraphrase.
   - Explain the *structure* of each argument and name where the difficulty lives —
     which lemma is the engine, what to read line by line, what to take on faith first.
   - `notebox` for something easily missed; `pitfallbox` for the subtlety that actually
     trips people. Don't use them for ordinary commentary.
   - No throat-clearing; lead with the point.
3. **Show the user** the draft chapter; revise before moving on.

Do not write all of Part II in one pass without review. A guide benefits from
course-correction mid-stream — especially on how much proof detail to include.

Write the **roadmap** chapter early (it frames the rest) and the **notation/reference
appendix** last (you'll know what needs collecting).

---

## Step 8 — Verify the build

Once the preface and at least one chapter exist, test all three targets:

```
cd <guide-dir> && make pdf
cd <guide-dir> && make html
cd <guide-dir> && make epub
```

Fix failures before continuing. Common issues:

- `latexd` not installed or not on PATH — it's a Python tool in the lab software suite.
- Missing LaTeX packages (install via tlmgr) — note the math additions need `amsmath`,
  `amsthm`, `mathtools`.
- Non-ASCII characters inside `lstlisting` blocks — the listings package rejects them;
  use ASCII equivalents (`->` not `→`). This does **not** apply to display/inline math,
  which is fine.
- tex2torsor / pandoc math handling — check that display and inline math survive the HTML
  and EPUB conversions; if a construct breaks, simplify it or note it for the user.
- Pandoc not installed (needed for HTML via tex2torsor and for EPUB directly).
- Path issues — remember the epub target must `cd` into `latex/` before calling pandoc.

---

## Voice reminders (condensed)

- **Third person about the paper, always.** They prove; Section 3 establishes. Never "we."
- **A guide, never a contribution.** It explains an existing paper; it is not original
  work and not a survey.
- **Friendly and direct.** A colleague walking a respected paper, not a textbook.
- **Lead with the point.** State what a result buys before stating it.
- **Triage openly.** Say what's load-bearing and what's routine; what to read closely and
  what to skim.
- **Faithful.** Cite the paper's numbering; mark paraphrases; never silently restate
  results stronger or weaker than they are.
- **Calibrated.** The reader profile is the tie-breaker on how much to explain.
- **No:** "we prove," "our result," "seamless," "robust," "powerful," filler "elegant"/
  "beautiful," "simple"/"easy"/"straightforward," throat-clearing.

---

## What makes this part of the manual family

The guide shares with the *thing* / *shelf* manuals:
- the same LaTeX preamble (Solarized Cézanne palette, Garamond/Cabin fonts, box styles,
  `\code{}` macro) — extended, not altered, with the math block above
- the same tex2torsor converter and HTML design
- the same toolchain: `latexd` for PDF, pandoc for EPUB, `lab-view` for HTML preview
- the same author credit: `torsor lab` (in `pdfauthor`, the epub `--metadata author`, and the colophon page)
- the same colophon page on the title page's verso: `torsor lab` over the `torsor.org` link

What is unique to the guide:
- the two-part shape (overview → walk-through) instead of preface → big idea → features
- the third-person, companion-not-contribution framing
- the reader profile that calibrates depth
- the math additions to the preamble (theorem environments, `pitfallbox`)

A reader moving between a tool manual and a paper guide should feel the same hand at work.
Don't deviate from the shared design without a strong reason and the user's agreement.
