# The artifacts

What a run produces. The substrate is `ledger-model.md`; this is what gets made from it.

The governing division is the one SKILL.md draws under **Writing a guide from an existing
map**: **uniform in the gathering, selective in the presentation.** The ledgers keep everything. Every document below is a cut, and a cut has
a thread, which is the writing.

---

## The guide

Two parts, mirroring `write-paper-guide` deliberately — a reader moving between the two
should feel the same hand at work.

**Part I — the neighbourhoods.** Which literatures the paper turns out to sit in, what each
supplies, and where they meet. Read off the finished map rather than judged separately. This
is most of what a curious reader came for, and the only part that reads as an essay. It is
also the only part that can fail for want of material: on a thin map it degenerates into
three paragraphs of hedging, and where the map does not support it, it should not be written.

**Part II — through the paper.** The paper's own order, with the connections at each point.
Selective, because a thread means leaving things out.

**Written prose with generated boxes set into it.** The thread is written; nothing about a
connection is. Chapters carry `\input{callouts/<id>.tex}` at chosen points and every box is
generated from the ledger. This is what stops the prose drifting from what was found, and it
is why the same material either stands alone or is injected into an existing reading guide —
the boxes are the same boxes.

House format throughout: LaTeX to PDF, HTML, EPUB and Markdown, per the family.

## Generated views

Plain filters over the ledgers, not rankings.

- **The entries.** Every entry, every connection, every field. For lookup and for the next
  run to build on; nobody reads it through. Bound into the guide as an appendix while it is
  small; its own document once it is not. At a hundred and fifty entries it would swamp the
  document it is appended to.
- **What nothing was found for.** The `unlocated` lines collected. For an author this is the
  where-the-contribution-actually-is view, and it is the output that justifies the run.
- **Leads.** Named, unread, ordered only by how many searches nominated them independently.
  What a later extension picks up when someone has library access.

## Annotated copies

The mechanism is `annotate_tex.py` from `write-critical-guide`, substantially unchanged:
anchors that must be verbatim substrings of exactly one line of the annotation base, a check
pass that fails before generation rather than after, the generator copied into the package so
it rebuilds anywhere. That anchor rule is what makes the whole thing work and is inherited
word for word.

**Cut by literature, and the cut is forced by density.** Critical-guide notes are sparse
because defects are; these are not. At fine grain a single copy could carry a hundred and
fifty marks and have more annotation than text. Each literature touches perhaps a dozen
places, which is readable — and it is the better artifact anyway, since handing someone the
paper with every point where one literature enters marked answers "which conversations is
this part of" faster than any prose.

**One further copy: what nothing was found for.** For an author, their own contribution
mapped onto their own draft.

**And one combined copy: `annotated-all`, in PDF and EPUB.** Always made. Every admitted
record at its passage, from every literature at once, and each note carries the **whole
record** — what it changes, the source with its locator, the relation, how far the source was
read, the dictionary, where it stops — rather than a pointer. It is the copy that reads
without the guide open beside it, which is exactly the situation of an e-reader, so it is
also rendered to `annotated-all.epub` (`correspond.py epub`, run by `all`). In the EPUB each
note is a `<div>` classed by its relation and washed in the same pale colour as the PDF, with
the text colour pinned so the box stays legible when the reader switches to a dark theme.
The combined copy is the preferred product. The per-literature cut is made as well only
when the combined copy is crowded: `annotate` compiles the bare paper and the combined copy,
measures annotation as $1-P_0/P$ of an average page, and makes the cut when that exceeds about
60% (`CUT_SHARE`; override with `--cut always|never`). A record count is the wrong measure,
since the same number of records crowds a short paper and barely marks a long one.

**The note is one line.** Kind, source with locator, pointer into the guide:

```
analogy · B. Author \S4.5 Prop. 4.5.1 · \S E4
```

The kind is not decoration. Without it every mark looks alike and the copy reads as *all of
this is already known* — and two of the seven labels are not correspondences at all. Short
forms are in `ledger-model.md`.

Depth lives in the guide; the annotation is a pointer.

**Set the notes inline, not in the margin.** The margin is too narrow for a note carrying a
source, a locator and an entry pointer, and it truncates them — this is true regardless of
how many notes there are, so it is not a density question. Inline boxes also sidestep the
float problem entirely, since they are not floats: a copy that cannot be built in the margin
builds inline without incident, whatever its density.

The cost is that an inline box inserts at the next paragraph boundary rather than beside the
passage, so several notes arrive together and the reader matches them back by their entry
pointers. That is why the pointer is not optional.

**Colour is free here**, since the copies are already split by literature rather than by
category, so it can carry the label instead. Tightness then reads across a page at a glance —
a region that is all *analogy* and *thematic* against one that is all *same statement*. The
risk is that any ramp reads as a severity scale and drags the critical-guide register back
in, so: a neutral progression, never red-to-green, and a key that says plainly it grades
nothing.

**Pale washes, not saturated fills.** With inline boxes the note text sits *on* the colour
rather than beside it, so anything below roughly 0.85 in each channel fights the text. The
first palette here was built for margin marks at 0.20–0.46 and was unreadable the moment the
notes moved inline.

**Intake.** `write-critical-guide`'s hardest case is this one's rarest. It must cope with a
submitted PDF and no source; here the primary use is an author on their own complete draft,
where source is always in hand. Where there is a PDF and nothing else — the curious-reader
case — the annotated copies simply do not exist, and the package says so plainly rather than
leaving their absence to be inferred.

## Focused guides — the second invocation

Same generator, narrower scope: `§2`, `the representation-theoretic connections`, `everything
touching the kernel`. Cheap and repeatable, because the map is already paid for. This is
where selection is legitimate and open: a stated purpose, over a substrate that kept
everything.

## The package

```
correspondence-guide/
  00-guide.pdf                Part I and Part II, house format
  01-neighbourhoods.md        written
  02-through-the-paper.md     written, with generated boxes set in
  A-entries.md                generated
  A-unlocated.md              generated
  A-leads.md                  generated
  inventory.yaml              ledger
  correspondences.yaml        ledger
  callouts/<id>.tex           generated; injectable into a reading guide
  annotated-all.tex/.pdf      generated, every admitted record in full; always made
  annotated-all.epub          generated from annotated-all.tex by pandoc; always made
  annotated-<literature>.tex  generated, one per literature, only when annotation
                              exceeds ~60% of an average page of annotated-all
  annotated-unlocated.tex     generated
  correspond.py               copied in, so the package rebuilds without the skill
  Makefile                    from references/Makefile.package
  README.md
search-notes/                 the audit trail: inventory passes, search records,
                              disagreements, the full union of what was looked at.
                              Kept, not handed over.
```

## Hazards of annotating someone else's source

None of these appears against the fixture; each is the kind of thing only a source written
by someone else, in their own conventions, produces. The generator handles them; they are
recorded because the next person to touch it will be tempted to simplify one away.

- **Its `inputenc` is not your encoding.** A paper may declare `latin9` on a file that is
  actually UTF-8. Anything inserted must be ASCII LaTeX; an em-dash is a fatal error.
- **Its preamble does not have your macros.** `\code{}` is this family's; a source we
  annotate defines `\texttt{}` and little else of ours.
- **Searchers write mathematics as prose.** `P^2=P`, `S_n-module`. Outside math mode
  those are fatal; escape them.
- **Backticks are quotation marks as often as code fences.** A quotation opened with a
  backtick inside a ledger field turns into a mangled `\texttt{}` spanning half a sentence.
- **Margin notes are floats, and LaTeX has room for eighteen.** A densely marked copy dies
  with "Float(s) lost", reported at `\end{document}` rather than anywhere near the cause.
  Enlarge the pool in proportion to the marks inserted.
- **`pdflatex` output is not valid UTF-8.** It echoes source bytes. Decode leniently or the
  build tool dies on a document that would have compiled.
- **Self-referential numbering needs three passes**, not two.
- **Place the marks before touching the preamble, and verify where they landed.** Mark
  positions are computed against the original source; anything inserted above them first
  slides every note earlier in the body by that many lines. On one run this put every note
  at a passage it had nothing to do with — while every anchor still resolved, every document
  still built, and nothing reported a problem. It was found by a reader looking at a page.
  Checking that an anchor RESOLVES is not the same claim as checking that a note LANDS
  there, and only the second is the product. Verify the generated file: the anchor must
  appear above its note. Test ordering, not distance — a note is legitimately pushed past a
  long display, but must never precede the text it concerns.
- **Ledger prose carries stray braces.** `S\{v_0}` -- an escaped opener with a bare closer
  -- ends the note's group early, and the build dies further down with "Extra }". Braces in
  a ledger field are literal or malformed, never grouping, since mathematics is held out
  separately; make them all literal.
- **A ledger is written by many hands and they bring their own preambles.** `\Av`, `\Proj`,
  `\rank`: sensible in the notation a searcher was thinking in, undefined in the
  paper being annotated. Emit a `\providecommand` stub for every macro a note uses that the
  base does not define -- a no-op where it exists, and `\ensuremath` makes it legal in text
  and mathematics alike. Telling searchers to use only the paper's macros is an instruction
  nobody can follow.
- **Dense margin notes cannot be made to work, so fall back rather than insist.** Margin
  notes are floats; past some density — a couple of dozen notes on a copy can be enough —
  LaTeX loses them whatever the pool size. Inline boxes
  are not floats and always place. Detect the failure and regenerate that one document
  inline, saying which and why. And note that `inline` is an option of the `\todo` command, not of the
  package: passing it to `\usepackage` is "Unknown option `inline'".
- **A note cannot go everywhere a paragraph can.** The insertion logic inherited from
  `write-critical-guide` avoids mathematics and verbatim blocks, and a list environment is a
  third such place: nothing may sit between `\begin{itemize}` and its first `\item`. LaTeX
  reports it as "Something's wrong--perhaps a missing \item", which names neither the note
  nor the list.
- **Every text transform must protect mathematics, not just the last one.** Two functions
  here each held `$...$` spans correctly, and composing them did not: the one that ran first
  stripped Markdown emphasis without protection, so a searcher's `$c^*$` -- a starred map --
  lost its asterisks to the italic rule and became `$c^$`, a superscript with no argument.
  It failed a thousand lines downstream at an unrelated `\todo`, reporting only "A left
  brace was mandatory here". Sanitise once, at the boundary, or make every transform in the
  chain protect the same spans.

## Open

- Whether Part I is written on a first run or only once the map supports it.
- Whether the entries appendix binds into the guide by default.
- Margin notes against inline boxes, beside display math.
