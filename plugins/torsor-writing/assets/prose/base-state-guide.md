# Base mechanics — workshop state guide

The format rules for a `write-workshop-state-guide` state guide. These are stable and
**voice-independent**: they hold no matter which `voices/*.md` is paired with them. Pair
this file with exactly one voice for the full style guide.

---

## What a state guide actually is (get this right first)

**A dated snapshot of live work for a collaborator who must steer — not a finished-paper
appreciation.** It captures where a room stands *right now*, so someone deciding the next
move can trust the picture. It never announces a result, and it never reads as if the work
were done. The work is live; the guide sounds live.

**Attribute to the room and the moment, not timeless authors.** Present-tense, dated,
commit-stamped. Write "As of `c29366e`, the room has verified X on the generic fibre; Y is
staged for referee; Z is open" — not "the authors establish X." There are no timeless
authors here, only a room at a moment. Every load-bearing claim carries the commit or date
it was last touched, because a state that isn't stamped can't be steered by.

**Translate, never re-grade (the docent invariant).** The room owns the labels; the guide
re-arranges and exposits them. Carry every confidence label (`[Formalized]`, `[Proved]`,
`[Refuted]`, `[Verified]`, `[Conjectured]`, `[Heuristic]`, `[Open]`) and every provenance
tag (`[Standard]`, `[Folklore]`, `[Published]`, `[Preprint]`, `[Premise]`) **verbatim**.
Never silently upgrade a `[Conjectured]` to `[Proved]` because the prose wanted a stronger
verb. A confident-but-wrong carry-over is worse than a flagged gap: it hides the debt
instead of naming it. When in doubt, under-claim.

**Describe the reader, don't grade them.** Say what the reader is *familiar with*, never how
good they are. No "strong student," "expert," "owns this outright," "for the sophisticated
reader" — and, just as much, no veiled criticism. The reader should read a sentence about
themselves and feel only accurately located, neither flattered nor judged. Prefer "familiar
with X," "comfortable with," "may not have had reason to" over "fluent in," "should already
know," "has never bothered with." This holds in every voice.

**The reader is a collaborator steering live work.** Not a student learning an idea, not a
referee judging a finished result. Calibrate to the next judgment call they face: surface
decision points and forks, not just background. The tie-breaker, always, is the reader
profile.

---

## Lead with the ledger

**The confidence ledger is the guide's map, not an appendix.** It is the first orientation
the reader gets, before any exposition. It is assembled from the room's *own* labels —
harvested, not invented — and arranged into four bands. Name them exactly:

- **Solid** — `[Formalized]` / `[Proved]` / `[Verified]`. Carry the confidence label, and
  for `[Verified]` carry the range it was checked over. What the reader can build on now.
- **Provisional / just changed** — recently corrected or shifted; typically `[Conjectured]`.
  What moved lately and might still be settling.
- **Open / might still flip** — `[Open]` claims, **plus what is being checked that would move
  a label**. Not just "unknown," but "unknown, and here is the probe in flight."
- **Where to be skeptical** — staged-not-earned steps, load-bearing `[Preprint]` /
  `[Folklore]`, and the "if this framing is off, the approach is too" risks. What a
  careful collaborator should distrust even where the room sounds sure.

State the ledger explicitly and get the user's agreement on it: it is the single most
consequential editorial choice in the guide, the analog of a concept spine — except
harvested from the record rather than decided.

---

## Mathematical content

**The five state questions.** These *replace* the six questions a finished-paper guide
answers. They reward calibration, not appreciation:

1. **What's being attempted** — the *question*, not "the contribution."
2. **What's solid right now, at what confidence** — the ledger, up front.
3. **What's provisional / just changed** — recent corrections and shifts.
4. **What's open or might still flip** — and what's being checked that would move a label.
5. **Where to be skeptical** — what a careful reader should distrust; what's staged-not-earned.

State plainly: **"why it's hard / plausible" is optional** — include it only when it helps
the reader judge a fork. **"why it's new" and "why they pulled it off" are cut entirely** —
they are a finished-paper's concerns, and this is not a finished paper.

**State results faithfully, with their labels attached.** Do not silently strengthen or
weaken. A paraphrase is marked as a paraphrase and points to the exact statement; the label
travels with the claim. The reader must be able to trust the guide against the record.

**Distinguish load-bearing from routine — and earned from staged.** Say plainly which claim
the next move depends on, and which is bookkeeping; which is `[Verified]` and which is
staged-not-earned. This triage, keyed to confidence, is the most valuable thing the guide
provides.

**Use display math in service of prose, and stamp it.** Drop in the definition or identity
the work turns on; where it matters, note the commit at which it took its current form.
Don't transcribe the record.

**Notation is a kindness — and rooms clash.** Where the record's notation is scattered or
two rooms disagree, pin one convention up front, verified against the record, and carry it
everywhere. A short table pays for itself.

---

## "What changed / what might change" is mandatory

**A correction is a valued output, not a failure.** This is the register's core
anti-result-maxing stance. The guide has a dedicated, first-class "what changed / what
might change" section, and it normalizes corrections rather than hiding them: a claim that
was wrong and got fixed is exactly the kind of thing a steering collaborator most needs to
see.

**Dead ends and superseded branches are first-class content, not footnotes.** The branch
that was tried and abandoned tells the reader where *not* to spend the next week. Give it a
home in the prose, not a parenthetical. This is culture §13 "Protect The Quiet Good Idea"
(the abandoned branch may be quietly right) and §15 "Maintain Branches" (superseded work
stays visible) made concrete in the register.

**Active checks belong here too.** "Being checked: whether the cover descends to the model
level; the referee's objection to Lemma 3." What is in flight, and what its outcome would
move, is part of the live state.

---

## Words and numbers (house rules)

**Prefer:** as of `<commit>`, the room has; is staged for referee; is being checked; was
corrected; still open; flagged because; the room, at this moment; verified on; carries the
label; roughly, precisely, faithfully.

**Banned — the result-maxing rhetoric (in every voice):** `contribution`, "why it's new,"
"pulled it off," `impressive`, `breakthrough`, `novel`, `finally`, "we now have" — and **any
summary that reads as "done" while the work is live**. The whole point of the register is to
refuse premature closure.

**The no-premature-closure rule.** Never write a sentence that would still make sense after the
work is finished and refereed. If a phrasing implies the question is settled when the ledger
says `[Conjectured]` or `[Open]`, it is banned. **`establishes` / `proves` are earned only
by `[Proved]` / `[Formalized]` units** — for anything provisional, the room "argues,"
"suggests," "has staged," "is checking," never "establishes" or "proves."

**Banned filler (kept from the paper base, in every voice):** "we prove," "our result," "in
this paper we" (that is the record's voice, not the guide's); presenting the guide as a
contribution or survey; utilize, leverage, seamless, robust, powerful, elegant-as-filler,
beautiful-as-filler, simple / easy / straightforward (show it), "it is well known that" (to
whom?); **clean** (an AI tell — not the register mathematicians actually write in: don't
call an idea, a proof, a step, or a case "clean").

**Numbers:** spell out one through nine; numerals for 10 and above, and always for theorem,
section, equation, commit, and reference numbers.

**Be consistent in small forms.** One spelling of recurring notation ($\ell$th vs. $\ell$-th),
one dash convention, one name per object, one way of writing a commit stamp. Inconsistency
here reads as carelessness even when the mathematics is right.

---

## What a state guide is not

- Not the room's record rewritten — if a passage could appear verbatim in the journal or the
  status cards, it belongs there, not in the guide.
- Not a paper — it announces nothing and closes nothing; the work is live.
- Not a survey of the field — context serves *this* room's next move, not a literature review.
- **Not a finished-result announcement** — no "here is the beautiful result" opening, ever.
- Not a referee report — it translates and locates; it does not re-judge the math or rule on
  publishability.

---

## The contrast (the tone shift, concretely)

*Result-maxing (wrong register):*

> The room's contribution is to make both things concrete… Why it is new… Why the room
> could pull it off: because it named the right function.

*State register (right):*

> As of `c29366e`, the room has an explicit `$f$` for `$n=4,5,6$`, verified on the generic
> fibre. Whether these are the model-level covers is open. The move that made it compute was
> reading `$f$` as the Miller function — flagged because if that framing is off, the approach
> is too.

The second sentence never claims the question is settled, stamps its state, carries the
`[Open]`, and names its own risk. That is the whole shift.

---

## The family it belongs to

The guide shares the manual family's preamble (Solarized Cézanne palette, Garamond/Cabin
fonts, box styles, `\code{}`), `tex2torsor` and HTML design, toolchain (`latexd`, pandoc,
`lab-view`), the math block (theorem environments, `pitfallbox`), and `torsor lab` credit —
all inherited verbatim via the commons scaffold. Unique to the state guide: the **confidence
ledger** as its spine, the **present-tense, dated, commit-stamped** register, the mandatory
**what changed / what might change** section, and the reader profile of a collaborator
steering live work. A reader moving between a tool manual, a paper guide, and a state guide
should feel the same hand at work.
