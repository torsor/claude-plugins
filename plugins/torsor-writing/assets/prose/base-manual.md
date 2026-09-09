# Base mechanics — tool manual

The format rules for a `write-manual` user's manual. These are stable and **voice-
independent**: they hold no matter which `voices/*.md` is paired with them. Pair this file
with exactly one voice for the full style guide.

Project-specific framing and glossary (what *this* tool is, its preferred terms) are not
here — they belong in the individual manual. What follows is the house mechanics every
manual shares.

---

## Audience

**Inclusive and low-assumption.** Don't assume the reader is a 22-year-old with a CS
degree; do assume they can handle technical ideas when explained clearly. Avoid gendered
examples. Don't assume their operating system unless it's relevant. This holds in every
voice.

**Describe the reader, don't grade them.** Say what the reader is *familiar with*, never how
good they are. No "power user," "expert," "for advanced readers" as flattery, and no veiled
criticism either. A reader should read a sentence about themselves and feel only accurately
located, neither flattered nor judged. Prefer "familiar with X," "comfortable with," "may not
have had reason to" over "fluent in," "should already know." This holds in every voice.

---

## Technical content

**Explain the *why* before the *how*.** Before showing a command, give one sentence about
what problem it solves. One sentence is enough — not a paragraph.

**Don't over-explain commands.** If a flag name makes its purpose obvious (`--no-browser`,
`--yes`, `--interactive`), don't define it. Annotate only what would genuinely surprise a
reader.

**Code in listings, names in `\code{}`.** Commands longer than a few words go in
`lstlisting` blocks. Inline command names, file names, field names, and short flag strings
use `\code{}`. Never mix running prose into a code block.

**Concrete over abstract.** "You have forty things — projects, tools, research, notes" beats
"you may have a significant number of tracked directories." Name real scenarios; use
real-looking (but clearly fake) paths and IDs.

**Trust the reader to generalize.** Show one good example rather than exhaustive
variations. The quick-reference chapter exists for exhaustive coverage; prose chapters
illustrate, not enumerate.

---

## Structure

**Chapters tell a story; sections answer questions.** A chapter opens by orienting the
reader — what problem does it solve, why care? Sections within can be more utilitarian.

**Transitions matter at chapter level, not section level.** End a chapter with a sentence
or two pointing forward if it helps. Don't add "And now we turn to…" between every section.

**The structural rhythm:** preface → one "big idea" chapter → feature/workflow chapters →
quick-reference appendix → optional afterword.

**Notes and warnings are for genuine exceptions.** A `notebox` is for something the reader
might genuinely miss that matters. A `warnbox` is for something that could cause real harm
(data loss, corruption). Don't use them for general advice or "pro tips."

---

## Words and numbers (house rules)

**Banned outright — in every voice:** **load-bearing** / "load bearing" — overused to the point of tell, and in
mathematics it grades nothing: either a step is used or the result is false. Say what
a result actually does: it is *central*, it *carries the argument*, it *does the work*,
it is *the engine of the proof*, everything *turns on* it.

**Banned filler — in every voice:** utilize (use "use"), leverage (use "use" or be
specific), seamless, robust, powerful, simple (show it; don't claim it), easy (same),
straightforward; **clean** (an AI tell — don't call an idea, a solution, or a step "clean").

**Numbers:** spell out one through nine; use numerals for 10 and above, and always for
version numbers, port numbers, and counts where precision matters.

**Be consistent in small forms.** Pick one spelling and casing of each recurring term and
hold it; one dash convention (hyphen vs. en-dash); one name per concept. Inconsistency reads
as carelessness even when everything is correct.

---

## What a manual is not

- Not a corporate knowledge base — no bullet-heavy walls of text with zero prose.
- Not a man page — no terseness for its own sake, no omitting articles.
- Not a tutorial blog post — no "Step 1… Step 2…" unless a genuine ordered sequence needs it.
- Not a narrow technical reference — the prose reflects what the tool does without
  becoming a feature list.

---

## The family it belongs to

All manuals share the LaTeX preamble (Solarized Cézanne palette, Garamond/Cabin fonts, box
styles, `\code{}` macro), the `tex2torsor` converter and HTML design, the toolchain
(`latexd` PDF, pandoc EPUB, `lab-view` preview), and the author credit `torsor lab`. A
reader moving between manuals should feel at home. Don't deviate from the design without a
strong reason and the author's agreement.
