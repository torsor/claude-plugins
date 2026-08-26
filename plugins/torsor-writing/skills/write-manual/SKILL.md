---
name: write-manual
description: Create a styled user's manual for a project — LaTeX source with HTML, PDF, EPUB, and Markdown output — following the torsor design and Scalzi-influenced prose style used in the thing manual.
argument-hint: [path or description of the project to document]
---

You are helping the user write a user's manual for a project. The manual will be a LaTeX book with matching HTML, PDF, EPUB, and Markdown output, following the design and voice established in the *thing: A User's Manual*.

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

2. **Worked example** — the shelf manual, for layout and prose rhythm:
   ```
   ${CLAUDE_PLUGIN_ROOT}/assets/reference/shelf-00-preface.tex
   ```
   The **preamble, Makefile, and colophon are owned by the core** and generated for you
   (see the commons). You do **not** copy `shelf-main.tex` — author only chapters and a
   manifest. `shelf-main.tex` remains a reference for what the house style produces.

3. **Visual style reference** — the artifacts document's LaTeX preamble establishes the
   Solarized Cézanne color palette and Garamond/Cabin typography used in all manuals:
   ```
   ${CLAUDE_PLUGIN_ROOT}/assets/reference/artifacts.tex
   ```
   (Read lines 1–110 — that's the whole preamble.)

4. **Shared mechanics — the commons.** The build contract (author chapters + a `build.yaml`
   manifest; the core assembles `main.tex`/Makefile/STYLE.md/tooling and builds every
   format), the situational lessons, and the publication pass:
   ```
   ${CLAUDE_PLUGIN_ROOT}/assets/commons/scaffold.md
   ${CLAUDE_PLUGIN_ROOT}/assets/commons/lessons.md
   ${CLAUDE_PLUGIN_ROOT}/assets/commons/publication.md
   ```
   `scaffold.md` is required reading before Step 4. Reach for `lessons.md` when the
   toolchain misbehaves (`latexd` reporting success on a failed build, HTML/EPUB math
   not rendering). The tex2torsor converter lives at
   `${CLAUDE_PLUGIN_ROOT}/tools/tex2torsor/`.

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

## Step 4 — Set up the directory

Once the outline is confirmed, set up `manual/` per
`${CLAUDE_PLUGIN_ROOT}/assets/commons/scaffold.md`. You author only the chapters and a
manifest; the core generates `main.tex`, the Makefile, `STYLE.md`, the colophon, and the
vendored tooling — do **not** hand-build those.

- **Chapters:** author under `manual/latex/chapters/` — `00-preface.tex`,
  `01-<chapter>.tex`, …, `99-quick-reference.tex`, matching the confirmed outline. Put any
  images in `manual/latex/assets/`.
- **`manual/build.yaml`:** `genre: manual`, `title`, `subtitle`, `stem`, the chosen
  `voice`, and a `chapters:` block giving front/main/appendix/back order. The manual genre
  defaults to features `callouts, listings`, and STYLE.md is assembled from `base-manual.md`
  + the voice automatically.
- **Math:** add `extra_features: [math]` only if the manual genuinely needs mathematics
  (e.g. a CLI reference for a mathematical tool — then `$…$`, `\[…\]`, and the `paperthm`
  environments are available alongside code).

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

## Step 8 — Verify the build and run the publication pass

Once at least the preface and one chapter exist, assemble and build per the commons:

```
python3 ${CLAUDE_PLUGIN_ROOT}/tools/core/assemble.py manual/build.yaml manual --in-place
cd manual && make all
```

Re-run `assemble.py --in-place` after adding chapters or editing `build.yaml` (it is
idempotent), then `make all` — it builds every format and runs `check-build.py`. Fix what
it reports (common issues and fixes are in `scaffold.md` and `lessons.md`). The manual is
not done until the **publication pass** has run and returned a clean evidence report —
follow `${CLAUDE_PLUGIN_ROOT}/assets/commons/publication.md` (dispatch it as a subagent for
a long session).

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
- The same scaffold, build toolchain, and publication pass, from the commons
  (`assets/commons/`): `latexd` (or `latexmk` fallback) for PDF, tex2torsor for HTML,
  pandoc for EPUB and Markdown, `lab-view` for preview, check-build.py for verification
- The same author credit: `torsor lab` (in `pdfauthor`, the epub `--metadata author`, and the colophon page)
- The same colophon page on the title page's verso: `torsor lab` over the `torsor.org` link
- The same structural rhythm: preface → big idea → features → quick reference

This means a reader moving between manuals for different projects will feel at home. Don't deviate from the design without a strong reason and the user's agreement.
