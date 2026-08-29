---
name: write-body-of-work-summary
description: Use when the goal is a styled overview of one mathematician's whole body of work — a 2–3 page essay on the program followed by a short paragraph per paper — built by pre-summarizing many papers (Markdown/LaTeX preferred, PDFs vision-read) and gathering their themes. A sibling to write-topic-guide; output is the torsor house format (LaTeX → PDF, HTML, EPUB, Markdown). Triggers: "summarize X's body of work", "write an overview of my research program", "a survey of this person's papers for a committee/student".
argument-hint: [the mathematician, and the papers — a directory, arXiv ids, or a publication list]
---

**Family stance — read `${CLAUDE_PLUGIN_ROOT}/assets/commons/stance.md` before writing any
prose.** It binds every genre in this plugin and settles four things this file assumes rather
than states: that the document has no author and so no first person, that it does not address
its reader, that calibration is not content, and that a supplied PDF is the artifact under
study while its source is an aid.

You are helping the user write a **body-of-work summary**: one document that
overviews a single mathematician's program — a 2–3 page essay on the whole body
of work, followed by a short paragraph per paper. It shares the torsor design and
voice of the manual / paper-guide / topic-guide family, and reuses
`write-topic-guide`'s three-phase machinery. Its subject is a *person's work*.

The user has said: $ARGUMENTS

If no mathematician or papers were named, ask for both (whose work, and the
papers — a directory of files, a list of arXiv ids, or a publication list to
resolve) before proceeding.

## What this is, and how it differs from its siblings

`write-paper-guide` companions **one** paper; `write-topic-guide` explains **one
idea across sources**. This skill overviews **one person's program across their
papers**, organized by the **themes** that run through the work. Four things are
particular to it:

1. **A pre-summarization phase** (borrowed intact from `write-topic-guide`).
   Before any writing, each paper is distilled by a dedicated subagent, in its
   own context, into a structured markdown digest under `source-notes/`. The
   summary is written from those notes, never from the raw papers.
2. **A purpose mode that sets grammatical person.** You ask up front who the
   summary is for; the answer changes emphasis *and* whether it is written in the
   first or third person.
3. **A themes map instead of a concept spine.** You gather the threads that run
   through the corpus, map every paper onto them, and decide the overview's
   throughline and the organization of the paper paragraphs.
4. **The six-questions discipline, unlabeled.** The overview answers the same six
   framing questions a paper guide asks — but **never names them**, and there are
   **no** "Why it is hard" sections. Each per-paper paragraph does the same in
   miniature.

Two framing rules carry over from the family:

- **A summary, not a contribution or a survey.** It explains and appraises
  existing work; it is never original research and never a survey of the field.
- **Third person about the work by default.** *Krashen proves; the 2019 paper
  establishes.* The one exception is **self-presentation** mode (see Phase B),
  where the first person is the whole point.

## The shape of the job

```
Phase 0  Assemble + confirm the corpus       -> the agreed paper list
Phase A  Pre-summarize each paper            -> source-notes/*.md  (reviewed, kept)
Phase B  Purpose + reader + themes           -> reader-profile.md, source-notes/themes.md
Phase C  Author + build (compose w/ commons) -> the summary, four formats
```

Do them in order. Phase B's themes map gates Phase C: do not draft the overview
until the threads, the throughline, and the organization are agreed.

---

## Locating the shared assets — do this before reading them

The paths below are written `${CLAUDE_PLUGIN_ROOT}/…`. That resolves only when this skill is
loaded as part of an **installed plugin**; under a plain symlink into `~/.claude/skills/` it is
undefined, and the assets look as though they do not exist. So:

1. **Try the path as written.**
2. **If it is not there, derive the root.** You are told this skill's base directory when you
   are invoked. Resolve it first — it is often a symlink, so `readlink -f` or `realpath` it —
   and take its **grandparent** as the plugin root. Both install modes give the same tree from
   there: `assets/`, `tools/`, and the other skills' `references/`.
3. **If the assets are still not found, stop and say so.** They are required, not optional: the
   prose base and the chosen voice are what make the output part of this family, and the
   scaffold is what makes it build. A document written without them looks finished and is wrong
   in the way that is hardest to catch afterwards. Say the bundle is missing and let the user
   install the plugin; do not improvise a substitute.

---

## Reference materials — read these first

Before anything else, read:

1. **Style — base mechanics + the chosen voice.** This genre has its own base:
   ```
   ${CLAUDE_PLUGIN_ROOT}/assets/prose/base-body-of-work.md
   ${CLAUDE_PLUGIN_ROOT}/assets/prose/voices/01-direct.md
   ```
   `base-body-of-work.md` carries the two rules that define the genre: **answer
   the six framing questions without ever naming them**, and the banned-words
   list (**clean** and **load-bearing** are banned family-wide). Read it before writing
   a word.

2. **Voice catalog** — `01-direct` is the default; use it unless the user asks
   for another. The register for this genre is `01-direct`, *tightened* — serious,
   less playful than the manuals:
   ```
   ${CLAUDE_PLUGIN_ROOT}/assets/prose/README.md
   ```

3. **The commons** — the family scaffold, situational lessons, and publication
   pass. Required before Phase C:
   ```
   ${CLAUDE_PLUGIN_ROOT}/assets/commons/scaffold.md
   ${CLAUDE_PLUGIN_ROOT}/assets/commons/lessons.md
   ${CLAUDE_PLUGIN_ROOT}/assets/commons/publication.md
   ```

4. **Pre-summarization procedure** — the extraction method Phase A reuses intact
   (text-layer vs. scanned detection, TOC-locate-then-vision-read, the page-offset
   trick, the per-source review gate, err-on-the-side-of-more):
   ```
   ${CLAUDE_PLUGIN_ROOT}/skills/write-topic-guide/pre-summarization.md
   ```

5. **Layout exemplar** — the canonical preamble, title page, and Makefile:
   ```
   ${CLAUDE_PLUGIN_ROOT}/assets/reference/shelf-main.tex
   ${CLAUDE_PLUGIN_ROOT}/assets/reference/shelf-00-preface.tex
   ```

---

## Phase 0 — Assemble and confirm the corpus

The paper list is an editorial choice, not a given. Before extracting anything,
settle *which* papers the summary covers, because it interacts with the purpose
(a newcomer wants the essential threads; an evaluator's case may want everything;
an appreciation may want selected works).

- **Gather the sources.** Accept a directory of files, a list of arXiv ids/URLs,
  or a publication list to resolve. **Prefer supplied Markdown or LaTeX** — it is
  cleaner input than a PDF. Fall back to PDF where that is all there is.
- **Confirm the set with the user.** Everything, or selected works? Include
  surveys, notes, and proceedings, or only research papers? Record the agreed
  list. If it is large, that is expected — Phase A scales with subagents.
- **Do not vision-read yet.** Phase A does the reading, in isolated contexts.

---

## Phase A — Pre-summarize each paper

**This is the part agents skip by default. Do not read the raw papers into your
own context and write from them. Distill first.**

For each paper, dispatch a subagent that reads it in its own context and writes a
structured digest to `<summary-dir>/source-notes/<key>.md`, then review each
digest before trusting it.

**REQUIRED:** read
`${CLAUDE_PLUGIN_ROOT}/skills/write-topic-guide/pre-summarization.md` before
dispatching any extraction subagent. The non-negotiable rules from it:

- **Markdown/LaTeX sources: read directly.** They have a text layer; no vision
  needed. **Scanned/image PDFs: vision-read; never OCR** (tesseract/ocrmypdf
  mangle mathematics). Locate the relevant sections via the TOC, then read the
  page images.
- **One subagent per paper, isolated context.** Keeps a large corpus out of your
  thread and makes the notes a clean, reusable deliverable.
- **Capture more than you think you need,** and shape each note so it *internally*
  answers, for this paper: what it does, why it matters, where the difficulty is,
  what is new in it, and the technique that made it work — plus full citation
  metadata (authors, venue, year, arXiv id) and a short list of **which themes it
  touches** (you will refine the theme vocabulary in Phase B). These framing
  answers stay *inside the note*; they are never labeled in the summary itself.
- **Review every digest** for coverage and faithfulness before building on it.

Keep `source-notes/` — it is a reusable deliverable and part of the point.

---

## Phase B — Purpose, reader, themes

**Purpose mode (ask first — it sets the grammatical person).** Ask the user which
of these the summary is for; record the answer in `reader-profile.md`:

- **Newcomer orientation** — a student/postdoc entering the area. Emphasis: entry
  points, prerequisites, how the threads connect, what to read first. *Third
  person.*
- **Evaluator appraisal** — a hiring/tenure/prize committee. Emphasis: the arc,
  stature, what each result changed, the coherence of the program. *Third
  person.*
- **Self-presentation** — the mathematician presenting their own program
  (research statement, grant, prize submission). *First person is allowed and
  expected.*
- **Scholarly appreciation** — general mathematical readers; a collected-works
  introduction. *Third person, essayistic.*

**Reader profile.** As in `write-paper-guide` Step 2: establish field, what the
reader knows vs. needs developed, why they're reading, depth, and length
tolerance. Record verbatim into `<summary-dir>/latex/reader-profile.md` (not
compiled), together with the chosen purpose mode, the resulting grammatical
person, and the voice. Default voice `01-direct`.

**The themes map.** Dispatch a subagent to read all the `source-notes` and write
`source-notes/themes.md`. It must contain:

- **The themes** — the ordered threads that run through the work, named as they
  would be named in the overview ("Descent and patching," "Period and index"),
  each with a one-line gloss.
- **A paper → theme map** — every paper placed under its best-fit theme (note a
  second theme where a paper genuinely spans two).
- **The proposed organization** of the paper paragraphs — **grouped by theme** or
  a single **chronological** run — chosen to fit the corpus and the purpose, with
  a one-line reason. Present this to the user for agreement before writing; it is
  the most consequential editorial choice after the purpose.
- **The overview throughline** — the single argument the 2–3 page essay makes
  about how the work coheres and what it changed.
- **A significance ranking** — which papers are central, which consolidate, which
  opened or closed a direction. This drives the weight each paragraph gets and
  what the overview foregrounds.

Get the user's agreement on the themes and the organization before Phase C.

---

## Phase C — Author and build

Authoring reuses the family commons, with body-of-work deltas.
**REQUIRED:** scaffold and build per
`${CLAUDE_PLUGIN_ROOT}/assets/commons/scaffold.md` (directory, `.gitignore`,
Makefile, preamble rules, the math block, STYLE.md assembly, tex2torsor +
check-build.py copies). Consult
`${CLAUDE_PLUGIN_ROOT}/assets/commons/lessons.md` for math-rendering and `latexd`
gotchas. Do not re-derive the build.

Apply these deltas:

- **Directory.** Same layout as a guide, plus the kept `source-notes/` beside
  `latex/`.
- **Structure is overview-plus-paragraphs, not a two-part book.** Chapters:
  ```
  00-preface.tex          # whose work, who this is for, how to read it
  01-overview.tex         # the 2–3 page essay — the intellectual core
  02-the-papers.tex       # short paragraph per paper (theme-grouped or chronological)
  99-references.tex       # chronological citation list + themes × papers table
  ```
  For a large program, `02-the-papers.tex` may `\input` one file per theme.
- **Write the overview first, and make it earn the six answers without naming
  them.** It implicitly conveys what the work is about, why it is interesting, why
  it is plausible, where the difficulty lives, what is new, and the perspective
  that made it possible — with **no** headings or topic sentences that restate
  those questions. For a small corpus it is one continuous essay; for a large one
  it may be broken by **theme** subheadings (never question subheadings). Show the
  user; revise. Part II inherits its voice and calibration.
- **Then the per-paper paragraphs.** One short paragraph each, in the agreed
  organization, each implicitly conveying what the paper did, why it mattered,
  what was hard, and what was new — none of it labeled. Carry each paper's stable
  key so the reference card and the overview line up. When restating a result,
  use the math block's theorem environments and mark paraphrases as paraphrases.
- **Write from `source-notes` + `themes.md`,** not the raw papers.
- **For a large corpus, scale with subagents.** Dispatch one subagent per theme
  (or per batch of paragraphs), each given STYLE.md, `reader-profile.md`, the
  relevant `source-notes`, `themes.md`, and the finished overview as a voice
  exemplar. Keep a **progress ledger** and gate with a **whole-summary
  faithfulness review** at the end (the `superpowers:subagent-driven-development`
  pattern fits).
- **Title page.** Adapt the shelf title page: the **mathematician's name** is the
  subject, marked as a body-of-work summary; `torsor lab` authors the summary and
  belongs only in the colophon, metadata, and epub. In self-presentation mode the
  subject is still named on the title page as the subject of the work.

Build all four formats, run `make check`, and finish with the publication pass
(`${CLAUDE_PLUGIN_ROOT}/assets/commons/publication.md`). The deliverable is the
LaTeX/PDF/HTML/EPUB/Markdown **plus** the kept `source-notes/`.

---

## Output structure

```
<summary-dir>/
  Makefile  .gitignore  check-build.py       # from the commons scaffold
  source-notes/                              # KEPT deliverable — the pre-summarization
    <paper-a>.md  <paper-b>.md  ...
    themes.md                                # themes + paper→theme map + organization + throughline
  latex/
    main.tex  STYLE.md  reader-profile.md    # reader-profile records purpose mode + person + voice
    chapters/
      00-preface.tex
      01-overview.tex                        # the 2–3 page essay
      02-the-papers.tex                      # paragraph per paper (may \input per-theme files)
      99-references.tex                      # citation list + themes × papers table
  tex2torsor/                                # copied from the plugin (commons scaffold)
  html/  epub/  markdown/                    # build output
```

---

## Common mistakes

| Mistake | Do instead |
|---|---|
| Reading the raw papers into your own context and writing from them | Distill each into `source-notes/*.md` via isolated subagents first (Phase A) |
| **Labeling the six questions** — a "Why it is hard" heading or a "The difficulty is…" topic sentence | Answer all six *implicitly*, in running prose, with none named |
| **OCR**-ing a scanned paper (tesseract/ocrmypdf — mangles math) | Locate sections via TOC, then **vision-read** the page images |
| Writing a mini-guide for each paper | One short paragraph each — what it did and why it earned its place |
| Sliding into a field survey or a recommendation letter | Summarize *this person's* work; explain and locate, don't review the area or lobby |
| Guessing the grammatical person | Ask the purpose mode first; third person unless self-presentation |
| Skipping the themes map and discovering mid-write that the work doesn't cohere as drafted | Produce `themes.md`; agree themes + organization before Phase C |
| Using "clean" or "load-bearing" | Banned family-wide — say *central*, *carries the argument*, *does the work*, *the engine of* |
| Guessing the build | Reuse the commons scaffold's `latexd` (→ `latexmk` fallback) / `tex2torsor` / pandoc toolchain + `lessons.md` |
| Throwing away the extraction work | Keep `source-notes/` — reusable, and part of the point |

## What stays the same as the family

Same torsor preamble (Solarized Cézanne, Garamond/Cabin, box styles, `\code{}`),
the math block (theorem environments, `pitfallbox`), `tex2torsor` + HTML design,
the `latexd` (→ `latexmk` fallback) / pandoc (EPUB + Markdown) / `lab-view`
toolchain, the publication pass, the `torsor lab` credit, and the colophon page
(inherited verbatim via the commons scaffold). A reader moving between a tool
manual, a paper guide, a topic guide, and a body-of-work summary should feel the
same hand at work.
