# Base mechanics — paper reading guide

The format rules for a `write-paper-guide` reading companion. These are stable and
**voice-independent**: they hold no matter which `voices/*.md` is paired with them. Pair
this file with exactly one voice for the full style guide.

---

## What a paper guide actually is (get this right first)

**A reading companion, not original research.** It helps a specific reader get into,
through, and out of one paper with the least wasted effort. It explains, contextualizes,
and signposts. It never re-derives the results or presents the paper's contributions as
its own.

**Write about the paper in the third person.** The authors prove, introduce, observe,
assume. Section 3 establishes. Theorem 4.2 states. Never "we prove" or "our construction"
— that is the paper's voice, not the guide's. The guide's own first person, if it appears,
belongs to the act of guiding: "Here is where it helps to slow down."

**It is honestly a guide and says so.** It may be opinionated about what is hard, what is
routine, what to read closely, what to skim. That candor is the point. Flattening
everything to uniform importance is no better than the paper's table of contents.

**It is calibrated to a named reader.** Every guide is written for the background captured
in the reader profile. Lean on what that reader knows; explain what they don't; don't
re-derive what they could write themselves. When in doubt, the reader profile is the
tie-breaker.

**Describe the reader, don't grade them.** Say what the reader is *familiar with*, never how
good they are. No "strong student," "expert," "owns this outright," "for the sophisticated
reader" — and, just as much, no veiled criticism. The reader should read a sentence about
themselves and feel only accurately located, neither flattered nor judged. Prefer "familiar
with X," "comfortable with," "may not have had reason to" over "fluent in," "should already
know," "has never bothered with." This holds in every voice.

---

## Mathematical content

**Explain the *why* before the *what*.** Before a definition, say what it is for; before a
lemma, what role it plays. One sentence is usually enough.

**State results faithfully.** Do not silently strengthen or weaken. Mark a paraphrase as a
paraphrase and point to the exact statement ("Theorem 4.2, slightly informally"). The
reader must be able to trust the guide against the paper.

**Cite by the paper's own numbering.** "Section 3," "Theorem 4.2," "equation (5.1)." The
guide is a map; its coordinates must match the territory.

**Distinguish load-bearing from routine.** Say plainly which lemma is the engine and which
is bookkeeping; what to read line by line and what to take on faith on a first pass. This
triage is the single most valuable thing a guide provides.

**Use display math in service of prose.** Drop in the key definition, the central
identity, the inequality everything turns on. Don't transcribe the paper.

**Notation is a kindness.** Where the paper's notation is heavy or scattered, collect it —
a short table or a paragraph fixing conventions up front pays for itself.

**Cite for a reason, not in a list.** Prefer giving the definition or statement to sending the
reader away for it; when you do point outward, say what each reference is *for* — "[X] for the
construction, [Y] for the comparison with the classical case" — never a bare "(see [X], [Y])."
A reference the reader can act on beats one they merely note.

---

## Structure

**Two parts, always.** Part I orients (what it is about, why interesting, why plausible,
why hard, why new, why the authors pulled it off). Part II navigates: the paper's
structure, results, and arguments, section by section, third person.

**Part I can be discursive; Part II stays tied to the paper.** Part II follows the paper's
spine and is honest about where the difficulty lives.

**Chapters tell a story; sections answer questions.** Open each chapter by orienting —
what does this part accomplish, why care? Sections within can be utilitarian.

**Callouts are for genuine exceptions.** A `notebox` is for something easily missed. A
`pitfallbox` is for the subtlety that actually trips people — the unstated hypothesis, the
index that shifts, the "obvious" step that isn't. Not for ordinary commentary.

---

## Words and numbers (house rules)

**Prefer:** the authors, they prove, they introduce, the construction, the argument turns
on, the key estimate, load-bearing, on a first pass, the engine of the proof, faithfully,
roughly, precisely.

**Banned — in every voice:** "we prove," "our result," "in this paper we" (the paper's
voice, not the guide's); presenting the guide as a contribution or survey; utilize, leverage,
seamless, robust, powerful, elegant-as-filler, beautiful-as-filler, simple/easy/
straightforward (show it), "it is well known that" (to whom?); **clean** (an AI tell — not the
register mathematicians actually write in: don't call an idea, a proof, a step, or a case
"clean").

**Numbers:** spell out one through nine; numerals for 10 and above, and always for theorem,
section, equation, and reference numbers.

**Be consistent in small forms.** Pick one spelling of recurring notation and hold it
($\ell$th vs. $\ell$-th, $n$-th vs. $n$th), one dash convention (hyphen vs. en-dash), one
name per object. Inconsistency in these reads as carelessness even when the mathematics is
right.

---

## What a paper guide is not

- Not the paper rewritten — if a passage could appear verbatim in the paper, it belongs in
  the paper.
- Not a survey of the field — context serves *this* paper, not a literature review.
- Not a textbook — it assumes the named reader's background and builds from there.
- Not a referee report — it explains and guides; it does not judge publishability.

---

## The family it belongs to

The guide shares the manual family's preamble (Solarized Cézanne palette, Garamond/Cabin
fonts, box styles, `\code{}`), `tex2torsor` and HTML design, toolchain (`latexd`, pandoc,
`lab-view`), and `torsor lab` credit — extended with the math block (theorem environments,
`pitfallbox`). Unique to the guide: the two-part shape, the third-person companion framing,
and the reader profile. A reader moving between a tool manual and a paper guide should feel
the same hand at work.
