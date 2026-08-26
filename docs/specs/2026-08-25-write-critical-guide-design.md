# Design — `write-critical-guide`

**Date:** 25 August 2026
**Status:** implemented, pending review and placement in the plugin repo

An automated pipeline producing a **critical guide** — working material for someone asked to
referee a paper, not a referee report — generalizing two hand-directed reviews:
`azumayification` (De Deyn, *The Azumification of orders*, arXiv:2606.05137v1) and
`c2-coalgebras` (Caradot–Lin, JPAA-D-25-00113).

---

## What the two originals did, and what each contributed

Both followed the same spine, and in both the critical-guide package was a **second act** — it came
after a full `write-paper-guide` pass, and the referee request was phrased as "use your
analysis of the paper so far." Both produced: a summary with context and significance; a
point-by-point issue list tagged and graded, partitioned mathematical / references /
typographical; three annotated copies of the paper's source carrying `\todo[inline]` notes;
and a typeset report PDF assembled by pandoc.

They diverged in ways that were complementary rather than contradictory, and the design takes
the union:

| | azumayification | c2-coalgebras | taken |
|---|---|---|---|
| Reference verification | every Stacks tag fetched and checked; a table of what came out **clean** | publisher front matter, DOIs, author bibliographies, dated | both, as Phase 2c |
| Severity | major / minor / trivial | potentially major / **dependent consequence** / minor | merged: grade × dependency, orthogonal |
| Repairs | folded into the issue text | separate document, plus a **four-branch dossier** with comparative synthesis | both: inline when one route, dossier when several |
| Pre-report analysis | direct | research context → dependency audit → repairs | folded into Phases 2b/2d |
| Source situation | authors' `.tex` available | **PDF-only submission**; annotated the public arXiv source, kept page/line refs to the submission | Phase 0 Cases A/B/C |
| Mechanics | `make-annotated.py`, asserted anchors, Makefile, README | hand-built | generalized into `annotate-tex` |

## The problem that blocked automation

Neither run ever wrote down *why* the reviewer knew what to look at. The findings came from the
guide-writing read, and lived only in conversation context. A fresh referee agent does not have
that, which is why the flow could not simply be re-run.

**Resolution:** the Phase 1 invocation asks the guide pass to keep a running concerns ledger —
every place it had to supply a missing step, reconstruct an argument, disambiguate a symbol, or
check a citation, recorded with a verbatim quotation as it happens. The reading becomes the
discovery pass and the ledger is the handoff. Phase 2b seeds from it, and works without it.

## Decisions

**One skill, not two.** `write-paper-guide` is invoked as an installed black box with a single
argument string that pre-answers its interactive steps. No variant or fork: installed versions
differ, and the referee skill must not depend on the guide's directory layout, filenames, or
chapter numbering. It inspects what is on disk afterwards.

**The reader is fixed.** An active researcher in a roughly adjacent field — comfortable with the
general area and its standard machinery, not a specialist in this corner, reading in order to
referee. Fixing it is what lets the run be unattended.

**No recommendation.** The guide never says accept, revise, or reject. Ordering the findings
by consequence is as close as it comes. Rationale: the reviewer decides the disposition, and a
generated verdict is both presumptuous and the part most likely to be wrong. Phase 4's ordering
of *mathematical* repair routes is in scope; it is advice about mathematics, not publication.

**Adversarial verification of major findings.** Three independent skeptics per candidate,
prompted to refute, defaulting to refuted when uncertain; two of three kill it. A referee report
naming a defect that is not there costs the authors weeks; a missed typo costs a reader
seconds. The errors are asymmetric and the process reflects that. Promotion runs too: a minor
finding a main theorem rests on is re-examined.

**`issues.yaml` as single source of truth.** The Markdown issue list and the annotated sources
are generated from it. In both originals these were maintained in parallel by hand, which is
what produced the instruction "double check the original document to make sure that they
actually apply." An anchor that no longer matches is now a hard error.

**Fully unattended.** Every decision defaulted; only failure to identify the paper halts a run.

## Pipeline

0. **Intake** — identify the paper; settle the annotation base (Case A authors' source; Case B
   PDF submission + public source, with every passage checked against the submission; Case C
   PDF only, no annotated sources).
1. **Read** — invoke `write-paper-guide` with the reader specification and the concerns-ledger
   request.
2. **Sweeps, parallel and mutually blind** — typographical; mathematical audit with dependency
   map; reference verification with clean-checks table and an explicit not-verified list;
   context and significance.
3. **Refute** — adversarial pass over every candidate major finding.
4. **Repairs** — conditional; fires only on a confirmed major issue with several candidate
   routes. One agent per route, then a synthesis naming which hypothesis is exact and which
   merely sufficient.
5. **Ledger** — consolidate to `issues.yaml`; `annotate_tex.py check` is a hard gate.
6. **Write and generate** — summary by hand; issue list and annotated sources generated;
   repairs; README; report PDF via pandoc.
7. **Build and verify** — two `pdflatex` passes with `bibtex`; note counts reconciled against
   the ledger; page counts and mtimes checked.

## Components

- `skills/write-critical-guide/SKILL.md` — the pipeline.
- `references/base-critical-guide.md` — prose mechanics, pairing with one voice. Carries the
  banned list, including the disposition vocabulary, "load-bearing", the definite-article magic
  word, and negative framing where positive carries the same content.
- `references/issue-model.md` — tag / grade / dependency / confidence, the anchor rule, and the
  `issues.yaml` schema.
- `references/package-templates.md` — Makefile, pandoc preamble and metadata, README skeleton.
- `references/lessons.md` — the toolchain failures, pre-solved.
- `tools/annotate-tex/annotate_tex.py` — generator. Carries every hardening the bespoke script
  had: unique-anchor assertion, math-aware insertion, caption sanitizing, inline index in place
  of `\listoftodos`. Adds: category-agnostic operation, table rendering for bulk copy-editing
  with per-issue lift-out, dependency map, clean-checks table, stale-aux clearing, and a
  `check` mode.

## Validated

`annotate_tex.py` was run against the real azumayification source with nine genuine issues
across three categories: all anchors resolved uniquely, all three annotated sources compiled on
the first pass with notes at the correct passages, and the generated issue list carried the
dependency map, clean-checks table, and scope caveat. A second run exercised table rendering
with a consequential item lifted out into a full entry, reproducing the original's `[T-33]`
treatment.

## Resolved after review

**"Load-bearing" is now banned family-wide.** It had been listed among `base-paper-guide.md`'s
*preferred* words while `base-body-of-work.md` banned it. All four prose bases now ban it with
one phrasing, and the prose uses across the paper, study, and workshop-state guides were
reworded.

**Categories are guidelines, not a schema.** `issue-model.md` gives the default three with
their colours and the reason they work — they split by what the author must *do* — and
licenses inventing others when the paper warrants. Phase 2's sweeps are likewise a starting
set.

**The build knowledge is inherited, not restated.** Phase 7 is the family publication pass
from `assets/commons/publication.md`; the local lessons file keeps only the referee-specific
delta.

**The name.** Originally `write-referee-report`. Renamed because the artifact is not a report:
it is the material a referee works from in writing one. The old name misdescribed the
deliverable and risked steering an agent into writing a signed verdict.
