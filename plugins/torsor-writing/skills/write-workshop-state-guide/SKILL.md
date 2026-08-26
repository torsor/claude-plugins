---
name: write-workshop-state-guide
description: Use to report where live workshop work stands — a docent's state-of-the-work guide built on a confidence-ledger spine, calibrated to a collaborator who must steer the work, written present-tense/dated/commit-stamped and published as a dated snapshot in the docent's guide/ stream. Output is the torsor house format (LaTeX → PDF, HTML, EPUB, Markdown). Triggers: "write up the state of the room", "where does the workshop stand", "state guide for <problem>".
argument-hint: [single room or whole workshop, and the reader]
---

You are helping the user write a **workshop state guide**: the docent's **state-of-the-work
guide**, one dated present-tense snapshot of where live research work stands, so a collaborator
deciding the next move can trust the picture. It shares the torsor design, commons scaffold,
four-format build, and `01-direct` voice of the `write-topic-guide` / `write-paper-guide`
siblings — but its subject is a *live room at a moment*, not a finished paper or a timeless idea.

The user has said: $ARGUMENTS

If it was not said, ask up front for **both** the grain (single room vs. whole workshop) and the
reader (the collaborator this snapshot is for) before proceeding.

Two framing rules govern everything below:

1. **Present-tense, dated, room-attributed — never timeless-authorial.** Write "as of
   `c29366e`, the room has verified X on the generic fibre; Y is staged for referee; Z is open,"
   never "the authors establish X." There are no timeless authors here, only a room at a moment;
   every claim the work depends on carries the commit or date it was last touched.
2. **Translate faithfully, never re-grade — the docent invariant.** The room owns the labels;
   the guide re-arranges and exposits them. Carry every confidence label and provenance tag
   verbatim; never silently upgrade a `[Conjectured]` to `[Proved]` because the prose wanted a
   stronger verb. When in doubt, under-claim.

## How it differs from `write-topic-guide`

Same A/B/C shape, commons scaffold, and four-format build as its sibling; the deltas:

| | `write-topic-guide` | `write-workshop-state-guide` |
|---|---|---|
| Corpus (Phase A) | external source PDFs → `source-notes/` | the room's own live record → `state-notes/` |
| Spine | a concept spine you **decide** | the **confidence ledger**, harvested from the room's labels (never decided) |
| Reader | a student learning an idea | a **collaborator steering live work** |
| Voice | third person, timeless | **present-tense, dated, commit-stamped** |
| Time | static | **structural** — a mandatory "what changed / what might change" |

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

Before doing anything else, read:

1. **Style — base mechanics + the chosen voice.** Composed from the torsor prose library:
   format/register mechanics plus one selectable voice. Read both
   `${CLAUDE_PLUGIN_ROOT}/assets/prose/base-state-guide.md` and
   `${CLAUDE_PLUGIN_ROOT}/assets/prose/voices/01-direct.md`. `base-state-guide.md` is where the
   register lives — the ledger-first framing, the five state questions, the no-premature-closure
   rule, the extended result-maxing ban-list. The tone shift is the point of this skill.
2. **Voice catalog** — `${CLAUDE_PLUGIN_ROOT}/assets/prose/README.md`, the available voices and
   how base+voice compose. `01-direct` is the default; use it unless the user asks otherwise.
3. **Canonical preamble + layout** — `${CLAUDE_PLUGIN_ROOT}/assets/reference/shelf-main.tex`,
   the definitive worked example for preamble, title page, part/chapter structure, and Makefile.
4. **Shared mechanics — the commons.** `${CLAUDE_PLUGIN_ROOT}/assets/commons/scaffold.md`
   (directory, Makefile, `.gitignore`, preamble, math block, STYLE.md assembly, vendored tools,
   build verification), `${CLAUDE_PLUGIN_ROOT}/assets/commons/lessons.md` (situational
   math-rendering lessons), `${CLAUDE_PLUGIN_ROOT}/assets/commons/publication.md`.
5. **Distill-first discipline** —
   `${CLAUDE_PLUGIN_ROOT}/skills/write-topic-guide/pre-summarization.md`: the isolated-subagent,
   distill-before-writing, review-every-digest, err-on-the-side-of-more procedure that governs
   Phase A. Its scanned-PDF machinery (vision-read, never OCR) **only bites** when a steering
   decision pulls an *external* background PDF — the internal record is markdown.

---

## Invocation modes

Ask up front which grain the snapshot covers:

- **single-room** — one problem-room's current state.
- **whole-workshop** — the workshop across all active rooms. Phase A fans out one subagent per
  active room; the confidence ledger spans rooms.

---

## Phase A — Distill the record → `state-notes/`

**The corpus is the workshop's own record, not external PDFs.** Dispatch one subagent per room
(in **single-room** mode, just the one; in **whole-workshop** mode, one per active room). Each,
in isolated context, reads that room's `journal.md`, `status.md` + `STATUS.json`, the latest
`handoffs/` (and any carrying unwritten state), the relevant `rounds/`, and the room's slice of
`canonical/result.md`, then writes a **label-faithful** digest to `state-notes/<room>.md`. The
digest is the point:

- **Every claim is carried over with its *exact* confidence label** (`[Formalized]` /
  `[Proved]` / `[Refuted]` / `[Verified]` / `[Conjectured]` / `[Heuristic]` / `[Open]`) **and
  its provenance tag** (`[Standard]` / `[Folklore]` / `[Published]` / `[Preprint]` /
  `[Premise]`) — never silently upgraded.
- **Stamp each claim with the commit/date it was last touched** — the present-tense, dated
  register depends on this.
- **Capture the graveyard**: dead ends, superseded branches, and — first-class — *recent
  corrections* (a correction is a valued output, not a failure).

**Review every digest for label-faithfulness** before building on it. A confident-but-wrong
carry-over (promoting a `[Conjectured]` to `[Proved]`) is worse than a flagged gap — it hides
the debt. `state-notes/` is a directory **distinct from** the docent's background `source-notes/`:
state digests are stamped live-record snapshots, source-notes are durable background. They
coexist beside `latex/`.

---

## Phase B — Reader, the ledger, synthesis

**Reader profile.** Reuse the docent's per-collaborator profile; record it verbatim into
`latex/reader-profile.md` (not compiled). The reader model is a **collaborator steering live
work**, so debt triage becomes: *what do they need to make the next judgment call?* Surface
decision points and forks, not just background. Default voice `01-direct` (read another voice
file if asked). Describe the reader — familiar-with, comfortable-with — never grade them.

**The confidence ledger replaces the concept spine.** It is assembled mechanically from the
state-notes' *existing* labels — every claim with its label + provenance + last-touched commit —
and arranged into four bands. The docent re-arranges and exposits; it **never re-grades**:

- **Solid** — `[Formalized]` / `[Proved]` / `[Verified]` (carry the confidence, and for
  `[Verified]` the range it was checked over). What the reader can build on now.
- **Provisional / just changed** — recently corrected or shifted; typically `[Conjectured]`.
- **Open / might still flip** — `[Open]` claims, plus *what is being checked that would move a
  label*.
- **Where to be skeptical** — staged-not-earned steps, depended-upon `[Preprint]` /
  `[Folklore]`, and the "if this framing is off, the approach is off too" risks.

State the ledger explicitly and get the user's agreement — it is the guide's map and the single
most consequential editorial choice (the analog of a concept spine, but harvested rather than
invented).

**The synthesis note → `state-notes/synthesis.md`.** A subagent reads all state-notes + the
ledger and writes, per band, which room/claim populates it, the cleanest *faithful* statement to
use, and where the record is ambiguous. It ends with three mandatory pieces: a **unified
notation/convention table** (rooms may clash — pin ONE, verified against a state-note, carry it
everywhere); a **what changed / what might change** section (recent corrections + active checks
that could flip a label — the live-work analog the topic guide has no need for); and a
**decision-points / forks list** for the human (the steering analog of the topic guide's gaps
list: the judgment calls the collaborator faces next).

---

## Phase C — Author and build

Authoring reuses the family commons and the four-format build **verbatim** (full build every
time). Scaffold per `${CLAUDE_PLUGIN_ROOT}/assets/commons/scaffold.md`; assemble STYLE.md from
`base-state-guide.md` + the chosen voice; consult
`${CLAUDE_PLUGIN_ROOT}/assets/commons/lessons.md` for math-rendering gotchas. Apply these deltas:

- **Placement — a new dated artifact, never an overwrite.** The guide lives at
  `guide/<YYYY-MM-DD>-<slug>-state/` in the docent's `guide/` stream, listed in `guide/INDEX.md`;
  a later state guide on the same room is a *new* dated artifact so the progression stays visible.
- **Structure is ledger-driven, not paper-driven.**
  - **Part I — the state map.** Lead with the ledger (Solid / Provisional / Open / Skeptical)
    as the reader's *first* orientation. Present-tense, dated, commit-stamped. No "here's the
    beautiful result" opening, ever.
  - **Part II — band-by-band walk-through.** One chapter per ledger band (or per live problem
    within a band), faithful to the record's labels, every claim carrying its commit/date stamp.
  - **A mandatory "what changed / what might change" chapter.** Recent corrections and active
    checks; dead ends and superseded branches are **first-class content here**, not footnotes
    (culture §13 "Protect The Quiet Good Idea" / §15 "Maintain Branches").
  - **Appendix — the reference card.** The ledger as a table (claim | label | provenance |
    last-touched commit | room) + notation reconciliation.
- **Title page** marks it "State of the Work as of `<date>` / `<commit>`", calibrated to
  `<reader>`; the colophon stays verbatim (`torsor lab` is the guide's author).
- **Scale with subagents** for a large whole-workshop guide (one per chapter, a progress ledger,
  final whole-guide **label-faithfulness** review), exactly as the topic guide does.

Build all four formats, run `make check`, and finish with the publication pass
(`${CLAUDE_PLUGIN_ROOT}/assets/commons/publication.md`). The deliverable is the four-format
output **plus** the `state-notes/` directory.

---

## Output structure

```
guide/<YYYY-MM-DD>-<slug>-state/
  Makefile  .gitignore  check-build.py       # from the commons scaffold
  state-notes/                               # KEPT deliverable — the live-record distillation
    <room-a>.md  <room-b>.md  ...            # label-faithful, commit-stamped digests
    synthesis.md                             # ledger map + notation + what-changed + forks list
  latex/
    main.tex  STYLE.md  reader-profile.md
    chapters/
      00-preface.tex
      01-state-map.tex                       # Part I — lead with the ledger
      02-...                                 # Part II — one chapter per ledger BAND
      NN-what-changed.tex                    # mandatory: corrections + active checks + graveyard
      99-ledger-and-reference.tex            # the ledger as a table + notation reconciliation
  tex2torsor/                                # copied from the plugin (commons scaffold)
  html/  epub/  markdown/                    # build output
```

`guide/INDEX.md` lists it chronologically and by topic (per `guide/README.md`).

---

## Common mistakes

| Mistake | Do instead |
|---|---|
| Writing from the raw journals/rounds in your own context | Distill each room into `state-notes/*.md` via isolated subagents first (Phase A) |
| Silently upgrading a `[Conjectured]` to `[Proved]` while expositing | Carry every label **verbatim**; the docent translates, never re-grades |
| Leading with "the beautiful result" | Lead with the **confidence ledger** (Solid / Provisional / Open / Skeptical) |
| Timeless "the authors establish X" voice | Present-tense, dated, commit-stamped: "as of `<commit>`, the room has X" |
| Burying corrections and dead ends in footnotes | Make them a **first-class chapter** ("what changed / what might change") |
| Result-maxing rhetoric ("contribution," "pulled it off," "impressive") | Use the five state questions; obey the extended ban-list + no-premature-closure rule |
| Overwriting last week's state guide | Write a **new dated artifact**; progression must stay visible |
| Guessing the build toolchain | Reuse the commons scaffold (`latexd`→`latexmk`, `tex2torsor`, pandoc) + `lessons.md` |
| Throwing away the distillation | Keep `state-notes/` as a deliverable, distinct from background `source-notes/` |

---

## What stays the same as the manual family

Same torsor preamble (Solarized Cézanne, Garamond/Cabin, box styles, `\code{}`), math block
(theorem environments, `pitfallbox`), `tex2torsor` + HTML design, `latexd` (→ `latexmk`) /
pandoc (EPUB + Markdown) / `lab-view` toolchain, publication pass, `torsor lab` credit, and
colophon page — all inherited verbatim via the commons scaffold. Unique to the state guide: the
**confidence ledger** as its spine, the **present-tense, dated, commit-stamped** register, the
mandatory **what changed / what might change** section, and the collaborator-steering reader.
A reader moving between a tool manual, a paper guide, a topic guide, and a state guide should
feel the same hand at work.
