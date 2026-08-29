# Base mechanics — body-of-work summary

The format rules for a `write-body-of-work-summary`: a styled overview of one
mathematician's program — a 2–3 page essay followed by a short paragraph per
paper. These rules are stable and **voice-independent**: they hold no matter
which `voices/*.md` is paired with them. Pair this file with exactly one voice
(default `01-direct`, tightened as below) for the full style guide.

This genre is a sibling of the paper guide, and inherits most of its mechanics.
It differs in three ways that matter: its subject is a *person's program*, not
one paper; its overview must answer six framing questions **without ever naming
them**; and each paper gets a single paragraph, not a chapter.

---

## What a body-of-work summary actually is (get this right first)

**A summary of a program, not original research and not a field survey.** It
locates one mathematician's work: what runs through it, what it changed, why it
holds together. It explains and appraises existing papers; it never re-derives a
result, and it never widens into a survey of everyone who has worked nearby.

**Person depends on the purpose mode.** The summary is written for a stated
purpose, recorded in the reader profile. In **self-presentation** mode the
subject is presenting their own program — first person is allowed ("I show,"
"my main construction"). This is the family's one standing exception to
`${CLAUDE_PLUGIN_ROOT}/assets/commons/stance.md`, which otherwise forbids the
first person outright: here the "I" is the mathematician's own, and it has an
author. It does not license a first person for the document's producer.

In every other mode — **newcomer orientation**,
**evaluator appraisal**, **scholarly appreciation** — write about the
mathematician in the third person: *Krashen proves, the 2019 paper establishes,
the construction of Section 3.* Pick one and hold it throughout.

**It is opinionated about what matters.** It may say plainly which papers are
central, which are consolidation, which opened a direction and which closed one.
Flattening everything to equal weight is no better than a publication list.

**It is calibrated to a named reader and purpose.** Emphasis follows the mode: a
newcomer needs entry points and prerequisites; an evaluator needs the arc and
the stakes; an appreciation needs the throughline. When in doubt, the reader
profile is the tie-breaker.

**Describe the reader, don't grade them.** Say what the reader is *familiar
with*, never how good they are. No "strong student," "expert," "for the
sophisticated reader" — and no veiled criticism either. Prefer "familiar with
X," "comfortable with," "may not have had reason to." This holds in every voice.

---

## The six questions — answer them, never name them

The overview must implicitly answer the same six questions a paper guide asks, at
the scale of the whole program rather than one paper:

- what the work is about;
- why it is interesting;
- why the results are plausible / where the intuition comes from;
- where the real difficulty lives;
- what is new in it, relative to what came before;
- what perspective or technique let this person do it.

**Do not label any of these.** There is no "Why it is hard" heading, no "Why it
is new" section, no sentence of the form "The difficulty here is…" acting as a
signpost. The questions are answered as the prose moves through the work — a
reader should finish the overview knowing all six answers and never have seen the
questions. If a draft grows a heading or a topic sentence that restates one of
these questions, cut it and fold the content into the argument.

The same discipline governs each **per-paper paragraph**: it should convey what
the paper does, why it mattered, what was hard about it, and what was new — in
running prose, in one paragraph, with none of those four labeled.

---

## Mathematical content

**Explain the *why* before the *what*.** Before naming a construction or a
theorem, say what it is for and what it changed. One clause is often enough.

**State results faithfully.** Do not silently strengthen or weaken. When you
restate a paper's result, mark a paraphrase as a paraphrase and, where it helps,
point to the paper. The summary must be trustworthy against the papers.

**Cite the papers by a stable key.** Refer to each paper by a consistent short
handle (year, or an `[AuthorYY]`-style key carried into the appendix), so a
reader can move between the overview, the paragraph, and the reference card.

**Use display math sparingly and in service of prose.** A summary is mostly
words. Drop in the one identity or object that a theme genuinely turns on; do not
transcribe theorems the paragraph only needs to gesture at.

**Group by idea, not by chronology of technique.** The overview's job is to show
the program as a connected thing. Let the mathematics organize the essay; dates
belong to the paragraphs and the appendix.

**Cite for a reason, not in a list.** When you point outward — to a collaborator's
work, to the problem's origin — say what the reference is *for*. A reference the
reader can act on beats one they merely note.

---

## Structure

**Preface, overview, papers, reference card.** A short preface (whose work, who
this is for, how to read it); the 2–3 page overview essay; the per-paper
paragraphs; an appendix reference card (a full chronological citation list and a
themes × papers table). No two-part book structure.

**The overview is one continuous argument.** For a small corpus it runs as an
unbroken essay. For a large program it may be broken by **theme** subheadings —
the names of the threads themselves (e.g. "Descent and patching," "Period and
index"), never the names of the six questions. Decide by length and propose the
choice before writing.

**The papers section carries the same organizing choice.** Either grouped under
the same theme headings as the overview, or a single chronological run — chosen
per subject and confirmed with the user before writing. A paper that sits in two
themes is placed once, by best fit, and cross-referenced.

**One paragraph per paper.** Short. It says what the paper did and why it earned
its place in the program. It is not an abstract and not a mini-guide.

**Callouts are rare here.** This genre is mostly plain prose. A `notebox` for
something genuinely easy to miss about the arc; a `pitfallbox` almost never. If
you reach for a callout in every theme, the prose is doing too little.

---

## Words and numbers (house rules)

**Prefer:** the work, the program, runs through, turns on, the central
construction, what changed, the engine of, on a first reading, faithfully,
roughly, precisely, central, consolidates, opens, closes off.

**Banned — in every voice:**

- "we prove," "our result," "in this paper we" — *except* in self-presentation
  mode, where the first person is the point;
- presenting the summary as a contribution or a survey of the field;
- utilize, leverage, seamless, robust, powerful, elegant-as-filler,
  beautiful-as-filler, simple/easy/straightforward (show it), "it is well known
  that" (to whom?);
- **clean** — an AI tell, not the register mathematicians write in: don't call an
  idea, a proof, a step, or a case "clean";
- **load-bearing** / "load bearing" — overused to the point of tell, and in
  mathematics it grades nothing: either a step is used or the result is false. Say
  what a result actually does: it is *central*, it *carries the argument*, it *does
  the work*, it is *the engine of the proof*, everything *turns on* it. Banned
  family-wide, in every genre and every voice.

**Numbers:** spell out one through nine; numerals for 10 and above, and always
for theorem, section, equation, and reference numbers, and for years.

**Be consistent in small forms.** One spelling of recurring notation, one dash
convention, one name per object and one key per paper. Inconsistency reads as
carelessness even when the mathematics is right.

---

## What a body-of-work summary is not

- Not each paper rewritten — one paragraph, not an abstract or a guide.
- Not a survey of the field — context serves *this person's* work, not a
  literature review of the area.
- Not a CV or a publication list — the appendix may list; the prose must argue.
- Not a letter of recommendation — even in evaluator mode it summarizes and
  locates the work; it does not lobby.
- Not a textbook — it assumes the named reader's background and builds from there.

---

## The family it belongs to

The summary shares the manual family's preamble (Solarized Cézanne palette,
Garamond/Cabin fonts, box styles, `\code{}`), `tex2torsor` and HTML design,
toolchain (`latexd`, pandoc, `lab-view`), and `torsor lab` credit — extended with
the math block (theorem environments, `pitfallbox`). Unique to this genre: the
overview-plus-paragraphs shape, the purpose modes that set grammatical person,
and the discipline of answering the six framing questions without naming them. A
reader moving between a tool manual, a paper guide, and a body-of-work summary
should feel the same hand at work.
