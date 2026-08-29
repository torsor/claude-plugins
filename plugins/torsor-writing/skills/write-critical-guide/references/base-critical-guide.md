# Base mechanics — critical guide

The format rules for a `write-critical-guide` package. These are stable and
**voice-independent**: they hold whichever `voices/*.md` is paired with them. Pair this file
with exactly one voice for the full style guide.

---

## What a critical guide is (get this right first)

> **Calibration, not content.** This section and "What a critical guide is not" below
> exist to settle what is being written. None of it belongs in the document. Every
> sentence in both fails the substitution test in
> `${CLAUDE_PLUGIN_ROOT}/assets/commons/stance.md` — each stays true of any paper, so
> none is a finding about this one. They read as finished prose, which is exactly why
> they get transcribed; do not.

**Working material for a critical reader, not the formal evaluation.** A formal evaluation is signed and
sent to an editor and carries one person's judgment. This is what that person works from: the
paper read closely, its context established, everything questionable found, located, and
verified, with repairs where repairs exist. They decide what they agree with, what matters,
and what to write. Some of these sentences may end up in their report; that is a use of the
document, not its purpose.

**A critical guide, not an expository one.** The genre is the reading guide's sibling: same
family, same close reading, same voice, opposite job. A reading guide takes the paper as given
and helps someone through it. This one asks whether it holds. Where a reading guide would
smooth a compressed passage over so the reader can keep moving, this one stops and says the
passage is compressed, what is missing, and whether the gap can be closed.

**No disposition.** The words *accept*, *accept with revision*, *major revision*, *minor
revision*, and *reject* do not appear as judgments about the work under review. Say what the
paper does, what it is worth, what is wrong with it, and what would repair each thing — and
stop. The verdict is the reader's, and a guide that reaches one invites them to ratify a
judgment they did not make.

**Addressed to the critical reader, and written so it can be worked from.** They need to get to the
paper's shape quickly, then to any particular issue without hunting. The summary document
serves the first, the issue list and the annotated sources the second, and neither is a
compressed version of the other. Everything is located precisely enough to check.

**It states its own coverage.** Say what was checked and came out clean, and say what was not
checked. A list of nine problems otherwise reads as the whole result of the examination. If
thirty citations were verified and nine were wrong, say thirty. If the long computation in §6
was not re-derived, say so. Where the coverage ends is where the reader's own work begins,
and they cannot see that boundary unless it is drawn.

**It is written from a position, and owns it.** "I verified every tag the paper cites that I
had reason to doubt." "I found no error that I believe threatens the main theorem." The
judgments are yours; attributing them to no one makes them harder to weigh, not more
objective. They are also *yours* rather than the reader's — write so the two never blur.

---

## Agency, tense, and grammatical person

**The paper in the third person.** The authors prove, introduce, observe, assume. Section 3
establishes. Theorem 4.2 states. Never "we prove" — that is the paper's voice.

**The examination with the evidence as subject.** No first person: the document has no
author, and the rule with its worked replacements is in
`${CLAUDE_PLUGIN_ROOT}/assets/commons/stance.md`. "A diff against arXiv:1909.04683 gives
0.9429 similarity," not "I diffed it." "Step 3 does not follow: the kernel is computed on the
wrong submodule," not "I could not follow Step 3." Never the editorial "we"; it hides whether
a thing was done or merely believed, which is the failure the evidence-as-subject rule exists
to prevent. And never a sentence written for the reader to sign.

**Present tense for what the paper says; past for what the examination did.** "Step 1 replaces
the order by a maximal one" — the paper still says that. "Nine cited tags were checked against
their sources" — that happened once. Where the past tense forces a passive, promote the
evidence instead: "The diff gives 0.9429 similarity."

---

## Evidence language

Keep four things in separate sentences or clauses, and never let them blur:

| Role | Form |
|---|---|
| What the paper says | quote it, verbatim, or cite the statement number |
| What its argument establishes | "the preceding sentence gives …" |
| What is missing between them | "it does not address …", "this is asserted with neither proof nor reference" |
| What you supplied | "a short argument: …" — then give it in full |

**Quote before you characterize.** An issue that opens with the paper's own words is one the
authors can locate in seconds and cannot misread as being about a different passage.

**Distinguish a gap you closed from one you could not.** "It does not, and the ingredients are
already in §2.2" is a different finding from "I could not see how to repair this." Both are
useful; conflating them is not. Where you closed it, say how long the closure is — "one
sentence would settle this," "two lines suffice" — because that tells the author the size of
the work.

**Grade by consequence, not by length.** A misprinted subscript that makes two displays
contradict each other is major; a paragraph of awkward prose is trivial. What matters is what
it costs a reader or the argument, not how much text the item takes to state.

**Say when a finding is inherited.** A theorem whose proof fails only because a lemma it cites
fails is not a second error. Mark it as depending on the first and let its status follow.

**Separate a direct check from an assessment.** "I verified this against the source" and "this
route looks viable but I have not written it out" are different epistemic acts. Label them.

---

## Mathematical content

**Cite by the paper's own numbering**, plus a location precise enough to find without it —
section and step, or page and line. The report is a set of coordinates into the paper; they
must match the territory.

**State results faithfully.** Do not silently strengthen or weaken what the paper claims. Mark
a paraphrase as a paraphrase.

**Give the repair where you have one.** A comment that names a defect and stops is
half a comment. Where the fix is short, write it out; where it is a choice among routes, name
the routes and what each costs.

**Be specific about hypotheses.** "It also holds only under a hypothesis on $X$ that is not
stated" is actionable. "The hypotheses are unclear" is not.

**Do not report a preference as an error.** Where the authors' choice is defensible and merely
not yours, either leave it or mark it plainly as a suggestion.

---

## Structure

**Four documents, each with one job.** The summary is prose and argues an assessment. The
issue list is a reference and is exhaustive. The repairs document is constructive. The
annotated sources are for reading the paper against, and are the part a reader is most
likely to pass on. Do not let any of them become a shorter copy of another.

**Group issues by kind, then by theme.** Group at the top by what the author must *do* about
them — usually mathematical, references, typographical, though the paper decides — and then
within a group by what kind of problem it is: claims not argued, statements wrong as printed,
hypotheses never discharged, notation collisions, structure. A reader working through
twenty-five mathematical items needs the shape of them.

**Set bulk copy-editing in a table.** Thirty one-line usage corrections belong in a
three-column table — location, what the paper writes, what to write — and not in thirty
paragraphs. Reserve prose entries for items that need an argument. When a single typographical
item does carry real consequence, lift it out of the table and give it a full entry.

**Order the summary's findings by consequence**, and cross-reference each to its tag. That
ordering is the most useful thing the summary does, and it is the closest the guide comes to a
judgment — which is why it must be an ordering and not a conclusion.

---

## Words and numbers (house rules)

**Prefer:** the authors, they assert, they establish, the argument turns on, this is asserted
without, it does not address, the paper compresses, I verified, I was able to supply, one
sentence would close this, at the point of use, as printed.

**Banned — in every voice:**

- **Disposition vocabulary** as a judgment on this paper: accept, reject, revision,
  publishable, "worthy of publication." Equally, anything that writes the formal evaluation
  for them — "I recommend," "this reviewer finds," "in my report I will."
- **"Load-bearing."** Say what rests on what. In mathematics either a step is used or the
  result is false, so the metaphor grades nothing; and it has become a tic. "This parenthesis
  supplies the middle equality, without which Step 3 has nothing to glue" tells the author
  something. "This is load-bearing" does not.
- **The definite-article magic word:** "the key definition," "the point is," "the crucial
  step." There is rarely exactly one. Name the thing and say what it does.
- **Negative framing where positive would carry the same content.** "This is not merely a
  change of notation," "the method is not mysterious," "Section 7 is not a formal appendix."
  State what it *is*. Keep negation for a genuine contrast the reader would otherwise draw
  wrongly.
- **Executive-summary register:** "headline," "takeaway," "at a glance" as a substitute for
  saying the thing, "TL;DR."
- **Reading advice to the author:** "you can postpone this," "do not try to memorize." The
  authors wrote the paper.
- **Filler:** utilize, leverage, seamless, robust, powerful, elegant and beautiful as filler,
  simple/easy/straightforward (show it), "it is well known that" (to whom?), **clean** — do not
  call an idea, a proof, a step, or a case clean.

**Numbers:** spell out one through nine; numerals for 10 and above, and always for theorem,
section, equation, page, line, and reference numbers.

**Be consistent in small forms.** One spelling of recurring notation, one dash convention, one
name per object, one tag per issue used identically in every document. In a report whose
subject is partly the authors' inconsistency, the report's own inconsistency reads badly.

---

## What a critical guide is not

- **Not a formal evaluation.** It is the material one is written from. It carries no signature
  and reaches no disposition.
- Not a reading guide — it assesses and itemizes; it does not orient a newcomer. (A reading
  guide is the input to this process, not a component of its output.)
- Not a rewrite of the paper — where the authors' prose is merely not yours, leave it.
- Not a survey — context serves the assessment of *this* paper.
- Not a recommendation. Findings, ordered by consequence. The decision belongs to the reader.
