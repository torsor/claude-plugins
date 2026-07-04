# Design — `write-body-of-work-summary`

*2026-07-03. Status: approved, in implementation.*

A fifth skill for the `torsor-writing` plugin: a styled summary of one
mathematician's **body of work** — an overview essay plus a short paragraph per
paper. Sibling to `write-topic-guide`; reuses its three-phase machinery and the
shared commons scaffold. Output is the torsor house format (LaTeX → PDF, HTML,
EPUB, Markdown).

## What it is

- Subject is neither one paper (`write-paper-guide`) nor one idea
  (`write-topic-guide`) but **one person's program**.
- Deliverable shape: a short, essayistic document, not a two-part book.
  - **Preface** — a few lines: whose work, who the summary is for, how to read it.
  - **The overview** — a 2–3 page essay. The intellectual core.
  - **The papers** — a short paragraph per paper, organized theme-wise or
    chronologically (the skill decides per subject and proposes before writing).
  - **Appendix** — a reference card: full chronological citation list + a
    themes × papers table.

## The two governing constraints (the point of the genre)

1. **Never label the six questions.** The overview must implicitly answer the
   same six questions `write-paper-guide` asks — *what it's about, why
   interesting, why plausible, why hard, why new, why they pulled it off* — but
   with **no** "Why it is hard" heading and no "the difficulty here is…"
   scaffolding. The questions are answered as the argument moves.
2. **Per-paper paragraph = one short paragraph** that implicitly hits the same
   questions for that paper — no labels, no checklist.

Register: serious-Scalzi. Direct, plainspoken, leads with the point; **less
playful** than the manuals. Base voice stays `01-direct`, tightened.

## Purpose modes (runtime question)

The skill asks the purpose at creation time; it sets emphasis **and grammatical
person**:

| Mode | Emphasis | Person |
|---|---|---|
| Newcomer orientation | entry points, prerequisites, how threads connect, what to read first | third |
| Evaluator appraisal | the arc, stature, what each result changed, coherence | third |
| Self-presentation | the program as the author frames it (research statement, grant, prize) | **first** |
| Scholarly appreciation | collected-works introduction / survey of contributions | third |

## Phases (mirroring `write-topic-guide` A/B/C, with a Phase 0)

- **Phase 0 — Assemble and confirm the corpus.** The paper list is itself
  editorial. Accept a directory of files, arXiv ids, or a publication list to
  resolve. Confirm *which* papers (everything vs. selected works) with the user,
  since that interacts with the chosen purpose. Prefer supplied Markdown/LaTeX;
  fall back to PDF (vision-read, never OCR — via `pre-summarization.md`).
- **Phase A — Pre-summarize each paper (kept).** One subagent per paper writes
  `source-notes/<paper>.md`: a structured digest that *internally* answers the
  six questions, plus citation metadata and which themes it touches. Kept as a
  reusable deliverable. Reuses `pre-summarization.md` wholesale.
- **Phase B — Purpose, reader, themes.** Ask the purpose mode (sets person) and
  the reader calibration (as in paper-guide Step 2); record both into
  `reader-profile.md`. A synthesis subagent reads all notes →
  `source-notes/themes.md`: main themes, paper→theme map, proposed organization
  (theme vs chronological), the overview throughline, and a significance
  ranking. Gates the overview.
- **Phase C — Author and build.** Write the overview essay first (implicitly
  answering all six questions, no labels), show the user, revise. Then the
  per-paper paragraphs (subagent-scaled for a large corpus; each fed the note +
  `themes.md` + STYLE.md + the overview as a voice exemplar). Build four
  formats, `make check`, publication pass.

## Files

New:
- `skills/write-body-of-work-summary/SKILL.md`
- `assets/prose/base-body-of-work.md` — genre mechanics; derived from
  `base-paper-guide.md`.

Touched:
- `.claude-plugin/plugin.json` — description string lists the new skill.
- `~/.claude/skills/write-body-of-work-summary` — symlink, matching siblings.

Reused unchanged: `write-topic-guide/pre-summarization.md`,
`assets/commons/{scaffold,lessons,publication}.md`, `voices/01-direct.md`,
`assets/reference/*`, `tools/tex2torsor`.

## Why a separate base prose file

Rather than loosening the shared `base-paper-guide.md`, the genre gets its own
`base-body-of-work.md`. Two reasons: it carries the "never label the six
questions" rule, which is meaningless for a paper guide; and it must **ban**
`load-bearing`, which `base-paper-guide.md` actively *endorses* ("distinguish
load-bearing from routine"). A separate file keeps that departure — and the
banned `clean` / `load-bearing` list — from leaking into the paper guide.

## Deliberately out of scope (YAGNI)

- No automatic corpus discovery from an arXiv author page or CV parser; the user
  supplies or points at the papers, and Phase 0 confirms the set.
- No new voice; `01-direct` (tightened via the base) covers it.
- No per-paper chapters — one paragraph each is the whole point.
