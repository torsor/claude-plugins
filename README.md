# torsor-plugins

A [Claude Code](https://claude.com/claude-code) plugin marketplace from torsor lab. One
plugin so far:

## torsor-writing

The `write-manual` and `write-paper-guide` skills, packaged to run on **any** machine. Both
skills used to read the torsor prose library, a reference manual, a style preamble, and
`tex2torsor` by absolute paths on one machine; here those are vendored into the plugin and
referenced via `${CLAUDE_PLUGIN_ROOT}`, so nothing is tied to a particular machine.

```
plugins/torsor-writing/
  .claude-plugin/plugin.json
  skills/
    write-manual/SKILL.md
    write-paper-guide/SKILL.md  (+ lessons.md)
  assets/
    prose/          the torsor prose library (base + voices + README)
    reference/      shelf-main.tex, shelf-00-preface.tex, artifacts-preamble (style only)
  tools/
    tex2torsor/     LaTeX → HTML converter
  scripts/
    sync-assets.sh  refresh + de-identify the snapshots from the source tree (maintainer only)
```

### Install (on each machine)

```bash
claude plugin marketplace add <this-repo-url-or-path>
claude plugin install torsor-writing@torsor-plugins
claude plugin list
```

Then `/write-manual` and `/write-paper-guide` are available there.

### Build prerequisites

The skills author and reference everything themselves, but **building** a manual/guide still
needs these on the box that runs `make`:

- a TeX install (with `amsmath`, `amsthm`, `mathtools` for guides)
- `pandoc` (EPUB, and HTML via tex2torsor)
- `latexd` and `lab-view` — the torsor lab build/preview tools; install them separately, or
  build PDF/HTML by hand (`latexmk`, and `make TEX2TORSOR_ROOT=… html`)

`tex2torsor` itself is bundled, so it is **not** a separate prerequisite.

### Maintaining the bundled assets

The snapshots in `assets/` and `tools/` are generated from a private source tree by
`scripts/sync-assets.sh`, which also strips maintainer identifiers on the way in (the
originals are left untouched). To refresh:

```bash
LAB=/path/to/source-tree plugins/torsor-writing/scripts/sync-assets.sh
git commit -am "sync assets" && git push
```

Other machines pick up the change with `claude plugin update torsor-writing`.
