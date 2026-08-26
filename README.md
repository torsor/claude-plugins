# torsor-plugins

A [Claude Code](https://claude.com/claude-code) plugin marketplace from torsor lab. One
plugin so far:

## torsor-writing

Eight styled-document skills, packaged to run on **any** machine. Each authors a document in
the torsor house format — LaTeX source with PDF, HTML, EPUB, and Markdown output — in the
torsor design and prose style. A shared **unified core** (`tools/core/`) owns the LaTeX
preamble, Makefile, tooling, and every output format (PDF, HTML, EPUB — MathML and SVG-math
when math is on — and Markdown); a skill authors only **chapters** plus a small `build.yaml`
manifest and lets the core build. The prose library, references, and the core are vendored and
referenced via `${CLAUDE_PLUGIN_ROOT}`, so nothing is tied to a particular machine.

| Skill | What it writes |
|-------|----------------|
| `write-manual` | A user's manual for a project (Scalzi-influenced prose). |
| `write-paper-guide` | A two-part reading guide to a single mathematical paper, calibrated to a specific reader. |
| `write-topic-guide` | One explanatory guide synthesizing several sources on a topic (handles large / scanned PDFs). |
| `write-study-guide` | A personalized route through one large tag-addressable corpus (Stacks, Kerodon) toward a target result. |
| `write-body-of-work-summary` | A styled overview of one mathematician's whole body of work — program essay plus a paragraph per paper. |
| `write-workshop-state-guide` | A state guide for a workshop / working session. |
| `write-pure-math-paper` | An original pure-mathematics paper or short note built around a main result and its proof architecture. |
| `write-technical-report` | A skeptical-reader report on a computational / mathematical / software experiment. |

```
plugins/torsor-writing/
  .claude-plugin/plugin.json
  skills/
    write-manual/               SKILL.md
    write-paper-guide/          SKILL.md (+ lessons.md)
    write-topic-guide/          SKILL.md
    write-study-guide/          SKILL.md
    write-body-of-work-summary/ SKILL.md
    write-workshop-state-guide/ SKILL.md
    write-pure-math-paper/      SKILL.md (+ agents/, references/)
    write-technical-report/     SKILL.md (+ agents/, references/)
  assets/
    commons/        scaffold.md (the build contract), lessons.md, publication.md
    prose/          the torsor prose library (base + voices + README)
    reference/      shelf-main.tex, shelf-00-preface.tex, artifacts (style reference only)
  tools/
    core/           the unified builder: base/ + features/ + formats/ + genres/,
                    assemble.py (--in-place), frontend_markdown.py, check-build.py, tex2torsor/,
                    test/smoke/ (a self-contained regression fixture)
  scripts/
    sync-assets.sh  refresh + de-identify the snapshots from the source tree (maintainer only)
```

Build flow: author `latex/chapters/*.tex` + `build.yaml`, then
`python3 ${CLAUDE_PLUGIN_ROOT}/tools/core/assemble.py <doc>/build.yaml <doc> --in-place`
and `cd <doc> && make all`. See `assets/commons/scaffold.md` for the full contract. To sanity-
check the core itself, build `tools/core/test/smoke/` (see its README) — it should PASS clean.

### Install (on each machine)

```bash
claude plugin marketplace add <this-repo-url-or-path>
claude plugin install torsor-writing@torsor-plugins
claude plugin list
```

Then the `/write-…` skills are available there.

### Build prerequisites

The skills author everything themselves, but **building** still needs these on the box that
runs `make`:

- a TeX install with `latexmk` (plus `amsmath`, `amsthm`, `mathtools`)
- `pandoc` (EPUB/Markdown, and HTML via tex2torsor)
- `dvisvgm` (ships with TeX) — for the SVG-math EPUB
- `biber` (ships with TeX) — only if a document uses the `bib` feature

`latexd`/`lab-view` are optional torsor-lab conveniences; the PDF build falls back to plain
`latexmk` when they are absent. `tex2torsor` and `check-build.py` are vendored by the core,
so they are **not** separate prerequisites.

### Maintaining the bundled assets

The snapshots in `assets/` and `tools/` are generated from a private source tree by
`scripts/sync-assets.sh`, which also strips maintainer identifiers on the way in (the
originals are left untouched). To refresh:

```bash
LAB=/path/to/source-tree plugins/torsor-writing/scripts/sync-assets.sh
git commit -am "sync assets" && git push
```

Other machines pick up the change with `claude plugin update torsor-writing`.
