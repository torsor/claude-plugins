# write-workshop-state-guide Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a new torsor-writing skill, `write-workshop-state-guide`, that produces the docent's dated state-of-the-work guide (confidence-ledger spine, present-tense/commit-stamped register) as a sibling to `write-topic-guide`.

**Architecture:** Two new authored files — a register base (`assets/prose/base-state-guide.md`) and the skill (`skills/write-workshop-state-guide/SKILL.md`) — plus two small edits to shared files (`assets/prose/README.md`, `.claude-plugin/plugin.json`). The skill reuses the commons scaffold, the four-format build, `01-direct` voice, and the `pre-summarization.md` discipline verbatim; only the register and the spine (a harvested confidence ledger) are new.

**Tech Stack:** Markdown (skill + prose files); JSON (plugin manifest). No compiler — acceptance checks are grep-based structural/consistency checks against the committed spec.

## Global Constraints

- **Repo & branch:** `torsor-writing-plugin`; work on `feature/write-workshop-state-guide` (already created). Plugin content lives under `plugins/torsor-writing/`.
- **Spec is the source of truth:** `docs/superpowers/specs/2026-07-03-write-workshop-state-guide-design.md` (committed). Every task traces to a spec section.
- **Style composition seam:** effective style = `base-state-guide.md` + `voices/01-direct.md`. The new base file is **voice-independent** (holds for any voice) and must never reach into voice/register territory that `01-direct.md` owns.
- **Reuse verbatim, do not fork:** `assets/commons/{scaffold,lessons,publication}.md`, `assets/prose/voices/01-direct.md`, `skills/write-topic-guide/pre-summarization.md`. Reference them by `${CLAUDE_PLUGIN_ROOT}/...` paths; never copy their content into the new files.
- **Docent invariant (bake into all prose):** the guide *translates faithfully and never re-grades a claim*. Every confidence label (`[Formalized]`/`[Proved]`/`[Refuted]`/`[Verified]`/`[Conjectured]`/`[Heuristic]`/`[Open]`) and provenance tag (`[Standard]`/`[Folklore]`/`[Published]`/`[Preprint]`/`[Premise]`) is carried over verbatim.
- **Shared-file caution (another agent is editing this repo):** Task 3 touches `README.md` and `plugin.json`, which a concurrent guide-skill branch may also touch. Do Task 3 **last**, keep the edits **minimal and additive**, and `git fetch` + rebase/merge carefully before committing (see Task 3 collision protocol).
- **Numbers/house rules:** inherited from `base-paper-guide.md` conventions (spell out one–nine; numerals for 10+ and for theorem/section/equation/reference numbers).

---

### Task 1: `base-state-guide.md` — the register/framing base

**Files:**
- Create: `plugins/torsor-writing/assets/prose/base-state-guide.md`
- Reference (read, do not modify): `plugins/torsor-writing/assets/prose/base-paper-guide.md` (the sibling this parallels), spec §4.

**Interfaces:**
- Produces: a voice-independent base file that `SKILL.md` (Task 2) pairs with `voices/01-direct.md`; and that `README.md` (Task 3) lists in its composition map as `base-state-guide.md ← mechanics for a workshop state guide (write-workshop-state-guide)`.

**Content requirements** (author these sections; parallel `base-paper-guide.md`'s structure, swap the framing per spec §4):

1. **Header + composition note** — mirror `base-paper-guide.md` lines 1–6: "format rules for a `write-workshop-state-guide` state guide … stable and **voice-independent** … Pair this file with exactly one voice."
2. **"What a state guide actually is"** — a *snapshot of live work for a collaborator who must steer*, not a finished-paper appreciation. Include, as explicit rules:
   - **Attribute to the room and the moment, not timeless authors.** Present-tense, dated, commit-stamped: "As of `c29366e`, the room has verified X on the generic fibre; Y is staged for referee; Z is open."
   - **Translate, never re-grade** (the docent invariant): carry every confidence label + provenance tag verbatim; a confident-but-wrong carry-over hides debt and is worse than a flagged gap.
   - **Describe the reader, don't grade them** — reuse `base-paper-guide.md` lines 30–35 verbatim in spirit (familiar with / comfortable with; no "strong"/"expert").
3. **"Lead with the ledger"** — the confidence ledger is the guide's map, not an appendix. Name the four bands: **Solid** (`[Formalized]`/`[Proved]`/`[Verified]`, carry the confidence and, for `[Verified]`, the range) · **Provisional / just changed** · **Open / might still flip** (+ what's being checked that would move a label) · **Where to be skeptical** (staged-not-earned, load-bearing `[Preprint]`/`[Folklore]`, "if this framing is off, the approach is too").
4. **The five state questions** (verbatim from spec §4), explicitly *replacing* the six paper questions:
   1. What's being attempted — the *question*, not "the contribution."
   2. What's solid right now, at what confidence — the ledger, up front.
   3. What's provisional / just changed.
   4. What's open or might still flip — and what's being checked that would move a label.
   5. Where to be skeptical — what to distrust; what's staged-not-earned.
   State plainly: "why it's hard/plausible" is **optional**; "why it's new" and "why they pulled it off" are **cut**.
5. **"What changed / what might change" is mandatory** — a correction is a valued output, not a failure (anti-result-maxing). Dead ends and superseded branches are **first-class content**, not footnotes (cite culture §13 "Protect The Quiet Good Idea" / §15 "Maintain Branches").
6. **Words and numbers (house rules)** — start from `base-paper-guide.md` §"Words and numbers" and **extend the ban-list** with the result-maxing rhetoric: `contribution`, `why it's new`, `pulled it off`, `impressive`, `breakthrough`, `novel`, `finally`, `we now have`, and *any summary that reads as "done" while the work is live*. Add an explicit **no-premature-closure rule**. Keep the banned filler from the paper base (`we prove`, `utilize`, `leverage`, `seamless`, `robust`, `powerful`, filler `elegant`/`beautiful`, `simple`/`easy`/`straightforward`, `clean`). Ban `establishes`/`proves` **for provisional units** (those verbs are earned only by `[Proved]`/`[Formalized]`).
7. **Prefer-list** — present-tense, dated, room-attributed verbs: "as of `<commit>`, the room has", "is staged for referee", "is being checked", "was corrected", "still open", "flagged because".
8. **"What a state guide is not"** — not the room's record rewritten; not a paper; not a survey; **not a finished-result announcement**; not a referee report.
9. **The contrast block** (verbatim from spec §4) — the result-maxing "The room's contribution is to make both things concrete…" vs. the state-register "As of `c29366e`, the room has an explicit `$f$` for `$n=4,5,6$`, verified on the generic fibre…".
10. **"The family it belongs to"** — same preamble / math block / `tex2torsor` / toolchain / `torsor lab` credit as the manual family; unique to the state guide: the ledger spine, the present-tense/commit-stamped register, the mandatory what-changed section, and the reader profile.

- [ ] **Step 1: Write the acceptance check first**

Create `/private/tmp/claude-501/scratch-check-base.sh` (throwaway) — but simpler: the check is the grep in Step 3. Skip a separate test file; the acceptance check is defined in Step 3 and must fail now (file absent).

Run: `test -f plugins/torsor-writing/assets/prose/base-state-guide.md && echo EXISTS || echo ABSENT`
Expected: `ABSENT`

- [ ] **Step 2: Author the file**

Write `plugins/torsor-writing/assets/prose/base-state-guide.md` covering sections 1–10 above. Parallel the section rhythm of `base-paper-guide.md`; keep it voice-independent.

- [ ] **Step 3: Run the acceptance check**

Run:
```bash
cd plugins/torsor-writing
f=assets/prose/base-state-guide.md
for s in "voice-independent" "confidence ledger" "Solid" "Provisional" "Where to be skeptical" \
         "What's being attempted" "what might change" "no-premature-closure" "contribution" \
         "pulled it off" "c29366e" "Protect The Quiet Good Idea"; do
  grep -q "$s" "$f" && echo "ok: $s" || echo "MISSING: $s"
done
grep -q "base-paper-guide" "$f" && echo "WARN: still references base-paper-guide as the paired base"
```
Expected: every line prints `ok:`; no `MISSING:` and no `WARN:`.

- [ ] **Step 4: Commit**

```bash
cd ~/Library/CloudStorage/Dropbox/lab/software/torsor-writing/torsor-writing-plugin
git add plugins/torsor-writing/assets/prose/base-state-guide.md
git commit -m "Add base-state-guide.md: register mechanics for state guides

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 2: `SKILL.md` — the skill entry point (phases A/B/C)

**Files:**
- Create: `plugins/torsor-writing/skills/write-workshop-state-guide/SKILL.md`
- Reference (read, do not modify): `skills/write-topic-guide/SKILL.md` (the structural sibling), `skills/write-topic-guide/pre-summarization.md`, `assets/commons/scaffold.md`, spec §§1–6.

**Interfaces:**
- Consumes: `base-state-guide.md` from Task 1 (referenced as `${CLAUDE_PLUGIN_ROOT}/assets/prose/base-state-guide.md`).
- Produces: a user-invocable skill named `write-workshop-state-guide`; its front-matter `name` must match the directory name exactly.

**Content requirements** (parallel `write-topic-guide/SKILL.md`; apply the state-guide deltas from spec §§3–6):

1. **Front-matter** — `name: write-workshop-state-guide`; `description:` a trigger-rich one-liner ("report where live workshop work stands … confidence-ledger spine … dated snapshot in the docent's guide/ stream … Triggers: 'write up the state of the room', 'where does the workshop stand', 'state guide for <problem>'"); `argument-hint: [single room or whole workshop, and the reader]`.
2. **Opening** — what this is (docent's state-of-the-work guide), the two framing rules: (a) **present-tense, dated, room-attributed**, never timeless-authorial; (b) **translate faithfully, never re-grade** — the docent invariant.
3. **How it differs from `write-topic-guide`** — reproduce the differences table from spec §1 (corpus = the room's own record; spine = harvested confidence ledger; reader = collaborator steering).
4. **Reference materials — read first** — mirror `write-paper-guide` §"Reference materials": read `${CLAUDE_PLUGIN_ROOT}/assets/prose/base-state-guide.md` + `voices/01-direct.md`; the voice catalog README; `assets/reference/shelf-main.tex` for layout; `assets/commons/{scaffold,lessons,publication}.md`; and `skills/write-topic-guide/pre-summarization.md` for the distill-first discipline.
5. **Invocation modes** — ask up front: **single-room** (one problem-room) vs **whole-workshop** (fan out one subagent per active room; ledger spans rooms). Per spec §3.
6. **Phase A — Distill the record → `state-notes/`** — per spec §3 Phase A: one subagent per room reads `journal.md`, `status.md`+`STATUS.json`, latest `handoffs/`, relevant `rounds/`, and the room's slice of `canonical/result.md`; writes a label-faithful, commit-stamped digest to `state-notes/<room>.md` capturing the graveyard (dead ends, superseded branches, recent corrections). Review each digest for label-faithfulness. State explicitly that `state-notes/` is **distinct from** the docent's background `source-notes/`. Note the pre-summarization scanned-PDF machinery only applies to external background pulled for a steering decision.
7. **Phase B — Reader, ledger, synthesis** — per spec §3 Phase B: reuse the docent's per-collaborator reader profile → `latex/reader-profile.md`; reader model = collaborator steering, debt triage = "what they need for the next judgment call." The **confidence ledger** is harvested from the state-notes' existing labels and arranged into the four bands (never re-graded); state it and get user agreement. `state-notes/synthesis.md` carries the three mandatory tails: unified notation table, **what changed / what might change**, and the **decision-points / forks list**.
8. **Phase C — Author and build** — per spec §3 Phase C: commons scaffold verbatim, full four-format build every time. Ledger-driven structure: Part I state map (lead with ledger), Part II band-by-band, mandatory "What changed / what might change" chapter (dead ends first-class), appendix ledger table. Placement: a **new dated artifact** `guide/<YYYY-MM-DD>-<slug>-state/` listed in `guide/INDEX.md`, never an overwrite. Title page "State of the Work as of `<date>`/`<commit>`". Scale with subagents for whole-workshop; final whole-guide **label-faithfulness** review.
9. **Output structure** — reproduce the tree from spec §5.
10. **Common mistakes** — reproduce the table from spec §6.
11. **What stays the same as the manual family** — per spec §7.

- [ ] **Step 1: Verify absent (the failing check)**

Run: `test -f plugins/torsor-writing/skills/write-workshop-state-guide/SKILL.md && echo EXISTS || echo ABSENT`
Expected: `ABSENT`

- [ ] **Step 2: Author the file**

Create the directory and write `SKILL.md` covering sections 1–11 above.

- [ ] **Step 3: Run the acceptance check**

Run:
```bash
cd plugins/torsor-writing
f=skills/write-workshop-state-guide/SKILL.md
# front-matter name matches dir
grep -q "^name: write-workshop-state-guide" "$f" && echo "ok: name" || echo "MISSING: name"
# references the new base, not the paper base, as its paired style
grep -q 'assets/prose/base-state-guide.md' "$f" && echo "ok: base ref" || echo "MISSING: base ref"
# reuses commons + pre-summarization by reference (not copied)
for s in 'assets/commons/scaffold.md' 'voices/01-direct.md' 'pre-summarization.md' \
         'state-notes/' 'confidence ledger' 'what changed' 'single-room' 'whole-workshop' \
         'guide/<YYYY-MM-DD>-<slug>-state' 'never re-grade'; do
  grep -q "$s" "$f" && echo "ok: $s" || echo "MISSING: $s"
done
# must NOT copy commons content wholesale — sanity: file stays a skill, not a scaffold dump
wc -l "$f"
```
Expected: every check prints `ok:`; no `MISSING:`. Line count in a sane skill range (roughly 120–220 lines, comparable to the topic-guide skill's 186).

- [ ] **Step 4: Confirm cross-references resolve**

Run:
```bash
cd plugins/torsor-writing
for p in assets/prose/base-state-guide.md assets/prose/voices/01-direct.md \
         assets/prose/README.md assets/commons/scaffold.md assets/commons/lessons.md \
         assets/commons/publication.md assets/reference/shelf-main.tex \
         skills/write-topic-guide/pre-summarization.md; do
  test -f "$p" && echo "ok: $p" || echo "BROKEN REF: $p"
done
```
Expected: every referenced asset prints `ok:` (all exist; `base-state-guide.md` from Task 1).

- [ ] **Step 5: Commit**

```bash
cd ~/Library/CloudStorage/Dropbox/lab/software/torsor-writing/torsor-writing-plugin
git add plugins/torsor-writing/skills/write-workshop-state-guide/SKILL.md
git commit -m "Add write-workshop-state-guide skill

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 3: Register the skill in shared files (do LAST — collision-prone)

**Files:**
- Modify: `plugins/torsor-writing/assets/prose/README.md` (composition map, `## How it composes`)
- Modify: `plugins/torsor-writing/.claude-plugin/plugin.json` (description + version)

**Interfaces:**
- Consumes: the filenames established in Tasks 1–2 (`base-state-guide.md`, skill name `write-workshop-state-guide`).
- Produces: nothing downstream — this is the final registration step.

**Collision protocol (another agent may be editing these two files):**

- [ ] **Step 1: Sync before touching shared files**

```bash
cd ~/Library/CloudStorage/Dropbox/lab/software/torsor-writing/torsor-writing-plugin
git fetch origin
git log --oneline origin/main -5   # see if the other guide landed
```
If `origin/main` has advanced, `git rebase origin/main` this branch first and re-run Task 1/2 acceptance checks. Resolve any README/plugin.json conflicts by **keeping both entries** (their new base/skill and ours).

- [ ] **Step 2: Edit `README.md` composition map**

In `assets/prose/README.md`, in the fenced `prose/` tree under `## How it composes`, add one line after the `base-paper-guide.md` line (currently line 18):
```
  base-state-guide.md    ← mechanics for a workshop state guide (write-workshop-state-guide)
```
Add nothing else. Do not reflow surrounding text.

- [ ] **Step 3: Edit `plugin.json`**

Change the `description` to list the new skill and bump `version` `0.3.0` → `0.4.0`:
```json
  "version": "0.4.0",
  "description": "Styled LaTeX writing skills (write-manual, write-paper-guide, write-topic-guide, write-workshop-state-guide) following the torsor design and prose style. Self-contained: bundles the torsor prose library, reference templates, and the tex2torsor converter so the skills run on any machine.",
```

- [ ] **Step 4: Validate JSON + the additions**

Run:
```bash
cd plugins/torsor-writing
python3 -m json.tool .claude-plugin/plugin.json >/dev/null && echo "ok: json valid" || echo "BROKEN json"
grep -q 'write-workshop-state-guide' .claude-plugin/plugin.json && echo "ok: skill in description" || echo "MISSING: description"
grep -q '"version": "0.4.0"' .claude-plugin/plugin.json && echo "ok: version" || echo "MISSING: version"
grep -q 'base-state-guide.md' assets/prose/README.md && echo "ok: readme map" || echo "MISSING: readme map"
```
Expected: all `ok:`, no `BROKEN`/`MISSING`.

- [ ] **Step 5: Commit**

```bash
cd ~/Library/CloudStorage/Dropbox/lab/software/torsor-writing/torsor-writing-plugin
git add plugins/torsor-writing/assets/prose/README.md plugins/torsor-writing/.claude-plugin/plugin.json
git commit -m "Register write-workshop-state-guide in prose README and plugin manifest

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 4: Whole-skill consistency review (no new files)

**Files:** none created; reads the three deliverables.

- [ ] **Step 1: Cross-file consistency check**

Run:
```bash
cd plugins/torsor-writing
# The four ledger bands are named identically in base + skill
for f in assets/prose/base-state-guide.md skills/write-workshop-state-guide/SKILL.md; do
  echo "== $f =="
  for b in "Solid" "Provisional" "Open" "Where to be skeptical"; do
    grep -q "$b" "$f" && echo "  ok: $b" || echo "  MISSING: $b"
  done
done
# The five state questions live in the base file, and the skill defers to it (no divergent copy)
grep -c "state question" skills/write-workshop-state-guide/SKILL.md   # expect the skill to point at the base, not restate all five differently
# No banned rhetoric leaked into our own prose (the skill/base describe the ban; they shouldn't self-violate in headings)
grep -nE "\b(pulled it off|breakthrough)\b" skills/write-workshop-state-guide/SKILL.md | grep -vi "ban\|avoid\|never\|not " || echo "ok: no self-violation"
```
Expected: band names present in both files; no self-violation outside the ban-list context.

- [ ] **Step 2: Spec-coverage read-through**

Open the spec (`docs/superpowers/specs/2026-07-03-write-workshop-state-guide-design.md`) and confirm each of §§1–7 is represented in the two authored files. Note any gap; if found, fix in the relevant file and re-commit under Task 1 or 2's file.

- [ ] **Step 3: Final commit if any fixes were made**

```bash
cd ~/Library/CloudStorage/Dropbox/lab/software/torsor-writing/torsor-writing-plugin
git add -A && git commit -m "Fix state-guide skill consistency gaps from review

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>" || echo "no fixes needed"
```

---

## Manual acceptance (post-plan, not a task)

The true end-to-end — invoke `write-workshop-state-guide` against a live (or sample) workshop room, build all four formats, run `make check` and the publication pass — requires a live room and the workshop toolchain. It is a manual acceptance step for the first real use, not part of authoring the skill. The build discipline itself is inherited verbatim from `assets/commons/scaffold.md`, already proven by the sibling skills.
