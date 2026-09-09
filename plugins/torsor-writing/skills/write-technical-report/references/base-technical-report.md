# Base mechanics — technical experiment report

Pair this file with exactly one torsor voice file. It defines the stable mechanics of a
`write-technical-report` document; the voice file controls rhythm, warmth, and humor.

## Contents

- [What the report is](#what-the-report-is)
- [Agency, tense, and grammatical person](#agency-tense-and-grammatical-person)
- [Evidence language](#evidence-language)
- [Section boundaries](#section-boundaries)
- [Numerical and visual reporting](#numerical-and-visual-reporting)
- [Prose and structure](#prose-and-structure)
- [Torsor format mechanics](#torsor-format-mechanics)
- [Words and numbers](#words-and-numbers)
- [What the report is not](#what-the-report-is-not)

---

## What the report is

**Write an evidence-led account, not an activity log.** Organize around a question, an
operational test, observed outcomes, validation, and a trust boundary. Mention chronology only
when order affects the result.

**Write for a skeptical technical reader.** Assume intelligence, not participation. Give the
reader enough context to evaluate the experiment without asking them to trust the operator,
agent, or evaluator.

**Narrow progressively.** Keep the title intelligible across the broad project, the abstract
accessible to a technically educated reader, the introduction useful to someone in the field,
and the Methods and appendices precise enough for a specialist.

**Repeat at increasing resolution.** State the question, method, result, and significance in
compressed form in the abstract; develop them in the introduction; support them in Results; and
qualify them in Discussion. Repetition earns its place when each pass adds precision.

---

## Agency, tense, and grammatical person

**Name who did what.** Use “the agent,” “the system,” “the evaluator,” and “a human operator”
when agency matters. Do not hide intervention in an ambiguous “we.”

**Use “we” for the investigators only when authorship is clear.** “We investigated whether…”
is appropriate. “We repaired the malformed input after run 3” is appropriate when the
investigators did so. “The agent proved…” is appropriate only when the agent produced a proof,
and the next sentence must state how that proof was checked.

**Use past tense for procedure and observations.** Use present tense for what the report,
figure, or evidence now shows and for conclusions that remain in force.

---

## Evidence language

Keep observation and interpretation in separate clauses or sentences.

| Evidential role | Prefer |
|---|---|
| Raw outcome | “The run produced…” / “The measured value was…” |
| Direct support | “This supports…” / “This is consistent with…” |
| Limited inference | “This suggests, but does not establish…” |
| Interpretation | “We infer…” / “A possible explanation is…” |
| Negative evidence | “The experiment did not detect…” |
| Unresolved | “The current evidence does not distinguish…” |

**Reserve “proved” for proof.** A theorem may be proved and a proof may be formally checked.
An empirical comparison supports, contradicts, reproduces, or fails to resolve a claim.

**State the validation channel.** Distinguish exact verification, automated tests, independent
reruns, expert review, heuristic checks, and unverified output. Do not imply that one substitutes
for another.

**Expose uncertainty locally.** Put the qualification beside the claim it limits. Do not make a
strong statement in Results and hope a generic limitations paragraph repairs it later.

---

## Section boundaries

**Introduction:** establish the problem, motivation, research question, prior expectation, and
precise contribution of this experiment.

**Methods:** state what was planned and done, including success criteria, comparisons,
environment, evaluation, exclusions, deviations, and human intervention.

**Results:** report observed quantities, validation outcomes, failures, and examples. Keep causal
or mechanistic explanation out unless it is itself a measured result.

**Discussion:** answer the question, interpret the pattern, consider alternatives, explain
limitations, state implications, and identify the next discriminating experiment.

**Conclusion:** compress the answer and confidence. Add no new evidence.

---

## Numerical and visual reporting

**Give denominators.** Prefer “38 of 420 candidates (9.0%) passed” to “9% passed.”

**Report precision the design earned.** Do not print extra decimal places, narrow uncertainty,
or a precise effect size when the run count, evaluator, or sampling process does not support it.

**Describe variation, not just averages.** Include ranges, medians, dispersion, per-run values,
or uncertainty intervals when they change interpretation.

**Account for failures and missingness.** State whether denominators include failed, excluded,
timed-out, or missing runs.

**Use tables for exact comparisons and figures for patterns.** Every table and figure must have
a conclusion-bearing caption, labeled units, an identified source, and a reference in the prose.
Do not decorate a one-number result with a chart.

---

## Prose and structure

**Lead with the point.** Put the finding before the procedural detail needed to support it.

**Use one idea per paragraph.** Separate outcome, validation, and interpretation when each needs
its own qualification.

**Define essential terms once.** Do not begin with internal filenames, prompt parameters, or code
architecture. Introduce them when the Methods require them.

**Anticipate five objections without performing a sales pitch:**

1. I do not understand it.
2. I understand it, but it is not interesting.
3. It would be interesting, but the result is probably wrong.
4. It may be correct, but the task was trivial.
5. It may be nontrivial, but it was already known.

Answer with definitions, motivation, evidence, the genuine uncertainty, and a bounded novelty
statement. The goal is accurate evaluation, not persuasion.

---

## Torsor format mechanics

Use the shared Solarized Cézanne preamble, Garamond/Cabin typography, title hierarchy, colophon,
and four-format build.

Use `\code{}` for inline identifiers and `lstlisting` for multiline code. Keep raw logs and long
prompts in appendices or linked artifacts rather than the main narrative.

Use `notebox` sparingly for a trust boundary, protocol deviation, or easily missed condition.
Use `warnbox` only for an operational hazard such as destructive reproduction steps. If the
commons math block is present, use `pitfallbox` only for a genuine mathematical or inferential
trap.

Do not use callouts for ordinary commentary. A caveat that directly limits a result belongs in
the prose beside that result.

---

## Words and numbers

Prefer concrete verbs: measured, produced, passed, failed, reproduced, contradicted, supported,
suggested, remained unresolved, verified over, reviewed by.

Avoid: seamless, robust, powerful, easy, simple, straightforward, utilize, leverage,
“the results are discussed,” “the experiment was successful” without a measure, “proved” for an
empirical result, “novel” without a completed novelty check, and “fully autonomous” when a human
intervened.

Use numerals for measurements, run counts, percentages, versions, dates, section numbers, and
identifiers. Include units and denominators. Keep naming, dash conventions, and significant
figures consistent.

---

## What the report is not

- Not a transcript of terminal commands or agent messages.
- Not a product announcement or capability claim detached from evidence.
- Not a research paper padded beyond what one experiment supports.
- Not a repository README.
- Not a place to hide failed runs or evaluator debt.

The report succeeds when a skeptical reader can understand what happened, why it mattered, why
the evidence may be trusted, and where that trust must stop.
