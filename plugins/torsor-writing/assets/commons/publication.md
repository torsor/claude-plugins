# The publication pass — verification by evidence, not vigilance

Every torsor book ends with this pass. It exists because the failure modes of the
toolchain are quiet: `latexd` exits 0 on failure, an equation walks past the margin
without breaking anything, HTML math silently degrades to raw TeX. The pass moves the
checks from "remember to look" to mechanism, in three tiers. A document is not done —
not committed, not delivered, not declared finished — until the pass has run and its
report is clean or its exceptions are explicitly accepted by the user.

Run it as a **dedicated subagent** when the writing session is long (the pass needs no
authoring context and shouldn't crowd it); run it inline when the session is short.
Either way the output is the same: an evidence report.

## Tier 1 — mechanical checks (scripted)

From the document root:

```
make check          # runs check-build.py
```

If the document predates check-build.py, copy it in first:
`cp ${CLAUDE_PLUGIN_ROOT}/tools/check-build.py <doc-dir>/` (and add the `check` target
from `scaffold.md`, or run `python3 check-build.py` directly).

The script verifies: the PDF exists, is newer than every `.tex` source, and reports a
sane page count; the log carries no LaTeX errors, no undefined references or citations;
it itemizes overfull hboxes (with pt overrun and source lines); it flags non-ASCII
inside `lstlisting`; it flags HTML math spans with no MathJax loader present; it notes
missing EPUB/Markdown outputs. Exit 0 with warnings is possible — read the report, not
just the exit code.

## Tier 2 — vision checks (sampled, targeted)

The residue that is genuinely visual: display math that fits the hbox but crowds the
margin, tables broken badly across pages, a diagram rendered as garbage in HTML, a title
page with a misplaced element. Do not re-read the whole book. Render and inspect a
targeted sample with the Read tool on the built PDF:

- the title page and the colophon page;
- one body page per chapter;
- **every page containing a region tier 1 flagged** (map overfull source lines to pages
  via content);
- every page with a display equation, table, or diagram, when the document is
  math-heavy (for a light document, a sample of them).

For HTML: open `html/manual.html` output and check the hardest math example in the
document actually renders (MathJax loaded, no raw `$...$` visible), plus one callout of
each type used. For EPUB: spot-check only if the document is math-heavy (pandoc's MathML
path — see `lessons.md`).

## Tier 3 — the evidence report (the gate)

The pass concludes with a report of **evidence, not verdicts**. "Everything looks good"
is not an acceptable return value. Required shape:

```
## Publication pass — <doc> — <date>

Tier 1 (make check):
  PDF: <n> pages, built <time>, fresh against sources: yes/no
  LaTeX errors: none | <list>
  Undefined refs/citations: none | <list>
  Overfull hboxes: <count> (worst <pt>) | itemized if > 0
  lstlisting non-ASCII: none | <files:lines>
  HTML math: <n> fallback spans, MathJax loader present: yes/no/n-a

Tier 2 (visual, <k> pages inspected):
  Pages read: <list>
  Findings: none | <specific: "p. 34 display eq crowds right margin", ...>
  HTML spot-check: <what was checked, what it looked like>

Exceptions accepted: none | <user-approved list>
```

If the pass is run by a subagent, this report is its entire return value. Uncertainty is
marked explicitly (the `[CHECK]` convention), never smoothed over.

## Subagent brief (template)

> Run the publication pass on the torsor document at `<doc-dir>`, per
> `${CLAUDE_PLUGIN_ROOT}/assets/commons/publication.md`. Run `make check` (copy
> `check-build.py` from `${CLAUDE_PLUGIN_ROOT}/tools/` if absent). Then vision-inspect
> the targeted sample: title page, colophon, one page per chapter, every page implicated
> by a tier-1 flag, and display-math/table pages. Check the HTML's hardest math example.
> Return ONLY the evidence report in the required shape — evidence, not verdicts. Do not
> fix anything; report.
