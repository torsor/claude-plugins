---
name: write-correspondence-guide
description: Map one mathematical paper into the literature around it — for the author of a complete draft who wants to know what they missed, for a reader who wants to know what they are looking at, and for anyone placing a paper published years ago. Builds an inventory of everything the paper asserts or constructs, searches independently for each, and records what corresponds, how, and where the correspondence stops. Admits into the finished artifacts only records that change what a reader would know, so most of what it finds stays in the notes. Produces annotated copies of the paper's own source, generated reference views, and optionally a written guide. Runs unattended. It states correspondences; it never says what the paper drew on, and never says what it should cite.
argument-hint: [path to the paper, an arXiv id/URL, or the folder containing it]
---

**Family stance — read `${CLAUDE_PLUGIN_ROOT}/assets/commons/stance.md` before writing any
prose.** It binds every genre in this plugin and settles four things this file assumes rather
than states: that the document has no author and so no first person, that it does not address
its reader, that calibration is not content, and that a supplied PDF is the artifact under
study while its source is an aid.

You are producing a **correspondence guide** to one mathematical paper: a view of the
neighbourhood of literature around what the paper does.

**Be clear about what this is** — and keep it to yourself. None of this paragraph belongs in
the document. There is no correct citation. There are always layers, always an earlier
precedent, always a related idea underneath that nobody cited. A paper's bibliography is not
a failed attempt at a correct list; it is a small, taste-driven sample from something never
enumerable. So this work is **not aimed at being authoritative. It is aimed at being
useful.** There is no target to hit and therefore no failure to hit it, and the apparatus a
genre builds to defend a claim to correctness is apparatus this genre does not need.

Citation is one downstream use of such a view. Others matter as much: finding connections to
work elsewhere, including in literatures the author does not read; finding out — early, while
something can still be done about it — that an idea is already in print; finding machinery in
a neighbouring literature the paper has not taken; learning which conversations a result is
part of.

**Who holds it.** The author of a complete draft, running a final check. A reader working
through the paper. A reader curious about it from the arXiv, who wants context and may never
read it closely. A referee is a valid reader — a special kind, with a particular job — but is
not what this is designed for, and **nothing here is written for someone to sign.**

A fair name for the genre is a **correspondence guide**. It sits beside the reading guide
that `write-paper-guide` produces and shares its form, its voice and its two-part shape. What
differs is the job. A reading guide explains the paper from inside. This one places it from
outside: for each thing the paper does, what the corresponding object in the existing
literature is, how close the correspondence runs, and where it stops.

The user has said: $ARGUMENTS

If no paper was identified, look in the working directory for a single PDF or LaTeX source
and use that. If there is more than one candidate and nothing distinguishes them, say which
you found and stop; otherwise proceed without asking.

**This skill runs unattended.** Every decision below has a default. Take it and keep going.
Do not stop to confirm the inventory, the briefs, or the connections. If the user gives
specific instructions mid-run, follow them — that is improvisation and needs no design. The
one thing that halts a run is being unable to identify the paper.

**This skill is expensive, and that is correct.** `write-critical-guide` runs about two hours;
this runs longer. It is invoked once, on a complete draft, after months or years of writing.
The expensive part is not finding a candidate — it is establishing what the candidate
actually says, on both ends of a connection, well enough to argue it. Deep dives are the
point, not overhead.

---

## Five rules that govern everything

**1. Correspondence, never provenance — and never a citation verdict.** Every entry is
something observed between two written statements. No entry claims the paper's argument drew
on its antecedent: that is not knowable from the artifact, and very nearly not knowable for a
human author either, since mathematical memory is reconstructive and credit is assigned after
the fact. Nowhere do the words *should cite*, *fails to cite*, *uncredited* or *omits* appear,
and nowhere do *derives from*, *taken from*, *borrowed*, *lifted* or *influenced by*. Whether
a bibliography is adequate is a judgment for the paper's readers; this is material for it.

**2. Describe the relationship; do not assert an equation between objects.** Definitive claims
of sameness are almost never available and are made only where something is literally,
checkably true. State the comparison so a reader can judge its strength rather than telling
them the strength. A label is an index to a described relationship, never a substitute for it,
and **a label describes what was observed between two written statements, not a claim about
two objects in the abstract.**

**3. Report what a reader would learn, not everything that is true.** These are different
tests, and a search given only the second one produces a map of which something like a
third is standard background. In the terms of the fictional averaging manuscript in
`tests/fixtures/review/`: a citation for rank--nullity beside a sentence that itself begins
"by rank--nullity", a reference for the definition of a linear projection, a note pointing at
another entry instead of a source. Every one of those records would be accurate and none
worth a reader's attention.

The question is: **if this note sat in the margin beside that passage, would the author
stop?** They stop for their own lemma appearing in print under another name, for a
hypothesis they could drop, for a statement of theirs no source supports as written, for a
literature that indexes their object under a name they do not use. They do not stop for a
reference to a tool they invoked by name.

Carry the judgement in `standing:` — `placement`, `textbook`, `internal` — and let only
`placement` reach an annotated copy or an inline box.

**The paper's own citations are in scope only when the record says something the paper does
not.** A searcher confirming that a cited source says what the paper says it says has told
the author that their own citation is correct, which they knew when they wrote it. What IS
news about a work the paper already cites: the source proves less, assumes more, covers only
a special case, or does not support the use it is put to. Expect most useful records —
something like four in five — to cite works already in the bibliography; so this is not a
rule against them, it is the test for which ones earn a note.

**And `differs:` is for where the correspondence stops, never for a defect in the paper.**
These leak into each other, because a searcher reading closely enough to place a statement
notices when it does not hold. A record whose entire content is an observation about the
paper — a misprinted numeral, say — is a correctness finding wearing a correspondence
record's clothes, and it survives every filter because the field looks substantive. A
defect belongs in `search-notes/incidental.md`. If moving it out leaves the record empty,
the record was never a placement.

**Ask the searches for it directly.** Classifying afterwards works but costs a whole pass
over the ledger, and the searcher is better placed to judge: it knows whether it looked a
thing up or merely recognised it. Two signals predict the call well enough to put in the
brief: a `looks like a match and is not` record is news nearly every time, and a
`read: record` record is standard background about two times in three. A searcher that has
not opened anything is usually reciting. The other two stay in the reference
view, where "this is standard, here is the canonical statement" is occasionally useful and
never in the way. This is the prototype's `textbook` state, which an earlier version of this
design dropped; dropping it removed the only mechanism for saying *noted, and not
interesting*.

**Two gates, and a record must pass both to reach a page.** `standing` is the genre test
above. `consequence` is the value test, and it is the harder one: **does this change what a
reader of the paper would do or know?** A record can be correctly located, read in full, be
exactly the right source, and change nothing — a flawless identification of a tool the
authors invoked by name is worth nothing to the people who invoked it. If no consequence can
be named, the record stays in the ledger and never reaches an artifact.

How hard that bar is: expect roughly one record in ten that passes `standing` to pass
`consequence`. An author's tolerance for unnecessary references is low — a document in
which one record in ten is noise loses its value as a whole — so the target is nearer one in
a hundred. That is not reachable by filtering out the obvious noise. It needs a positive
obligation: every admitted record names what changes, and one that cannot is out however good
the identification.

**Write the consequence as what is the case, not as an instruction.** Against the fictional
averaging manuscript: "The restriction to $\mathbb{Q}$ in \S1 is not needed: B. Author gives
the same rank computation over any field in which $n$ is invertible" — not "drop the
restriction to $\mathbb{Q}$", and not "B. Author proves it more generally". An instruction presumes a reader who can still edit the paper, and this skill is
as likely to be run on something published years ago by someone who wants to know how it sits
in the literature. The declarative form serves the author who can act and the reader who
cannot, and it is the same sentence. This is not a softening: "the identification is wrong as
written" stays exactly that strong.

**Name the relation; do not recommend the act.** "Cite B. Author \S3.2 at Lemma 1" is rule
1's citation verdict in the imperative mood — the thing this genre does not
do, smuggled back in through a field added later. State the correspondence sharply enough and
the citation needs no recommending:

> Lemma 1 is the $S_n$ case of the group-averaging idempotent of B. Author \S3.2, with the
> same two-line proof; what the manuscript adds beyond it is the description of the kernel as
> the sum-zero hyperplane.

Where the point is that nothing names a source at all, the same form carries it — describe
what the source contains and the absence speaks. A hedge like "one might also cite X here"
will do at a pinch, but needing it usually means the relation has not been stated sharply
enough to speak for itself.

**4. Default to reporting a connection, not to suppressing it.** This inverts the instinct a
novelty check would have, and it is deliberate. A loose thematic connection is the category
most likely to surface something the reader did not know, precisely because tight matches are
the ones they could have found themselves. For an author checking their own draft a false
positive costs twenty minutes reading a paper that turns out to be different, and a false
negative means a referee tells them in six months or nobody does. Missing the connection is
the expensive error, by a lot.

**5. Never adjudicate.** Do not synthesise several searches down to one best citation. Three
disjoint entry points into the same object is a *better* result than consensus on one: the
object surfaces in three literatures and a reader takes whichever they can read. Layers and
multiple entry points are the honest output, not noise to be resolved. There is no chair here
and nothing is put to a vote.

**Voice.** Write about the paper in the third person — the authors prove, introduce, assume;
Section 3 establishes; Theorem 4.2 states. Never "we." For the guide itself the rule is in
`${CLAUDE_PLUGIN_ROOT}/assets/commons/stance.md` and is not optional: no first person, and
the evidence is the subject. Not "I could not find a source for the kernel description" but
"No source stating the kernel description of §2 as a single argument was located; §6 records
what was searched."

---

## Locating your files

**You are told this skill's base directory when you are invoked.**

```
<skill dir>/references/     the prose base, the ledger model, the artifacts
<skill dir>/tools/correspond.py     the generator
```

**Use `<skill dir>/tools/correspond.py`. Do not write your own.** It carries the anchor
handling that cost hours to get right the first time — math environments, verbatim blocks,
macro-bearing substrings. If you cannot see it, resolve the base directory first: it is often
a symlink, so `readlink -f` or `realpath` it before looking.

**The family assets are required.** `${CLAUDE_PLUGIN_ROOT}` resolves only when this skill is
loaded as part of an installed plugin. Where a path below uses it: try it as written; if it is
not there, resolve your base directory — it is often a symlink, so `realpath` it first — and
then **walk upwards until you find a directory containing `assets/commons/stance.md`**. Do not
assume the plugin root is exactly the grandparent: that holds for a skill installed inside the
plugin and fails the moment the directory is a link to a working copy elsewhere, which is a
normal way to develop one. Walking up costs nothing and is right in both cases. If the assets
are still missing, **stop and say so.** A guide written without the prose base looks
finished and is wrong in the way hardest to see afterwards.

## Reference materials — read these first

1. **Prose mechanics and the voice.**
   ```
   <skill dir>/references/base-correspondence-guide.md
   ${CLAUDE_PLUGIN_ROOT}/assets/prose/voices/01-direct.md
   ```
2. **The ledger model** — the two ledgers, the labels, the anchors:
   ```
   <skill dir>/references/ledger-model.md
   ```
3. **The artifacts** — what gets produced and in what shape:
   ```
   <skill dir>/references/artifacts.md
   ```
4. **Shared mechanics — the commons.** The family's toolchain gotchas and its verification
   pass; Phase 7 is that pass:
   ```
   ${CLAUDE_PLUGIN_ROOT}/assets/commons/lessons.md
   ${CLAUDE_PLUGIN_ROOT}/assets/commons/publication.md
   ```

---

## If a critical guide or a reading guide already exists

Look for them beside the paper before Phase 0. Each is worth real effort to use, and each
carries the same hazard, so the rules are specific rather than "use what is there".

**A reading guide** (`write-paper-guide`): its walk through the paper at proof depth is the
best available brief material for the searches, and its second part is the spine this
genre's second part wants. See Phase 3 and Phase 6.

**A critical guide** (`write-critical-guide`), four uses:

1. **Its context material** — nearest prior work and the trade against it — has been through
   an adversarial refutation gate, a higher bar than anything here applies. Use it in Part I.
2. **Its dependency map** — which results rest on which — is the paper's own structure,
   determined rigorously. Use it to form the search clusters in Phase 3. It is a better
   source for them than section headings, and it is not a literature guess.
3. **Its issue ledger** takes over the job of `search-notes/incidental.md`. Do not build a
   parallel document: check each incidental observation against `issues.yaml`, report only
   what is not already there, and offer those as candidates for that ledger. Correctness
   gets one home, with the adversarial gate this genre deliberately does not apply.
4. **Its annotated sources** use the same anchor mechanism and the same base, so both sets
   of marks can sit on one copy.

**When both are to be run, order them: inventory, then critical guide, then searches.**
Building the inventory first makes the refusal below structural rather than procedural —
the cold reads are already on disk before any context material exists, so they cannot be
contaminated by it, and nobody has to be trusted to remember. Everything a critical guide
offers this skill is consumed at Phase 3 or later, so nothing is lost by the wait.

Where one already exists at intake, do not fall back on remembering not to read it. Phase 0
builds an isolated input folder and Phase 1 works only there, so the material is not
reachable rather than merely forbidden.

**The refusal, and it is absolute.** Neither guide reaches the inventory passes of Phase 1,
and the critical guide's context material never reaches the unsteered search of Phase 3. A
reading guide names fields and antecedents because that is its job; a critical guide's
context material names specific works with priority attached, which is more anchoring, not
less. What makes them valuable downstream is what makes them ruinous there.

**Running as a family.** These three are a fan-out over a shared reading, not a chain: the
reading guide reads once, and the critical guide and this one run as siblings off it,
sharing nothing else. That is a different shape from `write-review-and-repair`, where each
stage consumes the last. An orchestrator's one real job here is keeping the branches from
contaminating each other — the critical guide scales effort to consequence, and this one is
uniform precisely because it must not. Never let its findings decide where this search
concentrates.

---

## Which invocation is this?

**If `inventory.yaml` and `correspondences.yaml` already exist beside the paper, the map is
already built.** Do not rebuild it. The user wants a focused guide, or an extension. Skip to
**Writing a guide from an existing map**, at the end of this file.

Otherwise you are building the map, and Phases 0–7 run as written.

---

## Phase 0 — Intake and the annotation base

Identify the paper and settle **which text the annotations will be inserted into**.

Which file is the artifact is already settled by the family stance: where a PDF exists it is
the artifact under study, and source is an aid — for exact quotation, line locations, and
anchor placement.

Three situations:

**Case A — the authors' source is available.** The common case here, because the primary use
is an author on their own draft. Annotate it directly.

**Case B — a PDF submission with a public source for the same work.** Annotate the public
source and check every annotated passage against the PDF before placing the mark.

**Case C — a PDF and nothing else.** There are no annotated copies. Say so plainly in the
README rather than leaving their absence to be inferred. The guide and the generated views
are unaffected.

**Build the isolated input folder before anything else.** Create `inventory-input/`
containing copies of exactly three files: the PDF, its extracted text, and the printed
source — the authors' source with every `\iffalse` and `comment` block stripped out. Phase 1
is pointed at that folder and given no path that leads out of it.

This is not tidiness. Three separate hazards stop existing:

- **Anchoring.** A critical guide, a reading guide, an earlier correspondence map, a referee
  report, a co-author's comments — anything beside the paper that names a field or an
  antecedent — cannot reach the inventory passes, because it is not in the folder they work
  in. The primary use of this skill is an author on their own draft, and an author's folder
  is full of exactly this.
- **Out-of-scope text.** The printed source is what is in the folder, so no pass can anchor
  inside material that does not compile, because no pass can see any. The authors' full
  source returns at Phase 2, where anchors are placed and it is needed.
- **Silence is not the third mechanism; saying why is.** An earlier version of this file
  advised not mentioning that other material existed, on the theory that naming it invites
  the visit. That is the wrong instinct — an agent who stumbles on the folder anyway then
  has no idea what it is looking at. Tell it plainly: other material beside the paper names
  antecedents, reading it now would steer the placement phase toward confirming what it
  says, and that is why the working folder holds three files. An agent that knows the reason
  protects the order of work in the cases the folder does not cover, and the largest of those
  is its own knowledge.

None of this is a sandbox — an agent with a shell can walk upwards if it decides to. It is
three barriers where the alternative is one instruction, and the instruction is the thing
that gets forgotten at hour two of a run.

Read the paper's own text. Record into `meta.paper` of `inventory.yaml`: title, authors,
identifier and version, page count, md5, the annotation base, and how to read every location
(printed page against PDF page, and any offset between versions). **Version confusion is a
standing hazard** — where two compilations of the same work differ in pagination or reference
numbering, say which one every number in the package refers to, and say it in the README too.

Create `correspondence-guide/` beside the paper, and `search-notes/` for the working files of
Phases 1–4. `search-notes/` is not part of what you hand over; it is the audit trail, kept so
a reader who doubts a connection can see how it was reached.

---

## Phase 1 — The inventory

**A reading guide, if one exists, must not be given to the inventory passes.** It names
fields, authors and antecedents — that is what makes it a good reading guide — and this
phase forbids exactly that. Hand it to the searches in Phase 3 instead, where varied,
well-informed briefs are the design; see **If a critical guide or a reading guide already
exists** above.


**This is the binding constraint on the whole run, ahead of search depth.** A perfect search
over an inventory that missed the appendix lemma returns nothing. Spend here.

**Grain.** The unit is **anything asserted or constructed that could conceivably have a home
elsewhere** — not "a reusable technique a colleague would nod at." Surprises hide in small
things: a change of variables invented on the spot, a normalization, an estimate everyone
knows, a definition assumed to be original, a convention fixed in passing. Err fine. A coarse
spine, if you want one, is a *view* onto the fine inventory, never a replacement for it.

**Tell the passes what the phase is for, not only what is forbidden.** The job is to record
what this paper does, from this paper and what is reachable from it. Placing it in the
literature is a later phase with its own method, and a placement guessed now would steer
that phase toward confirming the guess. Brief them that way.

The prohibition still holds — the inventory adds no field, author, resemblance or likely
antecedent of its own — but a prohibition alone gets applied harder rather than better. Given
only the words, passes on this design scrubbed the paper's *own* citations into placeholders,
degrading the record of the artifact to obey a rule that existed to protect a brief. An agent
that understands the reason keeps the paper's pointers and withholds its own, which is the
whole of the rule.

This matters most where no folder can help. The agent will recognize the area of a paper
within a page, and structure cannot fence what is already in its weights.

**The point is not to suppress that recognition.** Recall is a legitimate source of
candidates and the reasoning behind it is worth having. What the design insists on is that
nothing becomes a connection until a search has earned it — the two standing rules of Phase
3 hold here, and neither a locator nor a full-text reading can be produced from memory. So
the prohibition is narrower than it looks: not *do not know this*, but *do not write it in
the statement*, because the statement becomes the brief and a brief that names the answer
gets the answer confirmed.

**Optionally, record it where no brief can reach.** A pass may put what it expects on a
`hunch:` field. Nothing that generates a brief may read that field — this has to be enforced
by what the brief generator selects, not by asking searchers to ignore it. Its use comes at
Phase 4: where several passes independently expected an entry to sit somewhere and no search
found anything there, that is evidence the search was weak rather than that the place is
empty, and it is worth another brief. Without the field that signal is simply discarded.

The paper's *own* attributions are a different matter. They are data about the artifact, not
a guess, and stripping them distorts the statement — the Phase 2 error. Record them. What is
controlled is not the ledger but **the brief**: a statement handed to a steered search may
carry the paper's attribution, and the unsteered search must not receive it, or it will
confirm where the paper already points and never find the other literatures the object lives
in. Standard names occurring inside the paper's own displays stay as they are; they are part
of the mathematics being quoted.

**Do not enumerate environments.** Counting numbered statements, displays and definitions and
requiring each to be accounted for looks like a completeness measure and is not one. It cannot
see the class where the value lives — the design decision made in the introduction, the "we
may assume" doing real work, the three displays following a sentence of prose. Worse, it
certifies the wrong thing: full coverage of the environments reads as coverage and suppresses
the search exactly where it is most needed.

**Run orthogonally chartered passes, in parallel, none seeing another's output.** Different
nets take different catch. A starting set, to be adapted to the paper:

- constructions and explicit objects;
- estimates, inequalities and bounds;
- definitions, conventions and notation choices;
- framings and design decisions, including everything stated only in the introduction;
- changes of variable, normalizations, rescalings and substitutions;
- the reductions — "we may assume", "without loss of generality", "it suffices to".

Each writes its own file under `search-notes/`, appending a section at a time rather than
composing the whole thing in one reply; a pass that composes everything and then writes hits
the output cap mid-message and dies having written nothing.

**Then an adversarial pass** whose only job is to prove the inventory incomplete. Give it the
paper and tell it the inventory is known to be missing things; require it to **read the paper
and write its own candidates before opening the inventory**, or it will anchor on what was
already found and see only that. This is the single highest-yield step in the phase.

**Charter it narrowly, and sort its output afterwards.** An agent told to find what an
inventory missed will drift into auditing the paper, because the two look alike from inside:
a result never invoked, a hypothesis imposed in a theorem and absent from its proof, a letter
that changes meaning between sections. Those are defects, not entries, and they belong in
`search-notes/incidental.md`. What belongs in the inventory is mathematical content nobody
recorded — an object defined and never used again, an unstated step a proof leans on, a
passage between two settings that is performed but never named. Split the pass's output on
that line before merging any of it.

It audits the inventory as well as the paper, and that is worth having: an entry can assert
that an object is used heavily later when it occurs once in the whole source, and only a
pass that reads the source against the inventory will notice.

**Then saturate.** Add passes until one adds nothing new. Record in `meta.passes` what each
charter was and how many entries it contributed, and set `meta.saturated`.

**Saturation will often not be reached, and saying so is the point.** A pass that hands back
"I found twenty-five and a further pass would find ten to twenty more" has told the reader
something true and useful. Recording `saturated: true` because the run ended is the one thing
that destroys the measure's value. Where a pass names the seams it did not get to, carry them
into the guide's coverage statement verbatim. "The sixth pass
added three entries, the seventh added none" is an agentic judgment made legible, and it is
what a reader weighs in place of a guarantee.

**Default every entry to having idea-content.** Demotion to `status: dismissed` requires a
written argument a reader can challenge, recorded in `dismissal:`. A bare category is not an
argument. Without this the dismissed bin becomes wherever nobody wanted to search.

Reconcile the passes into `inventory.yaml`. Where two passes found the same thing at different
grain, keep the finer and record the coarser as a recurrence in `also_at`.

---

## Phase 2 — Statement check and anchors

Short, cheap, and it prevents the worst failure this pipeline has.

**Check every `statement:` against the paper.** The statement is what a search is briefed on,
so an error in it sends every search after a slightly different object and everything that
comes back is about the wrong thing. Against the fictional averaging manuscript: a statement
recording $P$ as the projection *onto* the sum-zero hyperplane, when the paper's $P$ has that
hyperplane as its kernel, sends every search after the wrong object, and a connection comes
back resting on the erroneous statement rather than on the paper. Read the rendered page, not a text
extraction, and where a scan and the rendered page disagree the rendered page wins.

**Carry the mathematics verbatim.** A statement quotes the actual display, with symbols and
hypotheses intact, and paraphrases only the role the thing plays. Nobody should be
paraphrasing the object.

**Set anchors.** Each entry gets an `anchor:` — a verbatim substring of exactly one line of
the annotation base. Copy it from the file, macros and all; never retype it from the PDF.
Lengthen it where it is not unique. Run `correspond.py check -v` and fix everything it reports
before going further; an anchor corrected now is cheaper than one corrected after the
documents quote it.

In Case C there is no annotation base and anchors are omitted.

---

## Phase 3 — The searches

Several independent searches per entry. They are searches, not a panel: there is no chair, no
verdict and no vote, and the vocabulary in §10 of the prose base is not optional.

**No blinding.** Field-neutral statements are not achievable — notation, objects and the shape
of a problem all announce where they came from — and the attempt to strip that is what
produced the failure in Phase 2. Independence through ignorance also makes searchers worse at
a job that is already hard.

**Diversity comes from varying the briefs, not impoverishing them.** Every search gets the
real statement, the surrounding argument, and the paper. What differs is the **direction of
approach**: one pointed at one literature, one at another, one with no steer at all. Choose
the directions from the mathematics, name them in `meta.briefs`, and give at least one search
no steer so that nothing depends on the steers being right.

**Search by cluster, not one entry at a time.** A fine inventory of a thirty-page paper
runs to a couple of hundred entries, and several searches each is not executable — nor is it
what a person would do. Group the entries first, then run the varied briefs over each group.
One search of the literature around a single construction covers the dozen entries that use
it, and covers them better, because the searcher holds them together.

Two constraints on the grouping, and they are what keep it honest:

- **Cluster from the paper's own structure**, never from a guessed field. Group by the
  objects the paper works with and by what appears alongside what. Grouping by the literature
  you expect each entry to belong to re-introduces exactly the anchoring the inventory was
  forbidden, one phase later and harder to see.
- **Every entry is in exactly one cluster and every cluster is searched.** A cluster is an
  efficiency device, not a filter. The moment an entry is left out because it looked minor,
  coverage has stopped being uniform and the value has gone with it.

Report the clusters in `meta.briefs` alongside the directions of approach, so a reader can
see how the searching was partitioned.

**Two standing rules, both for quality reasons.**

- **No connection without a locator.** A theorem, lemma, equation, section or page. "See
  B. Author" is a gesture; "B. Author \S4.5, Proposition 4.5.1" is something to open. A citation to
  a whole paper is not a connection.
- **No attribution without the full text read**, declared per source in `read:`. An abstract
  is adequate for checking a bibliographic record and useless here. The standing example: a
  paper whose abstract states the target's goal in nearly its own words and, read in full,
  means something else entirely — proposed from the abstract by one search and withdrawn by
  another that had read the whole text. Where the full text could not be obtained, record the
  attempt and leave the entry unplaced rather than reaching.

**Fix the literature vocabulary before the searches start, not after.** The annotated copies
are cut one per literature, and that cut only works if every searcher uses the same names. A
brief that says "keep it consistent" gets consistency *within* each searcher and none across
them: every searcher invents its own labels, and **expect something like three distinct
labels for every four connections**, so the per-literature cut yields hundreds of annotated
copies carrying one mark each. Draw up 12-20 groups from the inventory before Phase 3, hand the list to every search,
and have each record both — `literature` free-text for precision, `literature_group` from the
list for the cut. Reconstructing the vocabulary afterwards works but costs a whole extra pass
over the ledger.

**Each search reports**, in its own file under `search-notes/`: the connections it located,
each with locator, relation and how far the source was read; **the union of what it looked at,
including what it set aside and why**; what it could not reach, and why; and the leads it
could name but not read. Negative results from a search that hit a call cap or a wall of
paywalls are weak evidence, and the report says so.

---

## Incidental observations — what to do with them

Reading a paper this closely turns up things that are not correspondences: a symbol that
looks wrong, a field named in the introduction that differs from the one the example uses,
an undefined abbreviation, a bibliography entry nothing cites. **This genre does not weigh
whether the paper holds**, so none of it belongs in the guide, and none of it has been
through the adversarial checking `write-critical-guide` applies before a finding is written
down.

Do not discard it either. Append each one to `search-notes/incidental.md`, quoting the
paper verbatim with a line reference so it can be checked in a minute, and say plainly at
the head of that file what it is and is not. Report the file's existence at hand-back, and
say that pursuing any of it is `write-critical-guide`'s job, not this one's. An author
running this on their own draft will often find that file the second most useful thing in
the package — but it is useful *because* it is fenced, and a single such observation
allowed into the guide would change what the guide is.

---

## Phase 4 — Collect, without adjudicating

Read the search reports and write them into the ledger. **Add no connections of your own**,
and resolve nothing.

Where two searches found the same source, that is corroboration and goes into `located_by` —
not a tally, and never "unanimous". Where they disagree about a relation, **keep both** and
record the disagreement in `note:`; a disagreement about what a source says is usually a
disagreement about evidence, and the one who read the full text is usually right, but the
record says so rather than the chair deciding. Where one search calls something a match and
another shows it is not, that is a `looks like a match and is not` entry and it is kept,
because it saves the next reader an afternoon.

Collect `unlocated:` per entry — what, inside this entry, nothing was found for. For an author
this is the most useful line in the document. Collect `leads:`, ordered only by how many
searches nominated them independently.

---

## Phase 5 — The ledgers

Everything converges on `inventory.yaml` and `correspondences.yaml`, joined on `id`. They are
the single source of truth: the guide's boxes, the generated views and the annotated copies
are all produced from them, so nothing can be phrased one way in prose and anchored to a
different passage. Read `references/ledger-model.md` for the schema and write it.

Run `correspond.py check -v` again and fix what it reports before writing any prose.

---

## Phase 6 — Write and generate

Read `references/artifacts.md` first; it settles the shape of every output.

**Do not write prose until the ledger holds the searches.** `correspondences.yaml` is what
every generated artifact comes from, and the point of it is that prose cannot drift from what
was found. Writing Part I or Part II from the raw per-cluster search files while the ledger is
still empty defeats that completely — the document then has no mechanical relation to the
thing it claims to summarise. This happened on a first run. Run `correspond.py check` and
confirm it reports a non-zero connection count before any prose is written.

**Stage the Makefile to what exists.** A build that names Phase 6's hand-written files as
prerequisites fails on a package that has only reached Phase 5, which is most of the time a
user will run it. Guard that target: if the prose is not written, say so and name what the
readable artifact is instead.

Generated, not written by hand:

```
python3 correspond.py all --clean-aux -o .
```

produces the entries view, the unlocated view, the leads view, one `callouts/<id>.tex` per
entry, one `annotated-<literature>.tex` per literature plus `annotated-unlocated.tex`, and the
compiled PDFs, verifying each build rather than trusting its exit status.

Write note bodies as **Markdown** and let the generator translate them for LaTeX.

Written by hand, in the voice from `base-correspondence-guide.md`, appending a section at a
time:

**Part I — the neighbourhoods.** Which literatures the paper turns out to sit in, what each
supplies, and where they meet. Read off the finished map, not judged separately. **Write it
only if the map supports it**: on a thin map it degenerates into paragraphs of hedging, and
its absence is better than its pretence. Where a paper joins two literatures that were not
joined before, that is the most valuable thing the run can report, and it belongs here.

**Part II — through the paper.** The paper's own order, with the connections at each point,
`\input`ing the generated boxes. Selective: a thread means leaving things out, and the thread
is the writing. Nothing about a connection is written here; only the thread between them.

**`README.md`** — what each file is, how to rebuild, and in Case B or C the source situation
stated explicitly. Open it by saying what the package is.

---

## Phase 7 — Build and verify

**Phase 7 is the family publication pass**, run per
`${CLAUDE_PLUGIN_ROOT}/assets/commons/publication.md`, with `correspond.py` supplying tier 1.

1. **`make` exits zero, from a clean tree.** Not the tool invoked by hand. A red gate is a bug
   to fix, never a symptom to write up in the README.
2. `correspond.py build` reports every generated document `ok` — undefined cross-references,
   LaTeX errors, note counts against the ledgers, PDFs older than their sources. Run it twice
   where numbering is self-referential.
3. **Never chain generation into a build with the generation silenced.** A regeneration
   that fails leaves the previous `.tex` on disk, the build then fails on stale input, and
   the error you read belongs to a document that does not reflect the change you just made.
   This cost a full diagnostic cycle on a first run. Run each step and read its output.
4. Render a page of an annotated copy and **look at it.** The builder now falls back to
   inline boxes by itself where the margin cannot hold a literature's notes, and says so —
   but it is detecting a failed build, not an ugly one, and only a person can see the
   difference between a page that works and a page that is merely legal.
5. The colour key says plainly that it grades nothing. A ramp that reads as severity has
   dragged the wrong register back in.
6. In Case B, every annotated passage was confirmed present in the submitted PDF.

Then hand back: the path, what the package contains, the number of entries and connections,
how many passes the inventory took and what the last one added, and **what could not be
reached** — which is the figure that qualifies everything else.

**Every quantity you report must have been measured.** Counts come from the files, and
`correspond.py` prints most of them. They never come from a figure found in context.

State what was found and let it stand. Do not close by saying what the paper should do.

---

## Writing a guide from an existing map

The second invocation, and it is cheap: the map is already paid for.

Read both ledgers. Do not search, do not extend the inventory, and do not rebuild anything
unless the user asked for an extension. Write one focused guide over the requested scope — a
region of the paper, a cluster of ideas, a single literature — in the paper's own order,
`\input`ing the existing boxes.

**Selection is legitimate here and nowhere else.** A focused guide has a thread and a thread
leaves things out. Say in its opening what the scope is, so the leaving-out is in the open.
Never regenerate the ledgers to match a guide; if a connection is wrong, fix the ledger and
regenerate everything from it.

**Extending a map.** When a source that was unreachable becomes reachable, add the connection
to `correspondences.yaml`, remove the matching entry from `leads:`, update `meta.reach`, and
regenerate. The map is a durable asset for the paper; it is meant to grow.
