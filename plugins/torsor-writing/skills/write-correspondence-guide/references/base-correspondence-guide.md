# Base mechanics — correspondence guide

The format rules for a `write-correspondence-guide` document. Stable and
**voice-independent**: they hold whichever `voices/*.md` is paired with them. Pair this file
with exactly one voice for the full style guide.

Read `${CLAUDE_PLUGIN_ROOT}/assets/commons/stance.md` first. Everything below assumes it.

---

## What a correspondence guide actually is (get this right first)

**A view of the neighbourhood, not a bibliography.** For each thing the paper asserts or
constructs, what the corresponding object in the existing literature is, how close the
correspondence runs, and where it stops. It is not a corrected bibliography, a reconstructed
one, or a list of what is missing from one.

**It is useful, not authoritative.** There is no correct citation — always layers, always an
earlier precedent, always a related idea underneath. So the document does not aim at a target
it could miss. A reader gets more connections than they will use and decides which matter,
because they have context the document does not.

**It never says what the paper drew on.** Provenance is not knowable from the artifact and
very nearly not knowable for a human author. Every claim is about what two written statements
show.

**It never says what the paper should cite.** Whether a bibliography is adequate belongs to
the paper's readers. The density of connections in a region tells an editor everything they
need without a sentence saying it.

**It never adjudicates.** Several sources for the same object is a result, not a problem.
Nothing is synthesised down to a best citation and nothing is put to a vote.

**It is calibrated to the paper, not to a reader.** This is a **named exception** to
`base-paper-guide.md`, which makes the reader profile the tie-breaker. There is no reader
profile here. Uniform coverage in the paper's order is the same document for the curious
reader, the close reader, and the author checking a draft; they read different amounts of it.

## Mathematical content

**State both objects, not one.** A connection that gives the source's statement and gestures
at the paper's is half a connection. The reader must be able to hold the two side by side.

**Give the dictionary.** Which thing corresponds to which — the substitution, the
variable-by-variable map, the hypothesis-by-hypothesis comparison. This is the content, and
everything else in a connection is scaffolding around it.

**Say where the correspondence stops.** Anything short of a literal match leaves a residue,
and the residue is the point: it is either where the paper has something of its own, or where
there is machinery in the neighbouring literature it has not taken. Both are wanted.

**Describe the relationship; do not assert an equation between objects.** State the comparison
so a reader can judge its strength rather than telling them the strength. Claims of sameness
are made only where something is literally, checkably true.

**Cite by the paper's own numbering**, and by the source's own numbering. Both ends of a
connection are locatable or it is not a connection.

**Mark how far each source was read.** Full text, part, abstract, or bibliographic record
only. An abstract can state a paper's goal in nearly the words of the work it does not
resemble.

**Say what could not be reached.** A search that exhausted a call budget or hit paywalls owes
the reader that fact, and "nothing located" then means *not located among the sources
reachable from one machine*.

## Structure

**Two parts.** Part I orients: which literatures the paper sits in, what each supplies, where
they meet. Part II navigates: the paper's own order, connections at each point. Part I is
written only if the map supports it.

**Part II is a thread with generated boxes set into it.** The thread is written; nothing about
a connection is. A box is `\input` at the point in the exposition where its subject appears.

**Callouts.** An `antecedentbox` carries one connection. A `pitfallbox` is for something that
would mislead — a near miss that looks like a match, or an error found in a statement the
searches worked from. Not for ordinary commentary.

## Words (house rules)

Everything in `${CLAUDE_PLUGIN_ROOT}/assets/prose/base-paper-guide.md` under **Words and
numbers** carries over unchanged, including the ban on *clean* and *load-bearing* as tells,
and numbers spelled out below 10. Plus:

**Banned — the tribunal.** *panel, reviewer, verdict, chair, unanimity, dissent, adjudicate,
finding.* Several searches agreeing is corroboration, not a vote; write "located independently
by three searches", never "3/3" or "unanimous".

**Banned — provenance.** *derives from, taken from, borrowed, lifted, owes, influenced by,
inspired by, adapted from.* These creep in as ordinary English and each one is a claim the
document cannot make.

**Banned — the citation verdict.** *should cite, fails to cite, uncredited, omits, neglects to
mention.*

**Banned — the review pipeline.** *referee, reviewer, submission, before publication, prior
to submission, the editor.* This guide is not for preparing a paper for refereeing. It is as
likely to be run on something published years ago by someone who wants to know how it sits in
the literature, and the vocabulary of judgement imports a register the genre does not have.
Where a source's own text uses those words, quote it; do not adopt them.

**Write what is the case, not what someone should do about it.** A consequence stated as an
instruction — "flag at line 160", "cite X at Lemma 2.3", "drop the hypothesis" — presumes a
reader who can still edit the paper. Half the time there isn't one. State the fact and let
the action follow from it, as here against the fictional averaging manuscript in
`tests/fixtures/review/`: *"The restriction to $\mathbb{Q}$ in \S1 is not needed: B. Author
gives the same rank computation over any field in which $n$ is invertible."* That serves the author who can act and the
reader who cannot, and it is the same sentence.

This is not a softening. "The identification is wrong as written" stays exactly that strong;
it is a statement about the mathematics, not about the people.

**Banned — priority.** *novel, first, original, new* applied to the paper's own content.
Nothing here supports them. "No source was located for X" is the available sentence and it is
about the search.

**Preferred**, since a prohibition alone strands the writer:

> has the form of · matches, under the substitution · the same computation appears at ·
> differs only in · recovers, when specialized · plays the role that X plays in · appears, in
> a different notation, as · can be read as · runs parallel to · sits in the X literature ·
> the corresponding object is · where the correspondence stops

**On "standard".** Permitted, and useful — knowing a lemma is standard is exactly what lets a
reader stop worrying about it. But it must be anchored to a citation with a locator. Unanchored
it is "it is well known that", which is already banned.

## What a correspondence guide is not

- Not a literature survey — context serves *this* paper, not the field.
- Not a critical guide — it places the paper, it does not weigh whether it holds. Its
  evaluative sibling is `write-critical-guide`.
- Not a referee report, and nothing in it is written for someone to sign.
- Not a novelty claim. An entry with nothing located is a statement about a search.
