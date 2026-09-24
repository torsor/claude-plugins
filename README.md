# torsor-plugins

A [Claude Code](https://claude.com/claude-code) plugin marketplace from torsor lab. One
plugin so far:

## torsor-writing

Eleven styled LaTeX writing skills, packaged to run on **any** machine. The skills used to read
the torsor prose library, reference templates, a style preamble, and `tex2torsor` by absolute
paths on one machine; here those are vendored into the plugin and referenced via
`${CLAUDE_PLUGIN_ROOT}`, so nothing is tied to a particular machine.

Each skill produces a document in the torsor house format — LaTeX source with PDF, HTML,
EPUB, and Markdown output — in the torsor design and prose style.

| Skill | What it writes |
|-------|----------------|
| `write-manual` | A user's manual for a project (direct, conversational prose). |
| `write-paper-guide` | A two-part reading guide to a single mathematical paper, calibrated to a specific reader. |
| `write-critical-guide` | A critical guide to one paper — summary, graded issue list, repairs, and annotated copies of its source. Working material for a critical reader; runs unattended and reaches no verdict. |
| `write-paper-repairs` | Repairs for the issues a critical guide found, written into the paper's own source as tracked changes. Applies only what the paper forces; proposes the rest. |
| `write-review-and-repair` | Runs the pair end to end — `write-critical-guide` then `write-paper-repairs` on one paper — as a single unattended pipeline. A thin orchestrator; adds no judgment of its own. |
| `write-topic-guide` | One explanatory guide synthesizing several sources on a topic (handles large / scanned PDFs). |
| `write-study-guide` | A personalized route through one large tag-addressable corpus (Stacks, Kerodon) toward a target result. |
| `write-body-of-work-summary` | A styled overview of one mathematician's whole body of work — program essay plus a paragraph per paper. |
| `write-workshop-state-guide` | A state guide for a workshop / working session. |
| `write-pure-math-paper` | A mathematics paper in the house style. |
| `write-technical-report` | An evidence-led technical experiment report. |

```
plugins/torsor-writing/
  .claude-plugin/plugin.json
  skills/
    write-manual/               SKILL.md
    write-paper-guide/          SKILL.md (+ lessons.md)
    write-critical-guide/       SKILL.md (+ references/, agents/, tools/annotate_tex.py)
    write-paper-repairs/        SKILL.md (+ references/, agents/, assets/)
    write-review-and-repair/    SKILL.md
    write-topic-guide/          SKILL.md
    write-study-guide/          SKILL.md
    write-body-of-work-summary/ SKILL.md
    write-workshop-state-guide/ SKILL.md
    write-pure-math-paper/      SKILL.md (+ references/, agents/)
    write-technical-report/     SKILL.md (+ references/, agents/)
  assets/
    commons/        shared scaffold, lessons, and publication pass used across the skills
    prose/          the torsor prose library (base + voices + README) — canonical, not a snapshot
    reference/      shelf-main.tex, shelf-00-preface.tex, artifacts-preamble (style only)
  tools/
    tex2torsor/     LaTeX → HTML converter
```

### Install (on each machine)

```bash
claude plugin marketplace add <this-repo-url-or-path>
claude plugin install torsor-writing@torsor-plugins
claude plugin list
```

Then all eleven `/write-…` skills are available there.

### Build prerequisites

The skills author and reference everything themselves, but **building** a manual/guide still
needs these on the box that runs `make`:

- a TeX install (with `amsmath`, `amsthm`, `mathtools` for guides)
- `pandoc` (EPUB, and HTML via tex2torsor)
- `latexmk` (part of TeX Live / MacTeX) for the PDF
- optionally `lab-view`, the torsor lab previewer used by `make view`; the other targets
  do not need it

`tex2torsor` itself is bundled, so it is **not** a separate prerequisite.

### The bundled assets

`assets/reference/` and `tools/tex2torsor/` are snapshots of a separate source tree, kept
here so the plugin is self-contained. `assets/prose/` is canonical here and is edited in
place — see `assets/prose/README.md`.

Machines pick up changes with `claude plugin update torsor-writing`.

### Tests

[Implementation status](docs/STATUS.md) distinguishes executable checks from workflows that
still require expert review.

```bash
python3 -m pip install -r requirements-dev.txt
make test
```

The suite exercises the critical-guide annotation tool against a fictional manuscript with
an executable issue ledger (`tests/fixtures/review/`).

New examples require a manual provenance review. Keep commissioned documents and case
records outside this repository. The concrete review example lives in
`tests/fixtures/review/` and was written solely for documentation and tests.
