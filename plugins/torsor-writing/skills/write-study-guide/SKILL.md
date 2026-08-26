---
name: write-study-guide
description: Use when the goal is a personalized study guide that ROUTES a specific reader through one large tag-addressable corpus (the Stacks project, Kerodon) toward a target result or topic — spine computed from the corpus citation graph pruned by the reader's frontier, calibrated to a persistent reader profile. Output is the torsor house format (LaTeX → PDF, HTML, EPUB, Markdown). Triggers: "make a study guide to X in the Stacks project", "what should <reader> read to get to <result>", "route me through Kerodon to Y".
argument-hint: [target topic/result, the corpus, and the reader (profile file or description)]
---

You are helping the user write a **study guide**: a personalized route through one large,
tag-addressable corpus — the Stacks project, Kerodon, or a similar reference with
addressable chunks and a citation structure — bringing one named reader from what they
already know to a target result or topic. It shares the torsor design and voice of the
family, and the two framing rules of `write-paper-guide` carry over unchanged:
third person about the corpus (the authors prove; Tag 01JF establishes), and the guide
is a companion, never a contribution. The guide's "you" addresses the *reader*.

The user has said: $ARGUMENTS

If the target, corpus, or reader is missing, ask before proceeding.

## What this is, and how it differs from write-topic-guide

`write-topic-guide` synthesizes several scattered sources into one exposition — it must
*carry* the exposition, because no single source does. A study guide's corpus already
contains excellent exposition with explicit dependencies; the guide's value is
**selection, ordering, motivation, and triage**. Four things are unique to this skill:

1. **A persistent reader profile.** The reader's background and per-corpus *frontier*
   (what they already know, in the corpus's own coordinates) live in a profile file that
   outlives any one guide. Profiles are reused, updated, and — for non-personal
   "archetype" profiles — shareable.
2. **A computed spine.** The route comes from the corpus citation graph — dependency
   closure of the targets, pruned by the frontier — not from editorial synthesis. The
   model edits the route; it does not invent it.
3. **Triage as the core editorial act.** Citation is not pedagogical dependence. The
   guide marks every stop: read closely / skim / black-box for now.
4. **Checkpoints that move the frontier.** Each milestone ends with a checkpoint; a
   passed checkpoint is a frontier update back into the profile.

## The shape of the job

```
Phase 0  Reader profile: load or create, reconfirm the frontier   -> reader-profile snapshot
Phase A  Targets -> route -> milestones -> triage                 -> the spine (user-approved)
Phase A' Targeted digests of the spine's tags                     -> source-notes/*.md
Phase B  Author + build (commons scaffold, four formats)          -> the guide
Close    Offer the frontier update                                -> profile log + commit
```

---

## Reference materials — read these first

1. Style: `${CLAUDE_PLUGIN_ROOT}/assets/prose/base-paper-guide.md` + the chosen voice
   (default `01-direct`; catalog in `assets/prose/README.md`).
2. Commons: `${CLAUDE_PLUGIN_ROOT}/assets/commons/scaffold.md` (required before
   Phase B), `assets/commons/lessons.md` (math-rendering and `latexd` gotchas — a study
   guide is always math-heavy), `assets/commons/publication.md`.
3. Layout reference: `${CLAUDE_PLUGIN_ROOT}/assets/reference/shelf-main.tex`.

---

## Phase 0 — The reader profile

**If a profile file was given or a profile collection exists,** read the profile. A
profile has a prose Background (calibrates tone and depth — it plays the role of
`write-paper-guide`'s Step 2 answers), per-corpus Frontier blocks (fenced YAML, the
machine contract below), and a dated Log. Ask the user where their reader-profiles
collection lives the first time; do not assume a path.

**If no profile exists for this reader,** run the interview — `write-paper-guide`
Step 2's question batch, plus one more: *the frontier in the corpus's coordinates*
(which chapters they could pass a qual on, which specific tags/sections they know
beyond those). Then **create the profile file** in the user's collection (offer to
create the collection itself if none exists) — every guide leaves a profile behind, so
the interview never runs twice for the same reader.

**Reconfirm the frontier — always.** A profile is a memory, not an authority. Show the
frontier and ask "still right?" before computing anything. One question here is cheap;
a guide calibrated to a stale frontier wastes the whole build. Mark uncertain entries
`[CHECK]` rather than guessing.

The frontier contract (what the graph tooling consumes):

```yaml
corpus: stacks
known_chapters: [algebra, schemes, morphisms]   # file stems — whole chapter known
known_sections: []                              # section tags known beyond those
known_tags: ["01JF"]                            # individual tags beyond those
```

Once the guide directory exists, **snapshot** the profile into
`latex/reader-profile.md` with provenance (source file, date, and commit if the
collection is a git repo). The canonical copy stays in the collection; the guide
carries the frozen version it was calibrated to.

---

## Phase A — Targets, route, spine

### Choose the destination

Mapping "I want to understand X" to concrete target tags is **not a retrieval
problem** — the corpus surrounds every canonical result with near-duplicate variants.
Work in this order:

1. **Propose targets from knowledge.** Name the landmark results and their approximate
   home chapters yourself.
2. **Verify against the corpus.** Use the corpus tooling to pin exact tags and catch
   omissions — for the Stacks project, `stacks-search` (semantic `query`, the chapter
   catalog, and `revdeps` for "what cites this" as a canonicality check). Search is the
   verifier and expander, not the selector. High in-degree marks the summit; its lemma
   swarm is not the destination.
3. **Confirm the targets with the user** in one line each: tag, statement gist, why
   it's the destination.

### Compute the route

Extract the profile's frontier block for this corpus into a file, then:

```
stacks-search route <tag> [<tag>...] --frontier frontier.yaml --json
```

The JSON gives the pruned closure in topological order (dependencies first), grouped by
chapter, each tag enriched with `env_type`, `title`, section, and `in_degree`. Two
things to know: the output **excludes the target tags themselves** — re-add them as the
final milestone — and it may carry cycle warnings (take the stated order as advisory
there). If the graph index is missing, run `stacks-search refresh-graph <corpus-dir>`
first; if the corpus has no graph tooling at all, fall back to editorial routing (your
knowledge + search + the table of contents) and *say so in the preface* — the reader
should know the route wasn't computed.

### Triage and cluster — the edit that carries the guide

The route is a **superset skeleton**: citation edges encode citation, not what a
learner must internalize. Edit it hard:

- **Cluster** the surviving tags into milestones — 4–10 coherent units, each a real
  conceptual step (often but not always chapter-aligned). The milestone sequence is the
  guide's Part II.
- **Triage every stop:** *read closely* (the engine results and definitions), *skim*
  (statements needed for context; trust the proofs), *black-box for now* (cite it, use
  it, return later — say when "later" is). The frontier already cut the closure once;
  honest triage cuts it again. Both cuts are where personalization does its work.
- **In-degree is your canonicality signal** — a tag cited from many later chapters is
  central; a depth-7 technical lemma with in-degree 1 is a black-box candidate.

**Present the spine to the user** — numbered milestones, each with its tags and triage
marks and one sentence of why it's on the path — and get agreement before writing
anything. This is the same gate as `write-topic-guide`'s concept spine.

---

## Phase A′ — Targeted digests

Pre-summarize **only the spine's read-closely and skim tags** into
`<guide-dir>/source-notes/<milestone>.md` — statements with exact tag numbers, proof
spines of the engine results, a notation key. The corpus is text-layer LaTeX with small
chunks, so this is far lighter than `write-topic-guide`'s Phase A: dispatch one
subagent per milestone (or do it inline for a short spine), and review each digest for
faithfulness before building on it. Follow the same rules as
`write-topic-guide`/`pre-summarization.md` where they apply: exact refs everywhere,
`[CHECK]` for anything uncertain, err on the side of more. Keep `source-notes/` as a
deliverable.

A single-corpus guide rarely has clashing conventions, so no synthesis note is needed —
the route JSON plus the digests play that role. If notation *does* shift across the
corpus's chapters, pin one convention in the appendix as topic-guide does.

---

## Phase B — Author and build

Scaffold and build per the commons: **REQUIRED** —
`${CLAUDE_PLUGIN_ROOT}/assets/commons/scaffold.md` (with the **math block**: theorem
environments and `pitfallbox`), verification per `make check`, and the publication pass
(`assets/commons/publication.md`) before the guide is called done. Genre parameters:

- **Chapters:**
  ```
  00-preface.tex                    ← who this is for, the destination, how to use it
  01-the-route-at-a-glance.tex      ← Part I: the whole spine as an intuition map — why
                                      each milestone exists, no proofs; plus what was
                                      deliberately left out (the black-box ledger)
  02-<milestone>.tex ... N-<milestone>.tex   ← Part II: one chapter per milestone
  99-tag-map-and-notation.tex       ← appendix: guide chapters ↔ tags, all deep-linked
  ```
- **Makefile:** genre comment `# <topic> study guide`; EPUB
  `--metadata title="A Study Guide: <topic>"`; `pdftitle` to match.
- **STYLE.md:** assemble from `base-paper-guide.md` + the chosen voice.
- **Title page:** adapt `write-paper-guide`'s, crediting the corpus as the subject —
  "A Study Guide / <topic> in <the Stacks project>" — with the one-line orientation
  naming the reader profile's reader. Colophon verbatim per the scaffold.
- **Deep links.** Every tag mention links into the corpus. Define once in the preamble:
  ```latex
  \newcommand{\stag}[1]{\href{https://stacks.math.columbia.edu/tag/#1}{\code{#1}}}
  % Kerodon: \newcommand{\ktag}[1]{\href{https://kerodon.net/tag/#1}{\code{#1}}}
  ```
  and use `\stag{01JF}` throughout. The HTML build is where these shine; check a few in
  the publication pass.

**Each Part II chapter:** opens with why this milestone is on the path (why before
what); walks its read-closely tags via `paperthm`/`paperdefn` restatements that always
carry the tag number; names where the difficulty lives; marks skim and black-box stops
explicitly (`notebox` for easily-missed, `pitfallbox` for the subtlety that trips
people); and **ends with a checkpoint** — a short `notebox` beginning
`\textbf{Checkpoint.}` stating what the reader should now be able to do without
looking ("prove \stag{023N} for the affine case"). Write from the digests, not the raw
corpus. Show the user Part I, then chapters as they come — same review rhythm as the
rest of the family. For a long spine, one subagent per chapter with a progress ledger
and a final faithfulness review, as in `write-topic-guide` Phase C.

---

## Close — move the frontier

When the guide is delivered (and later, when the reader reports progress), offer the
profile update: checkpoints passed become `known_tags`/`known_chapters` entries, with a
dated Log line, and a commit if the collection is a git repo. The guide is a build
product; the profile is the durable artifact — this closing step is what makes the
*next* guide for this reader start further along.

---

## Common mistakes

| Mistake | Do instead |
|---|---|
| Picking targets by embedding similarity | Propose from knowledge; verify with search + `revdeps`; confirm with the user |
| Treating the route JSON as the reading list | It is a superset skeleton — cluster, triage, cut |
| Skipping the frontier reconfirmation | One question vs. a wasted book; profiles are memories, not authorities |
| Writing from the raw corpus | Digest the spine's tags into `source-notes/` first; write from the digests |
| Re-expounding what the corpus explains well | Route and motivate; the corpus carries the exposition — link into it |
| Forgetting the targets aren't in the route output | Re-add them as the final milestone |
| Silent black-boxing | Every black-box is named in the chapter AND in Part I's ledger, with when to return |
| Ending a guide without offering the profile update | The frontier moving is the point of the system |

## What stays the same as the family

Same torsor preamble and math block, commons scaffold / build toolchain / publication
pass, `torsor lab` credit and colophon, third-person-about-the-sources voice, and the
review rhythm. A reader moving between a manual, a paper guide, a topic guide, and a
study guide should feel the same hand at work.
