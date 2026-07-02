---
name: write-topic-guide
description: Use when the goal is a single learning-oriented explanatory guide that synthesizes SEVERAL sources (papers, books, theses) on one mathematical topic or concept — especially when the sources are large or include scanned/no-text-layer PDFs — rather than a companion to one paper. Output is the torsor house format (LaTeX → PDF, HTML, EPUB, Markdown). Triggers: "explain how to think about X across these papers", "turn these sources into a guide", "orient a student to this idea".
argument-hint: [the topic/idea, and the source PDFs to synthesize]
---

You are helping the user write a **topic guide**: one learning-oriented explanatory
document that teaches a specific reader how to think about a mathematical *idea*, built by
synthesizing several sources. It shares the torsor design and voice of the *thing* / *shelf*
manuals and the `write-paper-guide` companion — but its subject is a concept, not a paper.

The user has said: $ARGUMENTS

If no topic or sources were named, ask for both (the idea to explain, and the source PDFs /
arXiv ids) before proceeding.

## What this is, and how it differs from write-paper-guide

`write-paper-guide` is a third-person companion to **one** paper, organized by that paper's
sections. This skill produces a guide to **one idea across many sources**, organized by a
**conceptual spine** you decide. Four things are unique to it:

1. **A pre-summarization phase.** Before any writing, each source is distilled — by a
   dedicated subagent, in its own context — into a structured, reusable markdown digest
   under `source-notes/`. The guide is written from those notes, never from the raw PDFs.
2. **Scanned-PDF handling.** Sources are often large or image-only. You locate the relevant
   chapters, then **vision-read** the pages — you do not OCR them.
3. **A concept spine + gaps list.** You decide the throughline up front, map every source
   onto it, and produce an honest list of what no source covers — which gates whether the
   guide can be written without more reading.
4. **Learning orientation.** The guide is calibrated to bring one named reader *to*
   understanding, develops missing prerequisites from scratch, and leaves the `source-notes`
   behind as a durable study artifact.

Two framing rules carry over unchanged from `write-paper-guide`:

- **Third person about the sources.** The authors prove; Section 3 establishes. Never "we
  prove" / "our construction." The guide's "you" addresses the *reader*, not the sources.
- **A guide, not a contribution.** It explains and synthesizes existing work; it is never
  original research and never a survey of the field.

## The shape of the job

```
Phase A  Pre-summarize the sources        -> source-notes/*.md  (reviewed, kept)
Phase B  Reader + concept spine + synthesis -> reader-profile.md, the spine, gaps list
Phase C  Author + build (compose w/ write-paper-guide) -> the guide, four formats
```

Do them in order. Phase B's gaps list is a gate: if a spine step is covered by no source,
fill it (from background, or by reading more) before Phase C.

---

## Phase A — Pre-summarize the sources

**This is the part `write-paper-guide` does not have, and the part agents skip by default.
Do not read the raw PDFs into your own context and write from them. Distill first.**

For each source, dispatch a subagent that reads it in its own context and writes a
structured English digest to `<guide-dir>/source-notes/<source>.md`. Then review each
digest before trusting it. The full procedure — text-layer vs. scanned detection, the
TOC-locate-then-vision-read pattern for image PDFs, the printed↔PDF page-offset trick,
French/foreign-language handling, the per-source review gate, and the
**err-on-the-side-of-more** principle — is in:

**REQUIRED:** read [pre-summarization.md](pre-summarization.md) before dispatching any
extraction subagent.

The non-negotiable rules from it:

- **Vision-read scanned PDFs; never OCR them.** The Read tool renders PDF pages as images
  the model sees directly — far better on mathematics than tesseract/ocrmypdf.
- **One subagent per source, isolated context.** Keeps a 300-page scan out of your thread
  and makes the notes a clean, reusable deliverable.
- **Capture more than you think you need.** Definitions, statements with exact section/page
  refs, tables, proof sketches, a notation key. These notes outlive this guide.
- **Review every digest** for coverage and faithfulness before building on it.

---

## Phase B — Reader, concept spine, synthesis

**Reader profile.** As in `write-paper-guide` Step 2: establish field, what the reader knows
vs. needs developed, why they're reading, depth, and length tolerance. Record verbatim into
`<guide-dir>/latex/reader-profile.md` (not compiled). Default voice `01-direct`.

**The concept spine.** Decide the throughline — the ordered sequence of milestones the guide
builds, from the reader's current vantage to the payoff. This is the guide's skeleton and
replaces "the paper's section order." State it explicitly (a numbered list) and get the
user's agreement before writing; it is the single most consequential editorial choice.

**The synthesis note.** Dispatch a subagent to read all the `source-notes` plus the spine
and write `source-notes/synthesis.md`: for each spine step, which source(s) cover it, the
cleanest statement to use, where sources diverge, and which framing to lead with. It must
end with two things:

- a **unified notation/convention table** — sources routinely disagree (sign conventions,
  index conventions); pin ONE, verified against a source, and carry it everywhere; and
- a **gaps list** — every spine step no source covers, each marked *fillable from
  background* or *needs more reading*. Resolve the genuine gaps before Phase C.

---

## Phase C — Author and build

Authoring reuses the family commons and `write-paper-guide`, with topic-guide deltas.
**REQUIRED:** scaffold and build per `${CLAUDE_PLUGIN_ROOT}/assets/commons/scaffold.md`
(directory, `.gitignore`, Makefile, preamble rules, the math block, STYLE.md assembly,
tex2torsor + check-build.py copies); take the guide-genre specifics — title page,
reader profile, outline conventions — from `write-paper-guide` Steps 4–5; and consult
`${CLAUDE_PLUGIN_ROOT}/assets/commons/lessons.md` for the math-rendering and `latexd`
gotchas. Do not re-derive the build.

Apply these deltas to those steps:

- **Directory.** Same as a paper guide, plus the kept `source-notes/` beside `latex/`.
- **Structure is spine-driven, not paper-driven.** Part I is the **intuition map** of the
  whole spine (no proofs). Part II is the **detailed walk-through**, one chapter per spine
  milestone (not per source-section), pulling from whichever source the synthesis note says
  leads that step. The appendix's reference card reconciles **all sources'** notation into
  the one verified convention.
- **Write from `source-notes` + `synthesis.md`,** not the raw PDFs. The notes are the
  pre-digested material the chapter authors consume.
- **Calibrate to learning.** Develop the prerequisites the reader profile says are missing;
  lead each milestone with *why* before *what*.
- **For a large guide, scale with subagents.** Drafting many faithful chapters by hand is
  slow and risks running out of context. Dispatch one subagent per chapter (each given
  STYLE.md, reader-profile.md, the relevant `source-notes`, the spine, and Part I as a voice
  exemplar), keep a **progress ledger**, and gate with a **whole-guide faithfulness review**
  at the end. The `superpowers:subagent-driven-development` pattern fits this directly.

Build all four formats, run `make check`, and finish with the publication pass
(`${CLAUDE_PLUGIN_ROOT}/assets/commons/publication.md`). The guide deliverable is
the LaTeX/PDF/HTML/EPUB/Markdown **plus** the `source-notes/` directory. The `pdf` target
falls back to `latexmk` where `latexd` isn't installed; the Markdown export (`make md`) is
part of the default build.

---

## Output structure

```
<guide-dir>/
  Makefile  .gitignore  check-build.py # from the commons scaffold
  source-notes/                        # KEPT deliverable — the pre-summarization
    <source-a>.md  <source-b>.md  ...
    synthesis.md                       # spine map + unified notation + gaps list
  latex/
    main.tex  STYLE.md  reader-profile.md
    chapters/
      00-preface.tex
      01-what-its-about.tex            # Part I — intuition map
      02-shape-of-the-contribution.tex
      03-roadmap.tex                   # Part II — one chapter per SPINE milestone
      04-...  05-...  ...
      99-notation-and-reference.tex    # reconciles all sources' notation
  tex2torsor/                          # copied from the plugin (commons scaffold)
  html/  epub/  markdown/              # build output
```

---

## Common mistakes

| Mistake | Do instead |
|---|---|
| Reading the raw PDFs into your own context and writing from them | Distill each into `source-notes/*.md` via isolated subagents first (Phase A) |
| **OCR**-ing the scanned book (tesseract/ocrmypdf — mangles math) | Locate chapters via TOC, then **vision-read** the page images |
| Treating the topic as a fake single "paper" and walking its sections | Decide a **concept spine**; organize Part II by milestone, not by source |
| Skipping the synthesis/gaps step and discovering mid-write a step no source covers | Produce `synthesis.md` with a gaps list; resolve gaps before Phase C |
| Letting sources' clashing conventions leak in | Pin ONE verified convention in `synthesis.md` and the appendix; reconcile everywhere |
| Guessing the build (`xelatex`/`make4ht`/`tex4ebook`) | Reuse the commons scaffold's `latexd` (→ `latexmk` fallback) / `tex2torsor` / `pandoc` (EPUB + Markdown) toolchain + `assets/commons/lessons.md` |
| Hand-writing every chapter sequentially for a large guide | Subagent per chapter + progress ledger + final faithfulness review |
| Throwing away the extraction work | Keep `source-notes/` as a deliverable — it is reusable and is part of the point |

## What stays the same as the manual family

Same torsor preamble (Solarized Cézanne, Garamond/Cabin, box styles, `\code{}`), the math
block (theorem environments, `pitfallbox`), `tex2torsor` + HTML design, the `latexd`
(→ `latexmk` fallback) / pandoc (EPUB + Markdown) / `lab-view` toolchain, the publication
pass, the `torsor lab` credit, and the colophon page on the title
page's verso (`torsor lab` over the `torsor.org` link — inherited verbatim via the
commons scaffold this skill reuses). A reader moving between a tool manual, a
paper guide, and a topic guide should feel the same hand at work.
