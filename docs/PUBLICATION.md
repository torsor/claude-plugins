# Publishing repository changes

Commissioned documents, review records, incident notes, private sanitization rules,
and historical backups stay outside this repository. Git ignore rules prevent some
accidental additions; they do not protect a file that is already tracked.

## Examples

Use examples written expressly for the repository. `tests/fixtures/review/` contains
the fictional averaging manuscript and its ledger. When an example needs additional
mathematics, introduce it as a hypothetical extension and explain it from first principles.
Do not adapt a real finding by changing its names or measurements. Public descriptions
of validation should identify the mechanism tested and its limits.

Before staging a new example, manually check its provenance, quoted text, labels,
measurements, and relationship to other examples. Pattern scanning cannot perform this
review. Public tool and project documentation links remain appropriate.

## Checks

Python 3 and PyYAML are needed for the test suite. The audit itself uses only Python's
standard library and Git. From the repository root:

```sh
python3 -m pip install -r requirements-dev.txt
make enable-hooks
make check
```

The same test and history checks run on GitHub pushes and pull requests. Local hooks
are still needed to catch problems before upload; a remote check runs after the upload.

The pre-commit hook checks working files and the index. The pre-push hook checks all
local history and every outgoing object, including commits pushed by object ID. The
history check includes branches, tags, historical paths, blobs, and message bodies.
Commit author and tagger metadata remain ordinary Git attribution.

The checks reject identifier shapes, non-placeholder author lists, personal paths,
common credential patterns, tracked private-looking files, and unreviewed binary content.
They fail on Git errors. There are no blanket exclusions for detector files or test files.
Only exact approved placeholder values are exempt. Fix a finding; do not hide its line
behind an allowed value.

A maintainer can configure an additional private UTF-8 substring list:

```sh
git config --local torsor.auditDenylist /path/outside/repository/terms.txt
```

Alternatively pass `--denylist /path/to/terms.txt` to `audit-public.sh` or set
`TORSOR_AUDIT_DENYLIST`. A configured list that is missing or empty fails the audit.
The list's values and matched passages are not printed.

## Asset imports and releases

`sync-assets.sh` requires nonempty `scripts/sanitize.local` rules before copying anything.
It sanitizes and audits a temporary snapshot, then installs the checked reference and
converter files. The prose library is maintained directly in the repository. Review the
diff even after the automated import passes.

For a release, update the plugin version, run the checks, review the full staged diff,
and create a version tag. After pushing, audit a fresh clone with all remote branches and
tags fetched. Use a fresh clone when a repository's history has been replaced; retain any
needed work privately and reapply reviewed changes without merging the old history.
