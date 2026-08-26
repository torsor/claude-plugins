# The markup contract

`assets/agentic-edits.tex` is `\input` from the preamble of your working copy. Copy it in
beside the paper; do not rewrite it.

## Which build is which

The toggle is **not** a line you edit. It comes from the command line:

```
pdflatex -jobname <paper>-repaired-notes  <paper>-repaired.tex
pdflatex -jobname <paper>-repaired-clean  "\def\agenticclean{}\input{<paper>-repaired}"
```

Notes-on is the default deliberately: a file of unmarked edits that reads as the authors' own
text is the dangerous artifact, so the clean build has to be asked for.

## Three states

| State | Notes build | Clean build |
|---|---|---|
| **applied** | struck-out red original, blue replacement | replacement silently in place |
| **proposed** | purple, labelled, replacement text shown in position | **absent** — it was not adopted |
| **removed** | framed and greyed, labelled | gone |

```latex
\agenticaddition[M-5]{text}        \agenticremoval[M-5]{text}
\agenticremovalbox[M-5]{text}      % fragile tokens: \cite, \ref, \label
\agenticproposal[M-5]{replacement} % worked out, not adopted
\agenticmathadd[M-5]{t}  \agenticmathdel[M-5]{t}   % inside an existing display
\agenticitem[M-5]{text}            % a whole new list item
\agenticnote{why this change}      % one line, footnoted

\begin{agenticadded}[M-5]    … \end{agenticadded}
\begin{agenticremoved}[M-5]  … \end{agenticremoved}
\begin{agenticproposed}[M-5] … \end{agenticproposed}
```

**Inline commands cannot carry display math, theorem environments, or anything crossing a
paragraph.** Use the environments for those. Always carry the issue tag; every change gets an
`\agenticnote` saying why, because an unexplained diff is not a repair.

## Rules that came out of real use

**Never duplicate a display to show a change inside it.** `\agenticmathdel`/`\agenticmathadd`
work *within* the existing display. Showing a one-glyph fix as two whole displays is the
failure this replaced.

**Box the fragile token and nothing else, and hang the tag off the last piece.** `\sout`
refuses `\cite`; `\mbox` fixes that but makes its argument unbreakable. Measured on a real
paper: boxing the citation together with its surrounding words took a paragraph's overfull box
from 14.0pt to 47.5pt; boxing only the `\cite` gave 24.8pt, because the tag then sat mid-phrase
and forced a break there; boxing only the `\cite` and putting the tag on the trailing plain
`\agenticremoval` returned it to 14.0pt, the original.

**A proposal must not consume a number.** Counters are frozen across `agenticproposed`, so it
cannot. If the proposal restates a numbered result, step the counter inside the block so it
prints the number it replaces — and prefer `\addtocounter{thm}{-1}` to `\setcounter`, since a
paper numbering by section has no literal `16` anywhere in its source to set.

**`\label` is disabled inside a proposal.** A label defined there resolves in the notes build
and prints `??` in the clean build, where the proposal is not present to define it. That makes
the clean build wrong, not merely untidy.

## Known limits

- **A proposal cannot add a bibliography entry.** A `\bibitem` inside the block is discarded in
  the clean build; outside it, it leaks into a build that never proposed it. Cite such a source
  as plain text in the proposal and flag it in the log.
- **A tag inside math is boxed**, so it cannot break across lines.
- Verified against `amsart` and `elsarticle`, including `mdframed` around theorem environments
  inside and outside lists, class-defined theorem environments sharing a counter, and `\cancel`
  in displays. Another class may differ; find out on a trivial change, not a deep one.
