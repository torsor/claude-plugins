# Design note — the unified builder core, parked for later, 27 August 2026

*A forward-looking note, not a status of shipped work. There is a second, unmerged line of
development — a DRY "unified builder core" — that reimagines how every document builds. It is
complete and green on its own branch but deliberately **not** merged: `main` builds fine today
the hand-scaffold way, and adopting the core would mean editing the skills, which we are not
doing yet. This records the design goal and the reconciliation analysis so a future session
picks up with full context instead of re-deriving it.*

## Where the work lives

- Branch: **`feat/unified-builder-core`** (pushed to origin; based on `main` at `11cd4ac`,
  now behind).
- The core itself: `plugins/torsor-writing/tools/core/` — `base/` + `features/` + `formats/`
  + `genres/`, plus `assemble.py`, `frontend_markdown.py`, `check-build.py`, `normalize_tables.py`.
- Its contract/spec: `docs/specs/2026-07-15-unified-builder-contract-design.md` (on the branch).
- A green, self-contained regression fixture: `tools/core/test/smoke/` (on the branch).

Nothing here is on `main`. `main` is untouched by it.

## The design goal worth keeping

Separate **authoring** (structure, prose, calibration — expensive) from the **mechanical
build** (scaffold, Makefile, tooling, every output format — cheap and identical across genres),
and make the mechanical half DRY and modular so features/formats/voices/genres can be added
without tangling. Organizing principles:

- Four orthogonal axes: **formats** (pdf/html/epub/epub-svg/md), **features**
  (math/callouts/listings/bib), **voices**, **genres** (feature bundles).
- **Feature co-location:** a feature owns its slice in every format (preamble fragment,
  tex2torsor mapping, CSS, make fragment) in one directory — adding one never edits a monolith.
- **Assemble, don't branch:** `main.tex` / mappings / CSS / Makefile are concatenated from
  fragments; the Makefile `include`s wildcards and features self-register their targets.
- LaTeX tree stays the canonical intermediate (a LaTeX-first primary source is still the right
  call); Markdown is one front-end that produces it.

## Why it is not merged: two build models in the same layer

`main` builds the **hand-scaffold** way: each skill reads `assets/commons/scaffold.md` and
hand-writes the doc's `Makefile` + `main.tex`, copies `tex2torsor`/`check-build.py` in per-doc,
then runs `make pdf html epub md check`. `main` has **zero** references to the core.

The core **replaces exactly that layer** (author `chapters/` + `build.yaml` →
`assemble.py --in-place` → `make all`). So the two overlap where they meet — README, the six
house-doc SKILL.md build sections, `base-body-of-work.md`, `.gitignore` — and can't both be
true at once. That is the whole reason a merge is a design decision, not a mechanical one.

## Reconciliation analysis (so we don't redo it)

The 10 skills fall into three tiers against the core's genres (manual, paper-guide, topic-guide,
study-guide, body-of-work, state-guide, technical-doc):

- **Tier 1 — already rewired on the branch** (manual, paper-guide, topic-guide, study-guide,
  body-of-work, workshop-state-guide). Cost = *merge only*: keep `main`'s new
  "Locating the shared assets" block + prose, re-express the build section as the core flow.
- **Tier 2 — natural additions** (`write-pure-math-paper`, `write-technical-report`). Cost =
  *net-new construction*: two new core genres, place their prose bases (they live in each
  skill's `references/base-*.md`, not `assets/prose/`), rewrite the build sections, test-build.
- **Tier 3 — a different artifact class** (`write-critical-guide`, `write-paper-repairs`).
  These operate on an **external** paper: critical-guide runs a 934-line `annotate_tex.py` and
  emits annotated copies via its own `references/package-templates.md`; paper-repairs injects
  tracked-change markup (`agentic-edits.tex`) into the paper's own source. They do **not** fit
  "our chapters → our house formats" and probably should stay **off** the core rather than
  bloat it. This shrinks any core adoption from 10 skills to ~8.

**Coupling constraint:** because every house-doc skill reads `scaffold.md`, swapping it for the
core contract is **all-or-nothing** for those ~8 — you cannot half-migrate and leave a coherent
`scaffold.md`.

**Standing tension:** adopting the core *inherently* edits the skills' build sections. Any
future move has to reconcile that with the "don't rewrite the working skills out from under us"
instinct — the migration must be surgical and content-preserving, not a wholesale replacement.

## When we revisit

Open question to decide first: **adopt the core as the build layer (and migrate the ~8
house-doc skills), or keep the hand-scaffold model and retire the branch?** If adopt: rebase the
branch onto current `main`, do the Tier 1 merges, build the Tier 2 genres, leave Tier 3 alone,
cut over `scaffold.md` once, and PR. If retire: keep the branch as a reference and delete this
open thread. Until then, `main` is the source of truth and nothing is broken.
