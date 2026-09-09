# Implementation and validation status

The review pipeline has three parts: a critical guide, a repair workflow, and an
orchestrator that runs them in sequence.

| Component | Implemented behavior | Verification available here |
|---|---|---|
| Issue ledger and annotation generator | Unique anchors, category-specific annotations, generated issue list | Fictional manuscript fixture; automated anchor and generation checks |
| Publication audit | Working files, index, history, tags, and proposed outgoing objects | Regression tests including scanner failures and exemption bypasses |
| Repair markup | Applied, proposed, and removed content; marked and clean builds | Source implementation; inspect both builds for each new document |
| Long-document review | Per-chunk ledger, inherited issues, final synthesis | Documented workflow; no end-to-end long-document fixture |
| Mathematical assessment and repair selection | Instructions for independent verification and scoped repairs | Requires expert review; the repository tests do not validate mathematical judgment |

`tests/fixtures/review/` contains a purpose-written elementary manuscript with intentional
errors and its issue ledger. It is documentation and test data, with no connection to a
commissioned review. See `docs/PUBLICATION.md` for the publication checks.

The shared builder remains a future design described in
`specs/2026-08-27-unified-builder-core-future-goals.md`.
