# Stance — whose voice, which artifact, what belongs in the document

Family-wide, binding on every genre in this plugin. Where a genre needs an exception it is
named here, not asserted locally. Read this before writing prose; it settles four things the
per-genre bases assume rather than state.

---

## 1. The document has no author

These documents are produced by a workflow of several interacting agents, working from a
human-authored design concept. There is no single author. There is no one to credit and no
one to blame. The document is what it is, and it stands on its evidence.

**No first person for the producer.** Not "I checked," not "I could not follow," and never
the editorial "we." An "I" in this text names someone who does not exist, and invites the
reader to weigh a claim by trusting a person instead of by reading the evidence for it.

**Make the evidence the subject.** This is the positive rule, and it is worth more than the
prohibition: naming what was examined carries real content that "I verified X" does not.

| not this | this |
|---|---|
| I diffed their source against the paper's | A diff against arXiv:1909.04683 gives 0.9429 similarity over 412 tokens, longest identical run 207 |
| I could not follow Step 3 | Step 3 does not follow: the kernel is computed on the wrong submodule |
| I verified the nine tags I had reason to doubt | Nine cited tags check out against their sources; the table gives each |
| I found no error that threatens the main theorem | Nothing in the four sweeps reaches the main theorem |
| I was able to supply the missing step | The missing step is supplied by a residue argument, written out below |

Every replacement is shorter *and* says more. That is the test of whether the rewrite worked.

**The passive is the fallback, not the default.** Where there is genuinely no evidence to
promote to subject, "was checked against" is fine. Reaching for it first produces the limp,
agentless prose that makes people want the "I" back. Find the real subject first.

**Standing exception — `write-body-of-work-summary`, self-presentation mode.** There the
first person belongs to the mathematician whose work the document describes, writing a
research statement, grant narrative, or prize submission in their own voice. That "I" has an
author. It is untouched by this file; see `assets/prose/base-body-of-work.md`. In every other
mode of that skill, and in every other genre, the rule above holds.

---

## 2. The document does not address its reader

**No second person.** No "the judgment is yours," no "you will want to read Section 3 twice,"
no sentence written for someone to sign. The document reports; it does not instruct a person
it cannot see.

**Do not name the reader inside the artifact.** Calibrating to a target audience is real work
and belongs to the production process — it decides depth, vocabulary, and what needs
explaining. It must not surface as text. A document that describes its own intended reader is
telling that reader what they already know, in place of telling them something.

---

## 3. Calibration is not content

The SKILL.md files and prose bases state what each genre *is*. That text exists to calibrate
the writing. It is not material for the document, and it is dangerous precisely because it
reads as finished prose — finished prose gets transcribed.

**The test: swap the subject.** A sentence that stays true when the subject is replaced by a
different paper, corpus, or topic is calibration, not content. Cut it.

- *"It carries no recommendation and reaches no disposition."* — true of every document of its
  genre ever produced. Calibration.
- *"Proposition 3.24's central step rests on a cross-reference that prints as `??`."* — true of
  one paper. Content.

The test also settles the case that looks similar and is not: the **limits of the work done**
are content when they name specifics. "The injectivity half of Theorem 5.5 was not
re-derived" survives no substitution — it is a fact about this examination of this paper, and
a reader needs it. "This document does not claim completeness" survives every substitution
and belongs nowhere.

**The document opens on its subject.** No preamble explaining what kind of document this is,
who it is for, what it is not, or how it was made. Front matter that names the subject, the
version examined, and the date is not preamble — it is location.

---

## 4. The PDF is the artifact

**When a PDF is supplied, it is the artifact under study.** Everything else supplied with it —
LaTeX source, an arXiv e-print, a repository — is an aid. Aids are for exact quotation, line
locations, anchor placement, and corroborating what the compiled document shows. Findings are
about what the PDF contains.

**The test: does it appear in the compiled document?**

- It prints — an author's marker rendered by a macro, a cross-reference set as `??`, a
  sentence that stops mid-clause, a statement with no proof. **In scope.**
- It does not print — commented-out source, the author's working notes, material deleted in
  version control. **Out of scope**, and not to be referred to at all.

Working notes are not part of what is being analyzed. They are how someone got to the
document, not the document. Reasoning from them produces findings about a person's process
in place of findings about their work, and those findings are unsound in a way that is hard
to see: a passage may be commented out because it was wrong, superseded, or never meant to
survive, and none of that is knowable from outside.

**Source may corroborate, never originate.** Where a finding is already visible in the PDF,
source-level evidence for it is legitimate and often decisive — an unadapted macro surviving
from another paper's source is good evidence about text that is in the PDF. Where the finding
exists only in the source, there is no finding.

**Sometimes there is no PDF, and sometimes there is only a PDF.** Neither changes the rule.
Given source alone, compile it and study what compiles. Given a PDF alone, everything above
holds already and locations are by page. Given both, the PDF has priority and the source is
the aid — which is the common case, and the one this section exists for.
