---
name: write-paper-repairs
description: Work out repairs for the problems a critical guide found in a mathematical paper, adversarially audit each repair, and write the ones that are forced into a copy of the paper's own LaTeX source using tracked-change markup. Produces a corrected source that compiles two ways — changes marked for review, or silently in place — plus the worked-out repairs it did not adopt, shown in position for the reader to choose from, and a report of what cannot be repaired at all. Requires an existing critical-guide package. It repairs; it does not decide what the paper should claim.
argument-hint: [path to the paper folder, or to its critical-guide/ package]
---

**Family stance — read `${CLAUDE_PLUGIN_ROOT}/assets/commons/stance.md` before writing any
prose.** It binds every genre in this plugin and settles four things this file assumes rather
than states: that the document has no author and so no first person, that it does not address
its reader, that calibration is not content, and that a supplied PDF is the artifact under
study while its source is an aid.

You are repairing problems that someone else's examination has already found. A critical guide
to this paper exists — a ledger of issues, each located, graded, and argued. **Your job is to
work out the mathematics that fixes them**, and to write into the paper only the fixes that the
paper itself forces.

The user has said: $ARGUMENTS

## What you produce

A working copy of the paper's source carrying tracked changes, compiling two ways: with the
changes marked up for review, and with them silently in place. Beside it, the repairs you
worked out but did not adopt — shown *in position* in the marked-up build, so a reader can
browse and choose — and a report of what no repair reaches.

**Do not skip the mathematics.** "One would need to show that the adjunction extends" is not a
repair. Write the argument.

**Do not decide what the paper claims.** Repairing a paper and rewriting it are different acts,
and the boundary between them is the subject of most of this skill.

---

## Locating the shared assets — do this before reading them

The paths below are written `${CLAUDE_PLUGIN_ROOT}/…`. That resolves only when this skill is
loaded as part of an **installed plugin**; under a plain symlink into `~/.claude/skills/` it is
undefined, and the assets look as though they do not exist. So:

1. **Try the path as written.**
2. **If it is not there, derive the root.** You are told this skill's base directory when you
   are invoked. Resolve it first — it is often a symlink, so `readlink -f` or `realpath` it —
   and take its **grandparent** as the plugin root.
3. **If the assets are still not found, stop and say so.** They are required, not optional.

---

## Reference materials — read these first

1. **The markup contract** — the three states, the build commands, and the rules that came out
   of real use:
   ```
   <skill dir>/references/markup.md
   <skill dir>/assets/agentic-edits.tex
   ```

2. **The issue model** — what the ledger's tags, grades, dependencies and confidence bases
   mean. You are consuming a ledger written under this schema:
   ```
   ${CLAUDE_PLUGIN_ROOT}/skills/write-critical-guide/references/issue-model.md
   ```

3. **Shared mechanics** — the toolchain gotchas and the verification pass:
   ```
   ${CLAUDE_PLUGIN_ROOT}/assets/commons/lessons.md
   ${CLAUDE_PLUGIN_ROOT}/assets/commons/publication.md
   ```
   Two from `lessons.md` bite in this genre specifically: a long document composed in one reply
   is lost entirely, and an append to a file that is not there is silent — check both.

The generator that maintains the ledger lives at
`${CLAUDE_PLUGIN_ROOT}/skills/write-critical-guide/tools/annotate_tex.py`.

---

## Phase 0 — Preconditions, and refusing when they fail

**This skill consumes a critical-guide package. It does not produce one.** If there is none,
say so and stop: `write-critical-guide` comes first.

Four checks, in order:

1. A `critical-guide/` directory exists with `issues.yaml`.
2. The annotation base named in `paper.source` resolves.
3. **Every anchor still matches the source** — run `annotate_tex.py check`. This is the check
   that matters. If anchors have stopped resolving, the source has moved on since the guide was
   written: the authors posted a new version, or the file was edited. **Stop.** Repairing
   against a stale ledger produces changes aimed at passages that no longer exist, which is
   worse than not repairing.
4. The issues you intend to repair carry enough to work from — a `note`, ideally a `request`.

Then copy the source: `cp <paper>.tex <paper>-repaired.tex`, and copy `agentic-edits.tex` in
beside it. **The original is never modified.** Work only on the copy.

---

## Phase 1 — Triage, before any mathematics

Classify every issue you might repair. This costs little and it determines the shape of
everything after, so do it first and look at the result before committing to a workload.

**Absence or positive error?** An issue saying a proof is missing, a definition is never given,
a claim is asserted and never established, is an **absence**. An issue saying a sign is wrong, a
base ring is not commutative, a statement is false as printed, is a **positive error**.

Absences are almost never repairable by you. Supplying the missing proof of someone's main
theorem is doing the authors' work, and it is not recoverable from the paper. Expect absences
to route to proposals or to the critical report, and **do not plan a repair workload around
them**. In one examined paper, 31 of 55 major mathematical issues were absences.

**Consolidate absences rather than enumerating them.** Thirty-one separate notes saying "no
proof given" serve a reader far worse than one statement — "§4.5 onward is announced rather
than written, specifically: …". Look for whether the guide's own ledger already contains such a
census.

**Group interacting issues.** Two repairs interact if they touch the same object, or if one's
proof cites the other's statement. The ledger's `depends_on` field names some of these; it will
not name all of them, and the ones it misses are the dangerous kind. Groups matter because
dispositions are assigned to groups, not to items (Phase 4).

**Prefer dependency roots.** Repairing a root can retire its dependants for free — and an
apparent branch may dissolve entirely once the mathematics is done. That has happened: an issue
recorded as admitting two routes turned out to admit one, because the second was not a route at
all.

---

## Phase 2 — Choose what to repair

**Do not attempt everything.** Work out repairs for a set you can audit properly, weighted to
dependency roots and to positive errors. Everything else stays in the guide as it already
stands.

Say what you scoped and why, in the log and in the hand-back. A silently truncated workload
reads as a completed one.

---

## Phase 3 — Work out the repairs

For each issue: what the paper claims, what its argument establishes, what is missing between
them, and **the mathematics that closes the gap, written out in full**. Where you cannot close
it, say so precisely — that is a result, and it is what Phase 5's critical report is made of.

Write incrementally, appending as you go. Never compose a long analysis in one reply.

---

## Phase 4 — Audit every repair before it lands

Each repair goes to an independent skeptic asking **four** questions, not one:

1. Does it actually fix the stated problem?
2. Does it break anything else in the paper?
3. Is it minimal, or does it change more than it needs to?
4. Does it change what the paper claims?

Scale the number of skeptics to what being wrong would cost — one for a local repair, three for
anything touching a hypothesis or a statement. This is not where the savings are. In one trial,
seventeen skeptics were dispatched against six repairs and **four of the six left the audit in a
different state than they entered**; the audit also found two errors in the ledger it was
checking against.

A repair that fails audit is recorded with its refutation, never silently dropped.

---

## Phase 5 — Disposition: apply, propose, or escalate

Not a question of how big the change is. Every repair changes what the paper says — fixing a
misprinted subscript changes what a display asserts. The question is whether the repair is
**forced**.

**Apply** when the correction is *recoverable from the paper itself*: there is exactly one way
to make the text consistent with what is demonstrably already there — the paper's own diagram,
its own proof, how a later section uses the result, the actual content of a work it cites. You
are not deciding; you are reading off what the paper already commits to.

**Propose** when the repair requires a **decision the paper does not determine**. Several
defensible corrections exist and choosing needs information the paper does not supply. Choosing
for the authors would put words in their mouths.

**Escalate to the critical report** when no repair is available, or when the choice sits
upstream of most of the remaining repairs — if resolving it one way or the other changes what a
large part of the paper says, the repair is not determined and a source silently embodying one
resolution misleads.

The test: **could you reconstruct this correction from the paper alone, or did you have to
decide something?**

### Apply few, and by default

Even among forced repairs, **apply two or three at most** unless the user has asked for more.
Two reasons, and the second is the load-bearing one.

Writing into someone's paper is a strong act and the reader should choose. And **interactions
scale quadratically**: three applied repairs give three pairs to check for coherence; twenty
give a hundred and ninety. The coherence check below is only tractable at small numbers.

Everything else is **proposed** — rendered in position with `\agenticproposal` /
`agenticproposed`, so the marked-up build is a menu the reader browses and answers by tag.

### Dispositions belong to groups, not items

Two repairs can each be classified correctly alone and be incoherent together. Observed: a
clause applied to a condition invalidated a step in a corollary's proof; the cure was a second
repair which the per-item rule sent to *propose*. Both applied was coherent. Both proposed was
coherent. **Applied-plus-proposed was the one combination that left a defect — and it is what
per-item classification produces.**

So decide the disposition for each interacting group. If the per-item rule would split a group
incoherently, say so rather than following it: move the whole group to propose, or apply the
whole group and flag it. Where a split is unavoidable, state in the source, in the proposals
document, and in the log exactly what gap it leaves and which proposal closes it.

### When a repair admits several routes

Report the routes; do not develop a tree. Inside a route, a second choice *whose options depend
on which route you are in* does not get to branch. Resolve it in this order:

1. **Correctness first.** Establish which options are actually right; if only one survives, take
   it whatever route you are in.
2. **Consistency is only a tiebreaker**, between options already known to be sound.

The order matters more than it looks: "consistent with the route you are in" reads like a
reason, and an agent following it in good faith will reach a wrong answer while believing it
complied. This has happened. Consistency is never evidence.

---

## Phase 6 — Write the repairs into the copy

Per `references/markup.md`. Applied repairs get the addition/removal markup; proposals get the
proposal markup **with their full replacement text in position**, so the reader never has to
open another file to learn what a proposal says. Every change carries its issue tag and an
`\agenticnote` giving the reason.

---

## Phase 7 — Build both, and verify

```
pdflatex -jobname <paper>-repaired-notes  <paper>-repaired.tex
pdflatex -jobname <paper>-repaired-clean  "\def\agenticclean{}\input{<paper>-repaired}"
```

Two passes each, `bibtex` between if the paper has a bibliography. Then check:

- **The clean build contains every applied repair and no trace of any proposal.**
- **Numbered statements carry the same numbers in both builds, and the same as the original.**
  Compare `\newlabel` entries in the `.aux` files — **not** scraped `pdftotext`. A repair that
  changes a sentence's length reflows the paragraph, so which statements begin a line differs
  between builds even when every number is identical. That produces false divergences.
- No unresolved references, and no new overfull boxes beyond the original's.

Run the family publication pass (`commons/publication.md`) over both.

---

## Phase 8 — Feed corrections back to the ledger

**Finding errors in the guide is an expected output, not a surprise.** Writing the mathematics
out is a stronger check on a finding than the finding's own verification was, because it forces
contact the original sweep never had. One trial found two — a citation tag that named the wrong
result, and a claim about which hypothesis sufficed.

Write corrections to `critical-guide/issues-revised.yaml` — **never overwrite `issues.yaml`**,
since the diff between them is the audit trail — and report the differences. Regenerate the
guide's own artifacts from the revised ledger only if the user asks.

---

## Hand back

State what was applied, what is proposed and where to see it, and how to ask for more. Name the
tags: without them the user cannot reply precisely.

> Two of the eleven major mathematical issues had repairs forced by the paper's own text, so I
> applied those: **[M-11]** and **[M-24]**. The clean build reads correctly with them in place.
>
> The other nine have worked-out repairs I have **not** applied, because each needs a decision
> the paper does not determine. They are shown in position in `<paper>-repaired-notes.pdf`,
> marked as proposals with their tags, with the reasoning in `04-proposed.md`.
>
> To adopt any, name the tags — "apply M-5 and M-31" — and I will write them in and re-check
> the combination for coherence.

**Every quantity you report must have been measured.** Counts come from the files. Durations
come from `date -Is` stamped into the log at each phase boundary, or from output mtimes — never
from a figure found in context, including one this package recorded for an earlier run. If you
did not measure something, say so rather than estimating it.

## Adopting a proposal later

Named tags are not a text edit. Move each named proposal to applied, then **re-run the
coherence check** of Phase 5 against everything already applied, and rebuild and re-verify per
Phase 7. A proposal adopted in isolation is exactly the split that Phase 5 exists to prevent.
