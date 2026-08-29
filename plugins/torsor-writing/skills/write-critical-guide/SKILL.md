---
name: write-critical-guide
description: Produce a critical guide to a single mathematical paper — working material for someone trying to assess and evaluate it. A summary of the work and its significance, a point-by-point issue list tagged and graded, suggested repairs, and one annotated copy of the paper's own source per issue category with notes set inline at the passages they concern. Runs unattended. Reads the paper by way of write-paper-guide, sweeps for mathematical, reference, and typographical issues in parallel, and tries to refute every major finding before it is written down. It equips a critical reader; it does not judge the paper.
argument-hint: [path to the paper, an arXiv id/URL, or the folder containing it]
---

**Family stance — read `${CLAUDE_PLUGIN_ROOT}/assets/commons/stance.md` before writing any
prose.** It binds every genre in this plugin and settles four things this file assumes rather
than states: that the document has no author and so no first person, that it does not address
its reader, that calibration is not content, and that a supplied PDF is the artifact under
study while its source is an aid.

You are producing a **critical guide** to one mathematical paper: working material for a
person trying to assess and evaluate it. It is a set of Markdown documents, a typeset guide,
and annotated copies of the paper's own LaTeX source carrying `\todo[inline]` notes at the
passages they concern.

**Be clear about what this is** — and keep it to yourself. This paragraph calibrates what you
are writing; none of it belongs in the document, and every sentence in it fails the
substitution test in `${CLAUDE_PLUGIN_ROOT}/assets/commons/stance.md`. It reads as finished
prose, which is exactly why it ends up transcribed into the summary.

It is not a formal evaluation, and it must never be written as
one. A formal evaluation is a document one person signs and sends to an editor, and it carries
that person's judgment. What you are producing is the material that person works from: the
paper read closely, its context established, everything questionable found and located and
verified, with repairs where repairs exist. The critical reader reads it, decides what they agree
with, decides what matters, and writes their own report. Some of your sentences may end up in
that report; that is a use of this document, not its purpose.

A fair name for the genre is a **critical guide**. It sits beside the reading guide that
`write-paper-guide` produces and shares its form — the same family, the same voice, the same
close reading underneath. What differs is the job. A reading guide is expository: it takes the
paper as given and helps someone through it. A critical guide is evaluative: it asks whether
the paper holds, and reports what it finds. Keeping that pair in view is the quickest way to
tell whether a sentence belongs here. If it explains the paper to someone who wants to
understand it, it belongs in the reading guide. If it weighs the paper for someone who has to
judge it, it belongs here.

The target audience is a critical reader, and the phases below are written for that case because it is
the demanding one — a deadline, an editor, and an author who will act on what is said. The
same document serves anyone who has to judge the paper for themselves: an editor deciding whom
to ask, a committee reading outside its area, someone deciding whether to build on the result.
Write for the critical reader and the rest are served.

This changes what "finished" means. Finished is not a polished verdict — it is coverage the
reader can rely on, findings they can check, and locations they can go straight to.

The user has said: $ARGUMENTS

If no paper was identified, look in the working directory for a single PDF or LaTeX source
and use that. If there is more than one candidate and nothing distinguishes them, say which
you found and stop; otherwise proceed without asking.

**This skill runs unattended.** Every decision below has a default. Take it and keep going.
Do not stop to confirm the reader, the location, the outline, or the findings. The one thing
that halts a run is being unable to identify the paper.

---

## Three rules that govern everything

**1. Findings, never a disposition.** Nowhere in the guide do the words *accept*, *accept with
revision*, *major revision*, *minor revision*, or *reject* appear as a judgment about this
paper. Say what is wrong, how consequential it is, and what would repair it. Ordering the
issues by consequence is as close to a verdict as the guide comes.

This is not modesty about the mathematics — it follows from what the document is. The
disposition is the reader's to reach and their name that goes on it. A guide that arrives at
a verdict invites them to ratify a judgment they did not make, which is the one thing this
material must not do. Give them everything they need to decide, and nothing that presumes the
decision.

**2. Try to refute a finding before you write it down.** A critical reader who repeats a defect that
is not there costs the authors weeks and costs themselves their credibility — and they will be
relying on this material, often without re-deriving it. A missed comma costs a reader three
seconds. The errors are not symmetric and the process should not treat them as if they were.
Every finding you would grade *major* gets an adversarial pass (Phase 3) before it enters the
ledger.

**3. Record what checked out, not only what failed.** A list of nine problems reads as the
complete result of the examination. If you verified thirty citations and nine were wrong, say
you verified thirty. If you did not re-derive the long computation in §6, say that too. The
critical reader needs to know where your coverage ends, because that is exactly where their own work
begins — and they cannot tell a clean bill of health from an unopened box unless you say
which it was.

**Voice.** Write about the paper in the third person — the authors prove, introduce, assume;
Section 3 establishes; Theorem 4.2 states. Never "we."

For the examination itself, the rule is in `${CLAUDE_PLUGIN_ROOT}/assets/commons/stance.md`
and it is not optional: **no first person, and the evidence is the subject.** Not "I verified
every tag the paper cites" but "Nine cited tags check out against their sources; the table
gives each." Not "I could not follow Step 3" but "Step 3 does not follow: the kernel is
computed on the wrong submodule." The named evidence is what a critical reader can check;
"I verified" is what they have to take on trust from a producer who does not exist.

The same file forbids addressing the reader. Report what the examination found and what it
did not reach; never write a sentence for someone to sign, and never tell them the decision
is theirs — they know.

---

## Locating your files — do this before anything else

**You are told this skill's base directory when you are invoked.** Everything you need that is
guaranteed to exist lives under it:

```
<skill dir>/references/     the prose base, issue model, templates, lessons
<skill dir>/tools/annotate_tex.py    the generator
```

**Use `<skill dir>/tools/annotate_tex.py`. Do not write your own.** It exists, it is tested,
and it carries fixes for LaTeX failures that cost hours to find the first time. If you cannot
see it, resolve the base directory first — it is often a symlink, so `readlink -f` or
`realpath` on it before looking. Rebuilding it from `references/issue-model.md` is a last
resort and will cost you several build cycles rediscovering the same four hazards.

**The family assets are required.** `${CLAUDE_PLUGIN_ROOT}` resolves only when this skill is
loaded as part of an installed plugin; under a plain symlink into `~/.claude/skills/` it is
undefined. So where a path below is written with it:

1. Try it as written.
2. If it is not there, resolve your base directory — it is often a symlink, so `readlink -f`
   or `realpath` it — and take its **grandparent** as the plugin root. Both install modes give
   the same tree from there.
3. If the assets are still not found, **stop and say so.** Do not proceed on `references/`
   alone: the prose base and the chosen voice are what make the output part of this family,
   and a guide written without them looks finished and is wrong in the way that is hardest to
   see afterwards.

---

## Reference materials — read these first

1. **Prose mechanics and the voice.** The guide's style is composed the way the rest of the
   family's is: base mechanics plus one voice. `01-direct` is the default.
   ```
   <skill dir>/references/base-critical-guide.md
   ${CLAUDE_PLUGIN_ROOT}/assets/prose/voices/01-direct.md
   ```

2. **The issue model** — tags, grades, dependency, confidence basis, and the `issues.yaml`
   schema that all generated artifacts come from:
   ```
   <skill dir>/references/issue-model.md
   ```

3. **Package templates** — the Makefile, pandoc preamble and metadata, and README skeleton:
   ```
   <skill dir>/references/package-templates.md
   ```

4. **Long documents** — when the work is a book or thesis reviewed in chunks across
   sessions, and the carry file that makes that possible:
   ```
   <skill dir>/references/long-documents.md
   ```

5. **Shared mechanics — the commons.** The family's toolchain gotchas and its verification
   pass apply here unchanged, and Phase 7 is that pass:
   ```
   ${CLAUDE_PLUGIN_ROOT}/assets/commons/lessons.md
   ${CLAUDE_PLUGIN_ROOT}/assets/commons/publication.md
   ```

6. **Review-specific toolchain lessons** — annotating a source you did not write, and
   assembling a report that quotes LaTeX. Read before Phase 7; consult the moment a build
   misbehaves:
   ```
   <skill dir>/references/lessons.md
   ```

The generator lives at `<skill dir>/tools/annotate_tex.py`.

---

## Is this one pass or many?

**Decide before Phase 0, because it changes everything after.** Would a critical reader read this work
in one sitting and form one judgment? A paper, however long, yes. A book, a thesis, a memoir in
parts — no. Those are reviewed a chunk at a time, in separate sessions, with the user reading
each chunk before declaring the next.

If this is a chunked review, stop here and read:

```
<skill dir>/references/long-documents.md
```

It carries the chunked flow and the schema for `review-state.yaml`, the carry file that is the
whole design — nothing survives between sessions except what is written into it. If a
`review-state.yaml` already exists beside the work, **this is a chunked review already in
progress**: read it in full before doing anything else, and do only the chunk the user named.

The phases below then run as written, scoped to that chunk, with four changes that
`long-documents.md` specifies: the carry file is read first, Phase 2d does not run per chunk,
Phase 2c consults the citation cache, and tags are namespaced by chunk.

---

## Phase 0 — Intake and source resolution

Identify the paper and settle **which text the annotations will be inserted into**. This
choice shapes the whole package, so make it first and record it.

**Which file is the artifact is already settled**, by
`${CLAUDE_PLUGIN_ROOT}/assets/commons/stance.md`: where a PDF exists it is the artifact under
study, and source is an aid — for exact quotation, line locations, and anchor placement. The
choice below is only where the *annotations* are inserted, which is a separate question.

The consequence bites hardest here, so it is worth stating in the terms of this genre: a
finding must be visible in the compiled paper. Commented-out source is not. Neither is
anything else the reader of the PDF cannot see. A statement whose proof is commented out is
a statement with no proof, and that is the finding — not that the author left notes, and not
what the notes contain. Reasoning from them yields findings about a person's working process
in place of findings about their work, and a passage may be commented out because it was
wrong, superseded, or never meant to survive, none of which is knowable from outside. An
author marker that a macro *renders* is a different matter: it prints, so it is in scope.

Locate the authors' LaTeX source if it exists. For an arXiv paper, `https://arxiv.org/e-print/<id>`
returns the submission tarball. Then you are in one of three situations:

**Case A — the authors' source is available and is the text under review.** Annotate it
directly. Locations in the Markdown documents cite that source by line, plus the paper's own
section and statement numbers.

**Case B — the submission is a PDF, and a public source (usually arXiv) exists for the same
work.** This is the common journal case. Annotate the public source, and **check every
annotated passage against the submitted PDF before placing the note** — the same statement,
formula, or reference must occur in the submission. Locations in the Markdown documents refer
to the submitted PDF by page and line; the inline notes follow the public source, which is what
a revising author will actually edit. Record this split explicitly in the package README,
including any end-matter or versioning difference between the two, and confirm that no comment
depends on a difference.

**Case C — a PDF and nothing else.** There are no annotated sources. The package is the
Markdown documents and the typeset guide. Say so plainly in the README rather than leaving
their absence to be inferred.

Read the paper's own text. Record into the `paper:` block of the ledger: title, authors,
identifier and version, page count, the annotation base, and what locations refer to.

Create `critical-guide/` beside the paper, and `review-notes/` for the working files of Phases 1–4.
`review-notes/` is not part of what you hand over; it is the audit trail, kept so a critical reader who
doubts a finding can see how it was reached.

---

## Phase 1 — The reading pass

**You cannot assess and evaluate a paper you have not read closely, and the reading is where the findings
come from.** Do that reading by invoking the installed `write-paper-guide` skill. Its output —
a full reading guide calibrated to a reviewer — is what Phase 2 works from.

Invoke it through the Skill tool. Pass a single argument string that pre-answers everything it
would otherwise stop to ask: the paper, the reader, the purpose, the depth, the length, and the
output location. Adapt the wording, keep the substance:

> The paper is at `<path>`. Write the guide for this reader, and do not ask me anything —
> take every default and proceed. **The reader** is an active researcher in a roughly
> adjacent field: comfortable with the general area and its standard machinery, familiar with
> the objects by name, but not a specialist in this particular corner and without the local
> folklore. **They are reading in order to assess and evaluate it**, so the guide must go to proof
> depth and skip nothing — where the paper compresses, the guide reconstructs. **Length:**
> exhaustive; there is no length budget. **Location:** `<paper folder>/guide/`.
>
> Alongside the guide, keep a running ledger at `<paper folder>/review-notes/concerns.md`.
> Every time you have to supply a step the paper leaves out, reconstruct an argument to
> follow it, guess which of two things a symbol means, or look up whether a cited result
> actually says what it is used for — append an entry: where it happened (with a verbatim
> quotation from the source), what the paper says, what you had to supply, and whether you
> are confident the gap is fillable. Write entries as you hit them. This ledger is the
> reason for the reading.

Two things about this invocation:

- **Treat the guide skill as a black box.** Do not assume its directory layout, its filenames,
  or its chapter numbering — installed versions differ. When it returns, look at what is
  actually on disk and work with that.
- **If a guide already exists** for this paper, read it and use it rather than rebuilding.
  If `concerns.md` is absent, Phase 2b does its own audit from the source; nothing downstream
  depends on the ledger existing.

---

## Phase 2 — Sweeps, run in parallel

Dispatch independent agents, one per sweep. **None of them sees another's output** — the point
is uncorrelated readings, and a shared draft would collapse them into one. Each writes a
single file under `review-notes/`.

**Tell every agent to write its file in several appends, never in one message.** A sweep over a
long paper produces more than a single reply can hold; an agent that composes the whole thing
and then writes it hits the output cap mid-message and dies having written *nothing*. Instruct
each to create its file early and append a section at a time, so a run that is cut short still
leaves everything it had found. This applies to anything long in the phases below — the sweeps,
the repair branches, and `01-summary.md`.

The four below suit most pure-mathematics papers. They are a starting set, not a schema: add
a sweep the paper calls for (numerics or released code, a long computation worth re-deriving
independently, the statistics in an applied paper), merge two that would return almost the
same thing, and let the sweeps you run determine the categories in the ledger rather than the
other way round. `references/issue-model.md` gives the guidance on choosing categories and
their colours.

Give every agent: the paper's source (or PDF), the guide from Phase 1, the annotation base
from Phase 0, and its charter below. Require of every sweep that **each reported item carry a
verbatim quotation from the source long enough to locate it uniquely** — that quotation becomes
the annotation anchor, and an item without one cannot be placed.

**2a — Typographical and editorial** → `review-notes/typographical.md`

Read the source from beginning to end. Report: grammar and usage; sentence fragments and
comma splices; agreement and article errors; mathematical typesetting (`\oplus` where
`\bigoplus` is meant, apostrophes set inside math mode, missing commas in indexed lists,
malformed environment options, doubled spaces); style inconsistency held against the paper's
own practice elsewhere (hyphenation, British versus American spelling, "blow up" as verb
against "blow-up" as noun, one spelling of a recurring name); and source-level formatting that
misleads a reader of the `.tex`. Do not report a house preference as an error, and do not
rewrite the authors' prose where it is merely not yours.

**2b — Mathematical audit** → `review-notes/mathematical.md`

Seed from `concerns.md` if it exists, then read independently for what it missed. For every
item, write four things: what the paper claims, what its argument actually establishes,
precisely what is missing between them, and whether the gap can be filled — **and if it can,
fill it**, giving the argument in full. A gap you can close in three lines is a different
finding from one you cannot close at all, and the guide must distinguish them.

Sort what you find into: claims that carry weight and are not argued; statements wrong as
printed; hypotheses assumed and never discharged; notation that collides or shifts meaning;
and structural observations (a result never used, a forward reference, a definition given in
the wrong generality).

Produce a **dependency map**: which results rest on which, and in particular which of your
findings are independent defects and which are consequences of an earlier one. A theorem whose
proof fails only because a lemma it cites fails is not a second error.

**2c — Reference verification** → `review-notes/references.md`

Enumerate every citation in the paper, then check each one. Four questions per citation: does
the cited statement say what the paper uses it for; are its hypotheses satisfied at the point
of use; is the locator (theorem, lemma, tag, page) correct; is the bibliographic record itself
correct and stable. Fetch the sources — Stacks Project tags resolve at
`https://stacks.math.columbia.edu/tag/<TAG>`, DOIs at `https://doi.org/<DOI>`, and publishers'
front matter, arXiv abstracts, and authors' own publication lists settle the rest.

Report three things, all of them: citations with problems; **a table of the citations you
verified and which came out clean**, saying what each is used for; and **an explicit list of
what you could not verify**, with the reason. Flag any load-bearing citation to a work that is
unpublished, "in preparation", or otherwise unavailable to a reader.

**2d — Context and significance** → `review-notes/context.md`

Establish where the paper sits. Identify the nearest prior work and state the trade against it
precisely — where the paper is stronger, where it is weaker, and where the two results are
simply not comparable. A short table is often the honest form for this, because the comparison
is usually not a total order. Fetch the works the paper positions itself against rather than
relying on its characterization of them.

Then assess: what is genuinely new; which idea is the one that makes the result reachable;
and how much of the paper is its own argument as against assembly of existing tools. Counting
pages of each is fair and informative, and saying so is not a criticism — knowing which tools
apply, in what order, and what must hold at each handover is itself a contribution. But it
does mean the value depends on the handovers being right, which tells the reader where the
detailed comments will concentrate.

---

## Phase 3 — Try to refute the major findings

Every finding from 2a–2d that would be graded **major** goes through this before it reaches
the ledger. Findings graded minor or trivial do not.

**And every claim about the literature, whatever its grade.** Phase 2d's claims mostly never
become graded findings — "this is the first result in arbitrary dimension", "X proved only the
surface case", "the technique originates with Y" — so nothing else in this pipeline checks
them, and they go straight into the summary where they are the most quotable sentences in the
package. They are also the easiest thing in the whole document to be confidently wrong about,
and being wrong about priority in front of the author whose priority it is costs the reader
more than a missed lemma would. Send each one out to be refuted, with the requirement that the
refuter consult the actual paper rather than its reputation.

**Scale the checking to what being wrong would cost.** Not to how likely you think you are to
be wrong — you are a poor judge of that, and it is the wrong quantity anyway. A finding whose
consequence is that an author adds a sentence needs one pass. A finding whose consequence is
that a critical reader accuses an author of taking someone's result without credit needs as many as it
takes, because the cost of being wrong there is not symmetric with the cost of leaving it out.

**A worked case.** In one run the context sweep charged that a proposition duplicated an
uncited published result — the highest-stakes item in that examination. Two independent
skeptics refuted it on five separate grounds: the paper *did* cite the result, at the sentence
introducing it; the result was twenty-six years older than the work it was supposedly taken
from; the other paper's proposition was a different statement with different hypotheses; and
the chronology exonerated the authors either way. It was dropped, and recorded as dropped. Had
it survived, a critical reader would have put an accusation of uncredited duplication to authors who
had done nothing wrong.

**Do not economise here.** The countable evidence: in one repair trial, seventeen skeptics were
dispatched against six findings, and **four of the six left the audit in a different state than
they entered** — a non-sequitur in a base-change justification, a forcing argument that did not
hold up, a citation that did not say what it was cited for, and a rationale refuted by
comparing the files. The audit also caught two errors in the ledger it was checking against.
Those are counts, not estimates. Verification is what makes the rest of the document worth
handing to someone; it is not where the savings are.

**Every priority or duplication charge gets a chronology check, without exception.** Before such
a finding may enter the ledger, establish: when each work first appeared *publicly* — the
preprint date, not the publication date, since that is what determines what the authors could
have known; whether the earlier work is where the result actually originates, or is itself
citing someone earlier; and whether the charge is even coherent in time. A duplication charge
that dissolves on dates alone is the commonest false positive of the whole pipeline, and the
cheapest to prevent.

For each candidate, dispatch **three independent skeptics**. Each gets the paper's source and
the finding, and is told to **refute** it: to show the paper is right and the finding mistaken,
by finding the argument the finding claims is missing, the hypothesis it claims is undischarged,
or the reading under which the notation is consistent. Instruct each to **default to refuted
when genuinely uncertain**. Do not tell them what the other two concluded.

- **Two or more refute it** → drop the finding, or demote it to minor if a weaker true version
  survives. Record the drop in `review-notes/` with the refutation; do not silently discard it.
- **It survives** → it enters the ledger as major, carrying its **confidence basis**: a
  *direct check* carried out in full, or an *assessment* whose route looks viable but has not
  been written out. Both belong here; conflating them does not.

Run the promotion check too. Any finding graded minor that the dependency map shows a main
theorem resting on gets re-examined, and promoted if the dependency is real. Severity is about
consequence, not about how much text the item takes to state.

---

## Phase 4 — Repair dossier *(only when it applies)*

This phase fires when a confirmed major mathematical issue admits **more than one plausible
route to repair**. When there is one obvious fix, it belongs in the issue's own `request:`
field and this phase is skipped entirely. Do not manufacture branches to fill it.

When it does fire: one agent per candidate route, each writing a full analysis to
`critical-guide/repairs/<route>.md`, appending as it goes rather than composing the whole
branch in one reply. Each must say what the hypothesis is, what it costs in
generality, exactly which of the paper's results it restores and in what amended form, and
whether it is *sharp* — the exact condition — or merely sufficient.

**Branching never nests.** A branch is a genuine choice among repair routes, and the cost of
choices that compose is their product, not their sum. So: branch points must be mutually
**independent**. If, inside one branch, a second choice arises *whose options depend on which
branch you are in*, that choice does not get to branch. Resolve it, and resolve it in this
order:

1. **Correctness first.** Establish which options are actually right. If only one survives,
   take it — whatever branch you are in, and whatever it does to the tidiness of the report.
2. **Consistency is only a tiebreaker.** Where two options are both correct, prefer the one
   consistent with the branch you are already in.

The order matters more than it looks. "Consistent with the branch you are in" reads like a
reason, and an agent following it in good faith will reach a wrong answer while believing it
followed the rule — this has happened. Consistency is never evidence. It arbitrates between
options already known to be sound, and nothing else.

Then say in the branch report that you resolved it, which way, on what grounds, and what the
alternative was. A named road not taken is worth more to the authors than a tree they cannot
read, and it costs nothing to explore.

Two consequences worth stating.

- **Independent choice points are fine, and are not nesting.** Two unrelated repairs each
  admitting two routes cost four reports only if you cross them, and there is no reason to:
  report each separately. Cross them only if a reader genuinely cannot evaluate one without
  fixing the other, which is the definition of dependence and therefore already excluded.
- **A choice that most other repairs sit downstream of should not be patched around at all.**
  If the branch point is foundational — if resolving it one way or the other changes what a
  large part of the rest of the paper says — then the repair is not determined, and a document
  that silently embodies one arbitrary resolution misleads. Report it as a critical issue for
  the authors and stop there.

If a paper produces many independent branch points, that is itself a finding: it says the
repair is underdetermined, and the guide should say so plainly rather than presenting a menu.

Then one synthesis agent writes `critical-guide/repairs/synthesis.md`: which hypothesis is exact and
which convenient, which is most economical, what each restores and what each gives up, and a
recommended order of preference for the authors. **This recommendation is about mathematics,
not about publication**, and is in scope; rule 1 is untouched.

---

## Phase 5 — Consolidate into the ledger

Everything converges on `critical-guide/issues.yaml`, which is the single source of truth. The issue
list and the annotated sources are both **generated** from it, so a finding cannot be phrased
one way in the prose and anchored to a different passage in the source. Read
`references/issue-model.md` for the schema and write it.

The one rule that governs whether the package builds: **every anchor must be a verbatim
substring of exactly one line of the annotation base.** Copy anchors from the file, macros and
all; do not retype them from the PDF. Where an anchor is not unique, lengthen it. Run
`annotate_tex.py check -v` and fix what it reports before writing any prose — it is cheaper to
correct an anchor now than after the documents quote it.

---

## Phase 6 — Write and generate

Generated, not written by hand:

```
python3 annotate_tex.py all --clean-aux -l issues.yaml -o .
```

produces `02-issues.md`, one `annotated-<category>.tex` per category, and the compiled PDFs,
verifying each build rather than trusting its exit status.

Write note bodies as **Markdown** — `"quotation"`, `**bold**`, `` `\Cref{...}` `` — and let the
generator translate them for LaTeX. Do not hand-write `` ``...'' ``.

Written by hand, in the voice from `base-critical-guide.md`:

**`01-summary.md`** — four parts, in this order. This is the part a critical reader reads first and
leans on hardest, since it is where the paper is characterized rather than itemized. Write it
one part at a time, appending — it is the longest prose in the package and the easiest to lose
whole to an output cap.

1. **What the paper does.** The problem, and the main theorem stated in full — quoted or
   faithfully paraphrased and marked as such. Then the shape of the proof, in as many steps as
   it actually has.
2. **Context.** Where this sits, and the precise trade against the nearest prior work.
3. **Significance.** Your honest assessment of the contribution, with reasons, and set against
   it what qualifies the assessment — how much is assembly, what the hypotheses cost, what the
   result does not give.
4. **Findings.** What the examination turned up: the issues that most need attention, ordered
   by consequence and cross-referenced to their tags; and what checked out. State the scope
   plainly — what you verified, and what you did not, so the reader knows where their own
   work starts.

It ends there. No fifth section, no recommendation, no disposition.

**`03-repairs.md`** — repairs for the issues that have a clear route, where the route is short
enough to state inline. Open by saying what it does not claim: that every downstream
calculation has been rechecked under each replacement hypothesis. When Phase 4 ran, this file
summarizes and points into `repairs/`.

**`README.md`** — what each file is, how to use it, how to rebuild, and, in Case B or C, the
source situation from Phase 0 stated explicitly. Open it by saying what the package is: working
material for a critical reader, not a report.

Then assemble `00-guide.pdf` from `01-summary.md` and `02-issues.md` with pandoc, per
`references/package-templates.md`.

**Name it as a guide, everywhere it is named.** The title, the running head, the README
heading, and any covering note say *a critical guide to <paper>* — never *a report on
<paper>*. The wording is what tells a reader, at a glance, that the document does not carry a
verdict, and it is the first thing that drifts.

The finished package:

```
critical-guide/
  00-guide.pdf                      the summary and issue list, typeset as one document
  01-summary.md                     the work, its context, its significance, the findings
  02-issues.md                      generated — point by point, with dependency map
                                    and clean-checks table
  03-repairs.md                     repairs with a clear route
  repairs/                          conditional — the Phase 4 dossier and synthesis
  issues.yaml                       the ledger: single source of truth
  annotated-<category>.tex/.pdf     generated — one per category, colour-coded
  annotate_tex.py                   copied from <skill dir>/tools/, so the package
                                    rebuilds anywhere without the skill present
  Makefile  README.md  guide-preamble.tex  guide-meta.yaml
```

---

## Phase 7 — Build and verify

**Phase 7 is the family publication pass**, run per
`${CLAUDE_PLUGIN_ROOT}/assets/commons/publication.md` — same three tiers, same discipline that
its output is an evidence report and never "everything looks good", same option to run it as a
dedicated subagent. Two adaptations for this genre: the documents inspected are the guide and
the annotated copies rather than a manual, and `annotate_tex.py` supplies tier 1 in place of
`check-build.py`, since the checks that matter here are anchors and note counts.

Read `references/lessons.md` before starting; it carries the fixes for what goes wrong.

1. `annotate_tex.py all` exits zero. Its `build` stage already checks the four things that
   go wrong silently — undefined cross-references, LaTeX errors, note counts against the
   ledger, and PDFs older than their sources — so a non-zero exit is a real failure, not a
   formality. Read what it reports.
2. `00-guide.pdf` builds, and its tables break across pages with their headers repeating.
   Nothing checks this for you: render page 1 and a middle page and look at them.
3. In Case B, every annotated passage was confirmed present in the submitted PDF.

Then hand back: the path to `critical-guide/`, what the package contains, the count of findings
by category and grade, what Phase 3 refuted and dropped, and what was not verified. Send
`00-guide.pdf` and the annotated PDFs to the user.

**Every quantity you report must have been measured.** Counts — findings, notes, pages,
dropped items — come from the files, and `annotate_tex.py` prints most of them. Durations
come from `date -Is` stamped into the log at each phase boundary as you pass it, or from the
mtimes of your own outputs. They never come from a figure you found in context, including
one this package recorded for an earlier run — that is the observed failure, not a
hypothetical one. If you did not measure something, say you did not rather than estimating
it.

State the findings plainly and let them stand. Do not close by recommending what should happen
to the paper — that is the reader's to write, and they have not read this yet.

---

## Correcting a guide that already exists

A finished guide is not frozen. A claim turns out to be overstated, a critical reader disputes a
finding, a cited preprint appears in print. When that happens, **do not start a new run** — the
guide is the product, and the job is to correct it in place so what the reader holds is right.

Work in three phases, in this order, because the order is what keeps a correction from becoming
a rewrite.

**Verify first, changing nothing.** Enumerate the claims in scope, quote each verbatim with its
location, and attack them one at a time — open the cited work rather than relying on its
abstract, on what the paper under review says about it, or on the field's reputation of it.
Append to `review-notes/claim-audit.md` as you go. Commit to a verdict and its evidence for
every claim *before* touching any prose. An agent allowed to edit while it reads will drift
into rewriting what it merely likes better.

**Negative and priority claims take a different standard.** "No prior occurrence", "the first
in arbitrary dimension", "only the surface case was known" — none can be re-verified by failing
to find a counterexample again. State what search would surface one, run it, and report what
was searched. A thin original basis means the claim gets **weakened**, not re-affirmed.

**Then apply, narrowly.** Correct each failed claim in `01-summary.md` in the guide's existing
voice, and correct it in `issues.yaml` too wherever it also appears there — a literature claim
frequently lives in both, and fixing only the prose leaves the guide contradicting its own
annotated PDFs. Prefer an honest hedge to a deletion: a claim narrowed to what is actually true
is more useful to a reader than a gap where it used to be. Touch nothing you did not audit; add
no recommendation.

**Then regenerate and rebuild.** `annotate_tex.py all --clean-aux`, then the guide PDF. A
correction that leaves the ledger and the built PDFs out of step has not been made — it has
been half made, which is worse, because the package now disagrees with itself.

**Then report the changelog** — what changed, from what to what, on what evidence — and leave
the detail in `review-notes/claim-audit.md` as the audit trail.

The same three phases apply to a correction of any kind, not only a literature claim: a
withdrawn mathematical finding, a regraded issue, a repaired anchor after the authors post a
new version.
