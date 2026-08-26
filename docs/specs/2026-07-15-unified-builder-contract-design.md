# Design — the unified mechanical builder (writer ↔ builder contract)

*2026-07-15. Status: implemented — unified core built, all six skills wired, legacy forks retired.*

A contract that separates **authoring** (structure, prose, calibration — expensive
model) from the **mechanical build** (scaffold, Makefile, tools, build, check, safe
fixes — cheap model), so the two compose instead of each carrying its own copy of the
toolchain. Source material is sometimes Markdown, sometimes LaTeX; both must land in the
same builder.

## The problem this solves

The build machinery currently exists **twice** and has already diverged:

| Piece | `torsor-writing` plugin | `technical-doc-builder` |
|---|---|---|
| Preamble template | `assets/reference/shelf-main.tex` | `generate_main_tex()` in the scaffold |
| tex2torsor + CSS | `tools/tex2torsor/` (`manual.css`) | `assets/tex2torsor/` (`doc.css`) |
| `check-build.py` | `tools/check-build.py` | `assets/check-build.py` (**already differs**) |
| Makefile | `assets/commons/scaffold.md` (prose) | `generate_makefile()` (code) |
| EPUB variants | one (MathML) | **two** (MathML + SVG) — the new feature |

Same design, two lineages. The SVG-EPUB feature landed in one and not the other. Every
future mechanical improvement pays this tax twice or silently forks. The fix is not more
splitting — it is **one mechanical core** with a defined hand-off, consumed by both
source types and both distributions.

## The central decision — the LaTeX tree is the canonical intermediate

Both source types already converge on LaTeX:

- the Markdown builder converts `.md` → `latex/chapters/*.tex`, then builds from there;
- the writing skills author `latex/chapters/*.tex` directly.

So the contract's canonical artifact is the **LaTeX tree**:

```
latex/
  main.tex          ← assembled by the builder from the shared preamble + title page
  chapters/*.tex    ← THE authored content (the hand-off artifact)
  assets/           ← images, cover
  STYLE.md          ← voice record (informational)
```

Everything downstream — PDF, HTML, EPUB (MathML), EPUB (SVG), Markdown, `make check` —
is a function of this tree. Markdown is not a competing format; it is one **front-end**
that produces the tree.

## Modularity & extension model (the governing constraint)

The system will keep gaining formats, features, and voices. The design ideal is
**modularity / DRY**: an addition drops into one place and reaches everything it should,
without editing a monolith and without drifting across copies. Everything below serves
this; where the contract and this section conflict, this section wins.

**Four orthogonal extension axes:**

| Axis | A module is… | Registry |
|---|---|---|
| **Format** | a render target: `{ name, ext, recipe over the LaTeX tree, deps }` | `core/formats/` |
| **Feature** | a capability (math, callouts, listings, cover, bib, …) that contributes a **slice to every format** | `core/features/` |
| **Voice** | a prose register (already modular) — prose only, never build mechanics | `assets/prose/voices/` |
| **Genre** | a **bundle**: declares enabled features + title-page template + base prose + chapter plan | genre manifest |

**Feature co-location — the anti-tangle rule.** A single feature usually needs a piece in
*every* format: `pitfallbox` needs a LaTeX `newmdenv` (PDF), a tex2torsor callout mapping
(HTML), and a CSS rule (HTML/EPUB). Those pieces **live together in the feature module**:

```
core/features/callouts/
  preamble.tex     # \newmdenv{pitfallbox}{…}   (PDF)
  mappings.yaml    # tex2torsor: pitfallbox → callout--pitfall   (HTML)
  style.css        # .callout--pitfall {…}   (HTML/EPUB)
```

The builder assembles each format by collecting the relevant slice from every enabled
feature. Add or change a feature in **one directory**; it reaches all formats at once. This
is precisely what failed when the SVG-EPUB landed in one build lineage and not the other,
and when the two `check-build.py` copies drifted.

**Assemble, don't branch.** Preamble, `STYLE.md`, Makefile, tex2torsor mappings, and CSS
are all *assembled* by concatenating fragments from the enabled features + chosen voice —
generalizing the existing `base + voice → STYLE.md` assembly. No format-specific `if/else`
chains, no growing monolith f-string of hand-written targets.

**Formats can be variants.** A format may be one recipe parameterized, not a copy. `epub`
and `epub-svg` are the **same recipe** differing only by a `math` render strategy
(`mathml | svg`); the strategy is itself pluggable. So the second EPUB is not a second
target — it is `epub` with `math=svg`.

**YAGNI boundary.** Registries are *directories of small fragment files + a thin
assembler*, not a plugin DSL or dynamic loading. A format module is a few lines of recipe
template; a feature module is 1–4 short fragments. Keep each module boring.

**Honest status of what's already built.** The delivered SVG-EPUB is a bolted-on Makefile
target plus a loose `mathsvg_filter.py` — it works but is **not yet** in this shape. The
core extraction must land it as the `epub` recipe's `math=svg` variant, with the filter
owned by the `math` feature's EPUB slice. Same for the monolithic preamble and Makefile:
they get decomposed into base + feature fragments during extraction, not carried over
whole.

## Architecture — three layers

```
  ┌── front-ends (produce the LaTeX tree) ──────────────┐
  │  from-markdown:  .md  → chapters/*.tex   (mechanical)│
  │  from-latex:     author chapters/*.tex   (authoring) │
  │                  or bring existing LaTeX  (mechanical)│
  └──────────────────────────┬──────────────────────────┘
                             │  the LaTeX tree + a build manifest
  ┌──────────────────────────▼──────────────────────────┐
  │  CORE BUILDER (one copy, vendored into deliverables) │
  │   • assemble main.tex from shared preamble + genre   │
  │     title page                                       │
  │   • drop in Makefile, tex2torsor, check-build.py,    │
  │     scripts/ (prepare_markdown, inject_mathjax,      │
  │     mathsvg_filter)                                  │
  │   • make all → PDF, HTML, EPUB×2, MD                 │
  │   • make check → evidence report                     │
  └──────────────────────────┬──────────────────────────┘
                             │  evidence report
  ┌──────────────────────────▼──────────────────────────┐
  │  PUBLICATION PASS (tier 2 vision + escalated fixes)  │
  └─────────────────────────────────────────────────────┘
```

## The build contract — what the writer hands over

A **document directory** in this state, plus a **build manifest** (CLI flags or a small
`build.yaml`). Nothing else crosses the boundary.

Directory (minimum): `latex/chapters/*.tex` and `latex/assets/` (may be empty). The
writer does **not** author `main.tex`, the Makefile, the colophon, or drop in tools —
those are the builder's job. This narrows the writer's surface to content.

Manifest fields:

```yaml
source:   { kind: markdown|latex, path: <file-or-dir> }
genre:    manual | paper-guide | topic-guide | study-guide |
          body-of-work | state-guide | technical-doc
title:    "<Title>"
subtitle: "…"            # optional; genre title page decides if used
tagline:  "…"            # optional
blurb:    "…"            # optional
author:   "torsor lab"
cover:    <path>         # optional
voice:    01-direct      # recorded in STYLE.md
math:     auto           # auto = on for math genres; adds amsthm/mathtools + theorem envs
```

`genre` selects the title-page template and whether the math block is included;
everything else about the preamble is a family-wide constant the writer may not touch.

**Output filename.** There is no `basename` field. The output **stem is the deliverable
directory's name** — so `foo-bar-guide/` builds `foo-bar-guide.pdf`, `.html`, `.epub`,
`-svg.epub`, `.md`. This is self-describing once a PDF/EPUB is shared out of its folder
(the old `manual.*` stem was not), and matches how the deliverable folders are already
named. Confirmation is **mode-dependent** — see below. (Retires the legacy `manual.*`.)

## Invocation mode — autonomous vs interactive

The skills run **both autonomously and interactively**, and the contract branches on it.
The mode changes *when the builder pauses*, never *what it produces*.

- **Autonomous:** apply defaults silently and proceed. Output stem = directory name, no
  prompt. Escalations and uncertainties go into the **evidence report**; the run does not
  block waiting on a human.
- **Interactive:** confirm the same defaults before committing — surface the output stem
  ("build as `foo-bar-guide.*`?") and any genre default the user might want to change, and
  **ask** on escalations instead of only reporting them.

This is the same axis as the cheap-model safety contract below: an escalation in
autonomous mode is *reported and the loop halts on it*; in interactive mode it is *a
question to the user*. Mode is an input to the build request (default: autonomous when no
TTY / when dispatched as a subagent).

## What the builder guarantees back

- A **self-contained** deliverable folder: `.gitignore`, `Makefile`, vendored
  `tex2torsor/`, `check-build.py`, `scripts/`, assembled `latex/main.tex`, `STYLE.md`.
  (Tools are **copied**, not symlinked, so the deliverable survives a plugin
  update/uninstall — keep the plugin's current rule.)
- Built outputs (`<stem>` = deliverable directory name): `latex/<stem>.pdf` (latexmk
  `-jobname=<stem>`, source stays `main.tex`), `html/<stem>.html`, `epub/<stem>.epub`
  (MathML), `epub/<stem>-svg.epub` (SVG math), `markdown/<stem>.md`. (The examples show
  these renamed by hand — `gdti.pdf`, `dti.epub`; the stem rule automates that.)
- A `make check` **evidence report** (the tier-1 contract from `publication.md`): fresh
  PDF, no LaTeX errors, no undefined refs, itemized overfull hboxes, non-ASCII listings,
  HTML math loader present, all expected outputs present.

The report is evidence, not a verdict. "Looks good" is not a return value.

## The safety contract — the cheap model's action set

The split is only safe because `make check` is an objective verifier. The cheap builder's
autonomous authority is therefore **narrow and enumerated**:

**May apply without asking** (log-indicated, non-authorial):

- missing LaTeX package → install / add `\usepackage`
- non-ASCII inside `lstlisting` → ASCII equivalent (`->` not `→`)
- a long URL or long command overflowing → wrap in a code fence / `\url{}`
- stale or missing output → rebuild
- HTML math span without MathJax loader → run `inject_mathjax.py`

**Must escalate** (touches words or structure — expensive model / user):

- overfull hbox whose only fix is **shortening prose** or **redesigning a table**
- any ambiguous math/LaTeX interpretation
- source cleanup that changes document structure
- cover sizing/placement judgment
- anything requiring a guess about authorial intent

### Checker policy (resolved)

The unified `check-build.py` is **strict** (the builder's stance wins over the plugin's
warn-only), because the autonomous loop needs quality flags to be *fatal* — a warning gets
stepped over:

- **Non-ASCII inside `lstlisting` → hard failure.** Not cosmetic; the `listings` package
  chokes on it.
- **Overfull hbox → hard failure above a pt threshold** (default ~2pt). The threshold is
  the escape valve: it keeps the loop honest without trapping it on a sub-2pt math overrun
  that no rewrap can fix. Overruns below the threshold are reported, not fatal.
- **Mode tie-in:** in interactive mode a remaining overfull is an *accepted exception* the
  user signs off on; in autonomous mode it stays fatal and lands in the report.

The trap: recognizing "I am about to make an authorial decision" is exactly the judgment
cheap models are worst at. So the escalation list is **explicit and conservative** — the
builder escalates by category, not by its own confidence. `make check` catches *broken*
output; it does **not** catch *degraded-but-valid* prose, which is why prose-shortening is
never in the autonomous set.

## Model tiering (maps onto the layers)

| Work | Tier |
|---|---|
| Author `chapters/*.tex` (from-latex front-end) | Supervisor / Opus |
| Markdown → LaTeX front-end, scaffold, `make all`, safe fixes | Builder / Haiku or mini |
| Escalated content-touching fixes, tier-2 vision pass | Reviewer / Sonnet, Supervisor for ambiguity |

This is `technical-doc-formatter`'s Builder/Reviewer/Supervisor split, generalized to both
source types.

## Single source of truth — and staying self-contained

One canonical **core** directory holds: the preamble template, per-genre title-page
snippets, `tex2torsor/` (+ one CSS set, parameterized by `basename`), `check-build.py`,
the Makefile generator, and `scripts/` (incl. `mathsvg_filter.py`). Proposed home:
`plugins/torsor-writing/tools/` (the distribution the writers already live in).

Two consumers, kept in sync by the existing `sync-assets.sh` mechanism rather than by
hand-copying:

1. the plugin's writing skills (`from-latex`);
2. `technical-doc-builder` (`from-markdown`), which stays a separate cross-model
   distribution (it has `agents/openai.yaml`) but **vendors the same core** instead of
   maintaining a fork.

"Single source" is the **maintenance** source. Each *deliverable* still receives copied
tools at scaffold time — self-containment is preserved.

## Where `epub-svg` lives (modular framing)

Not as its own target. `epub` is one **format module** whose recipe takes a `math`
strategy; `epub-svg` is that recipe with `math=svg`. The SVG rendering itself
(`mathsvg_filter.py`, latex+dvisvgm) is the **`math` feature's EPUB slice** — co-located
with the math feature's preamble fragment and HTML/MathJax slice. Consequences:

- a genre that enables the `math` feature gets both EPUB variants for free;
- a non-math genre builds neither the theorem preamble nor the SVG filter — no dead
  machinery;
- adding a third math target later (e.g. `html` with `math=svg`) reuses the same feature
  slice instead of copying the filter.

This is the payoff of the co-location rule: the current asymmetry (feature in one lineage,
absent from the other) becomes impossible by construction.

## Migration — phased, each step shippable

1. **Reconcile the shared, format-neutral assets.** ✅ `check-build.py` (strict + threshold
   + stem-parameterized + both EPUBs) and ✅ `doc.css` (the superset) are done, in
   `plugins/torsor-writing/tools/`.
2. **Decompose into registries.** ✅ *Exemplar landed* in `tools/core/`: `base/` +
   `features/math/` (co-locating preamble / `math.mk` / `mathsvg_filter.py` /
   `inject_mathjax.py` / mappings / CSS) + `formats/{pdf,html,epub,md}.mk`. Features
   self-register targets (`epub-svg`, `html-mathjax`) via `FORMAT_TARGETS`; the SVG-EPUB is
   now the math feature's epub slice, not a bolted-on target. `callouts` extracted
   (default-on; note/warn/pitfall across PDF/HTML/EPUB) and `listings` extracted (opt-in,
   default-off; base now carries only typography/geometry/palette/headings/tables/layout).
   Three slice-shapes proven: build-target+outputs (math), all-format presentation
   (callouts), opt-in package+CSS (listings). Checker no longer hardcodes outputs — each
   format/feature declares `CHECK_OUTPUTS`, so a non-math doc is not asked for a SVG EPUB.
   Remaining: `cover`, `bib`. Known seam: `filter.lua`'s `shell`-class rule stays shared
   (inert when listings is off) rather than fragmenting Lua per feature.
3. **Build the assembler.** ✅ *Skeleton landed* — `core/assemble.py` stitches `main.tex`
   (base + feature preambles + body), vendors the core + enabled features, and merges each
   feature's tex2torsor mappings/CSS. Proven end-to-end: assemble a math doc → `make all` →
   check PASS with both EPUBs, embedded SVG math, and the pitfall callout in all formats.
   Remaining: `STYLE.md` prose assembly (base + voice), per-genre title pages, `build.yaml`
   as the committed manifest across genres.
4. **Re-front-end.** `from-latex` ✅ *proven*: a genre layer (`core/genres/<genre>/` with
   `genre.yaml` default features + optional `titlepage.tex` override) plus manifest-driven
   document structure (`chapters:` → `\frontmatter/\mainmatter/\appendix/\backmatter`). The
   pre-torsor `thing-manual` re-skinned cleanly through the core — 94-page PDF + all five
   formats, house-style title page with the icon as cover, features resolved from the
   `manual` genre. (The strict checker correctly escalated 20 overfull hboxes from
   `ll`/`lll` tables reflowed into 6×9 — reviewer-tier table redesign, not a builder fix.)
   `from-markdown` ✅ *proven* too: `core/frontend_markdown.py` converts Markdown → the
   LaTeX chapter tree (reusing the prepare-markdown logic) and delegates to `assemble.py`;
   PASSes end-to-end. Two integration fixes landed: a `\providecommand` shim for pandoc's
   `\tightlist`/`\pandocbounded`/`\passthrough`, and `--no-highlight` on the md→LaTeX
   conversion so language-tagged fences render as the house verbatim style (pandoc's
   `Shaded`/`Highlighting` are undefined in the core, and monochrome verbatim is the
   correct house choice anyway). `STYLE.md` prose assembly ✅ (base prose + voice).
5. **Wire the writing skills onto the core.** ✅ *Started*: `assemble.py` gained an
   `--in-place` mode (scaffold `main.tex`+tooling around chapters authored in the doc dir;
   idempotent) and `extra_features` (append to genre defaults — e.g. a code+math manual is
   `genre: manual` + `extra_features: [math]`, verified). Genre modules exist for all seven
   genres (`genre.yaml` = default features + prose base). `commons/scaffold.md` rewritten
   from the inlined Makefile/preamble into the core contract (author chapters + `build.yaml`
   → `assemble.py --in-place` → `make all`). **All six writing skills rewired** (each SKILL.md
   points to the core flow, correct genre, old `make pdf && …` chain gone, `shelf-main.tex`
   reframed to reference-only) — five via parallel subagents, verified consistent. **Guide
   title pages** done: one shared `genres/_shared/guide-titlepage.tex` ("A Reading Guide
   to …" shape), referenced by each guide genre's `genre.yaml` `titlepage:` key; verified
   across paper-guide and state-guide. Final regression green across from-latex/from-markdown/
   in-place/guide deliverables.
6. **Forks retired.** ✅ The from-markdown prepare logic was **vendored into the core**
   (`core/prepare_markdown.py` + `copy_markdown_and_images` in `frontend_markdown.py`), so the
   core no longer imports anything from `technical-doc-builder` — that standalone tree is now
   dead and can be archived. In-plugin legacy removed: `manual.css` deleted, the legacy
   `tex2torsor/mappings.yaml` minimized to the clean base (callout mappings live in the
   `callouts` feature; the assembler overwrites the vendored copy per deliverable). Full suite
   still green.
7. **`cover` and `bib` done.** Cover works across all three formats (PDF title page, EPUB
   `--epub-cover-image`, HTML image, now responsive) via the manifest `cover:` key. `bib` is
   a co-located feature: `features/bib/preamble.tex` (biblatex+biber for the PDF) +
   `features/bib/bib.mk` (sets `PANDOC_BIB`, which every pandoc format appends, so HTML/EPUB/
   Markdown resolve the same `\cite`s via pandoc `--citeproc`). Auto-enabled by the manifest
   `bibliography:` key; `tex2torsor.py` gained `--citeproc`/`--bibliography` passthrough.
   Verified: citations resolve in PDF (`[Ser55]`), HTML/EPUB/MD (`(Serre 1955)`) — the two
   citation styles differ (biblatex alphabetic vs citeproc author-date), a known dual-tooling
   quirk. No open items remain.

**Invariant for every step:** adding a format or feature must be a *new module*, never an
edit to a monolith. If a step would require editing a shared file to add one feature, the
decomposition isn't done.

## Deliberately out of scope (YAGNI)

- A GUI or web service — the contract is a directory + a manifest + `make`.
- New output formats beyond the current five (+ the second EPUB).
- Changing the house design (palette, fonts, boxes) — family-wide constants, untouched.
- A general pandoc-agnostic build system — this is the torsor toolchain, parameterized,
  not rewritten.

## Resolved decisions (2026-07-15)

- **Core home:** `plugins/torsor-writing/tools/` — the writers live there and
  `sync-assets.sh` already flows outward. `technical-doc-builder` vendors the same core.
- **Manifest:** a committed `build.yaml` in each deliverable (reproducible rebuilds +
  provenance), not ad-hoc CLI flags.
- **Output stem:** the deliverable directory name (retires `manual.*`); confirm
  interactively, silent in autonomous mode.
- **Checker policy:** strict — non-ASCII listings fatal, overfull fatal above a ~2pt
  threshold, interactive mode allows accepted exceptions.
- **CSS:** not a real fork — `doc.css` is `manual.css` + a `.titlepage img` rule. Unify to
  one file (the superset).
- **Math block:** family base preamble + math block as a `math: auto` toggle (on for math
  genres), matching the plugin's existing conditional.

## Open questions

1. **from-latex "bring your own":** when the user supplies existing LaTeX that is *not*
   torsor-shaped, reskin it into the family preamble (as `thing-manual` proved works) or
   build it as-is? Current behavior: reskin — the writer hands *chapters*, the core owns
   the preamble.

*Resolved:*
- **Genre title pages** — a genre supplies `genres/<g>/titlepage.tex` only when it differs
  from the base default; `genre.yaml` carries default features (later: prose base + plan).
- **Table reflow** — a **front-end normalization** (`core/normalize_tables.py`), NOT a
  feature (features stay preamble/mappings/CSS; source transforms live in the front-ends).
  Opt-in via manifest `fit_tables: true`; from-markdown defaults it on, from-latex leaves
  it off so authored LaTeX is never silently rewritten. Two mechanical modes: bare `l/c/r`
  → equal-width wrapping `L{}`; absolute `p{Xcm}` → the same widths rescaled proportionally
  to `\linewidth` (author ratios preserved). Column totals held under 1.0 for `\tabcolsep`.
- **Long inline code** — `base`'s `\code` is now breakable (expl3 inserts `\allowbreak`
  after `/ . , : ; " = [ ] -` and `\_`), so long paths / commands / dotted config keys wrap
  instead of overflowing; spaces and nested macros are preserved, short code never breaks.
  Together these took the re-skinned `thing-manual` to a **fully clean** build (0 overfulls).
