# Design — `write-workshop-state-guide`

**Date:** 2026-07-03
**Status:** approved, ready for implementation plan
**Repo:** `torsor-writing-plugin` (plugin content under `plugins/torsor-writing/`)

---

## 1. What it is

A new writing skill in the torsor-writing plugin: the **docent's state-of-the-work guide**.
It produces a *dated snapshot* of where a live workshop problem (or a whole workshop) stands,
organized by a **confidence ledger**, calibrated to a collaborator who needs to **steer** the
work — not a reader appreciating a finished paper.

It is a true **sibling to `write-topic-guide`**: same commons scaffold, same four-format
torsor build (full, every time), same `01-direct` voice. What is genuinely new is the
**register** (a state/present-tense voice that rewards calibration and bans premature closure)
and the **spine** (the confidence ledger, not a concept spine).

It belongs to the workshop method's **docent** role (`method/roles/docent.md` in the
workshop-template). The docent "translates faithfully" and "does not re-judge math." This skill
enforces exactly that: it re-arranges and exposits the room's *own* labels; it never re-grades a
claim.

### How it differs from its two siblings

| | `write-paper-guide` | `write-topic-guide` | `write-workshop-state-guide` |
|---|---|---|---|
| Subject | one finished paper | one idea across many sources | one live workshop/room's current state |
| Corpus (Phase A) | the paper | external source PDFs → `source-notes/` | the room's own record → `state-notes/` |
| Spine | the paper's sections | a concept spine you decide | the **confidence ledger** (harvested, not decided) |
| Reader model | someone reading/refereeing a finished result | a student learning an idea | a **collaborator steering live work** |
| Voice | third person, timeless ("the authors prove") | third person, timeless | **present-tense, dated, commit-stamped** ("as of `c29366e`, the room has verified X") |
| Time | static | static | **structural** — "what changed / what might change" is mandatory |

---

## 2. Files

New and reused files, all within `plugins/torsor-writing/`.

| File | Status | Notes |
|---|---|---|
| `skills/write-workshop-state-guide/SKILL.md` | **new** | the skill entry point (A/B/C phases re-aimed at the live record) |
| `assets/prose/base-state-guide.md` | **new** | the register/framing mechanics — the sibling to `base-paper-guide.md`; this is where the tone shift lives |
| `assets/prose/voices/01-direct.md` | reused **verbatim** | default voice, unchanged |
| `skills/write-topic-guide/pre-summarization.md` | reused (discipline) | isolated-subagent / distill-first / review-every-digest / err-on-more discipline applies; its **scanned-PDF machinery only bites** when a steering decision pulls an external background PDF (the internal record is markdown — no vision-read/OCR needed) |
| `assets/commons/scaffold.md` | reused **verbatim** | directory, `.gitignore`, Makefile, preamble, math block, STYLE.md assembly, `tex2torsor` + `check-build.py` |
| `assets/commons/lessons.md` | reused **verbatim** | math-rendering / `latexd` gotchas |
| `assets/commons/publication.md` | reused **verbatim** | final publication pass |
| `assets/prose/README.md` | **edit** | list `base-state-guide.md` in the composition map |
| `.claude-plugin/plugin.json` | **edit** | add the skill to the description; bump version |

**Style composition** (same seam as the other guides): effective style =
`base-state-guide.md` + `voices/01-direct.md`, assembled into the guide's `latex/STYLE.md`
with a header recording the voice. Default voice `01-direct` unless the user asks otherwise.

---

## 3. The three phases

Same A/B/C shape as `write-topic-guide`, re-aimed at the live record. Do them in order.

### Phase A — Distill the record → `state-notes/`

**The corpus is the workshop's own record, not external PDFs.** Dispatch one subagent per
room (in single-room mode, just the one; in whole-workshop mode, one per active room). Each
subagent, in isolated context, reads that room's:

- `journal.md` (append-only narrative — tried/worked/failed/dead-ends)
- `status.md` + `STATUS.json` (the state cards)
- `handoffs/handoff-<date>.md` (the latest, and any that carry unwritten state)
- relevant `rounds/round-N.md` entries
- the room's slice of `canonical/result.md`

and writes a **label-faithful** digest to `state-notes/<room>.md`. The digest is the point:

- **Every claim is carried over with its *exact* confidence label** (`[Formalized]` /
  `[Proved]` / `[Refuted]` / `[Verified]` / `[Conjectured]` / `[Heuristic]` / `[Open]`) **and
  its provenance tag** (`[Standard]` / `[Folklore]` / `[Published]` / `[Preprint]` /
  `[Premise]`) — never silently upgraded.
- **Stamp each claim with the commit/date it was last touched** (present-tense, dated voice
  depends on this).
- **Capture the graveyard**: dead ends, superseded branches, and — first-class — *recent
  corrections* (the `$I_1$` inversion is the paradigm case: a correction is a valued output,
  not a failure).

**Review every digest for label-faithfulness** before building on it. A confident-but-wrong
carry-over (promoting a `[Conjectured]` to `[Proved]`) is worse than a flagged gap — it hides
the debt. `pre-summarization.md` governs the isolation/distill discipline.

`state-notes/` is a **distinct directory** from the docent's background `source-notes/`
(confirmed): state digests are live-record snapshots, stamped and label-faithful; source-notes
are durable background digests. They coexist beside `latex/`.

### Phase B — Reader, the ledger, synthesis

**Reader profile.** Reuse the docent's per-collaborator profile (human-authored, living).
Record verbatim into `latex/reader-profile.md` (not compiled). The reader model is a
**collaborator steering live work**, so debt triage becomes: *what do they need to make the
next judgment call?* Surface decision points and forks, not just background.

**The confidence ledger replaces the concept spine.** It is **assembled mechanically from the
state-notes' existing labels** — harvest every claim with its label + provenance + last-touched
commit — and arranged into four bands. The docent re-arranges and exposits; it **never
re-grades**:

- **Solid** — `[Formalized]` / `[Proved]` / `[Verified]` (carry the confidence, and for
  `[Verified]` the range).
- **Provisional / just changed** — recently corrected or shifted; typically `[Conjectured]`.
- **Open / might still flip** — `[Open]`, plus *what is being checked that would move a label*.
- **Where to be skeptical** — staged-not-earned, load-bearing `[Preprint]`/`[Folklore]`, and
  the "if this framing is off, the approach is too" risks.

State the ledger explicitly and get the user's agreement — it is the guide's map, and the
single most consequential editorial choice (analogous to the concept spine in topic-guide,
but harvested rather than invented).

**The synthesis note → `state-notes/synthesis.md`.** A subagent reads all state-notes + the
ledger and writes, per band: which room/claim populates it, the cleanest *faithful* statement
to use, and where the record is ambiguous. It ends with three mandatory pieces:

- a **unified notation/convention table** — rooms may clash; pin ONE, verified against a
  state-note, carry it everywhere;
- a **what changed / what might change** section — recent corrections + active checks that
  could flip a label (this is the live-work analog that `write-topic-guide` has no need for);
- a **decision-points / forks list** for the human — the steering analog of topic-guide's
  gaps list: the judgment calls the collaborator faces next.

### Phase C — Author and build

Authoring reuses the family commons and the four-format build **verbatim** (full build every
time — confirmed). Scaffold per `assets/commons/scaffold.md`; take title-page / reader-profile
/ outline conventions from the guide genre; consult `lessons.md` for math-rendering gotchas.
Deltas:

- **Placement.** A *new dated artifact* in the docent's `guide/` stream:
  `guide/<YYYY-MM-DD>-<slug>-state/` (a multi-format directory), listed in `guide/INDEX.md`.
  **Never an overwrite** — a later state guide on the same room is a new dated artifact, so the
  progression stays visible (matches `guide/README.md`). `state-notes/` sits beside `latex/`.
- **Structure is ledger-driven.**
  - **Part I — the state map.** Lead with the ledger (Solid / Provisional / Open / Skeptical)
    as the reader's *first* orientation. Present-tense, dated, commit-stamped. No "here's the
    beautiful result" opening.
  - **Part II — the band-by-band walk-through.** One chapter per ledger band (or per live
    problem within a band), faithful to the record's labels, every claim carrying its
    commit/date stamp.
  - **A mandatory "What changed / what might change" chapter.** Recent corrections and active
    checks. Dead ends and superseded branches are **first-class content here**, not footnotes
    (culture §13 "Protect The Quiet Good Idea" / §15 "Maintain Branches").
  - **Appendix — the reference card.** The ledger as a table (claim | label | provenance |
    last-touched commit | room) + notation reconciliation.
- **Scale with subagents** for a large whole-workshop guide (one per chapter, progress ledger,
  final whole-guide **label-faithfulness** review), exactly as `write-topic-guide` does.
- **Title page** marks it "State of the Work" as of `<date>` / `<commit>`, calibrated to
  `<reader>`. Colophon stays verbatim (`torsor lab` is the guide's author).

Build all four formats, `make check`, and finish with the publication pass. Deliverable is the
LaTeX/PDF/HTML/EPUB/Markdown **plus** the `state-notes/` directory.

### Two invocation modes (confirmed)

The skill asks at invocation which grain:

- **Single-room** — one problem-room's current state.
- **Whole-workshop** — the workshop across all active rooms (Phase A fans out one subagent per
  room; the ledger spans rooms).

---

## 4. The register — `base-state-guide.md`

This new base file replaces `base-paper-guide.md`'s framing for a state guide. It is
voice-independent (pairs with any `voices/*.md`). Its distinctive content:

### The five state questions (replace the six paper questions)

Rewarding **calibration**, not appreciation:

1. **What's being attempted** — the *question*, not "the contribution."
2. **What's solid right now, at what confidence** — the ledger, up front.
3. **What's provisional / just changed** — recent corrections and shifts.
4. **What's open or might still flip** — and what's being checked that would move a label.
5. **Where to be skeptical** — what a careful reader should distrust; what's staged-not-earned.

"Why it's hard / plausible" is **demoted to optional**. "Why it's new" and "why the authors
pulled it off" are **cut entirely**.

### Framing rules

- **Attribute to the room and the moment, not timeless authors.** "As of `c29366e`, the room
  has verified X on the generic fibre; Y is staged for referee; Z is open." Present-tense,
  dated, commit-stamped.
- **Lead with the ledger.** The confidence ledger is the map, not an appendix.
- **Labels and provenance carried verbatim.** Ban "establishes / proves" for *provisional*
  units — those words are earned only by `[Proved]`/`[Formalized]`.
- **A correction is a valued output, not a failure.** The "what changed / what might change"
  section is mandatory; normalizing corrections is directly anti-result-maxing.
- **Dead ends and superseded branches are first-class**, per culture §13/§15.
- **Reader = collaborator steering live work.** Surface decision points / forks for the human.

### Extended ban-list (beyond `base-paper-guide.md`'s filler list)

Ban the **result-maxing rhetoric**, not just filler words: "contribution," "why it's new,"
"pulled it off," "impressive," "breakthrough," and any summary that reads as **"done"** when
the work is live. Add a **no-premature-closure rule**.

Contrast (the tone shift, concretely):

- *Now (result-maxing):* "The room's contribution is to make both things concrete… Why it is
  new… Why the room could pull it off: because it named the right function."
- *State register:* "As of `c29366e`, the room has an explicit `$f$` for `$n=4,5,6$`, verified
  on the generic fibre. Whether these are the model-level covers is open. The move that made it
  compute was reading `$f$` as the Miller function — flagged because if that framing is off, the
  approach is too."

### Kept from `base-paper-guide.md` (orthogonal to the tone problem)

The source-notes pre-summarization discipline; the synthesis + gaps list; the four-format
torsor build (format, not framing — reuse the commons scaffold verbatim); faithful
confidence/provenance labels; the reader profile; "describe the reader, don't grade them";
"distill first"; the shared preamble / math block / toolchain / colophon.

---

## 5. Output structure

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

`guide/INDEX.md` lists it chronologically + by topic (per `guide/README.md`).

---

## 6. Common mistakes (for the SKILL.md table)

| Mistake | Do instead |
|---|---|
| Writing from the raw journals/rounds in your own context | Distill each room into `state-notes/*.md` via isolated subagents first (Phase A) |
| Silently upgrading a `[Conjectured]` to `[Proved]` while expositing | Carry every label **verbatim**; the docent translates, never re-grades |
| Leading with "the beautiful result" | Lead with the **ledger** (Solid / Provisional / Open / Skeptical) |
| Timeless "the authors establish X" voice | Present-tense, dated, commit-stamped: "as of `<commit>`, the room has X" |
| Burying corrections and dead ends in footnotes | Make them a **first-class chapter** (what changed / what might change) |
| Result-maxing rhetoric ("contribution," "pulled it off," "impressive") | Use the five state questions; obey the extended ban-list + no-premature-closure rule |
| Overwriting last week's state guide | Write a **new dated artifact**; progression must stay visible |
| Guessing the build toolchain | Reuse the commons scaffold (`latexd`→`latexmk`, `tex2torsor`, pandoc) + `lessons.md` |
| Throwing away the distillation | Keep `state-notes/` as a deliverable, distinct from background `source-notes/` |

---

## 7. What stays the same as the manual family

Same torsor preamble (Solarized Cézanne, Garamond/Cabin, box styles, `\code{}`), the math
block (theorem environments, `pitfallbox`), `tex2torsor` + HTML design, the `latexd`
(→ `latexmk`) / pandoc (EPUB + Markdown) / `lab-view` toolchain, the publication pass, the
`torsor lab` credit, and the colophon page — all inherited verbatim via the commons scaffold.
A reader moving between a tool manual, a paper guide, a topic guide, and a state guide should
feel the same hand at work.
