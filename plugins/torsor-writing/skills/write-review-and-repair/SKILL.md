---
name: write-review-and-repair
description: Run the two-stage examine-then-repair pipeline end to end on one mathematical paper — first write-critical-guide to examine it and produce a graded, located issue ledger, then write-paper-repairs to work out and mark up the repairs that examination found. A thin orchestrator: it sequences the two skills against their shared on-disk package and carries no examination or repair judgment of its own. Runs unattended. It produces a critical guide plus a marked-up corrected source for you to review; it reaches no verdict and applies no change silently.
argument-hint: [path to the paper, an arXiv id/URL, or the folder containing it]
---

**Family stance — read `${CLAUDE_PLUGIN_ROOT}/assets/commons/stance.md` before writing any
prose.** It binds every genre in this plugin and settles four things this file assumes rather
than states: that the document has no author and so no first person, that it does not address
its reader, that calibration is not content, and that a supplied PDF is the artifact under
study while its source is an aid.

You are running a two-stage pipeline over a single mathematical paper: **examine it, then
repair it.** Both stages are existing skills that already run unattended and already share a
handoff. Your job is only to run them in order and confirm the handoff between them — you add
no findings and no repairs of your own.

The user has said: $ARGUMENTS

The two stages:

1. **`write-critical-guide`** reads the paper and produces a `critical-guide/` package in the
   paper's folder — a graded, located issue ledger (`issues.yaml`), annotated sources, and a
   typeset guide. It surfaces and grades issues; it reaches no verdict.
2. **`write-paper-repairs`** consumes that package and writes the forced repairs into a copy of
   the paper's own source as tracked changes, shows the repairs it worked out but did not adopt
   in position, and reports what cannot be repaired. It repairs; it does not decide what the
   paper should claim.

The handoff between them is entirely on disk: stage 1 writes `critical-guide/issues.yaml`,
stage 2 reads it. That means you hold almost no state — once stage 1 returns, the only thing
you carry into stage 2 is **where the package landed**. Everything else you can discard, which
is what keeps this pipeline light.

## What you do not do

- **Do not examine or repair the paper yourself.** If you find yourself forming an opinion on a
  proof or drafting a correction, you have stepped out of this skill. The two sub-skills own all
  of that; you are the glue.
- **Do not treat "repairs written" as "repairs accepted."** Stage 2's output is a *marked-up*
  build — proposed changes shown in position, nothing applied silently. Running both back to
  back does not adopt anything into the paper; the person reading the result decides. Say so
  plainly when you report.

## Step 1 — Examine

Invoke **`write-critical-guide`** through the Skill tool. Pass a single argument string that
pre-answers everything it would otherwise stop to ask, so it runs unattended:

> The paper is at `<path/arXiv id the user gave>`. Produce the critical-guide package for it,
> take every default, and do not ask me anything — proceed to completion. Put the package in the
> paper's own folder.

Two disciplines, both mirrored from how `write-critical-guide` itself calls `write-paper-guide`:

- **Treat it as a black box.** Do not assume its directory layout or filenames — installed
  versions differ. When it returns, look at what is actually on disk and work from that.
- **Reuse, don't rebuild.** If a `critical-guide/` package already exists for this paper, and
  the user has not asked to regenerate it, use it and skip to Step 2.

## Step 2 — Confirm the handoff

Before running repairs, verify the package is real and complete enough to repair against:

- a `critical-guide/` directory exists, and
- it contains `issues.yaml` (the ledger stage 2 consumes).

If it is missing or partial, **stop and report** — do not run `write-paper-repairs` against an
absent or half-written ledger; that produces repairs aimed at issues that were never recorded.
Say what stage 1 produced and let the user decide.

## Step 3 — Repair

Invoke **`write-paper-repairs`** through the Skill tool, pointed at the package from Step 1:

> The critical-guide package is at `<paper folder>/critical-guide/`. Work out and mark up the
> repairs it calls for, take every default, and do not ask me anything — proceed to completion.

Let stage 2 do its own input checks — in particular its verification that the ledger's anchors
still resolve against the source. Running immediately after Step 1 means the source has not
moved, so those anchors are as fresh as they will ever be, but the check is stage 2's to run;
do not skip or pre-empt it.

## Step 4 — Report

Tell the user, briefly: where the critical-guide package is, where the marked-up repaired source
and the not-adopted-repairs / unrepairable report are, and the one framing that matters — this
is **working material to review**, not an accepted revision. The critique stands on its own, and
the marked changes are proposals to accept or reject one by one; nothing has been applied silently.

If either stage stopped short (Step 2 failed, or a sub-skill could not find its bundle), report
exactly how far the pipeline got and what is needed to finish, rather than papering over it.
