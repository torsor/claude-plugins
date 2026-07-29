---
name: write-technical-report
description: Use when the goal is a skeptical-reader technical report about an autonomous, semi-autonomous, computational, mathematical, or software experiment. Turn protocols, run logs, outputs, tests, evaluator notes, interventions, and repository state into a reproducible account of the question, methods, results, validation, failures, limitations, and next experiment. Use for positive, negative, inconclusive, exploratory, comparative, ablation, reproduction, or capability-evaluation results. Output is the torsor house format (LaTeX → PDF, HTML, EPUB, Markdown).
---

You are helping the user write a **technical report** about an experiment. The report must let
an intelligent, technically capable reader who did not participate determine what was asked,
what was done, what happened, why the evidence deserves its stated level of trust, and where
that trust stops. It shares the torsor design and selectable voice of the manual/guide family,
but follows the structure of a scientific experiment report rather than a manual or reading
guide.

The user has said: $ARGUMENTS

If no experiment or source artifacts were identified, ask for both before proceeding. If the
reader was not specified, default to a technically educated, initially skeptical reader and
record that assumption.

Four rules govern the whole report:

1. **Lead with the scientific question, not the execution history.** A report is not a cleaned-up
   run log.
2. **Define success before announcing success.** Distinguish prespecified outcomes from post hoc
   analyses.
3. **Separate observation from interpretation.** Say what the run produced, then what that
   supports, suggests, or leaves unresolved.
4. **Expose the trust boundary.** Include failed runs, interventions, changing criteria,
   missing data, evaluator weaknesses, and unverified claims.

## The shape of the job

```
Phase 0  Scope the report and freeze provenance       -> experiment brief + reader profile
Phase A  Audit runs, artifacts, and validation        -> report-notes/*.md
Phase B  Fix the six-sentence spine and report plan   -> user-approved claims + section plan
Phase C  Author, build, and inspect                    -> LaTeX/PDF/HTML/EPUB/Markdown
```

Do these in order. Phase A is an evidence gate: do not draft a conclusion that the evidence
ledger cannot support.

---

## Reference materials — read these first

Before doing anything else, read:

1. **Report mechanics.** Read
   [references/base-technical-report.md](references/base-technical-report.md). It defines the
   progressively specialized audience, agency attribution, evidence verbs, section boundaries,
   numerical reporting, callout use, and report-specific banned language.
2. **The chosen voice.** Read
   `${CLAUDE_PLUGIN_ROOT}/assets/prose/voices/01-direct.md` and
   `${CLAUDE_PLUGIN_ROOT}/assets/prose/README.md`. `01-direct` is the default; use another voice
   only when the user requests it.
3. **Canonical layout.** Read
   `${CLAUDE_PLUGIN_ROOT}/assets/reference/shelf-main.tex` and
   `${CLAUDE_PLUGIN_ROOT}/assets/reference/shelf-00-preface.tex`. Use the first for the preamble
   and layout; use the second only for house rhythm, not report structure.
4. **Visual style.** Read lines 1–110 of
   `${CLAUDE_PLUGIN_ROOT}/assets/reference/artifacts.tex`.
5. **Shared mechanics.** Read `${CLAUDE_PLUGIN_ROOT}/assets/commons/scaffold.md` before
   scaffolding, consult `${CLAUDE_PLUGIN_ROOT}/assets/commons/lessons.md` for build and
   math-rendering problems, and finish with
   `${CLAUDE_PLUGIN_ROOT}/assets/commons/publication.md`.

---

## Phase 0 — Scope and provenance

### Identify the experiment

Establish:

- the scientific or engineering question;
- the experiment type: exploratory, confirmatory, comparative, ablation, reproduction,
  theorem-verification, search, simulation, or capability evaluation;
- the system, intervention, or method under test;
- the source-artifact set and its date range;
- whether the report is final, interim, negative, or inconclusive;
- the reader and what background can be assumed.

Do not force a positive-result shape onto a failed or exploratory experiment. “The current
evaluator cannot distinguish the two conditions” can be the report's real result.

### Fix the report location

Use a path supplied by the user. Otherwise propose a `report/` directory beside a single
experiment, or `reports/<YYYY-MM-DD>-<slug>/` in a project that accumulates experiments.
Confirm the path before creating files. Inspect an existing target and preserve its contents.

### Freeze provenance

Record the report date and timezone, repository path and commit, branch, relevant dirty-state
summary, experiment identifiers, and the exact artifact locations. Record model, prompt/skill,
tool, library, dataset, hardware, seed, network, time, and compute versions only when they can
materially affect the result. Mark unavailable values as unavailable; never reconstruct them
from memory.

Create `<report-dir>/report-notes/experiment-brief.md` and, once the directory exists,
`<report-dir>/latex/reader-profile.md`. The reader profile is not compiled.

---

## Phase A — Evidence audit

Read the experiment's actual artifacts before drafting prose. Prefer, in order:

- protocol, task specification, configuration, and prompts;
- run manifests, logs, checkpoints, and stopping conditions;
- raw outputs and retained examples;
- test results, certificates, evaluator outputs, and expert-review notes;
- intervention, exclusion, and protocol-deviation records;
- repository history and source code needed to interpret the run.

Do not treat a narrative summary as a substitute for raw evidence when the raw evidence exists.
Do not bury an absent artifact; record the gap and narrow the claim.

Create these kept working artifacts under `report-notes/`:

### `run-manifest.md`

Record one row per run: identifier, date/duration, condition/configuration, seed when applicable,
status, output location, validation status, and interventions. Include failed and excluded runs,
with the exclusion reason and whether it was chosen before or after inspection.

### `evidence-ledger.md`

Record each report-level claim with:

| Field | Content |
|---|---|
| Claim | The precise sentence the report may make |
| Kind | Primary / secondary / exploratory / post hoc |
| Evidence | Runs, files, tables, examples, or measurements supporting it |
| Validation | Exact, automated, replicated, expert-reviewed, heuristic, or unverified |
| Status | Observed / supported / suggested / unresolved / contradicted |
| Trust boundary | The limitation that most directly constrains the claim |
| Provenance | Stable path, run id, commit, tag, or date |

Do not flatten different validation modes into one confidence score. Exact symbolic verification,
expert judgment, rerun stability, and heuristic plausibility answer different questions.

### `artifact-index.md`

List the protocol, configuration, code, data, prompts, logs, outputs, evaluation scripts,
certificates, figures, and commits needed to reproduce or inspect the experiment. Prefer stable
relative paths and commit-stamped links where available.

### Review gate

Check that:

- every central number traces to a source;
- totals reconcile across stages;
- failed and missing runs are represented;
- human actions are distinguished from system actions;
- success criteria and exclusions are labeled prespecified or post hoc;
- every conclusion has a matching ledger entry;
- claims labeled “verified” say by what method and over what range.

For a large run corpus, dispatch one isolated subagent per independent run group, then perform a
whole-ledger reconciliation in the main thread. Give each subagent only the relevant raw
artifacts and the note schema—not the intended conclusion. Keep a progress ledger and review
every digest before synthesis.

---

## Phase B — Six-sentence spine and report plan

Before writing, state these six sentences:

1. **We investigated…**
2. **This matters because…**
3. **We did…**
4. **We observed…**
5. **We believe the result because…**
6. **The result does and does not establish…**

Keep “we” only when it clearly denotes the investigators. Attribute autonomous actions to the
agent or system and manual actions to the human.

Then fix:

- the scientific question and the operational criterion used to answer it;
- the hypothesis or the explicit statement that the experiment was exploratory;
- the primary outcome and its success criterion;
- secondary outcomes;
- exploratory and post hoc analyses;
- baselines, controls, comparison groups, and exclusions;
- the principal finding and its strongest defensible evidential status;
- the main unresolved uncertainty and the experiment that would reduce it.

Present the six sentences and the proposed section/subsection plan to the user. Resolve
disagreements before authoring; these sentences are the report's conceptual spine.

---

## Phase C — Scaffold, author, and build

### Scaffold the report

Scaffold `<report-dir>/` exactly per
`${CLAUDE_PLUGIN_ROOT}/assets/commons/scaffold.md`, with these genre parameters:

- **STYLE.md:** assemble
  `${CLAUDE_PLUGIN_ROOT}/skills/write-technical-report/references/base-technical-report.md`
  plus the chosen voice file. Record the voice in the header.
- **Chapters:**
  ```
  00-abstract.tex
  01-introduction.tex
  02-methods.tex
  03-results.tex
  04-discussion.tex
  05-conclusion.tex
  ```
  Add only the appendices the evidence requires:
  ```
  90-full-protocol.tex
  91-run-manifest.tex
  92-additional-results.tex
  93-verification-details.tex
  99-artifact-index.tex
  ```
- **Makefile:** genre comment `# <experiment> technical report`; EPUB title equal to the
  report title.
- **Title page:** label the document `Technical Report`; give the descriptive title, a one-line
  orientation, report date, and experiment/repository identifier when useful. Keep `torsor lab`
  in the colophon and metadata, not as the experiment's operator or scientific author.
- **Math block:** include the commons math block when the report contains substantive
  mathematics or formal statements; otherwise omit it.
- **Reader profile and notes:** keep `latex/reader-profile.md` uncompiled and `report-notes/`
  beside `latex/`.

### Write in this order

Draft the Results and Methods from the evidence ledger first, then the Discussion,
Introduction, Abstract, and Conclusion. Present the finished report in the reader's order below.
This drafting order keeps the opening claims tied to evidence rather than aspiration.

### Title

Identify the experiment's subject and principal aim or result. Make it intelligible to someone
who knows the broad project. Prefer “Testing Whether Structured Mutation Improves Counterexample
Discovery” to an internal label such as “Experiment 17 Final Results.”

### Abstract

Write one paragraph, usually 100–250 words. Answer: what problem, why it matters, what was done,
what was found, how strong the evidence is, and what follows. Include concrete findings and the
main limitation. Do not say only that results “are discussed.”

### Introduction

Narrow from broad context to the exact experiment:

1. **Background** — only what is needed to understand the object and difficulty.
2. **Motivation** — the decision, conjecture, capability, or uncertainty at stake.
3. **Research question** — state both the scientific question and operational criterion.
4. **Hypothesis or exploratory aim** — record the prior expectation, or say none was tested.
5. **Contribution** — state precisely what this experiment adds to the project.

### Methods

Make the experiment understandable and reproducible without dumping code:

1. **Experimental design** — runs, independence, baselines, controls, stopping rules, and
   whether the design was fixed in advance.
2. **System and environment** — only result-relevant versions, tools, access, budgets, and
   commit identifiers.
3. **Inputs and initial conditions** — what the system received, inferred, discovered, and
   received later from a human.
4. **Procedure** — major actions, loops, branching, retries, error recovery, and interventions,
   described at the level of decisions rather than terminal commands.
5. **Outcome measures** — primary, secondary, exploratory; define success before reporting it.
6. **Evaluation and validation** — what was checked automatically, manually, heuristically,
   independently, or not at all.
7. **Statistical or comparative analysis** — summaries, variation, uncertainty, effect sizes,
   and tests in proportion to the design.
8. **Deviations and interventions** — departures from protocol, why they occurred, and how they
   constrain interpretation.

### Results

Report what happened, not a chronological activity log:

1. **Run summary** — completed, failed, excluded, compute/time, outputs, and counts at each
   validation stage. Use a compact table when it makes the funnel easier to inspect.
2. **Primary result** — observed quantity, baseline or expectation, variation/uncertainty, and
   direct evidence.
3. **Secondary and exploratory results** — label them; do not promote an interesting post hoc
   pattern to the primary result.
4. **Validation results** — report checks and controls, including apparent successes rejected
   by stronger testing.
5. **Failures and negative results** — treat them as evidence, not implementation noise.
6. **Representative examples** — include a typical success, strong success, revealing failure,
   or boundary case as available. Do not replace aggregate evidence with anecdotes.

### Discussion

Interpret without blurring the evidence:

1. **Main finding** — answer the research question in substantive terms.
2. **Interpretation and alternatives** — distinguish supported mechanism from speculation.
3. **Limitations** — explain how each limitation changes what may be inferred.
4. **Implications** — state what the result changes for the project.
5. **Next experiment** — choose the experiment that addresses the principal uncertainty, not
   merely a larger copy of the current run.

### Conclusion

Write one short paragraph: what was tested, what was found, the appropriate confidence, and what
follows. Introduce no new evidence.

### Appendices

Include only what improves reproduction or inspection:

- full protocol, prompts, stopping rules, and permissions;
- run manifest;
- complete tables, examples, diagnostics, and ablations;
- proofs, certificates, test scripts, evaluator logic, or expert-review notes;
- artifact index.

---

## Build and publication gate

Build and check every standard format:

```
cd <report-dir> && make pdf && make html && make epub && make md && make check
```

Fix all reported issues. For quantitative claims, compare rendered tables and figures against
their source data. Check the hardest mathematics in PDF, HTML, and EPUB. Then run the publication
pass in `${CLAUDE_PLUGIN_ROOT}/assets/commons/publication.md`.

The report is not done until the publication pass returns a clean evidence report and every
central claim can be traced through `evidence-ledger.md` to an artifact.

---

## Output structure

```
<report-dir>/
  Makefile  .gitignore  check-build.py
  report-notes/
    experiment-brief.md
    run-manifest.md
    evidence-ledger.md
    artifact-index.md
  latex/
    main.tex  STYLE.md  reader-profile.md
    chapters/
      00-abstract.tex
      01-introduction.tex
      02-methods.tex
      03-results.tex
      04-discussion.tex
      05-conclusion.tex
      90-...  91-...  99-...              # optional appendices
  tex2torsor/
  html/  epub/  markdown/
```

---

## Common mistakes

| Mistake | Do instead |
|---|---|
| Writing a polished execution diary | Lead with the question; organize Results by claims and outcomes |
| Calling the run “successful” without a defined measure | State the primary outcome and observed value |
| Treating output as truth | Report the validation method and failures under stronger checks |
| Hiding restarts, exclusions, prompt changes, or manual repair | Record each intervention and its interpretive effect |
| Mixing observed output with a proposed explanation | Use separate observation and interpretation sentences |
| Presenting a post hoc criterion as prespecified | Label when the criterion was chosen |
| Using anecdotes instead of aggregate evidence | Give summaries first; use examples to make them concrete |
| Adding elaborate statistics to a tiny experiment | Report observed variation plainly and limit the inference |
| Claiming novelty before a literature check | State that novelty assessment is incomplete |
| Reporting only retained runs | Include failures and exclusions in the run manifest |
| Guessing missing version or provenance details | Mark them unavailable and narrow the reproducibility claim |
| Guessing the build | Reuse the commons scaffold, lessons, checks, and publication pass |

The final test is direct:

> Could a skeptical reader understand what happened, why it mattered, why the result might be
> trusted, and exactly where trust should stop?
