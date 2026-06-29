# Pre-summarization — turning raw sources into reusable source-notes

This is Phase A of `write-topic-guide`: distilling each source into a structured English
markdown digest, in its own subagent context, so the guide is written from clean notes
instead of raw PDFs. Read this before dispatching any extraction subagent.

## Why a subagent per source

- **Context.** A 300-page scan or a 100-page paper read into your own thread crowds out the
  work of orchestration. A subagent reads it in isolation and returns only the digest.
- **Parallelism.** Independent sources distill concurrently — dispatch them in one batch.
  They write disjoint files, so there is no conflict (the "no parallel writers" caution is
  about shared files, which does not apply here).
- **Reusability.** The digests are a kept deliverable: reusable for a future guide and for
  the reader's own study. Treat them as artifacts, not scratch.

## First, classify each source

For each PDF, check page count and whether it has a real text layer:

```bash
pdfinfo "$f" | awk '/Pages/{print $2}'
# sample text length on a middle page; ~0 chars => scanned image, no text layer
pdftotext -f $mid -l $mid "$f" - | tr -d '[:space:]' | wc -c
```

- **Text layer present** → the subagent runs `pdftotext` itself, and Reads specific pages as
  images only where equations/tables come out garbled.
- **No text layer (scanned image)** → vision-read (below). `pdftotext` returns nothing;
  do **not** reach for OCR.

## Scanned / image PDFs: locate, then vision-read

Never OCR a mathematics scan — tesseract/ocrmypdf mangle formulas. The Read tool renders
PDF pages as images the model reads directly, which is far better on math. But reading 300
pages blindly is wasteful, so split it:

1. **Locate the relevant chapters.** A subagent Reads the front matter (try the first ~10–16
   pages) to find the table of contents, and records each relevant unit's **printed** page
   range. You usually need a chapter or two, not the whole book.
2. **Compute the printed→PDF offset.** The PDF page index differs from the printed page
   number (front matter, inserts). Read one body page, compare its printed number to the
   index you requested, and record `PDF_index = printed + offset`. **Watch for duplicated
   scan pages** mid-book — the offset can jump by one or two partway through; re-derive it at
   each chapter start and allow a ±2 tolerance.
3. **Vision-read only the mapped ranges,** in chunks of ≤20 pages per Read call, and distill.

This two-step (locate → vision-read targeted ranges) is the difference between a feasible
read and an impossible one.

## Foreign-language sources

If a source is not in English, the subagent translates key definitions, statements, and the
structure of arguments into English while **keeping the original section/theorem numbers**
for cross-reference. Flag any passage where the translation is uncertain rather than
guessing.

## The extraction subagent brief

Give each extraction subagent: the source path, what to extract, where to write, and the
**err-on-the-side-of-more** instruction. A good brief asks for, with precise section/page
refs throughout:

- every relevant definition, with the source's own numbering;
- every theorem/lemma/proposition statement (a one-line restatement is fine), by number;
- the key tables and computations, transcribed (verify these from the page image, not
  garbled text);
- proof *spines* of the load-bearing results — the engine, not every step;
- a notation key, and notes on where this source is cleaner / more general than the others.

Tell it to write GitHub-flavored markdown with LaTeX math in `$...$`, to flag illegible or
uncertain spots with an inline `[CHECK]` marker rather than inventing content, and to reply
with only a short status (path, word count, concerns) — not the digest itself (it is in the
file).

## Review each digest (a gate, not a formality)

After each digest lands, dispatch a reviewer subagent (or check yourself) for **coverage**
(did it capture every required element?) and **internal consistency** (do the table values,
the prose, and the stated conventions agree?). Two failure modes recur and are worth
checking explicitly:

- **Convention slips.** A table whose values contradict its column headers, or a
  correspondence stated backwards. When sources use different sign/index conventions,
  **verify the convention against the page image** before trusting either the prose or a
  reviewer's inference — both can be wrong.
- **Over-confident claims on illegible content.** Confirm that uncertain spots are marked
  `[CHECK]`, not asserted.

Fix flagged issues with a targeted fix subagent before moving on. The digests feed
everything downstream; an error here propagates into the guide.

## Then: the synthesis note

Once all digests pass review, one more subagent reads them against the concept spine and
writes `source-notes/synthesis.md` (Phase B): the spine-to-source map, the single unified
notation/convention table, and the gaps list. This is the document the chapter authors lean
on most — it is where the multiple sources become one coherent throughline.
