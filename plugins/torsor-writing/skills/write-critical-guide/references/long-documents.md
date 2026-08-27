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

```yaml
work:
  title: "..."
  authors: ["..."]
  identifier: "..."            # arXiv id, submission number, or a description
  kind: book                   # book | thesis | memoir | long-paper
  source_root: "src/"          # where the chapter files live
  submitted: "manuscript.pdf"  # optional: what page/line references point at

structure:                     # written at chunk 0, status updated after each chunk
  - id: ch01
    title: "Orders and their ramification"
    file: "src/ch01.tex"
    lines: null                # only for a monolithic source: [1, 1840]
    pages: "1--38"
    tag_prefix: "M1"           # and R1, T1, ... per category
    chunk: 1
    status: reviewed           # pending | reviewed | needs-rerun
    reviewed_on: "2026-08-26"
    package: "chunks/ch01/critical-guide/"

decisions:                     # fixed at chunk 0. Do not drift.
  reader_profile: >
    An active researcher in a roughly adjacent field, reading in order to assess and evaluate it.
  voice: "01-direct"
  categories:
    mathematical:   {tag: M, colour: red}
    references:     {tag: R, colour: green}
    typographical:  {tag: T, colour: blue}

conventions:                   # notation the work establishes and later chunks assume
  - symbol: "$\\mathscr{A}$"
    introduced: "ch01, §1.2"
    meaning: >
      An order over the base, always torsion-free and generically Azumaya.
  - symbol: "friendly"
    introduced: "ch02, §2.1"
    meaning: >
      The author's term; base change commutes with pushforward for this sheaf.

inherited:                     # open defects that later chunks rest on
  - id: "M1-4"
    chunk: 1
    grade: major
    statement: >
      Condition (C) never requires $\mathscr O_S \to \pi_*\mathscr O_Y$ to be an isomorphism.
    affects: >
      Every result in ch03 and ch05 whose hypothesis is (C). Findings there that assume the
      condition holds are provisional on this being repaired.

precedents:                    # so severity does not drift between sessions
  - kind: "a standard result cited without a locator"
    graded: minor
    because: >
      The reader can find it, but the author should supply the locator. Not major unless the
      result is doing work the reader cannot reconstruct.
  - kind: "a lemma stated without proof and never used again"
    graded: minor
    because: >
      Graded on consequence: nothing downstream depends on it.

verified_clean:                # citation cache: check once, reuse
  - source: "stacks-project 0B8J"
    statement: >
      Sheaves of Modules 17.11.7 --- finitely presented and free at a point implies free nearby.
    checked_on: "2026-08-26"
    used_in: [ch01, ch03]

revisions:                     # findings that run backwards
  - target: ch01
    found_in: ch05
    what: >
      Definition 1.4's generality is contradicted by the use in §5.2.
    action: pending             # pending | note-only | rerun-requested | done

not_examined: >
  Appendices B and C. The long computation in ch04 §4.6 was not re-derived.
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
