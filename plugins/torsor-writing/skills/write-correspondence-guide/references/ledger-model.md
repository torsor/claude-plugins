# The ledger model

Two ledgers, written by different phases, joined on `id`. Everything generated — the inline
callouts, the appendix, every focused guide — reads off them, so nothing is transcribed by
hand and the prose cannot drift from what was found.

The governing constraint is rule 2 of SKILL.md: **the record is the content and the label is
an index.** Every field below exists because dropping it would leave a label standing alone.

---

## `inventory.yaml`

Written by the inventory passes. It must exist, complete with its dismissals, before any
search runs.

```yaml
meta:
  paper:
    title:
    authors: ["A. Author", "B. Coauthor"]   # as printed on the paper
    identifier:          # arXiv id, DOI, or a hash where there is neither
    version:             # and its date, where more than one exists
    md5:
    pages:
  locations: >-           # how to read every location below: printed page vs PDF page,
                          # and any offset between versions
  passes:                 # the completeness evidence of SKILL.md, Phase 1
    - charter:            # what this pass was reading for
      added:              # new entries it contributed
    - charter: adversarial
      added:
  saturated: true|false   # did a pass add nothing? if false, say why it stopped

entries:
  - id:                   # stable; every generated artifact refers to it
    name: >-              # a short label written here, never lifted from the paper
    statement: >-         # what the thing is, precisely, in the paper's own notation.
                          # This is what a search is briefed on, so it carries the actual
                          # display rather than a paraphrase of it.
    location: >-          # the paper's own numbering, plus a page
    anchor: >-            # a verbatim substring of exactly one line of the annotation
                          # base, used to place the mark in an annotated copy. Distinct
                          # from `location`, and doing work `location` cannot: fine-grain
                          # entries often sit in prose, at no numbered environment.
                          # Copy it from the file, macros and all; never retype it from
                          # the PDF. Lengthen it where it is not unique.
    also_at: []           # further sites where the same thing is used
    kind:                 # which charter surfaced it: construction, estimate, definition,
                          # framing, change of variable, convention, design decision
    hunch: >-             # optional. Where a pass expected this to live. **No brief
                          # generator may read this field.** Its only use is the coverage
                          # check at collection: several passes expecting a place that no
                          # search reached is evidence about the search, not the place.
    status: open|dismissed
    dismissal: >-         # required when dismissed. An argument a reader can challenge,
                          # per SKILL.md, Phase 1. Never a bare category.
```

Two things about `statement`. It is the brief, so it determines what comes back — and
since there is no blinding (SKILL.md, Phase 3), it should be generous rather than stripped:
the display verbatim, the hypotheses, the role the thing plays. And it must be checked
against the paper before searches run, because the prototype's worst error was a wrong
statement sending every search after a slightly different object.

## `correspondences.yaml`

Written by the searches and their record.

```yaml
meta:
  reach:                  # a search that hit limits owes the reader that fact (SKILL.md, Phase 3)
    unreachable: []       # named sources that could not be obtained, and why
    caps: >-              # call budgets exhausted, databases blocked
  briefs: []              # the directions of approach used, per SKILL.md, Phase 3

entries:
  - id:                   # matches inventory.yaml
    state: >-             # placed | partly placed | nothing located
                          # An epistemic state about this search, never about the
                          # mathematics. "Nothing located" is low-stakes.
    searched: >-          # the union of what was looked at, including what was looked at
                          # and set aside. Stops the next run re-treading the same ground.
    connections: []       # see below. Zero or many; there is no blessed one.
    unlocated: >-         # what, inside this entry, nothing was found for. Often the most
                          # useful line for an author.
    leads: []             # named, unread, ranked by how many searches nominated them
                          # independently. These are what a later extension picks up.
```

### A connection

Repeated under `connections:`. Self-contained, because a focused guide may lift one out.

```yaml
- work: >-                # author, title, venue, year
  locator: >-             # theorem, lemma, equation, section, page. Never a whole paper.
  read: full|partial|abstract|record
  literature_group:       # REQUIRED. One value from a controlled vocabulary fixed BEFORE
                          # the searches run and handed to every one of them. This is what
                          # the annotated copies are cut by, so it only works if every
                          # search uses the same names. 12-20 groups for a paper of
                          # ordinary length, nothing under ~8 connections.
  literature: >-          # free text: the body of work it sits in, as precisely as the
                          # searcher can put it. More precise than the group and kept
                          # alongside it, never instead of it.
  obtained: >-            # where, when it was not straightforward
  their_object: >-        # the source's object, stated precisely, from the text read
  dictionary: >-          # which thing corresponds to which — the substitution, the
                          # variable-by-variable map, the hypothesis-by-hypothesis
                          # comparison. This is the content.
  differs: >-             # where the correspondence stops. The residue: either where the
                          # paper has something of its own, or machinery in this literature
                          # it has not taken. SKILL.md, rule 3.
  consequence: >-         # REQUIRED for anything a person will read. What this record
                          # changes about what the author would DO -- drop a hypothesis,
                          # relate to a result that duplicates theirs, narrow a claim the
                          # source does not support, look in a literature that indexes
                          # their object under another name.
                          # NOT "this is a good identification". A record may be correctly
                          # located, read in full and exactly the right source and still
                          # change nothing. If no consequence can be named, the record
                          # stays in the ledger and never reaches an artifact.
                          # Breadth belongs at consideration; strictness at admission.
  standing:               # REQUIRED. placement | textbook | internal.
                          # `placement` -- a reader of this paper learns something.
                          # `textbook`  -- corresponds to something standard. Recorded
                          #                for completeness, NOT a finding. Kept in the
                          #                reference view, never set beside a passage.
                          # `internal`  -- about the paper or a sibling entry rather than
                          #                the literature; correspondence is not a
                          #                well-posed question for it.
                          # The searches judge whether a correspondence is TRUE. This
                          # field carries the other judgement, whether it is NEWS, and
                          # only the second decides whether a note belongs at a passage.
                          # When genuinely torn, choose `placement`.
  label:                  # an index to the above, never a substitute
  located_by: []          # which searches found it independently. Corroboration, not a vote.
  anchor: >-              # optional. Where this connection attaches, when that is not
                          # where the entry's own anchor sits.
  orients: >-             # optional, one line: what knowing this buys a reader. The
                          # view-building phase needs something to select on that is not
                          # strength of correspondence.
  note: >-                # optional: where searches disagreed and why, a caveat, or why
                          # something that looks like a match is not.
```

**On the two literature fields.** They exist as a pair because a single free-text field is
unusable for the cut: independent searches, each internally consistent, invent their own
labels — expect something like three distinct labels for every four connections — and the
per-literature cut then yields one annotated copy per mark. Precision and groupability are different jobs and
one field cannot do both. Fixing the vocabulary up front costs one pass over the inventory;
reconstructing it afterwards costs a pass over the whole ledger.

### Labels

Descriptions of what two written statements show, not claims about two objects in the
abstract (SKILL.md, rule 2).

The short form is what appears in an annotated copy, where the ledger label is too long
for a margin. Without it every mark looks alike and the copy reads as "all of this is
already known", which is exactly the misreading to avoid.

| Label | Short form | Means |
|---|---|---|
| `same statement` | same statement | The two displays say the same thing; print them side by side and see it. Rare, and requires that literal check. |
| `special case` | special case | The source's statement specializes to this one. |
| `differs in hypotheses` | variant | The same shape, under different assumptions — over $\mathbb{Q}$ where the source allows any field in which $n$ is invertible. |
| `same mechanism, different setting` | analogy | The argument runs the same way somewhere else. |
| `thematic` | thematic | A shared idea with no closer match found. Reported, not suppressed; often the connection a reader was least likely to know. |
| `contrast` | contrast | The comparison is informative because the two *differ* — every located source in a lineage does X and this one does not. Statement-numbered like any other. |
| `looks like a match and is not` | near miss | Worth recording so nobody else spends the afternoon. The standing example is a paper whose abstract states the target's goal in nearly its own words and, read in full, means something else. |

The last two are not correspondences and are kept anyway, because both are useful and
neither has anywhere else to live. The prototype had to smuggle both into prose.

---

## A worked entry

Written against the fictional averaging manuscript in `tests/fixtures/review/` — $P(x)$ the
mean of the coordinates times $(1,\dots,1)$ — with invented sources. No part of it comes from
a real paper or a real review.

```yaml
# inventory.yaml
- id: E4
  name: The averaging map built as a group average
  statement: >-
    For $x=(x_1,\dots,x_n)$ over $\mathbb{Q}$ the manuscript sets
    $P(x)=\frac{x_1+\cdots+x_n}{n}(1,\dots,1)$ and shows in Lemma 1 that its image is the
    span of $(1,\dots,1)$. The map is written down directly; it is not introduced as an
    average over a group action.
  location: "Lemma 1, p. 1"
  anchor: "The image of $P$ is the span of $(1,\\ldots,1)$."
  kind: construction
  status: open

# correspondences.yaml
- id: E4
  state: partly placed
  searched: >-
    Representation theory of finite groups; idempotents in group algebras; standard linear
    algebra treatments of projections.
  connections:
    - work: "B. Author, Projections and averages"
      locator: "\S3.2, Proposition 6"
      literature_group: representation theory of finite groups
      literature: "idempotents in the group algebra of a finite group"
      read: full
      standing: placement
      consequence: >-
        Lemma 1 is the $S_n$ case of the group-averaging idempotent of B. Author \S3.2, with
        the same two-line proof; what the manuscript adds beyond it is the description of the
        kernel as the sum-zero hyperplane.
      their_object: >-
        For a finite group $G$ acting linearly on a vector space $V$ over a field in which
        $|G|$ is invertible, $e=\frac{1}{|G|}\sum_{g\in G} g$ is idempotent, and $eV=V^G$.
      dictionary: >-
        $G \leftrightarrow S_n$ permuting coordinates; $V \leftrightarrow \mathbb{Q}^n$;
        $e \leftrightarrow P$; $V^G \leftrightarrow$ the constant vectors, which is the span
        of $(1,\dots,1)$. The manuscript's two-line proof is B. Author's, specialized.
      differs: >-
        B. Author states it for any field in which $|G|$ is invertible; the manuscript fixes
        $\mathbb{Q}$, so the restriction is not one the argument needs. Neither source
        describes the kernel, which is what the manuscript's \S2 is for.
      label: special case
      located_by: [unsteered, steered]
    - work: "C. Author, A first course in linear maps"
      locator: "Chapter 4, Theorem 11"
      literature_group: linear algebra
      literature: "rank and nullity of a projection"
      read: full
      standing: textbook
      consequence: ""
      their_object: >-
        A linear map $T$ with $T^2=T$ decomposes $V$ as $\operatorname{im} T \oplus \ker T$.
      dictionary: >-
        $T \leftrightarrow P$. Gives at once that the kernel has dimension $n-1$ once the
        image is known to be a line.
      differs: >-
        The standard statement of a fact the manuscript uses without naming it.
      label: same statement
      located_by: [steered]
  unlocated: >-
    No source was located that treats the averaging map together with an explicit kernel
    description in the form \S2 states it.
  leads:
    - work: "D. Author, Symmetric functions and averages"
      nominated_by: 2
      why: "named by both searches; not obtained"
```

Note the second record: correctly located, read in full, exactly the right source, and its
`consequence` is empty. It is standard background for a fact the manuscript uses in passing,
so it stays in the ledger and reaches no artifact. That is the common case.


---

## Open questions in the schema

- Whether `orients` survives as a field or collapses into `note`. It is the only field that
  makes a judgment, justified because the view-building phase has to select on something,
  and selection there is legitimate (SKILL.md, **Writing a guide from an existing map**). It
  is also the field most likely to
  drift into adjudication.
- Whether `state` is worth keeping at all, given that it is derivable from the connections
  and the prototype's version of it was a verdict.
- Whether recurrences (`also_at`) want their own entries when the same thing is used
  differently in two places.
