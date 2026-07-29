# Base mechanics — original pure mathematics paper

Pair this file with exactly one torsor voice file. It defines the stable mechanics of a
`write-pure-math-paper` document; the voice file controls rhythm and warmth without changing
mathematical status, attribution, or proof standards.

## Contents

- [Genre contract](#genre-contract)
- [Audience and mathematical story](#audience-and-mathematical-story)
- [Authorship and status language](#authorship-and-status-language)
- [Statements, definitions, and examples](#statements-definitions-and-examples)
- [Proof exposition](#proof-exposition)
- [Hypotheses and notation](#hypotheses-and-notation)
- [Prior work and attribution](#prior-work-and-attribution)
- [Torsor voice and format](#torsor-voice-and-format)
- [Words, symbols, and numbers](#words-symbols-and-numbers)
- [What the paper is not](#what-the-paper-is-not)

---

## Genre contract

**Write original research in the authors' voice.** Default the scientific author to
`torsor lab`; replace that default only when the user supplies another author list. First-person
plural is normal: “we prove,” “our construction,” “we do not know.” Unlike a reading guide, the
paper owns its statements and arguments.

**Preserve earned mathematical status.** A proved theorem, proof sketch, exact computation,
finite verification, heuristic, conjecture, and open question are different objects. Label them
accordingly and never let polishing erase the distinction.

**Organize conceptually, not chronologically.** Present the mathematical route the reader should
follow, not the order in which the authors discovered it.

**Prefer a narrower true statement to a broader apparent one.** State exceptional cases,
noncanonical choices, characteristic restrictions, external dependencies, and unresolved
arguments where they matter.

---

## Audience and mathematical story

**Narrow progressively.** Make the title legible near the broad field, the abstract complete
without reconstructed setup, and the opening pages useful to a professional mathematician who
knows the area but not the project. Let technical specialization increase only after the reader
knows what the machinery is for.

**Repeat at increasing resolution.** Give the mathematical story in the title, abstract,
informal introduction, formal theorem, proof overview, proof, and final perspective when useful.
Each pass must add precision, not padding.

**Answer predictable objections with mathematics:**

1. What does the theorem say?
2. Why does it change anything?
3. Where could the proof fail?
4. What is the genuinely difficult step?
5. How does this differ from the closest known result?

Do not answer with praise. Answer with a faithful statement, mathematical consequence, proof
architecture, obstruction, and precise comparison.

---

## Authorship and status language

Use “we” for the scientific authors. Use “the proof,” “the construction,” or a named section
when that is clearer than repeated authorial narration.

Use `torsor lab` in the title, colophon, PDF metadata, and EPUB metadata by default. If the user
specifies named authors or collaborators, use that author list exactly and retain `torsor lab`
only as the house credit in the colophon.

Use present tense for mathematical statements and proof actions: “Theorem A implies,” “we
construct,” “the diagram commutes.” Use past tense for historical facts and descriptions of
what earlier authors established when the time distinction matters.

Prefer:

- “We prove…”
- “The argument reduces the claim to…”
- “The computation verifies the assertion for…”
- “This suggests, but does not prove…”
- “We do not know whether…”
- “The method does not address…”

Never use rhetorical confidence as a substitute for proof status.

---

## Statements, definitions, and examples

**State the main result early.** Give a faithful informal version first when the formal statement
requires substantial notation.

**Include every essential hypothesis.** Specify the ambient category, quantified objects,
conclusion, uniformity, functoriality, and effective versus existential character when relevant.

**Introduce definitions for a reason.** Say what a nonstandard definition controls, distinguish
nearby notions, identify choice dependence, and give an example when it helps. Do not warehouse
notation pages before the reader knows the problem.

**Give lemmas roles.** Say when a lemma isolates the geometric step, supplies compatibility,
uses the only characteristic assumption, or reduces the theorem to a known case.

**Use examples as tests.** Let them demonstrate nonemptiness, expose a necessary hypothesis,
separate definitions, compute an invariant, or show the theorem's reach. Do not let examples
stand in for a general proof.

---

## Proof exposition

**Give architecture before detail.** Before a long proof, name the construction, reductions,
obstruction, decisive result, and assembly step.

**Justify transitions.** Explain “we may assume,” “the assertion is local,” “it follows
formally,” natural identifications, base change, and reductions. Cite a precise theorem when the
justification is external.

**Track the difficult points honestly.** Identify the engine of the proof and distinguish it
from routine verification. Do not flatten all lemmas to equal importance.

**Use local roadmaps.** Divide long arguments at genuine conceptual changes. State intermediate
claims when they make dependencies auditable.

**Close the loop.** End a long proof by matching established pieces to every clause of the
theorem: existence, independence of choices, uniqueness, functoriality, and so on.

---

## Hypotheses and notation

State standing conventions that change meaning: commutativity, units, noetherian hypotheses,
integrality, geometric integrality, characteristic, grading, signs, indexing, points,
coefficients, derived conventions, and tensor products.

Name where delicate hypotheses enter. When an assumption is used once, say so; that is useful
both for auditing and for possible generalization.

Use one symbol per object and one object per symbol whenever practical. Introduce notation near
use, remind the reader after long gaps, and warn explicitly when conventions differ from a
source.

Distinguish:

- existence from uniqueness;
- canonical from noncanonical;
- local from global;
- generic from geometric;
- arithmetic from geometric points;
- equality from canonical isomorphism;
- proof from finite or numerical evidence.

---

## Prior work and attribution

Treat citations as part of the argument. For a substantial borrowed result, identify the exact
statement or section and explain why it applies under the current hypotheses.

Compare close results by hypotheses, conclusion, method, and logical relation. Say when the
present proof is new but the conclusion overlaps, when the scope is broader but the conclusion
is weaker, or when neither theorem implies the other.

Credit ideas, examples, questions, conjectures, and proof strategies—not only theorem
statements. Mark uncertain provenance rather than assigning it confidently to a convenient
secondary source.

Avoid “the first,” “new,” “standard,” and “folklore” unless the evidence supports the word.

---

## Torsor voice and format

Use the direct voice as disciplined mathematical clarity: lead with the point, vary sentence
length, keep one idea per paragraph, and cut throat-clearing. Do not import manual-style “you,”
chatty solidarity, or dry jokes into theorem statements and proofs.

Use the shared Solarized Cézanne palette, Garamond/Cabin typography, section hierarchy,
colophon treatment, and four-format toolchain. Default the title and publication metadata author
to `torsor lab`; override only from an explicit user-supplied author list.

Use numbered theorem-like environments consistently. Keep labels semantic and stable:
`\label{thm:...}`, `\label{prop:...}`, `\label{lem:...}`, `\label{def:...}`,
`\label{sec:...}`, `\label{eq:...}`. Refer with `\ref`, `\eqref`, or the project's established
cross-reference system rather than hard-coded numbers.

Use `notebox` only for an expository warning that genuinely helps across formats. Mathematical
hypotheses, proof gaps, and qualifications belong in the theorem or prose, not in decorative
callouts.

---

## Words, symbols, and numbers

Prefer concrete mathematical verbs: prove, construct, classify, identify, reduce, descend,
lift, specialize, extend, obstruct, vanish, factor, compare, imply, and fail.

Avoid filler: interesting, important, elegant, beautiful, powerful, robust, seamless, simple,
easy, straightforward, clearly, obviously, “it is well known,” “by standard arguments,”
“several applications are discussed,” and “it would be interesting to generalize.” Replace each
with the mathematical content or a precise citation.

Use numerals for theorem, section, equation, characteristic, degree, dimension, page, and
reference numbers. Keep spelling, hyphenation, notation, and dash conventions consistent.

---

## What the paper is not

- Not a reading guide written about someone else's work.
- Not a diary of discovery.
- Not a survey of every related topic.
- Not a sequence of formally correct lemmas whose purpose is hidden.
- Not a place to convert computational evidence into a general proof.
- Not a venue for unsupported novelty or priority claims.
- Not a long paper merely because the result took a long time to find.

The paper succeeds when a skeptical mathematician can understand the theorem, see why it
matters, locate the new idea, audit the hard steps, distinguish proof from suggestion, and
identify the result's exact relation to prior work.
