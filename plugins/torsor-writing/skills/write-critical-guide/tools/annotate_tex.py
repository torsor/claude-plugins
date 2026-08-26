#!/usr/bin/env python3
r"""annotate_tex — build referee artifacts from a single issue ledger.

One ledger (``issues.yaml``) is the source of truth for a critical-guide package. From it
this tool generates, and keeps in step:

  * one annotated copy of the paper's own source per issue category, with each note
    inserted as a ``\todo[inline]`` at the passage it concerns;
  * the point-by-point issue list in Markdown.

The generation direction matters. Hand-maintaining the prose list and the annotation
anchors in parallel is what lets them drift, and a referee note pointing at the wrong
passage is worse than no note at all. Here an anchor that no longer matches its source
is a hard error, not a silent mismatch.

Subcommands
-----------
  check      verify every anchor against the annotation base; write nothing
  annotate   write one annotated .tex per category
  issues-md  write the point-by-point Markdown issue list
  build      compile each annotated .tex and verify the result
  all        check, annotate, issues-md, build

Seven LaTeX hazards are handled here so no individual review has to rediscover them:

1. ``\listoftodos`` derails ``\pdfstringdef`` under amsart+hyperref and aborts the
   build. An inline index of the file's own notes is emitted after ``\maketitle``
   instead.
2. Inline math and displays straddle line breaks in real sources, so a note dropped
   immediately after its anchor line can land inside ``$...$``. Insertion points are
   advanced to the next position outside all math.
3. TeX inside a ``\todo`` caption reaches hyperref as a PDF string and breaks it.
   Captions are reduced to plain ASCII prose.
4. Stale ``.tdo``/aux files from a failed run resurface as phantom errors on the next
   one. ``--clean-aux`` removes them alongside the outputs.
5. A ``%`` or ``#`` inside a quoted code span reaches LaTeX unescaped and comments out
   the rest of the note. Code spans are escaped character by character.
6. A quoted macro is one unbreakable box and overflows a narrow table cell with nothing
   in the log to say so. ``\allowbreak`` after each backslash and brace gives it
   somewhere to break.
7. pdflatex and pdfinfo emit bytes that are not valid UTF-8. Every read of their output
   replaces rather than raises.

``build`` exists because a single pdflatex pass leaves every cross-reference reading
``??``, and because both ``latexd`` and ``make`` exit 0 on a failed LaTeX run. It runs
the sequence that converges and then checks the log and the note count rather than
trusting the exit status.
"""

from __future__ import annotations

import argparse
import os
import re
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("annotate_tex needs PyYAML:  python3 -m pip install pyyaml")


# ----------------------------------------------------------------------
# ledger
# ----------------------------------------------------------------------

GRADES = ("major", "minor", "trivial")


class LedgerError(Exception):
    """A problem with issues.yaml that the reviewer must fix by hand."""


def load_ledger(path):
    with open(path, encoding="utf-8") as f:
        led = yaml.safe_load(f)
    if not isinstance(led, dict):
        raise LedgerError("%s: top level must be a mapping" % path)

    base = os.path.dirname(os.path.abspath(path))
    paper = led.setdefault("paper", {})
    src = paper.get("source")
    if not src:
        raise LedgerError("%s: paper.source (the annotation base .tex) is required" % path)
    paper["source_abs"] = os.path.normpath(os.path.join(base, src))

    cats = led.get("categories")
    if not cats:
        raise LedgerError("%s: at least one entry under categories is required" % path)

    seen = {}
    for n, iss in enumerate(led.get("issues") or [], 1):
        where = "issue #%d" % n
        for field in ("id", "category", "anchor", "note"):
            if not iss.get(field):
                raise LedgerError("%s: %s is required" % (where, field))
        if iss["id"] in seen:
            raise LedgerError("duplicate issue id %r" % iss["id"])
        seen[iss["id"]] = iss
        if iss["category"] not in cats:
            raise LedgerError("%s (%s): unknown category %r; known: %s"
                              % (where, iss["id"], iss["category"], ", ".join(sorted(cats))))
        grade = iss.setdefault("grade", "minor")
        if grade not in GRADES:
            raise LedgerError("%s (%s): grade %r must be one of %s"
                              % (where, iss["id"], grade, ", ".join(GRADES)))

    # dependencies must resolve, and must not be self-referential
    for iss in led.get("issues") or []:
        for dep in iss.get("depends_on") or []:
            if dep == iss["id"]:
                raise LedgerError("%s depends on itself" % iss["id"])
            if dep not in seen:
                raise LedgerError("%s depends on unknown issue %r" % (iss["id"], dep))
    return led


def issues_in(led, category):
    out = [i for i in (led.get("issues") or []) if i["category"] == category]
    return sorted(out, key=sort_key)


def sort_key(iss):
    """Order by the numeric part of the id, so M-2 precedes M-10."""
    m = re.search(r"(\d+)\s*$", iss["id"])
    return (int(m.group(1)) if m else 0, iss["id"])


# ----------------------------------------------------------------------
# caption sanitising  (hazard 3)
# ----------------------------------------------------------------------

# Macro names that carry meaning worth keeping in a plain-text caption. Anything
# else is dropped to its argument. Extend per paper via `caption_symbols:`.
DEFAULT_SYMBOLS = {
    "alpha": "alpha", "beta": "beta", "gamma": "gamma", "delta": "delta",
    "epsilon": "epsilon", "kappa": "kappa", "lambda": "lambda", "mu": "mu",
    "phi": "phi", "pi": "pi", "rho": "rho", "sigma": "sigma", "tau": "tau",
    "Gamma": "Gamma", "Delta": "Delta", "Lambda": "Lambda", "Sigma": "Sigma",
    "Omega": "Omega", "otimes": "tensor", "oplus": "+", "to": "->",
    "colon": ":", "times": "x", "cap": "and", "cup": "or", "subseteq": "in",
    "ge": ">=", "le": "<=", "neq": "!=", "cong": "=", "simeq": "=",
}


def clean_caption(text, symbols=None):
    r"""Reduce a caption to plain ASCII prose.

    Captions reach hyperref as PDF strings, which cannot carry math or macros.
    """
    table = dict(DEFAULT_SYMBOLS)
    table.update(symbols or {})

    def unmath(mo):
        inner = mo.group(1)
        inner = re.sub(r"\\([a-zA-Z]+)",
                       lambda m: table.get(m.group(1), m.group(1)), inner)
        return inner

    text = re.sub(r"\$([^$]*)\$", unmath, text)
    # unwrap one level of the common text-styling macros, keeping the argument
    for _ in range(3):
        text = re.sub(r"\\(?:texttt|textit|textbf|textrm|textsf|emph|mathrm|mathcal"
                      r"|mathbf|operatorname)\{([^{}]*)\}", r"\1", text)
    text = (text.replace(r"\textbackslash", "")
                .replace(r"\^{}", "^")
                .replace(r"\_", " ")
                .replace(r"\ldots", "...")
                .replace(r"\dots", "...")
                .replace("``", "'").replace("''", "'")
                .replace("\u2014", " - ").replace("\u2013", "-")
                .replace("\u2018", "'").replace("\u2019", "'")
                .replace("\u201c", "'").replace("\u201d", "'"))
    text = re.sub(r"\\[a-zA-Z]+\s*", "", text)          # surviving macros
    text = text.translate(str.maketrans("", "", "\\{}$_^~#&%"))
    text = text.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", text).strip()


# ----------------------------------------------------------------------
# note bodies: one Markdown source, two targets
# ----------------------------------------------------------------------

# `note`, `request` and `quote` are authored as Markdown, because that is what the
# issue list is. The LaTeX path has to translate them, and getting this wrong is
# conspicuous: a straight " reaching LaTeX sets as a *closing* quote, so a note
# about the authors' punctuation prints with the wrong punctuation.

_MATH_SPAN = re.compile(r"(?<!\\)\$(?:[^$\\]|\\.)*\$")


_HOLD = "\x00%d\x00"


def to_latex(text):
    r"""Translate a Markdown note body to LaTeX, leaving ``$...$`` untouched.

    Math and code spans are lifted out before anything else runs, so a quotation
    that happens to contain math -- "reflexive as an $\mathcal{O}_X$-module" --
    still pairs as one quotation, and so the backticks this function *produces*
    are never mistaken for the code spans it consumes.
    """
    text = " ".join(str(text).split())
    held = []

    def hold(m):
        held.append(m.group(0))
        return _HOLD % (len(held) - 1)

    # code spans first: their content is verbatim, and they are written with the
    # same backtick this function later uses for an opening quote
    text = re.sub(r"`([^`]+)`", lambda m: hold_code(m, held), text)
    text = _MATH_SPAN.sub(hold, text)

    # paired quotation marks, on the whole string now that math cannot split a pair
    text = re.sub(r'"([^"]*)"', lambda m: "``%s''" % m.group(1), text)
    text = text.replace("\u201c", "``").replace("\u201d", "''")
    text = text.replace("\u2018", "`").replace("\u2019", "'")
    text = text.replace("\u2014", "---").replace("\u2013", "--")
    text = text.replace("\u2192", r"$\to$").replace("\u2026", r"\ldots{}")
    # Markdown emphasis
    text = re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\\emph{\1}", text)
    # characters LaTeX reserves, where the author meant them literally
    text = re.sub(r"(?<!\\)([&%#])", r"\\\1", text)
    text = re.sub(r"(?<![\\{])_", r"\\_", text)

    for i, original in enumerate(held):
        text = text.replace(_HOLD % i, original)
    return text


_TT = {
    "\\": r"\textbackslash{}\allowbreak{}",
    "{": r"\{\allowbreak{}", "}": r"\}\allowbreak{}",
    "$": r"\$", "&": r"\&", "%": r"\%", "#": r"\#", "_": r"\_",
    "^": r"\textasciicircum{}", "~": r"\textasciitilde{}",
}


def hold_code(m, held):
    r"""A Markdown code span becomes ``\texttt{}``, escaped character by character.

    Two things go wrong with the naive version. A `%` or `#` inside the span reaches
    LaTeX unescaped — `%` comments out the rest of the line, silently swallowing the
    note. And a quoted macro like ``\Cref{lem: compat flat smooth cov}`` is one
    unbreakable box, which overflows a narrow table cell with nothing in the log to
    say so; the ``\allowbreak`` after each backslash and brace gives it somewhere to
    break.

    Escaping explicitly rather than with ``\detokenize``: detokenize inserts a space
    after every control sequence, so a quoted macro comes back with visible gaps.
    """
    held.append(r"\texttt{%s}" % "".join(_TT.get(c, c) for c in m.group(1)))
    return _HOLD % (len(held) - 1)


def strip_markdown(text):
    """Plain prose, for contexts that take neither Markdown nor LaTeX."""
    text = " ".join(str(text).split())
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\1", text)
    return re.sub(r"`([^`]+)`", r"\1", text)


# ----------------------------------------------------------------------
# placement  (hazard 2)
# ----------------------------------------------------------------------

MATH_ENVS = ("equation", "align", "multline", "gather", "flalign", "alignat",
             "eqnarray", "cases", "aligned", "split", "array", "matrix",
             "pmatrix", "bmatrix", "vmatrix", "tikzcd", "displaymath", "dmath")

VERBATIM_ENVS = ("verbatim", "lstlisting", "minted", "Verbatim", "alltt")


def _delims(line):
    """Count math delimiters on a line, ignoring escaped and commented text.

    ``$$`` is reported separately rather than as one open and one close: a display
    split across lines opens on one line and closes on another, and counting it as
    both would cancel to zero and let an annotation land inside it.
    """
    line = re.sub(r"(?<!\\)%.*$", "", line)     # strip trailing comment
    line = line.replace(r"\$", "")              # escaped dollars are not delimiters
    doubles = line.count("$$")
    dollars = line.count("$") - 2 * doubles
    opens = line.count(r"\[") + line.count(r"\(")
    closes = line.count(r"\]") + line.count(r"\)")
    return dollars, opens, closes, doubles, line


def safe_line(lines, start):
    r"""Smallest index j >= start at whose end we sit outside all math and verbatim.

    Real sources let ``$...$`` and displays straddle line breaks; an annotation
    inserted straight after the anchor line otherwise lands inside the math and the
    build fails with an unhelpful "Missing $ inserted".
    """
    inline = False
    dispdd = False
    display = 0
    envs = 0
    verb = 0
    for j, raw in enumerate(lines):
        dollars, opens, closes, doubles, line = _delims(raw)
        inline ^= (dollars % 2 == 1)
        dispdd ^= (doubles % 2 == 1)
        display += opens - closes
        for e in MATH_ENVS:
            envs += line.count(r"\begin{%s}" % e) + line.count(r"\begin{%s*}" % e)
            envs -= line.count(r"\end{%s}" % e) + line.count(r"\end{%s*}" % e)
        for e in VERBATIM_ENVS:
            verb += line.count(r"\begin{%s}" % e) - line.count(r"\end{%s}" % e)
        if (j >= start and not inline and not dispdd
                and display <= 0 and envs <= 0 and verb <= 0):
            if r"\end{document}" in lines[j]:
                break
            return j
    raise LedgerError("no safe insertion point at or after source line %d" % (start + 1))


def find_anchor(lines, iss):
    """Locate the unique source line carrying this issue's anchor."""
    anchor = iss["anchor"]
    hits = [i for i, ln in enumerate(lines) if anchor in ln]
    if not hits:
        raise LedgerError(
            "%s: anchor not found in the source.\n    anchor: %r\n"
            "    The anchor must be a verbatim substring of one source line. Re-read the\n"
            "    source and copy the text exactly, including its macros."
            % (iss["id"], anchor))
    want = iss.get("occurrence")
    if len(hits) > 1 and want is None:
        raise LedgerError(
            "%s: anchor matches %d lines (%s).\n    anchor: %r\n"
            "    Lengthen the anchor until it is unique, or set `occurrence: N`."
            % (iss["id"], len(hits), ", ".join(str(h + 1) for h in hits), anchor))
    if want is not None:
        if not 1 <= want <= len(hits):
            raise LedgerError("%s: occurrence %d requested, %d match(es) present"
                              % (iss["id"], want, len(hits)))
        return hits[want - 1]
    return hits[0]


# ----------------------------------------------------------------------
# annotated source
# ----------------------------------------------------------------------

TODO_PKG = re.compile(r"\\usepackage(\[[^\]]*\])?\{todonotes\}")


def set_todonotes(lines, colour):
    """Load todonotes with this category's colour, replacing any existing load."""
    opts = ("[textsize=small, color=%s!12, bordercolor=%s!60, linecolor=%s!60]"
            % (colour, colour, colour))
    for i, ln in enumerate(lines):
        if TODO_PKG.search(ln):
            lines[i] = TODO_PKG.sub(r"\\usepackage%s{todonotes}" % opts.replace("\\", r"\\"), ln)
            return lines
    # not loaded by the paper: add it as late in the preamble as possible, since
    # todonotes wants to come after most packages and before hyperref's setup
    for i, ln in enumerate(lines):
        if r"\begin{document}" in ln:
            lines.insert(i, r"\usepackage%s{todonotes}" % opts)
            return lines
    raise LedgerError(r"no \begin{document} found; is this a complete LaTeX source?")


def build_annotated(lines, led, cat_key):
    cat = led["categories"][cat_key]
    symbols = led.get("caption_symbols")
    lines = set_todonotes(list(lines), cat.get("colour", "gray"))

    issues = issues_in(led, cat_key)
    if not issues:
        raise LedgerError("category %r has no issues" % cat_key)

    bundled = bundled_into(led)
    placed = []
    for iss in issues:
        if iss["id"] in bundled:
            continue                      # carried in its host's box, not its own
        at = find_anchor(lines, iss)
        at = safe_line(lines, at)
        indent = lines[at][:len(lines[at]) - len(lines[at].lstrip())]
        caption = clean_caption(iss.get("caption") or iss.get("location") or iss["id"],
                                symbols)
        placed.append((at + 1, "%s\\todo[inline, caption={[%s] %s}]{%s}"
                               % (indent, iss["id"], caption, note_body(iss, led))))

    for at, note in sorted(placed, reverse=True):
        lines.insert(at, note)

    return insert_header(lines, led, cat_key, issues, symbols)


def note_body(iss, led, lead=True):
    r"""The text of one inline note, including any issues bundled into it.

    Parts are joined with a space and separated with ``\par``, never with ``\\``:
    ``\\`` followed by ``[`` is read as ``\\[<vertical skip>]``, so a note or a
    bundled tag beginning with ``[`` would be swallowed as a length argument.
    """
    parts = []
    if lead:
        parts.append(r"\textbf{[%s]} (\emph{%s})" % (iss["id"], grade_label(iss)))
    parts.append(to_latex(iss["note"]))
    if iss.get("request"):
        parts.append(r"\emph{Requested:} " + to_latex(iss["request"]))
    for other in bundled_issues(iss, led):
        parts.append(r"\smallskip\par\textbf{[%s]} (\emph{%s})"
                     % (other["id"], grade_label(other)))
        parts.append(to_latex(other["note"]))
        if other.get("request"):
            parts.append(r"\emph{Requested:} " + to_latex(other["request"]))
    return " ".join(parts)


def grade_label(iss):
    """The grade, plus the qualifier where the reviewer's judgment needs one."""
    if iss.get("grade_note"):
        return "%s, %s" % (iss["grade"], strip_markdown(iss["grade_note"]))
    return iss["grade"]


def bundled_issues(iss, led):
    """Issues this one carries in its box: two adjacent nits belong in one note."""
    by_id = {i["id"]: i for i in (led.get("issues") or [])}
    return [by_id[i] for i in (iss.get("also") or []) if i in by_id]


def bundled_into(led):
    """Every id that is carried in another issue's box rather than its own."""
    out = set()
    for iss in led.get("issues") or []:
        out.update(iss.get("also") or [])
    return out


def insert_header(lines, led, cat_key, issues, symbols):
    r"""Insert the file's own index of notes after \maketitle.

    Deliberately not ``\listoftodos``: under amsart with hyperref it derails
    ``\pdfstringdef`` and aborts the build.
    """
    cat = led["categories"][cat_key]
    title = cat.get("title", cat_key)
    blurb = " ".join(str(cat.get("blurb", "")).split())
    ledger_name = led.get("issue_list_name", "02-issues.md")

    index = [r"  \begin{itemize}\itemsep0pt"]
    for iss in issues:
        cap = clean_caption(iss.get("caption") or iss.get("location") or "", symbols)
        index.append(r"  \item \textbf{[%s]} (\emph{%s}) %s"
                     % (iss["id"], clean_caption(grade_label(iss), symbols), cap))
    index.append(r"  \end{itemize}")

    n_auth = len(led["paper"].get("authors") or [])
    whose = "author's" if n_auth == 1 else "authors'"

    header = ([
        "",
        r"\todo[inline, caption={Critical annotations: %s}]{\textbf{Critical annotations --- %s.}"
        % (clean_caption(title, symbols), clean_caption(title, symbols)),
        "  %s" % to_latex(blurb) if blurb else "",
        r"  Tags match the accompanying \texttt{%s}, which carries the full discussion." % ledger_name,
        "  This file is the %s own source with annotations added; nothing else has" % whose,
        "  been altered. Notes in this file, in order of tag:",
    ] + index + ["}", r"\clearpage", ""])

    hits = [i for i, ln in enumerate(lines)
            if r"\maketitle" in re.sub(r"(?<!\\)%.*$", "", ln)]
    if len(hits) > 1:
        raise LedgerError(r"\maketitle occurs %d times; cannot place the header note"
                          % len(hits))
    if hits:
        at = hits[0] + 1
    else:
        starts = [i for i, ln in enumerate(lines) if r"\begin{document}" in ln]
        if not starts:
            raise LedgerError(r"neither \maketitle nor \begin{document} found")
        at = starts[0] + 1

    for k, ln in enumerate(header):
        lines.insert(at + k, ln)
    return "\n".join(lines)


# ----------------------------------------------------------------------
# markdown issue list
# ----------------------------------------------------------------------

def render_issues_md(led):
    paper = led["paper"]
    out = []
    add = out.append

    add("# Detailed comments")
    add("")
    ident = paper.get("identifier", "")
    locbase = paper.get("locations_refer_to")
    intro = []
    if ident:
        intro.append("%s." % ident)
    if locbase:
        intro.append("Locations refer to %s;" % locbase)
        intro.append("section, statement and equation numbers are the paper's own.")
    if intro:
        add(" ".join(intro))
        add("")

    tags = ", ".join("**[%s]** %s" % (c.get("tag", k[:1].upper()), c.get("title", k).lower())
                     for k, c in led["categories"].items())
    add("Items are tagged %s, and graded:" % tags)
    add("")
    add("- **major** --- affects correctness, or a reader cannot follow without "
        "reconstructing the argument")
    add("- **minor** --- should be fixed, but the reader gets there")
    add("- **trivial** --- copy-editing")
    add("")

    if any(i.get("depends_on") for i in (led.get("issues") or [])):
        add("An item marked *depends on [X]* is not an independent defect: it records a "
            "place whose stated argument rests on [X], and its status follows from how [X] "
            "is resolved.")
        add("")

    if any(i.get("confidence") for i in (led.get("issues") or [])):
        add("Where a finding rests on something other than a check I carried out in full, "
            "the basis is stated with it; unmarked findings are direct checks.")
        add("")

    companions = [c["output"] for c in led["categories"].values()
                  if c.get("output") and issues_in(led, cat_key_of(led, c))]
    if len(companions) > 1:
        add("Companion files carry the same items as `\\todo[inline]` annotations placed in "
            "the text: %s." % ", ".join("`%s`" % c for c in companions))
        add("")

    add("---")

    letters = "ABCDEFGH"
    for n, (key, cat) in enumerate(led["categories"].items()):
        issues = issues_in(led, key)
        if not issues:
            continue
        if n:
            add("")
            add("---")
        add("")
        add("## %s. %s" % (letters[n], cat.get("title", key)))
        add("")
        if cat.get("preamble"):
            add(" ".join(str(cat["preamble"]).split()))
            add("")
        for s, (spec, group) in enumerate(group_by_section(issues, cat), 1):
            if spec:
                add("### %s.%d %s" % (letters[n], s, spec["name"]))
                add("")
            if spec and spec.get("render") == "table":
                add(render_section_table(spec, group))
                add("")
            else:
                for iss in group:
                    add(render_issue(iss))
                    add("")
        # the clean-checks table belongs with the category it concerns
        if cat.get("clean_checks"):
            clean = render_clean_checks(led, nested=True)
            if clean:
                add(clean)
                add("")

    dep = render_dependency_map(led)
    if dep:
        add(dep)

    if not any(c.get("clean_checks") for c in led["categories"].values()):
        clean = render_clean_checks(led)
        if clean:
            add(clean)

    if led.get("scope_caveat"):
        add("")
        add("---")
        add("")
        add("## Scope of this report")
        add("")
        add(" ".join(str(led["scope_caveat"]).split()))

    return "\n".join(out).rstrip() + "\n"


DEFAULT_COLUMNS = [
    {"header": "#", "field": "id"},
    {"header": "Location", "field": "location"},
    {"header": "The paper writes", "field": "quote"},
    {"header": "Suggested", "field": "request"},
]


def normalise_section(spec):
    """A section is either a bare name or a mapping carrying its rendering."""
    if isinstance(spec, str):
        return {"name": spec, "render": "prose"}
    spec = dict(spec)
    spec.setdefault("render", "prose")
    if spec["render"] == "table":
        spec.setdefault("columns", DEFAULT_COLUMNS)
    return spec


def group_by_section(issues, cat):
    """Group into the category's declared thematic sections, preserving their order."""
    order = [normalise_section(s) for s in (cat.get("sections") or [])]
    if not order:
        return [(None, issues)]
    groups, seen = [], set()
    for spec in order:
        members = [i for i in issues if i.get("section") == spec["name"]]
        if members:
            groups.append((spec, members))
            seen.update(id(i) for i in members)
    rest = [i for i in issues if id(i) not in seen]
    if rest:
        # Silent bucketing is the drift this tool exists to prevent: say so.
        sys.stderr.write(
            "  note: %d issue(s) name no section and fall to %r: %s\n"
            % (len(rest), cat.get("sections_other", "Further items"),
               ", ".join(i["id"] for i in rest)))
        groups.append(({"name": cat.get("sections_other", "Further items"),
                        "render": "prose"}, rest))
    return groups


def cell(iss, field):
    """One table cell: collapsed to a line, with pipes escaped so the row survives."""
    val = iss.get(field)
    if field == "id":
        val = "[%s]" % iss["id"]
    if val is None:
        return ""
    text = " ".join(str(val).split())
    return text.replace("|", r"\|")


def render_section_table(spec, issues):
    """Bulk copy-editing as a table.

    Thirty one-line usage corrections set as thirty paragraphs is far worse to read,
    and to work through, than one three-column table. An issue inside a table section
    that carries real consequence can set `render: prose` and is lifted out below it.
    """
    cols = [dict(c) for c in spec.get("columns", DEFAULT_COLUMNS)]
    tabular = [i for i in issues if i.get("render", "table") != "prose"]
    lifted = [i for i in issues if i.get("render") == "prose"]

    out = []
    if tabular:
        out.append("| " + " | ".join(c["header"] for c in cols) + " |")
        out.append("|" + "|".join("---" for _ in cols) + "|")
        for iss in tabular:
            out.append("| " + " | ".join(cell(iss, c["field"]) for c in cols) + " |")
    for iss in lifted:
        out.append("")
        out.append(render_issue(iss))
    return "\n".join(out)


def cat_key_of(led, cat):
    for k, c in led["categories"].items():
        if c is cat:
            return k
    return None


def render_issue(iss):
    head = "**[%s]" % iss["id"]
    if iss.get("location"):
        head += " %s." % iss["location"]
    head += " *%s.*" % grade_label(iss)
    if iss.get("depends_on"):
        head += " *Depends on %s.*" % ", ".join("[%s]" % d for d in iss["depends_on"])
    head += "**"

    # The quotation runs on from the heading, as it does in a hand-written report:
    # the paper's own words are what identify the passage, not a block of their own.
    if iss.get("quote"):
        head += ' "%s"' % " ".join(str(iss["quote"]).split())

    parts = [head, str(iss["note"]).strip()]
    if iss.get("request"):
        parts.append("*Requested:* %s" % " ".join(str(iss["request"]).split()))
    # A direct check is the expectation, stated once in the preamble; only a weaker
    # basis is worth repeating per item.
    if iss.get("confidence") and iss["confidence"] != "direct-check":
        parts.append("*Basis:* %s" % CONFIDENCE.get(iss["confidence"], iss["confidence"]))
    return "\n\n".join(parts)


CONFIDENCE = {
    "direct-check": "a direct check, carried out in full.",
    "assessment": "a feasibility assessment; the route looks viable but has not "
                  "been written out.",
    "reported": "reported from the source, not independently re-derived.",
}


def render_dependency_map(led):
    edges = [(i["id"], d) for i in (led.get("issues") or [])
             for d in (i.get("depends_on") or [])]
    if not edges:
        return ""
    out = ["", "---", "", "## Dependency map", "",
           "These items are consequences rather than independent defects. Resolving the "
           "item on the right settles the one on the left.", "",
           "| Item | Rests on |", "|---|---|"]
    for child, parent in sorted(edges):
        out.append("| [%s] | [%s] |" % (child, parent))
    return "\n".join(out)


def render_clean_checks(led, nested=False):
    rows = led.get("verified_clean") or []
    if not rows:
        return ""
    heading = ("### Checks that came out clean" if nested
               else "## Checks that came out clean")
    out = ([""] if nested else ["", "---", ""]) + [heading, "",
           "Recorded so the report says what was examined, not only what was found "
           "wanting. Each of the following says what the paper uses it for, with "
           "hypotheses satisfied at the point of use.", "",
           "| Source | Statement | Used for |", "|---|---|---|"]
    for r in rows:
        out.append("| %s | %s | %s |" % (r.get("source", ""), r.get("statement", ""),
                                         r.get("used_for", "")))
    if led.get("not_verified"):
        out += ["", " ".join(str(led["not_verified"]).split())]
    return "\n".join(out)


# ----------------------------------------------------------------------
# driver
# ----------------------------------------------------------------------

def read_source(led):
    path = led["paper"]["source_abs"]
    if not os.path.exists(path):
        raise LedgerError("annotation base not found: %s" % path)
    with open(path, encoding="utf-8") as f:
        return f.read().split("\n")


def cmd_check(led, args):
    lines = read_source(led)
    n = 0
    for iss in sorted(led.get("issues") or [], key=sort_key):
        at = find_anchor(lines, iss)
        safe_line(lines, at)
        n += 1
        if args.verbose:
            print("  %-8s line %-5d %s" % (iss["id"], at + 1, iss["anchor"][:56]))
    print("checked %d anchors against %s — all unique and placeable"
          % (n, os.path.basename(led["paper"]["source_abs"])))
    return 0


def cmd_annotate(led, args):
    lines = read_source(led)
    for key, cat in led["categories"].items():
        if not issues_in(led, key):
            print("  (skipping %s: no issues)" % key)
            continue
        name = cat.get("output", "annotated-%s.tex" % key)
        text = build_annotated(lines, led, key)
        path = os.path.join(args.outdir, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        print("wrote %s — %d notes" % (name, len(issues_in(led, key))))
    return 0


def cmd_issues_md(led, args):
    name = led.get("issue_list_name", "02-issues.md")
    path = os.path.join(args.outdir, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(render_issues_md(led))
    print("wrote %s — %d issues" % (name, len(led.get("issues") or [])))
    return 0


def cmd_build(led, args):
    r"""Compile each annotated source properly, and refuse to call ``??`` a success.

    One pdflatex pass leaves every cross-reference unresolved, which is how a
    critical-guide package ends up shipping a paper whose own theorem numbers read ``??``.
    Three passes with bibtex between is the sequence that actually converges, and
    the log is then checked rather than trusted.
    """
    import subprocess

    ok = True
    for cat in led["categories"].values():
        name = cat.get("output")
        if not name or not issues_in(led, cat_key_of(led, cat)):
            continue
        stem = os.path.splitext(name)[0]
        tex = os.path.join(args.outdir, name)
        if not os.path.exists(tex):
            print("  %-30s no .tex — run `annotate` first" % stem)
            ok = False
            continue

        log = os.path.join(args.outdir, stem + ".build.log")
        with open(log, "w", encoding="utf-8") as lf:
            for step in (("pdflatex",), ("bibtex",), ("pdflatex",), ("pdflatex",)):
                cmd = ([step[0], "-interaction=nonstopmode", name]
                       if step[0] == "pdflatex" else [step[0], stem])
                try:
                    subprocess.run(cmd, cwd=args.outdir, stdout=lf, stderr=lf,
                                   timeout=300, check=False)
                except FileNotFoundError:
                    if step[0] == "bibtex":
                        continue        # no bibtex installed; papers without one are fine
                    print("  %s: %s not found" % (stem, step[0]))
                    ok = False
                    break
                except subprocess.TimeoutExpired:
                    print("  %s: %s timed out" % (stem, step[0]))
                    ok = False
                    break

        ok = report_build(args.outdir, stem, tex, led) and ok

    return 0 if ok else 1


def report_build(outdir, stem, tex, led):
    """Verify the PDF rather than trusting the exit status, which lies."""
    pdf = os.path.join(outdir, stem + ".pdf")
    logf = os.path.join(outdir, stem + ".log")
    problems = []

    if not os.path.exists(pdf):
        print("  %-30s FAILED — no PDF" % stem)
        return False
    if os.path.getmtime(pdf) < os.path.getmtime(tex):
        problems.append("PDF older than its source")

    if os.path.exists(logf):
        with open(logf, encoding="utf-8", errors="replace") as f:
            text = f.read()
        undef = len(re.findall(r"Reference `[^']*' on page \d+ undefined", text))
        if undef:
            problems.append("%d undefined reference(s) — the run did not converge" % undef)
        if re.search(r"^! ", text, re.M):
            problems.append("LaTeX reported an error")

    # every note the ledger assigns here must actually be in the file
    cat = next(c for c in led["categories"].values()
               if os.path.splitext(c.get("output", ""))[0] == stem)
    want = len([i for i in issues_in(led, cat_key_of(led, cat))
                if i["id"] not in bundled_into(led)])
    with open(tex, encoding="utf-8") as f:
        got = f.read().count(r"\todo[inline")
    if got != want + 1:                 # +1 for the header note
        problems.append("%d note boxes, expected %d" % (got, want + 1))

    pages = ""
    try:
        import subprocess
        out = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True,
                             errors="replace", timeout=30)
        m = re.search(r"^Pages:\s+(\d+)", out.stdout, re.M)
        pages = "%s pages, " % m.group(1) if m else ""
    except Exception:
        pass

    if problems:
        print("  %-30s PROBLEM — %s" % (stem, "; ".join(problems)))
        return False
    print("  %-30s ok  (%s%d notes)" % (stem, pages, want + 1))
    return True


AUX = (".aux", ".log", ".out", ".toc", ".tdo", ".brf", ".fls", ".fdb_latexmk",
       ".blg", ".bbl", ".build.log")


def clean_aux(outdir):
    n = 0
    for f in os.listdir(outdir):
        if any(f.endswith(e) for e in AUX):
            os.remove(os.path.join(outdir, f))
            n += 1
    if n:
        print("removed %d stale build file(s)" % n)


def main(argv=None):
    p = argparse.ArgumentParser(prog="annotate_tex", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("command",
                   choices=("check", "annotate", "issues-md", "build", "all"))
    p.add_argument("-l", "--ledger", default="issues.yaml", help="path to issues.yaml")
    p.add_argument("-o", "--outdir", default=".", help="where to write outputs")
    p.add_argument("--clean-aux", action="store_true",
                   help="remove stale LaTeX build files first (see hazard 4)")
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args(argv)

    try:
        led = load_ledger(args.ledger)
        os.makedirs(args.outdir, exist_ok=True)
        if args.clean_aux:
            clean_aux(args.outdir)
        if args.command in ("check", "all"):
            cmd_check(led, args)
        if args.command in ("annotate", "all"):
            cmd_annotate(led, args)
        if args.command in ("issues-md", "all"):
            cmd_issues_md(led, args)
        if args.command in ("build", "all"):
            if cmd_build(led, args):
                sys.exit("annotate_tex: build did not come out clean (see above)")
    except LedgerError as e:
        sys.exit("annotate_tex: %s" % e)
    return 0


if __name__ == "__main__":
    sys.exit(main())
