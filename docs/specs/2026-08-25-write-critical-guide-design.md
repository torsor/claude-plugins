# Design — critical guides

The pipeline turns a close reading of one paper into a summary, an issue ledger,
suggested repairs, and annotated source copies. The reader decides how to use those
materials. The pipeline does not issue a publication recommendation.

## Handoffs

The reading pass records concerns with exact source locations. Separate mathematical,
reference, editorial, and contextual passes examine those concerns and discover others.
Independent checks attempt to refute consequential findings before they enter the ledger.
The repair pass distinguishes a demonstrated correction from a possible route.

`issues.yaml` is the single source of truth for generated issue lists and annotations.
An anchor must resolve in the selected source before generation proceeds. The compiled
paper is the artifact under study; source files support quotation and annotation.

## Decisions

- Categories describe the work a correction asks of the author. They can vary by paper.
- Grade, dependency, and confidence are independent fields.
- A finding whose premises fail must be corrected or withdrawn before publication.
- Source and submitted-PDF locations stay distinct when the versions differ.
- A repair affecting several statements is checked as a group.
- The package build verifies its output, including references and annotation counts.

## Components

`skills/write-critical-guide/SKILL.md` describes the pipeline. Its `references/` directory
contains the ledger schema, writing rules, package templates, and chunked-review design.
`tools/annotate_tex.py` generates the ledger's artifacts. `tools/check_guide.py` checks the
combined guide PDF.

The fictional fixture at `tests/fixtures/review/` supplies the public worked example.
Implementation and validation limits are recorded in `docs/STATUS.md`. Case records,
review transcripts, and source documents from commissioned work are kept outside this
repository.
