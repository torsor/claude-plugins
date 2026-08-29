---
name: write-pure-math-paper
description: Use when the goal is to author, organize, or substantially rewrite an original research paper or short note in pure mathematics from theorem statements, proofs, research notes, computations, references, or an existing manuscript. Build a rigorous paper around the main result, proof architecture, precise comparison with prior work, theorem dependencies, hypotheses, examples, applications, and open boundaries. Preserve proof status and flag gaps rather than inventing repairs. Output is the torsor house format (LaTeX → PDF, HTML, EPUB, Markdown).
---

**Family stance — read `${CLAUDE_PLUGIN_ROOT}/assets/commons/stance.md` before writing any
prose.** It binds every genre in this plugin and settles four things this file assumes rather
than states: that the document has no author and so no first person, that it does not address
its reader, that calibration is not content, and that a supplied PDF is the artifact under
study while its source is an aid.

You are helping the user write an **original pure mathematics paper**. The paper must let a
professional mathematician who did not participate understand the main theorem, see why it
matters, locate the new idea, audit the proof's difficult points, distinguish proved statements
from heuristics or open claims, and place the result precisely relative to prior work.

The user has said: $ARGUMENTS

If no mathematical source material was identified, ask for the theorem/result and the available
proofs, notes, computations, references, or manuscript before proceeding. If the intended
audience is unspecified, default to a professional mathematician near the broad area but outside
the immediate project.

Five rules govern the paper:

1. **Preserve mathematical truth before improving prose.** Never silently repair a gap,
   strengthen a theorem, weaken a hypothesis, or promote a heuristic.
2. **Lead with the problem and result, not notation or discovery history.** Organize by the
   conceptual dependency of the mathematics.
3. **State every result at its earned status.** Separate theorem, proof sketch, computational
   verification, heuristic, conjecture, and open question.
4. **Make proof architecture and hypothesis use visible.** The reader should know what does the
   work and where each delicate assumption enters.
5. **Compare with prior work precisely.** Do not infer novelty from missing citations or use a
   citation as a substitute for explaining the mathematical difference.

## The shape of the job

```
Phase 0  Scope the paper and freeze its sources       -> paper brief + source inventory
Phase A  Audit the mathematical content               -> paper-notes/*.md
Phase B  Fix the nine-sentence story and outline      -> user-approved architecture
Phase C  Author in dependency-aware passes            -> the paper in four formats
Phase D  Run integrity and publication audits         -> issue-free evidence report
```

Do these in order. Phase A is a truth gate: unresolved mathematical issues stay visible and
block any prose that would depend on them.

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

1. **Paper mechanics.** Read
   [references/base-pure-math-paper.md](references/base-pure-math-paper.md). It defines the
   original-research register, progressively specialized audience, theorem/proof exposition,
   notation, attribution, and report-status language.
2. **The chosen voice.** Read
   `${CLAUDE_PLUGIN_ROOT}/assets/prose/voices/01-direct.md` and
   `${CLAUDE_PLUGIN_ROOT}/assets/prose/README.md`. Use `01-direct` by default, tightened for a
   research article: point-first and readable, without manual-style direct address or incidental
   humor in formal mathematics.
3. **Canonical visual family.** Read
   `${CLAUDE_PLUGIN_ROOT}/assets/reference/shelf-main.tex`,
   `${CLAUDE_PLUGIN_ROOT}/assets/reference/shelf-00-preface.tex`, and lines 1–110 of
   `${CLAUDE_PLUGIN_ROOT}/assets/reference/artifacts.tex`. Reuse the visual system and prose
   rhythm, not the manual's chapter structure. Keep the family default author, `torsor lab`,
   unless the user specifies another author list for the paper.
4. **Shared mechanics.** Read `${CLAUDE_PLUGIN_ROOT}/assets/commons/scaffold.md` before
   scaffolding, consult `${CLAUDE_PLUGIN_ROOT}/assets/commons/lessons.md` for build and
   math-rendering problems, and finish with
   `${CLAUDE_PLUGIN_ROOT}/assets/commons/publication.md`.

---

## Phase 0 — Scope and source freeze

### Identify the paper

Establish:

- the mathematical field, central problem, and class of objects;
- the intended paper type: theorem-and-proof, construction/classification, counterexample,
  new method, or short note;
- the principal result and current proof status;
- the intended readers and safe prerequisites;
- the closest known literature supplied by the author;
- the scientific authors (default `torsor lab`) and required acknowledgments;
- whether the task starts from notes, a partial manuscript, or a mature draft.

A short theorem with a short proof should remain a short note. Do not expand it to imitate a
monograph.

### Fix the paper location

Use a path supplied by the user. Otherwise propose `paper/` in the research project or a
descriptive sibling directory. Confirm before creating files. Inspect an existing target and
preserve its contents, conventions, bibliography, macros, and user edits.

### Freeze the source set

Record the source paths, repository commit, date, and relevant dirty-state summary in
`<paper-dir>/paper-notes/paper-brief.md`. List every note, manuscript, proof file, computation,
reference, and correspondence excerpt authorized for use. Mark oral or remembered assertions as
such. Do not treat an existing polished sentence as stronger evidence than the underlying proof.

---

## Phase A — Mathematical audit

Read the actual mathematical sources before drafting. Preserve the author's terminology when it
is consistent; flag conflicts rather than normalizing them silently.

Create these kept working artifacts under `<paper-dir>/paper-notes/`.

### `theorem-inventory.md`

List every principal theorem, intermediate proposition, technical lemma, corollary, example,
counterexample, open question, and substantial external result. For each, record:

| Field | Content |
|---|---|
| Stable id | Existing number or temporary key |
| Statement | Exact hypotheses and conclusion |
| Role | Main result / structural step / technical tool / application / example |
| Status | Proved / proof sketched / claimed / computational / heuristic / open |
| Dependencies | Internal and external results used |
| Hypothesis use | Where each delicate assumption enters |
| Source | File, page/line, commit, or author note |
| Attribution | New, quoted, adapted, folklore, or uncertain |

Never promote an item because the intended outline needs it. If a required claim lacks a proof,
mark it and add it to `issues.md`.

### `dependency-map.md`

Map result dependencies and identify the proof spine:

- definitions required by the main theorem;
- reductions that move from the general statement to the workable case;
- the central construction or invariant;
- the decisive lemma;
- formal consequences after the decisive step;
- independent branches and applications.

Prefer a compact adjacency list or Mermaid-free text diagram that survives all output formats.
Use the map to order exposition, not the chronology of discovery.

### `hypothesis-and-notation.md`

Record:

- standing conventions;
- every hypothesis of the main results and where it is used;
- characteristic, finiteness, smoothness, regularity, properness, separability, boundedness, and
  coefficient assumptions;
- canonical versus choice-dependent constructions;
- notation, symbol meaning, scope, and collisions;
- translations between the paper's notation and cited sources.

### `attribution-ledger.md`

For each substantial borrowed result, idea, example, question, or proof strategy, record the
precise source and location when known, the exact form needed here, and any reduction needed to
apply it. Mark uncertain provenance `[CHECK]`. Do not write “first,” “new,” “standard,” or
“folklore” as an established fact without support.

### `issues.md`

Track gaps, ambiguous statements, inconsistent hypotheses, missing edge cases, notation
collisions, unverified citations, absent proofs, and author decisions. Separate:

- **mathematical blockers** — the paper cannot claim the result yet;
- **expository blockers** — the mathematics exists but cannot yet be stated faithfully;
- **attribution blockers** — novelty or provenance is unresolved;
- **optional improvements** — do not block the current theorem.

### Audit gate

Before outlining, verify:

- the main theorem has an exact supported statement;
- its proof dependencies all have earned status;
- external theorems apply under the present hypotheses;
- the theorem does not conflate existence/uniqueness, canonical/noncanonical,
  local/global, generic/geometric, or exact/experimental claims;
- every natural map has a source, target, and definition;
- every claimed isomorphism has a stated reason;
- empty, boundary, and characteristic-dependent cases are accounted for;
- the proposed novelty comparison is supported or marked provisional.

For a large manuscript, dispatch isolated subagents by coherent proof branch, giving each only
the relevant raw sources and inventory schema. Reconcile all outputs in the main thread; review
every item against the source before changing its status.

---

## Phase B — Nine-sentence story and paper architecture

Before drafting, state:

1. **The paper studies…**
2. **The central question is…**
3. **The main theorem says…**
4. **This matters because…**
5. **The closest previous result says…**
6. **The new contribution is…**
7. **The proof works by…**
8. **The main difficulty is…**
9. **The theorem does not claim…**

If the sources do not support a sentence, mark it for the author instead of inventing it.

Choose the smallest structure that fits the mathematics:

### Pattern A — Theorem and proof

Introduction/main results → background → structural reduction → main technical theorem → proof
of the principal theorem → applications/examples → optional final perspective.

### Pattern B — Construction or classification

Introduction → objects/invariants → construction → existence → uniqueness/classification →
examples/boundary cases → optional applications.

### Pattern C — Counterexample

Conjecture and counterexample → background → construction → verification of hypotheses → failure
of conclusion → consequences/corrected formulations.

### Pattern D — New method

Introduction/motivating problem → method overview → general framework → core technical results →
main theorem → applications → scope/limitations.

### Pattern E — Short note

Introduction and theorem → proof → optional example, remark, or consequence.

Turn the dependency map into descriptive section titles. Announce the main result early, but
place its proof only after its prerequisites. When dependency order would make the opening
unreadable, give a faithful informal statement first and defer the machinery.

Present the nine sentences, chosen pattern, section outline, theorem numbering plan, and open
blockers to the user. Get agreement before authoring.

---

## Phase C — Scaffold and author

### Scaffold the paper

Reuse the commons directory, toolchain, visual tokens, fonts, boxes, and build verification, with
these original-research deltas:

- **STYLE.md:** assemble
  `${CLAUDE_PLUGIN_ROOT}/skills/write-pure-math-paper/references/base-pure-math-paper.md`
  plus the chosen voice file. Record the voice in the header.
- **Document hierarchy:** keep the house title-page and colophon treatment, then use an
  article-style abstract, sections, subsections, bibliography, and appendices. Reuse the shelf
  preamble's colors, typography, headers, code, and callouts, adapting chapter-only commands to
  section-level equivalents.
- **Section files:** keep them under `latex/sections/`, named by mathematical function and then
  replaced with descriptive titles:
  ```
  00-abstract.tex
  01-introduction.tex
  02-background-and-setup.tex
  03-...tex  04-...tex  05-...tex          # proof architecture
  NN-examples-and-applications.tex           # when useful
  NN-final-perspective.tex                   # optional
  ```
- **Bibliography:** keep `latex/references.bib` or the project's existing bibliography system.
  Preserve existing citation keys where possible.
- **Math environments:** define numbered theorem, proposition, lemma, corollary, definition,
  example, remark, question, and conjecture environments suited to original statements. Do not
  use the commons' unnumbered `paperthm` restatement environments as the paper's primary system.
- **Authorship:** use `torsor lab` as the scientific author by default in the title, colophon,
  PDF metadata, and EPUB metadata. Replace it only when the user specifies another author or
  author list for the paper; then use that list exactly and keep `torsor lab` in the colophon as
  the house credit.
- **Makefile:** genre comment `# <short title> pure mathematics paper`; EPUB title and author
  metadata must match the paper.
- **Notes:** keep `paper-notes/` beside `latex/`; do not compile it.

### Write the title and abstract

Use a title that identifies the mathematical subject and principal phenomenon without implying
greater generality than proved.

Write a 100–250 word abstract containing the objects/problem, main conclusion, essential
hypotheses, precise increment over known work, central method when useful, and principal
consequence. Avoid notation not needed to identify the theorem and vague claims that
“applications are discussed.”

### Write the introduction

Move from broad problem to exact theorem:

1. Explain the problem, known setting, obstruction, and natural question.
2. Give an informal but faithful statement when the formal result is notation-heavy.
3. State the principal theorem early with all essential hypotheses—or a clearly labeled
   representative version when the general form must wait.
4. Explain significance by saying what changes mathematically.
5. Compare with the closest prior results: hypotheses, conclusions, method, and logical
   relation.
6. Give a proof overview that names the reduction, construction, decisive result, obstruction,
   and resolution.
7. Add a roadmap only when it explains what each section accomplishes.

### Write background and setup

Include only material needed to understand and verify the paper. State conventions explicitly,
introduce definitions near substantial use, explain nonstandard definitions' purpose, and give
running examples when they test hypotheses or foreshadow the construction.

State external results in the exact form used. If a source does not literally imply that form,
explain the translation or reduction.

### Write the mathematical body

Follow the dependency map, chapter by chapter or section by section:

- state each substantial result before proving it and explain its role;
- give a local roadmap before a long proof;
- mark where delicate hypotheses enter;
- justify “we may assume,” locality claims, natural identifications, and formal consequences;
- introduce notation near use and remind the reader after long gaps;
- distinguish the new idea from bookkeeping without calling routine steps “obvious”;
- use examples to illuminate definitions or test assumptions, never to replace a general proof;
- end long proofs by accounting for every part of the theorem.

Write applications as precise corollaries or propositions. Say whether each is immediate,
requires specialization, uses another theorem, or remains conditional.

For computer-assisted material, distinguish exact proof, finite verification, symbolic
simplification, search evidence, and numerical approximation. Include auditable artifacts and
never convert finite evidence into a general theorem.

### Use a final perspective only when it has work to do

Add a final section only to synthesize distributed results, define the method's boundary, state
precise open questions, or identify a concrete obstruction to generalization. Do not repeat the
introduction for symmetry.

### Use appendices honestly

Place long background, calculations, sign checks, alternative proofs, computational
certificates, or a notation index in appendices when they interrupt the main line. Never move an
essential gap-closing argument to an appendix merely because it is inconvenient.

---

## Phase D — Integrity, build, and publication gates

### Mathematical integrity pass

Check every statement:

- quantified objects are introduced;
- hypotheses in the abstract, introduction, and theorem agree;
- notation has one stable meaning;
- corollaries follow from the stated results;
- theorem numbering and cross-references resolve.

Check every proof:

- reductions preserve the claim;
- external results apply;
- existence and uniqueness remain distinct;
- canonical and noncanonical constructions remain distinct;
- local, generic, geometric, and global assertions remain distinct;
- edge and empty cases are treated;
- characteristic-dependent steps are named;
- maps, isomorphisms, and commutative diagrams are justified;
- the final paragraph closes every clause of the result.

Check exposition and attribution:

- the main result appears early;
- significance and novelty are precise;
- the proof overview matches the proof actually written;
- section order reflects conceptual dependencies;
- all borrowed results, ideas, examples, questions, and strategies are credited;
- uncertain novelty and folklore claims remain qualified.

Do not resolve a mathematical blocker by editing `issues.md`. Resolve it in the mathematics or
narrow the paper's claim with the author.

### Build and publication pass

Build every house format:

```
cd <paper-dir> && make pdf && make html && make epub && make md && make check
```

Fix all reported issues. Inspect the hardest displayed mathematics, theorem cross-references,
diagrams, citations, bibliography, and appendix links in every relevant format. Then run the
publication pass in `${CLAUDE_PLUGIN_ROOT}/assets/commons/publication.md`.

The paper is not done until the build is clean, the publication evidence report is clean, and
every item in `issues.md` is resolved, explicitly deferred, or reflected as a limitation in the
paper.

---

## Output structure

```
<paper-dir>/
  Makefile  .gitignore  check-build.py
  paper-notes/
    paper-brief.md
    theorem-inventory.md
    dependency-map.md
    hypothesis-and-notation.md
    attribution-ledger.md
    issues.md
  latex/
    main.tex  STYLE.md  references.bib
    sections/
      00-abstract.tex
      01-introduction.tex
      02-background-and-setup.tex
      03-...tex  04-...tex  05-...tex
      NN-examples-and-applications.tex       # optional
      NN-final-perspective.tex               # optional
      90-...tex                              # optional appendices
  tex2torsor/
  html/  epub/  markdown/
```

---

## Common mistakes

| Mistake | Do instead |
|---|---|
| Opening with notation or a historical survey | State the problem and result before machinery |
| Writing the chronology of discovery | Follow the conceptual dependency map |
| Silently strengthening a theorem during revision | Preserve the statement or flag an author decision |
| Promoting a sketch, computation, or heuristic to proof | Carry explicit proof status everywhere |
| Hiding a hypothesis in setup | Put it in the theorem and record where it enters |
| Calling a reduction “formal,” “standard,” or “obvious” without support | Give the reason or precise citation |
| Listing lemmas without saying why they exist | State each lemma's role in the proof spine |
| Claiming novelty because no citation was supplied | Compare against verified prior work and qualify uncertainty |
| Using citations as a literature list | Explain the mathematical relation and exact result used |
| Letting the abstract outrun the theorem | Cross-check objects, hypotheses, and conclusion verbatim |
| Adding examples that do not test or illuminate anything | Use examples to expose behavior, assumptions, or reach |
| Adding a conclusion that repeats the introduction | Omit it unless a final perspective performs real work |
| Guessing an author other than `torsor lab` | Default to `torsor lab`; override only when the user specifies the author list |
| Guessing the build | Reuse the commons tools, checks, lessons, and publication pass |

The final test is:

> Can a skeptical mathematician understand the theorem, see why it matters, locate the new idea,
> audit the proof's difficult points, distinguish what is proved from what is suggested, and
> identify exactly where the result sits relative to prior work?
