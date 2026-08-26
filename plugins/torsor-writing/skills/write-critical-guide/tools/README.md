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

`build` runs the pass sequence that converges and then checks the log, the note count, and the
PDF timestamp, exiting non-zero on any problem. It exists because one pdflatex pass leaves
every cross-reference reading `??` and `make` calls that a success.

Requires PyYAML. The schema, and the anchor rule that decides whether a package builds, are
documented in `../../skills/write-critical-guide/references/issue-model.md`.

Copy this file into each `critical-guide/` directory so the package rebuilds on any machine,
with or without the skill installed.

It lives inside the skill rather than under the plugin's shared `tools/` because exactly one
skill uses it — and because a skill symlinked into `~/.claude/skills/` has no
`${CLAUDE_PLUGIN_ROOT}`, so anything outside the skill directory may simply not be reachable.
