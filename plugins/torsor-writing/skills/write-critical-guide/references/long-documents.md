# Long documents — reviewing in chunks

A book, thesis, or long memoir cannot be examined in one pass. It is reviewed a chunk at a
time, in **separate sessions with separate agents**, with the user reading each chunk's output
before declaring the next. The pause between chunks is the point: it keeps a critical reader in control
of a long review instead of handing them one unreadable delivery at the end.

Nothing carries between those sessions except what is written down. **`review-state.yaml` is
that carry file, and it is the whole design** — the per-chunk work is the ordinary pipeline
pointed at a smaller source.

## When to chunk

Chunk when the work has parts a reader would review separately — chapters, or parts of a
thesis — and when no single pass could hold it. A 40-page paper is not chunked. A 300-page book
is. In between, ask: would a human reader read this in one sitting and form one judgment? If
not, chunk it.

Chunking also settles a tooling question. `annotate_tex.py` annotates one source file, so a
`main.tex` with `\include{ch01}` would otherwise fail on every anchor — the anchors live in the
chapter files. Under chunking each chunk's `paper.source` *is* its chapter file, and the problem
does not arise. For a genuinely monolithic single-file work, give each chunk the same source and
record its line range in `structure[].lines`.

---

## Chunk 0 — reconnaissance

Before any chapter is examined. **No deep reading**: front matter, table of contents,
introduction, bibliography, and a skim for structure. It produces `review-state.yaml` with
`work`, `structure` and `decisions` filled in, and nothing else.

It is cheap, and it stops chunk 1 from doing double duty as both a chapter review and the
establishment of the frame for every chunk after it. Categories, colours, reader profile and
voice are fixed here **and do not drift afterwards**.

---

## What changes in the per-chunk run

The pipeline runs as written, with four differences.

**Read the carry file first, in full.** It is the difference between a fresh agent and an
informed one. Do this before Phase 0.

**Phase 2d — context and significance — does not run per chunk.** Where the work sits, what is
new, how it compares to prior work: none of that is knowable from chapter 2, and a chunk that
attempts it produces confident nonsense. It belongs to the final synthesis.

**Phase 2c — reference verification — consults the cache first.** A book cites the same works
many times. `verified_clean` in the carry file records what has already been checked and what
it said; re-verify only what is new, and add what you check.

**Tags are namespaced by chunk.** `M1-7` is the seventh mathematical issue in chunk 1. No
collisions, no high-water mark to track, and a tag says where it lives.

At the end, update the carry file — see the rules below — and stop. Do not begin the next chunk.

---

## The final synthesis

After the last chunk, one pass over the accumulated state produces what no chunk could: the
summary with context and significance, the global assessment, the cross-chapter findings, and a
consolidated issue list. This is closer in shape to `write-body-of-work-summary` — pre-summarize
many, then synthesize — than to the single-paper flow.

---

## `review-state.yaml`

Lives beside the work, not inside any chunk's package.

The following book outline is invented for this schema. It extends the averaging fixture
into hypothetical chapters; it does not describe an examined book.

```yaml
work:
  title: "Coordinate averages: a fictional workbook"
  authors: ["A. Author"]
  identifier: "synthetic-workbook"
  kind: book
  source_root: "src/"
  submitted: "workbook.pdf"

structure:
  - id: ch01
    title: "The averaging projection"
    file: "src/ch01.tex"
    lines: null                 # optional source range for a monolithic file
    pages: "1--6"
    tag_prefix: "M1"
    chunk: 1
    status: reviewed
    reviewed_on: "<DATE>"
    package: "chunks/ch01/critical-guide/"

decisions:
  reader_profile: >
    A reader familiar with finite-dimensional linear algebra.
  voice: "01-direct"
  categories:
    mathematical:  {tag: M, colour: red}
    references:    {tag: R, colour: green}
    typographical: {tag: T, colour: blue}

conventions:
  - symbol: "$P$"
    introduced: "ch01, averaging definition"
    meaning: >
      The map that replaces each coordinate by the arithmetic mean.
  - symbol: "$H$"
    introduced: "ch01, kernel calculation"
    meaning: >
      The subspace of vectors whose coordinates sum to zero.

inherited:
  - id: "M1-1"
    chunk: 1
    grade: major
    statement: >
      The dimension assigned to the kernel is one too large.
    affects: >
      The basis count in the hypothetical weighted-averages chapter.

precedents:
  - kind: "a reference without a locator"
    graded: minor
    because: >
      The cited result can be found, but a locator would remove unnecessary searching.

verified_clean:
  - source: "Fixture lemma: constant vectors"
    statement: >
      The image of the averaging map is the span of the all-ones vector.
    checked_on: "<DATE>"
    used_in: [ch01]

revisions:
  - target: ch01
    found_in: ch02
    what: >
      The weighted formula requires a nonzero sum of weights; the earlier definition
      should state that restriction before introducing the formula.
    action: pending

not_examined: >
  The hypothetical chapter on weighted averages remains unreviewed.
```

## Rules for the carry file

**Read it in full before starting. Update it before stopping.** A chunk that does not update it
has broken the chain for every chunk after.

**`decisions` is written once, at chunk 0, and never edited.** If a later chunk finds the
category scheme inadequate, say so in the hand-back and let the user decide — changing it
mid-review makes the packages mutually inconsistent.

**`inherited` is the field that earns the design.** Before grading anything, check whether the
result you are examining rests on an open defect from an earlier chunk. If it does, the finding
is *provisional*, not independent, and must say so — the same distinction the ledger's
`depends_on` makes within a chunk, carried across chunks.

**`precedents` is added to whenever you make a grading call you had to think about.** Not every
grade; the ones where a reasonable reviewer could have gone the other way. That is what keeps
ten chapters graded by ten agents from disagreeing about what "major" means.

**`revisions` is appended, never acted on.** A chunk-5 agent that discovers a chapter-1 problem
records it and stops. Whether to re-run chapter 1 is the user's call, and re-running is
expensive.

**`not_examined` is cumulative and honest.** It is the field a reader will actually rely on to
know where the review's coverage ends.

## Hand-back, per chunk

State which chunk was done, what it found by category and grade, what it inherited from earlier
chunks and what is therefore provisional, anything appended to `revisions`, and **what remains
unreviewed**. Then stop, and say plainly that the next chunk is the user's to declare.
