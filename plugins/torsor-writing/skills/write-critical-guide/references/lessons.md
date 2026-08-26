# Toolchain lessons — critical guides

**Read the family lessons first**: `${CLAUDE_PLUGIN_ROOT}/assets/commons/lessons.md` carries
the gotchas every torsor document hits, and
`${CLAUDE_PLUGIN_ROOT}/assets/commons/publication.md` carries the verification pass and its
evidence-report discipline. Both apply here unchanged, including the one that matters most —
`latexd` and `make` exit 0 on a failed LaTeX run, so a build is verified, never assumed.

This file carries only what is specific to a critical guide: annotating a source you did not
write, and assembling a typeset document out of Markdown that quotes LaTeX.

---

## Annotating someone else's LaTeX

`annotate_tex.py` already handles the first four of these; they are recorded so that placing a
note by hand, or debugging a build, does not mean rediscovering them.

**`\listoftodos` aborts the build under amsart with hyperref.** It feeds todo captions to
`\pdfstringdef`, which cannot make a PDF string out of math or macros, and the run dies with
an error naming neither todonotes nor the caption. An inline index of the file's own notes,
emitted after `\maketitle`, replaces it — and is more useful, since it prints in the PDF
rather than living only in the navigation pane.

**TeX in a caption breaks hyperref even without `\listoftodos`.** Captions are sanitized to
plain ASCII. Where a paper's notation survives sanitizing as noise, add its macros to
`caption_symbols:` in the ledger.

**A note dropped after its anchor line can land inside math.** Real sources let `$...$` and
displays straddle line breaks, and the result is `! Missing $ inserted` pointing at a line you
did not write. Insertion points advance to the next position outside all math and verbatim.

**A stale `.tdo` resurfaces as a phantom error.** After a failed run the next one reads back
the old todo file and fails in a way unrelated to what you just changed. Clear aux files
before rebuilding (`--clean-aux`). When a build fails inexplicably right after a fix, suspect
this first.

**The paper may not load todonotes at all.** The package is inserted before `\begin{document}`
when absent, and only its options are replaced when present. Nothing else in the source is
touched — that is the promise the annotated file's header note makes to the authors, and it
must stay true.

**A `%` or `#` inside a quoted macro comments out the note.** An issue whose text quotes
`` `100%` `` or `` `\#1` `` reaches LaTeX unescaped, and everything after it on that line
disappears — including the closing brace of the note, so the error surfaces somewhere else
entirely. Code spans are escaped character by character, not passed through.

**A quoted macro is one unbreakable box.** `` `\Cref{lem: compat flat smooth cov}` `` set as
plain `\texttt{}` cannot break, so in a narrow table cell it runs into the margin — and an
overfull hbox is a warning, not an error, so the log will not stop you. An `\allowbreak` after
each backslash and brace gives it somewhere to break.

**Escape explicitly rather than with `\detokenize`.** Detokenize looks like the right tool for
setting a quoted macro verbatim, but it inserts a space after every control sequence, so the
macro comes back with visible gaps in it.

**`\\` followed by `[` is a length argument.** A note or a bundled tag that begins with `[`
turns `\\[M-1]` into `\\` with an optional vertical skip of `M-1`, which is not a length.
Separate parts of a note with `\par`, or write `\\{}` if you must use `\\`.

**pdflatex does not promise UTF-8.** Its console output and log can carry bytes in the source
file's own encoding. Read them with `errors="replace"`; a `UnicodeDecodeError` while *checking*
a build is an unusually annoying way to fail.

**Missing figures or class files are not yours to fix.** If the source needs something the
arXiv tarball did not carry, note it and let the build proceed with the placeholder. Do not
edit the authors' source to make it compile more prettily.

---

## Building the guide PDF with pandoc

**Bare LaTeX macros outside math must be in backticks.** A `\Cref{...}` quoted from the paper,
sitting in Markdown prose, goes straight to an engine that has never heard of it. Write
`` `\Cref{lem: compat flat smooth cov}` `` and it sets as code and survives. This is the
commonest way the report build breaks, because quoting the paper's macros is exactly what an
issue list does.

**Use `pdflatex`, not `lualatex`.** An order of magnitude faster here, and it handles every
non-ASCII character a critical guide actually uses; `lualatex` with font specifications is
slow enough on a long issue list to look like a hang. If you switch engines, drop the
`mainfont` / `sansfont` / `monofont` metadata keys with it — they are XeTeX and LuaTeX only.

**Long tables need `longtable` with repeating headers, and `\RaggedRight`.** An issue list's
typographical tables run past a page, and their "suggested wording" cells are long. Without
both, the table is silently truncated or overflows the margin, and the log says nothing.

**Do not repeat the title as a heading.** `guide-meta.yaml` carries it; a `# Title` at the
top of `01-summary.md` prints it twice.

---

## Case B — a PDF submission with a public source

**Check every annotated passage against the submission before placing the note.** The same
statement, formula, or reference must occur in both. A note about a sentence the authors have
already fixed is worse than no note.

**Keep the two location systems separate and say which is which.** Page and line numbers in
the Markdown refer to the submitted PDF; the inline notes follow the public source, which is
what a revising author edits. State this in the README, along with where the two versions
differ.

**Watch for a cover sheet.** Editorial Manager and similar prepend one, so the printed page
number and the PDF page number differ by one. Say which you used.
