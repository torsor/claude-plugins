# annotate-tex

Builds the generated half of a critical-guide package from one ledger.

`issues.yaml` is the single source of truth for a review's findings. From it this tool
produces the point-by-point Markdown issue list and one annotated copy of the paper's own
LaTeX source per issue category, each note set as a `\todo[inline]` at the passage it
concerns. Because both come from the same ledger, the prose and the annotation anchors cannot
drift apart.

    python3 annotate_tex.py check -v              # verify anchors; write nothing
    python3 annotate_tex.py annotate -o .         # the annotated .tex files
    python3 annotate_tex.py issues-md -o .        # the Markdown issue list
    python3 annotate_tex.py build -o .            # compile them, and verify the result
    python3 annotate_tex.py all --clean-aux -o .  # all four, after clearing stale aux files

`build` runs `pdflatex, bibtex, pdflatex, pdflatex` and then checks the log, the note count,
and the PDF timestamp, exiting non-zero on any problem. It exists because one pdflatex pass
leaves every cross-reference reading `??` and `make` calls that a success.

**Three passes are not always enough.** Where a paper's numbering is self-referential — the
observed case is `mathtools` with `showonlyrefs` plus `keytheorems` with `sharenumber=equation`,
where a statement's number depends on which equations the previous pass referenced — six are
needed. Run `build` twice and read what it reports; do not assume convergence.

`build` distinguishes two things that produce the same LaTeX warning. A reference whose label
exists in the source has not converged, and fails. A reference whose label does not exist
anywhere can never resolve, is the paper's own dangling cross-reference, prints `??` in the
author's PDF too, and is reported as a note. **A defect in the package fails the build; a
defect in the paper does not** — the paper is allowed to be broken, since that is what the
package is for.

`check_guide.py` applies the same rule to `00-guide.pdf`, which nothing else checks: LaTeX
errors, undefined citations by name, undefined references, `[?]` marks in the extracted text,
and the presence of a References section. Run it from the Makefile's guide target. Undefined
citations fail, because the guide cites what it cites; `??` quoted from the paper is a note.

Requires PyYAML. The schema, and the anchor rule that decides whether a package builds, are
documented in `../../skills/write-critical-guide/references/issue-model.md`.

Copy both scripts into each `critical-guide/` directory so the package rebuilds on any
machine, with or without the skill installed.

It lives inside the skill rather than under the plugin's shared `tools/` because exactly one
skill uses it — and because a skill symlinked into `~/.claude/skills/` has no
`${CLAUDE_PLUGIN_ROOT}`, so anything outside the skill directory may simply not be reachable.
