---
name: write-pure-math-paper-and-supplement
description: Use when an original pure-mathematics result should be published as a PAIR of documents — a streamlined journal paper (the "core") that a typical expert reads, and a companion Supplement that makes the pair as self-contained as reasonably possible by giving every proof the core states, sketches, or credits. Builds both from notes, proofs or an existing manuscript, with cross-document references (xr), a status-preserving split of every statement, an inputs appendix, a core-to-supplement concordance, versioned snapshots, and journal-layout PDFs (optionally also torsor house-format PDF/HTML/EPUB/Markdown). Extends write-pure-math-paper. Triggers: "paper and supplement", "core paper plus supplement", "split this manuscript into a journal paper and a supplement", "the paper is too long; move details to a supplement".
---

# write-pure-math-paper-and-supplement

You are writing an **original pure-mathematics paper as two documents**:

- **the core**: a conventional journal paper. It states every result the work claims, proves
  the ones that carry the new ideas, and states precisely, credits, and *points to the
  Supplement for* the material a typical expert would accept or skip;
- **the Supplement**: the complete account. It contains full proofs of everything the core
  states, sketches, or imports, from foundations the authors name, at whatever length and
  with whatever verifications (sign checks, conventions, comparisons) that requires.

The pair, not the core alone, is self-contained. The core says so in one plain sentence, e.g.
"The Supplement [S] is our attempt to be as self-contained as reasonably possible, for the
reader's convenience." This frees the core to read like a paper an expert would want to read,
and frees the Supplement from any length constraint.

The user has said: $ARGUMENTS

## This skill extends write-pure-math-paper — load it first

Read **in full** the sibling skill `${CLAUDE_PLUGIN_ROOT}/skills/write-pure-math-paper/SKILL.md`
and everything it tells you to read (stance, prose base, voice, commons scaffold, lessons and
publication pass). If `${CLAUDE_PLUGIN_ROOT}` does not resolve, resolve this skill's base
directory (`realpath`) and take its grandparent as the plugin root. If the sibling skill or the
assets still cannot be found, stop and say so — do not improvise the house assets.

**Everything in write-pure-math-paper applies to both documents** — its five rules, its Phases
0/A/B/C/D, its audit artifacts, its integrity and publication gates — **except where this file
says otherwise.** This file adds the split, the pair mechanics, and the pair gates.

Two rules are added to its five:

6. **The split never changes status.** A statement has the same hypotheses, conclusion and
   status (theorem / proposition / claim / conjecture / open) in both documents. Moving a proof
   to the Supplement is an editorial act, never a mathematical one: no statement becomes
   "standard" or "well known" because its proof moved.
7. **Every pointer resolves to a proof.** Each core statement whose proof is not complete in
   the core names the Supplement item that completes it, and that item exists and proves
   exactly that statement (or something visibly stronger).

## Defaults (each overridable by the user)

| Setting | Default |
|---|---|
| Core page budget | 40 pages in the journal layout; ask only if the material obviously cannot fit |
| Layout of both | journal layout: full US-letter page, 1in margins, default 10pt, standard amsthm styles (plain/definition/remark), **no callout boxes**, **no `parskip`** (it zeroes `\topsep`, so theorems run into the text), standard indented paragraphs, standard spacing around theorems and proofs. Do not squeeze to save pages |
| House-format editions | optional, on request: the same sources rebuilt in the torsor house format (PDF/HTML/EPUB/MD) as separate snapshots |
| Supplement front | its own title block ("Supplement to *Title*", same authors, date) and an "About this supplement" section with the concordance table |
| Authors | as for write-pure-math-paper (`torsor lab` unless the user gives a list) |
| Output location | a `versions/` directory of labelled snapshot pairs (see Versioning) |

## Phase 0 additions — what the core may rely on

Record in `paper-notes/paper-brief.md`:

- the **core budget** and the intended journal readership;
- the **foundations** the Supplement may start from (textbooks, named manuscripts, specified
  prior papers) and the rule for literature: by default, **literature is credit, not a logical
  input** — the pair proves what it uses from the named foundations; any exception
  (a specific appendix, a specific paper) is recorded explicitly as an author decision;
- the authors' own earlier papers, and the **self-reference convention**: in running text the
  authors' prior work is "X, Y, and the first author", "X and the authors", never their names in
  the third person; the abstract cites by reference ("the two-point statement of [7]");
  bibliography entries unchanged.

## Phase A additions — the split ledger

Add one column to `theorem-inventory.md`: **placement**, with exactly these values (they are
also the key of the concordance table the Supplement prints):

| Placement | Core | Supplement |
|---|---|---|
| **full** | statement + complete proof | same statement; proof possibly longer or with checks |
| **short** | statement + condensed proof or sketch, ending in a pointer | complete proof |
| **stated** | precise statement, credited where classical, pointer, no proof | complete proof |
| **here only** | absent (at most mentioned) | statement + proof |

Choose placement by the reader's need, not by convenience:

- **full in the core:** the main theorems, the decisive new lemma(s), and any argument that
  carries a new idea — even if long. A paper whose new idea lives only in a supplement is not a
  paper.
- **short:** proofs whose idea fits in a paragraph and whose remainder is verification
  (bookkeeping, sign and convention checks, degree counts, routine inductions).
- **stated:** foundational facts of the kind an expert in the area accepts on sight — but only
  when the Supplement proves them. Credit them where classical, and state them *in the exact
  form used*.
- **here only:** background re-derived for self-containment, comparison with other
  conventions, alternative proofs, extended examples, worked computations, provisional or
  exploratory extensions (clearly labelled), and long remarks.

Record the placement of every inventory item; the integrity gate in Phase D checks it.

## Phase B additions — the pair architecture

Present to the user, with the nine sentences and outline of write-pure-math-paper:

1. the **core outline** with an estimated page count per section against the budget;
2. the **Supplement outline** — it is usually the complete manuscript in dependency order,
   with appendices for foundations, standard results proved from scratch, and background;
3. the **split ledger** summary: counts of full / short / stated / here only, and the list of
   *stated* items (these are what the core asks the reader to accept);
4. the core's **inputs appendix** plan (below).

Get agreement before authoring.

## Phase C additions — authoring the pair

**Order.** Establish the Supplement as the complete reference first (assemble it from the
manuscript or write it), then cut the core from it. The core is the streamlined document; the
Supplement is never "the leftovers".

**Directory layout** (one snapshot pair; see Versioning):

```
versions/
  core-vNN/          main.tex  preamble.tex  sections/  Makefile  core-vNN.pdf  [REVISION-LOG.md]
  supplement-vNN/    main.tex  preamble.tex  sections/  concordance.md  supplement-vNN.pdf
  README.md          the table of snapshots
  Makefile           convenience: copy the latest of each format to stable names
```

**Cross-references** — `xr`, prefixes `S-` (in the core) and `C-` (in the Supplement):

```latex
% core preamble
\usepackage{xr}
\externaldocument[S-]{../supplement-vNN/main}
\newcommand{\supp}[1]{Supplement,~{\NoHyper\cref{S-#1}\endNoHyper}}      % "Supplement, Theorem 5.6"
\newcommand{\suppsec}[1]{Supplement,~{\NoHyper\S\ref{S-#1}\endNoHyper}}  % "Supplement, §4"
\newcommand{\suppl}[1]{Supplement,~{\NoHyper\cref{#1}\endNoHyper}}       % lists: \suppl{S-a,S-b}
% supplement preamble: \externaldocument[C-]{../core-vNN/main}, \core{...} likewise
```

Keep labels identical across the two documents for the same statement wherever possible
(`thm:log` in both), so pointers and the concordance are mechanical.

**Build order.** Each document reads the other's `.aux`. Build supplement → core → supplement
(`latexmk -g` on the second supplement pass). Never delete a sibling's `.aux` before building;
a missing `.aux` silently produces "??" everywhere. A snapshot's Makefile builds the pair:

```make
SUPP := ../supplement-vNN
pdf:
	cd $(SUPP) && latexmk -pdf -interaction=nonstopmode main.tex >/dev/null 2>&1 || true
	latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
	cd $(SUPP) && latexmk -g -pdf -interaction=nonstopmode main.tex >/dev/null 2>&1 || true
	cp main.pdf core-vNN.pdf; cp $(SUPP)/main.pdf $(SUPP)/supplement-vNN.pdf
check:
	@grep -c "LaTeX Warning: Reference" main.log || true
	@grep -c "undefined" main.log || true
	@pdfinfo main.pdf | grep Pages
```

**Core introduction.** As in write-pure-math-paper, plus:

- **Prior work, matter-of-fact.** Say plainly what was previously in print, with precise
  locators, then what this paper does. No "actually this aspect is not new", no contrastive
  novelty framing, no priority claims the record does not support. **Big central credits in the
  introduction; smaller credits next to the statement or proof they concern.** Keep the
  introduction lean.
- **Clarifying, not correcting.** When a prior statement must be read in a particular way to
  agree (e.g. locally rather than globally), say how it is to be read, in one sentence, and put
  the explanation in the Supplement.
- **The Supplement paragraph.** One short paragraph: the self-containment sentence; which
  statements the core states without full proof and where the list is (the inputs appendix);
  what the Supplement starts from. State only useful facts — not, e.g., that manuscripts are
  unpublished, and no internal project names.
- **What is not claimed** and **standing hypotheses**: as in write-pure-math-paper; each
  hypothesis lists where it is used, in both documents.

**Core inputs appendix** ("Statements used without proof"): a table of every *stated* item and
every *short* item whose omitted part matters, each with its Supplement location; note any
item the core *does* prove elsewhere (duplicates happen after streamlining).

**Supplement front matter.** Title block; "About this supplement": what the core is, the
self-containment sentence, what the Supplement starts from, and the **concordance table**
(core number → Supplement number → placement key full/short/stated/here only), generated from
the split ledger and kept in `concordance.md` as well. Number the Supplement independently;
never try to make the two numberings coincide.

**Supplement body.** The complete proofs, in dependency order, with "here only" material
clearly marked as such. Provisional or exploratory additions carry their status in the
statement title ("Claim", "Provisional") and are excluded from anything the core relies on.

## Phase D additions — pair gates

Run the write-pure-math-paper integrity pass on **each** document, then these pair checks.
For substantial pairs, dispatch an **independent checker agent** (no access to your reasoning,
only the two sources and the split ledger) and fix what it confirms:

1. **Statement agreement.** For every item placed full/short/stated: hypotheses, conclusion
   and status agree between core and Supplement (notation differences allowed, recorded).
2. **Pointer resolution.** Every `\supp`/`\suppsec`/`\suppl` resolves, and the target proves the
   statement pointed from. Zero undefined references in both logs.
3. **No silent dependence.** No core proof uses a Supplement-only result without a pointer;
   no Supplement proof uses a core result that is itself only stated.
4. **Inputs appendix complete** against the split ledger; concordance matches the ledger.
5. **Hypothesis lists** in both documents agree on where each hypothesis is used.
6. **Redundancy.** After the first full draft, run one streamlining pass on the core (remove
   repetition, restatements, over-long remarks) and then **recheck correctness** — streamlining
   is where false sentences and lost hedges creep in.
7. **Budget.** Core page count within budget in the journal layout.

**Build and visual gates (both documents, every format built):**

- zero undefined references/citations; no overfull boxes beyond trivia (fix them: break
  displays, `\allowbreak`, reorder words — never change mathematics to fix layout); no
  hyperref/font warnings;
- **visual inspection**: render pages (`pdftoppm -r 70 -png`) and look — title, TOC, hypothesis
  lists (description labels wider than `leftmargin` break onto their own line), theorem-dense
  pages, long displays, bibliography;
- house-format editions, if built: cross-document references render as plain text
  ("Supplement, Proposition 11.24") in HTML/EPUB/MD; EPUB passes `epubcheck` with 0 errors
  and 0 warnings (pandoc's output usually needs post-processing: `label=` attributes →
  `data-label=`; MathML `minsize`/`maxsize`; `mfrac displaystyle` → wrapped in `mstyle`;
  `mathml` property declared on every XHTML item, including the nav).

## Versioning — never overwrite

Every milestone is a frozen **snapshot pair** `core-vNN` + `supplement-vNN` (letters for small
follow-ups: `v06a`, `v06b`; suffix `-house` for house-format editions), each with:

- its sources and its built PDF(s); cross-references pointing to the sibling snapshot;
- a git tag per document and a row in `versions/README.md` saying what changed;
- a `REVISION-LOG.md` for revision passes (each change, and its reason).

Never edit a frozen snapshot — copy it to the next label, repoint the sibling paths, edit,
build, freeze. A `versions/Makefile` copying the latest snapshot of each format (by `sort -V`
over the snapshot directories that contain the file) to stable names saves the user hunting.

## Suggested companions

After a draft pair exists, these torsor-writing skills operate on the **core** (with the
Supplement as its companion): `write-critical-guide` (examination), `write-paper-repairs`,
and `write-correspondence-guide` (placement in the literature). Feed their findings back as a
new snapshot pair; credits found by a correspondence guide go in per the matter-of-fact rule
above.

## Common mistakes

| Mistake | Do instead |
|---|---|
| Moving the decisive argument to the Supplement to meet the budget | Keep it full in the core; cut elsewhere |
| A "stated" fact the Supplement does not actually prove | Prove it in the Supplement or change its status to imported, explicitly |
| Core and Supplement versions of a statement drift apart in revision | Revise both in the same pass; gate 1 |
| Calling a moved proof "standard" or "well known" | It is "proved in the Supplement"; credit separately |
| Squeezing layout (parskip, tight lists, small type) to hit the budget | Standard spacing; cut text instead, or ask to raise the budget |
| Building the core with the Supplement's `.aux` missing | Build supplement → core → supplement |
| Editing a frozen snapshot | New label, new directory, new tag |
| "Actually this isn't new" in the introduction | State plainly what was in print, then what the paper does |
| Naming the authors in the third person when citing their own work | "X, Y, and the first author" |

The final test is the one of write-pure-math-paper, applied to the core, plus:

> Could a reader who wants every detail find, from each core statement, the place in the
> Supplement where it is completely proved — and would that proof prove exactly that statement?
