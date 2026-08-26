# The issue model and the `issues.yaml` ledger

Every finding in a critical guide lives in one place: `critical-guide/issues.yaml`. The
point-by-point issue list and the annotated LaTeX sources are both **generated** from it by
`annotate_tex.py`. Nothing is maintained in two places, so the prose and the annotation
anchors cannot drift apart — the failure that makes a referee note point at the wrong passage.

---

## Choosing the categories

Nothing in the tool knows what a category is: they come from the ledger, and everything —
tags, colours, output files, the annotated copies — follows from what you declare. So choose
categories that fit the paper rather than forcing the paper into a default.

**The default three fit most pure-mathematics papers**, and they work because they split by
*what the author has to do*, not by subject matter:

| Category | Tag | Colour | What it asks of the author |
|---|---|---|---|
| Mathematical | `M` | `red` | think — supply an argument, discharge a hypothesis, rename a symbol |
| References | `R` | `green` | look something up — check a locator, fix a record, add a citation |
| Typographical and editorial | `T` | `blue` | retype — grammar, usage, typesetting |

An author works through those three in different sittings and often in different moods, which
is the whole reason the split earns its keep.

**Depart from them when the paper warrants it.** A paper with substantial numerics or code may
deserve a `computational` category; one whose real problems are organisational may deserve
`exposition` separate from `typographical`; a survey may need `attribution`. Split
`mathematical` into `correctness` and `rigour` if the distinction is doing work for this
paper. Invent what fits — you are closer to the paper than this file is.

**A worked example.** A paper proposing a generalisation of an existing theory — where the
contested question is how much of it is new — was given a fourth category, `attribution`
(violet), separate from `references`. It carried the most consequential findings in the
package: an uncited paper producing the same headline examples, whose author was thanked in
the acknowledgements; a prior body of work under almost the same name; a remark in a cited
paper that already asserted the generalisation. None of those belongs in `references`, which
is about locators and records and asks the author to look something up. None is `mathematical`
either — the mathematics was fine. They ask the author to reconsider what they are claiming to
have done, which is a third kind of act, and it deserved its own file and its own colour.

The signal to watch for: when the paper's *claim to novelty* is the thing under examination
rather than its correctness, attribution is doing enough work to stand alone.

Two constraints, and they are the only ones:

- **A category that would hold one or two items is not a category.** Fold it into a
  neighbour and let the item's own text carry the distinction. Every category costs the
  reader another PDF to open.
- **Categories partition.** Every issue belongs to exactly one. If an item genuinely
  straddles two, file it where the *action* lies and cross-reference from the other with
  `depends_on` or a sentence.

**Colour guidance.** Any `xcolor` name works; it is used at `!12` as a fill and `!60` as a
border. Keep the hues far apart so a reader flipping between PDFs can tell them by glance
alone, and keep each category's colour stable across the package and across revisions. After
red / green / blue, reach for `orange`, `violet`, `teal`, `brown`. Avoid `yellow` and
`lime` — invisible at `!12` — and avoid a second colour close in hue to one already in use.

---

## Tag, grade, dependency, basis

Four independent attributes. Keep them independent; collapsing any two loses information the
author needs.

**Tag** — which category, and the identity of the issue. `[M-7]`, `[R-3]`, `[T-21]`. The same
tag is used in the issue list, in the summary's cross-references, and in the inline note, so
an author can move between them without translating. Tags are stable once assigned; if an
issue is dropped, retire its number rather than renumbering the rest.

**Grade** — what it costs.

| Grade | Meaning |
|---|---|
| `major` | affects correctness, or a reader cannot follow without reconstructing the argument |
| `minor` | should be fixed, but the reader gets there |
| `trivial` | copy-editing |

Grade by consequence, not by how much text the item takes to state. A misprinted subscript
that makes two displays contradict each other is major. A paragraph of clumsy prose is trivial.

**Dependency** — `depends_on: [M-2]`. This item is not an independent defect; its stated
argument rests on another finding, and its status follows from how that one is resolved. A
theorem whose proof fails only because a lemma it cites fails is one error, not two. Dependent
items are still listed — the author needs to know which downstream statements are affected —
but the guide must not present them as a longer list of separate problems.

**Confidence basis** — how you know.

| Value | Renders as |
|---|---|
| `direct-check` | a direct check, carried out in full |
| `assessment` | a feasibility assessment; the route looks viable but has not been written out |
| `reported` | reported from the source, not independently re-derived |

Every `major` finding carries one. "I checked this" and "this looks repairable" are different
claims, and a guide that does not distinguish them cannot be calibrated. `direct-check` is the
expectation and prints nothing per item — the issue list says once, in its preamble, that
unmarked findings are direct checks.

**Grade qualifier** — `grade_note: "for readability"` renders as *major (for readability)*. The
three grades are the machine-readable spine; the qualifier is where a referee's judgment
actually lives. "Trivial but should be reconciled" and "trivial" are different instructions to
an author, and both hand-made reports needed the distinction.

---

## Anchors — the one rule that decides whether the package builds

**An anchor must be a verbatim substring of exactly one line of the annotation base.**

Copy it out of the `.tex` file, macros and all — `The descent data of $\Acal$ consists of an
isomorphism`, not the rendered `The descent data of 𝒜 consists of an isomorphism`. Retyping
from the PDF produces anchors that will never match.

- Not found → lengthen or correct it against the file.
- Matches several lines → lengthen it until unique, or set `occurrence: 2` when the repetition
  is real and you want the second.
- The generator advances the insertion point past any straddling inline math or display, so an
  anchor on a line that ends mid-`$...$` is fine.

Run `annotate_tex.py check -v` before writing any prose. Fixing an anchor is cheap; fixing it
after four documents quote the passage is not.

---

## Schema

```yaml
paper:
  title: "The Azumification of orders"
  authors: ["Timothy De Deyn"]
  identifier: "arXiv:2606.05137v1"
  source: "../arXiv-2606.05137v1/azumification.tex"   # the annotation base; relative to this file
  submitted: "../2606.05137v1.pdf"                    # optional — the text actually under review
  locations_refer_to: "the arXiv source `azumification.tex`"

issue_list_name: "02-issues.md"

scope_caveat: >
  What this report does not claim to have certified.

caption_symbols:            # optional — extra macro→ASCII map for this paper's notation
  Acal: "A"
  bE: "E"

categories:
  mathematical:
    tag: M
    title: Mathematical
    colour: red             # any xcolor name; drives the todonotes tint
    output: annotated-mathematical.tex
    blurb: >
      One paragraph, printed in the annotated file's own header note.
    preamble: >
      Optional prose printed under the category heading in the issue list.
    sections:               # optional thematic grouping, in the order given
      - "Claims that carry weight and are not argued"
      - "A statement that is wrong as printed"
      - "Hypotheses assumed and never discharged"
      - "Notation a reader will trip on"
      - "Structure"
    sections_other: "Further items"     # heading for anything unassigned

  typographical:
    tag: T
    title: Typographical and editorial
    colour: blue
    output: annotated-typographical.tex
    blurb: >
      Grammar, usage, mathematical typesetting, and source formatting.
    sections:
      # A section may instead be a mapping, and may render as a table.
      - name: "Grammar and usage"
        render: table
        columns:
          - {header: "#",                field: id}
          - {header: "Location",         field: location}
          - {header: "The paper writes", field: quote}
          - {header: "Suggested",        field: request}
      - name: "Mathematical typesetting"
        render: table
        columns:
          - {header: "#",        field: id}
          - {header: "Location", field: location}
          - {header: "Issue",    field: note}
      - name: "Style"           # a bare string renders as prose

issues:
  - id: M-1
    category: mathematical
    grade: major
    section: "Claims that carry weight and are not argued"
    location: "§3, opening"
    anchor: "In this case being Azumaya is equivalent to being Azumaya in codimension one"
    caption: "Azumaya in codim. one: unargued"     # short label; index and note caption
    quote: >
      The paper's own words, if the issue turns on them.
    note: >
      The finding, and the argument for it. Where you can close the gap, close it here.
    request: >
      What the authors should do. Optional but usually worth writing.
    depends_on: []                                  # e.g. [M-2]
    confidence: direct-check
    occurrence: 1                                   # only when the anchor is deliberately non-unique
    render: prose                                   # force a full entry inside a table section
    grade_note: "for readability"                   # qualifier appended to the grade
    also: [T-3, T-5]                                # carry these in this issue's box

verified_clean:
  - source: "Tag 0B8J"
    statement: "Sheaves of Modules 17.11.7 --- finitely presented and free at a point implies free nearby"
    used_for: "openness of Azumaya (§2.3)"

not_verified: >
  What was not checked, and why.
```

### Required per issue

`id`, `category`, `anchor`, `note`. Everything else is optional; `grade` defaults to `minor`.

### Which fields go where

| Field | Issue list | Inline note | Header index |
|---|---|---|---|
| `id` | ✓ | ✓ | ✓ |
| `grade` | ✓ | ✓ | ✓ |
| `location` | ✓ | — | fallback for `caption` |
| `caption` | — | note caption | ✓ |
| `quote` | ✓ | — | — |
| `note` | ✓ | ✓ | — |
| `request` | ✓ | ✓ | — |
| `depends_on` | ✓ + dependency map | — | — |
| `confidence` | ✓ | — | — |
| `anchor` | — | placement | — |

The annotated source deliberately omits the quotation: the note sits at the passage, so
quoting it back is noise. The issue list deliberately includes it, since it is read away from
the paper.

---

## Bundling: `also:`

Two adjacent one-line nits in the same paragraph belong in one annotation box, not two stacked
boxes each a line tall. `also: [T-3, T-5]` on an issue carries those items inside its box:
they get no box of their own, and they still appear as their own entries or table rows in the
Markdown. The azumayification package does this throughout — 44 typographical tags in
34 boxes.

The build check accounts for it: the expected note count is the issues in the category minus
those bundled elsewhere, plus one for the header note.

---

## Note bodies are Markdown

`note`, `request` and `quote` are written as **Markdown**, because the issue list is Markdown.
The generator translates them for the LaTeX path: `"..."` becomes proper directional quotes,
`**bold**` and `*emphasis*` become `\textbf` and `\emph`, `` `code` `` becomes `\texttt`,
`---` becomes an em dash, and `&`, `%`, `#`, `_` outside math are escaped.

**`$...$` passes through untouched**, so write mathematics normally. A quotation containing
math still pairs correctly: `"reflexive as an $\mathcal{O}_X$-module"` comes out as one
quotation, not two stray marks.

Do not write LaTeX quoting (`` ``...'' ``) in a note — it would reach the Markdown literally.
Write `"..."` and let the generator do it.

---

## Prose entries and table entries

A section rendering as a **table** is the right form for bulk copy-editing — thirty one-line
usage corrections as thirty paragraphs is far worse to read and act on than one three-column
table. Reserve prose entries for items that need an argument.

When a single item inside a table section carries real consequence — a garbled sentence that
happens to be the one completing the proof — give it `render: prose` and it is lifted out of
the table into a full entry, keeping its tag. The original azumayification report does exactly
this with `[T-33]`.

Table sections still produce inline annotations in the LaTeX like any other issue; the table
governs the Markdown only.

---

## Generating

```bash
python3 annotate_tex.py check -v                  # anchors only; write nothing
python3 annotate_tex.py all --clean-aux -o .      # check, annotate, issue list, build
```

`all` ends with `build`, which compiles each annotated source with the pass sequence that
converges (`pdflatex`, `bibtex`, `pdflatex`, `pdflatex`) and then **checks the result** rather
than trusting the exit status: undefined references, LaTeX errors, note count against the
ledger, and whether the PDF is actually newer than its source. It exits non-zero when any of
those fail. One pass leaves every cross-reference reading `??`, and `make` reports success
anyway.

`check` is a hard gate: an anchor that no longer matches its source is an error, never a
silently dropped note.
