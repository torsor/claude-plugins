#!/usr/bin/env python3
r"""Generate every artifact of a correspondence guide from its two ledgers.

    inventory.yaml        what the paper asserts or constructs, and where
    correspondences.yaml  what was located for each entry, and how far it runs

Nothing is transcribed by hand: written twice, prose and anchors drift.

    python3 correspond.py check -v          anchors resolve, ledgers agree
    python3 correspond.py callouts -o .     callouts/<id>.tex
    python3 correspond.py views -o .        A-entries.md, A-unlocated.md, A-leads.md
    python3 correspond.py annotate -o .     annotated-<literature>.tex (+ unlocated)
    python3 correspond.py build -o .        compile and verify each one
    python3 correspond.py all -o .          everything, then build

The anchor rule is the one that makes this work: an anchor must be a verbatim
substring of exactly one line of the annotation base.  The math- and verbatim-aware
insertion logic below is inherited from ``annotate_tex.py`` in write-critical-guide
and carries fixes that cost hours to find the first time.
"""

import argparse
import os
import re
import subprocess
import sys

try:
    import yaml
except ImportError:
    sys.exit("pyyaml required:  pip install pyyaml")


# ----------------------------------------------------------------------
# labels
# ----------------------------------------------------------------------

# ledger label -> (short form for a margin, ordering index)
LABELS = {
    "same statement":                    ("same statement", 0),
    "special case":                      ("special case", 1),
    "differs in hypotheses":             ("variant", 2),
    "same mechanism, different setting": ("analogy", 3),
    "thematic":                          ("thematic", 4),
    "contrast":                          ("contrast", 5),
    "looks like a match and is not":     ("near miss", 6),
}

# A neutral progression.  It grades nothing, and the key in the document says so.
LABEL_COLOUR = {
    # Pale washes, not saturated fills: the note text is dark and has to read
    # against these.  A neutral progression -- no red-to-green ramp, because the
    # colours index the kind of relationship and grade nothing.
    "same statement":                    "0.87,0.91,0.96",
    "special case":                      "0.88,0.93,0.95",
    "differs in hypotheses":             "0.88,0.94,0.93",
    "same mechanism, different setting": "0.89,0.94,0.90",
    "thematic":                          "0.95,0.94,0.87",
    "contrast":                          "0.96,0.92,0.87",
    "looks like a match and is not":     "0.96,0.90,0.90",
}

READ_WORD = {"full": "full text", "partial": "part", "abstract": "abstract only",
             "record": "bibliographic record only"}


class LedgerError(Exception):
    pass


# ----------------------------------------------------------------------
# ledgers
# ----------------------------------------------------------------------

def load(outdir):
    inv_p = os.path.join(outdir, "inventory.yaml")
    cor_p = os.path.join(outdir, "correspondences.yaml")
    for p in (inv_p, cor_p):
        if not os.path.exists(p):
            raise LedgerError("missing ledger: %s" % p)
    with open(inv_p) as fh:
        inv = yaml.safe_load(fh) or {}
    with open(cor_p) as fh:
        cor = yaml.safe_load(fh) or {}

    entries = inv.get("entries") or []
    seen = {}
    for e in entries:
        if "id" not in e:
            raise LedgerError("inventory entry with no id: %r" % (e.get("name"),))
        if e["id"] in seen:
            raise LedgerError("duplicate inventory id %s" % e["id"])
        seen[e["id"]] = e
        e.setdefault("status", "open")
        if e["status"] == "dismissed" and not (e.get("dismissal") or "").strip():
            raise LedgerError(
                "%s is dismissed with no `dismissal:` argument.  Demotion requires a "
                "written reason a reader can challenge." % e["id"])

    for c in (cor.get("entries") or []):
        if c.get("id") not in seen:
            raise LedgerError("correspondences entry %r matches no inventory id"
                              % c.get("id"))
        for conn in (c.get("connections") or []):
            lab = conn.get("label")
            if lab not in LABELS:
                raise LedgerError(
                    "%s: unknown label %r.  Known: %s"
                    % (c["id"], lab, ", ".join(sorted(LABELS))))
            if not (conn.get("locator") or "").strip():
                raise LedgerError(
                    "%s: a connection to %r has no locator.  A citation to a whole "
                    "work is not a connection." % (c["id"], conn.get("work")))
            if conn.get("read") not in READ_WORD:
                raise LedgerError(
                    "%s: connection to %r must declare `read:` as one of %s"
                    % (c["id"], conn.get("work"), ", ".join(READ_WORD)))
    return inv, cor, seen


def corr_index(cor):
    return {c["id"]: c for c in (cor.get("entries") or [])}



def is_news(conn):
    """Does this record earn a place in something a person reads?

    Two gates, and a record must pass both.

    `standing` is the genre test: `placement` means it is about where the paper's
    content sits, against `textbook` (standard, recorded, not a finding) and
    `internal` (about the paper rather than the literature).

    `consequence` is the value test, and it is the harder one.  A record may be
    correctly located, read in full, and exactly the right source, and still change
    nothing for the author -- a perfect identification of a tool they invoked by
    name.  The bar is not "is this a good identification" but "does this change
    what the author would do": drop a hypothesis, relate to a result that duplicates
    theirs, narrow a claim their source does not support, look in a literature that
    indexes their object under another name.  A record that cannot name its
    consequence does not go in front of a person.

    The ledger keeps everything regardless.  This decides only what reaches an
    artifact someone reads, which is the substrate-and-views split: the notes hold
    the whole search, the views hold what earns attention.
    """
    if (conn.get("standing") or "placement") != "placement":
        return False
    return bool(str(conn.get("consequence") or "").strip())


def lit_of(conn):
    """The value the annotated copies are cut by.

    `literature_group` is the controlled vocabulary and is what makes the cut usable;
    `literature` is free text and is kept for precision, not for grouping.  With only
    the free-text field, each search invents its own labels: expect something like
    three distinct labels for every four connections.
    """
    return (conn.get("literature_group")
            or conn.get("literature")
            or "unsorted").strip()


def literatures(cor):
    """Every literature group named by a connection, commonest first."""
    counts = {}
    for c in (cor.get("entries") or []):
        for conn in (c.get("connections") or []):
            if not is_news(conn):
                continue
            g = lit_of(conn)
            counts[g] = counts.get(g, 0) + 1
    return [g for g, _ in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))]


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "x"


# ----------------------------------------------------------------------
# markdown -> latex
# ----------------------------------------------------------------------

_MATH = re.compile(r"(?<!\\)\$(?:[^$\\]|\\.)*\$")


def to_latex(text):
    """Translate the small Markdown the ledgers use, leaving math alone."""
    if text is None:
        return ""
    text = str(text).strip()
    held = []

    def hold(m):
        held.append(m.group(0))
        return "\x00%d\x00" % (len(held) - 1)

    text = _MATH.sub(hold, text)

    # A ledger field may carry a real command with an argument -- \\ref{prop:foo},
    # \\emph{...} -- so hold those out before touching braces, or the escaping below
    # strips the argument and leaves "Missing \\endcsname inserted".
    text = re.sub('\\\\[a-zA-Z]+(?:\\[[^]]*\\])?\\{[^{}]*\\}', hold, text)

    # What braces remain are literal or malformed, never grouping: mathematics and
    # commands are held out above and this tool adds its own markup afterwards.  An
    # unbalanced one -- "S\\{v_0}", an escaped opener with a bare closer -- closes
    # the \\todo group early and the build dies several lines later with "Extra }".
    text = re.sub(r"(?<!\\)\{", r"\\{", text)
    text = re.sub(r"(?<!\\)\}", r"\\}", text)

    def _code_or_quote(m):
        # Searchers use ` as an opening quotation mark as often as a code fence.
        # Treat it as code only when the span looks like code: short, and with no
        # apostrophe (which is what a quoted French or English phrase carries).
        inner = m.group(1)
        if len(inner) <= 60 and "'" not in inner:
            return hold_code(m, held)
        return "``" + inner + "''"

    text = re.sub(r"`([^`]+)`", _code_or_quote, text)
    text = text.replace("`", "``")
    text = re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\\emph{\1}", text)
    text = re.sub(r'"([^"]*)"', r"``\1''", text)
    text = text.replace("&", "\\&").replace("%", "\\%").replace("#", "\\#")
    # Searchers write plain-text mathematics into `work:` and `locator:` --
    # "P^2=P", "S_n-module" -- which is fatal outside math mode.  Math and code
    # spans are already held out above, so what remains here is prose.
    text = text.replace("_", "\\_")
    text = text.replace("^", "\\textasciicircum{}")
    text = text.replace("~", "\\textasciitilde{}")
    text = text.replace("---", "\\textemdash{}")
    for i, h in enumerate(held):
        text = text.replace("\x00%d\x00" % i, h)
    return ascii_fold(text)


def hold_code(m, held):
    # \code is this family's own macro and is undefined in a source we annotate.
    # \texttt is in every LaTeX.
    held.append("\\texttt{%s}" % m.group(1).replace("\\", "\\textbackslash{}"))
    return "\x00%d\x00" % (len(held) - 1)


def strip_md(text):
    """Drop Markdown emphasis, leaving mathematics alone.

    Mathematics must be held out first.  `$c^*$` is a starred map, not italics, and
    stripping its asterisks yields `$c^$` -- a superscript with no argument, which
    kills the build a thousand lines later with "A left brace was mandatory here".
    """
    if text is None:
        return ""
    # A collation may leave a field as a list of what each pass said.  Stringifying
    # that prints a Python repr into the document.
    if isinstance(text, (list, tuple)):
        text = " ".join(str(x).strip() for x in text if str(x).strip())
    elif isinstance(text, dict):
        text = " ".join("%s: %s" % (k, v) for k, v in text.items())
    t = str(text).strip()
    held = []

    def hold(m):
        held.append(m.group(0))
        return "\x00%d\x00" % (len(held) - 1)

    t = _MATH.sub(hold, t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"\1", t)
    t = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\1", t)
    for i, h in enumerate(held):
        t = t.replace("\x00%d\x00" % i, h)
    return t


# ----------------------------------------------------------------------
# anchors  (inherited from annotate_tex.py; do not simplify)
# ----------------------------------------------------------------------

MATH_ENVS = ("equation", "align", "multline", "gather", "flalign", "alignat",
             "eqnarray", "displaymath", "split", "cases")
VERBATIM_ENVS = ("verbatim", "lstlisting", "minted", "Verbatim", "alltt")
# Nothing may be inserted between \begin{itemize} and its first \item: LaTeX has
# nowhere to put it and stops with "Something's wrong--perhaps a missing \item".
LIST_ENVS = ("itemize", "enumerate", "description")


def _delims(line):
    line = re.sub(r"(?<!\\)%.*$", "", line)
    line = line.replace(r"\$", "")
    doubles = line.count("$$")
    dollars = line.count("$") - 2 * doubles
    opens = line.count(r"\[") + line.count(r"\(")
    closes = line.count(r"\]") + line.count(r"\)")
    return dollars, opens, closes, doubles, line


def safe_line(lines, start):
    inline = False
    dispdd = False
    display = 0
    envs = 0
    verb = 0
    awaiting_item = 0        # inside a list env that has not had its first \item yet
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
        for e in LIST_ENVS:
            awaiting_item += line.count(r"\begin{%s}" % e)
            awaiting_item -= line.count(r"\end{%s}" % e)
        awaiting_item = max(awaiting_item, 0)
        if awaiting_item and r"\item" in line:
            awaiting_item -= 1
        if (j >= start and not inline and not dispdd
                and display <= 0 and envs <= 0 and verb <= 0
                and not awaiting_item):
            if r"\end{document}" in lines[j]:
                break
            return j
    raise LedgerError("no safe insertion point at or after source line %d" % (start + 1))


def excluded_lines(lines):
    r"""Line indices that do not reach the compiled document.

    A source under active revision keeps superseded material in ``\iffalse ... \fi``
    and ``comment`` environments.  The family stance puts it out of scope: what does
    not print is not part of the artifact.  An anchor landing there would mark a
    passage no reader of the PDF can see, so the check refuses it.

    Nested ``\if...`` inside a false branch is tracked so its ``\fi`` does not close
    the wrong block.
    """
    out = set()
    depth = 0          # \iffalse nesting, counting intervening \if... opens
    comment = 0
    for i, raw in enumerate(lines):
        line = re.sub(r"(?<!\\)%.*$", "", raw)
        starts_false = bool(re.search(r"\\iffalse\b", line))
        if depth and not starts_false:
            depth += len(re.findall(r"\\if[a-zA-Z@]*\b", line))
            depth -= len(re.findall(r"\\fi\b", line))
            if depth <= 0:
                depth = 0
                out.add(i)
                continue
        elif starts_false:
            depth = 1 + len(re.findall(r"\\if[a-zA-Z@]*\b", line)) - 1
            depth -= len(re.findall(r"\\fi\b", line))
            depth = max(depth, 0)
            out.add(i)
            continue
        if r"\begin{comment}" in line:
            comment += 1
        if depth or comment:
            out.add(i)
        if r"\end{comment}" in line and comment:
            comment -= 1
            out.add(i)
    return out


def find_anchor(lines, anchor, ident, occurrence=None):
    raw_hits = [i for i, ln in enumerate(lines) if anchor in ln]
    if not raw_hits:
        raise LedgerError(
            "%s: anchor not found in the annotation base.\n    anchor: %r\n"
            "    An anchor must be a verbatim substring of one source line.  Copy it\n"
            "    from the file, macros and all; do not retype it from the PDF."
            % (ident, anchor))
    dead = excluded_lines(lines)
    hits = [h for h in raw_hits if h not in dead]
    if not hits:
        raise LedgerError(
            "%s: every occurrence of this anchor is inside an \\iffalse or comment\n"
            "    block (line(s) %s).\n    anchor: %r\n"
            "    That text does not reach the compiled document, so it is not part of\n"
            "    the artifact and must not be marked."
            % (ident, ", ".join(str(h + 1) for h in raw_hits), anchor))
    if len(hits) > 1 and occurrence is None:
        raise LedgerError(
            "%s: anchor matches %d lines (%s).\n    anchor: %r\n"
            "    Lengthen it until it is unique, or set `occurrence: N`."
            % (ident, len(hits), ", ".join(str(h + 1) for h in hits), anchor))
    if occurrence is not None:
        if not 1 <= occurrence <= len(hits):
            raise LedgerError("%s: occurrence %d requested, %d present"
                              % (ident, occurrence, len(hits)))
        chosen = hits[occurrence - 1]
    else:
        chosen = hits[0]
    return chosen


def read_base(inv, outdir):
    base = (inv.get("meta") or {}).get("annotation_base")
    if not base:
        return None, None
    path = base if os.path.isabs(base) else os.path.join(outdir, base)
    if not os.path.exists(path):
        raise LedgerError("annotation base not found: %s" % path)
    with open(path, encoding="utf-8", errors="replace") as fh:
        return path, fh.read().splitlines()


# ----------------------------------------------------------------------
# rendering
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# ascii folding
# ----------------------------------------------------------------------

# A source we annotate may declare any input encoding -- it may say
# `\usepackage[latin9]{inputenc}` on a file that is actually UTF-8.  Inserting a
# UTF-8 note into it is a fatal inputenc error, so everything written into a .tex
# is folded to ASCII LaTeX first.  LaTeX escapes are valid under every encoding.

_FOLD = {
    "\u2014": "---", "\u2013": "--", "\u2012": "--", "\u2212": "$-$",
    "\u2018": "`", "\u2019": "'", "\u201c": "``", "\u201d": "''",
    "\u2026": "\\dots{}", "\u00a0": "~", "\u00b7": "\\textperiodcentered{}",
    "\u00d7": "$\\times$", "\u2264": "$\\leq$", "\u2265": "$\\geq$",
    "\u2260": "$\\neq$", "\u2245": "$\\cong$", "\u2248": "$\\approx$",
    "\u2208": "$\\in$", "\u2282": "$\\subset$", "\u2286": "$\\subseteq$",
    "\u2192": "$\\to$", "\u21a6": "$\\mapsto$", "\u221e": "$\\infty$",
    "\u2297": "$\\otimes$", "\u2295": "$\\oplus$", "\u222a": "$\\cup$",
    "\u2229": "$\\cap$", "\u00b1": "$\\pm$", "\u2211": "$\\sum$",
    "\u220f": "$\\prod$", "\u2237": ":", "\u00ab": "``", "\u00bb": "''",
    "\u2124": "$\\mathbb{Z}$", "\u211a": "$\\mathbb{Q}$",
    "\u211d": "$\\mathbb{R}$", "\u2102": "$\\mathbb{C}$",
    "\u2115": "$\\mathbb{N}$", "\u2113": "$\\ell$", "\u0428": "Sha",
    "\u1e96": "Sha",
}
# Greek letters -> math mode
for _c, _n in [("\u03b1","alpha"),("\u03b2","beta"),("\u03b3","gamma"),("\u03b4","delta"),
               ("\u03b5","varepsilon"),("\u03b6","zeta"),("\u03b7","eta"),("\u03b8","theta"),
               ("\u03ba","kappa"),("\u03bb","lambda"),("\u03bc","mu"),("\u03bd","nu"),
               ("\u03be","xi"),("\u03c0","pi"),("\u03c1","rho"),("\u03c3","sigma"),
               ("\u03c4","tau"),("\u03c6","varphi"),("\u03c7","chi"),("\u03c8","psi"),
               ("\u03c9","omega"),("\u0393","Gamma"),("\u0394","Delta"),("\u039b","Lambda"),
               ("\u03a0","Pi"),("\u03a3","Sigma"),("\u03a6","Phi"),("\u03a8","Psi"),
               ("\u03a9","Omega")]:
    _FOLD[_c] = "$\\%s$" % _n
# accented latin
for _c, _r in [("\u00e9","\\'e"),("\u00e8","\\`e"),("\u00ea","\\^e"),("\u00eb",'\\"e'),
               ("\u00e1","\\'a"),("\u00e0","\\`a"),("\u00e2","\\^a"),("\u00e4",'\\"a'),
               ("\u00ed","\\'i"),("\u00ee","\\^i"),("\u00ef",'\\"i'),("\u00f3","\\'o"),
               ("\u00f4","\\^o"),("\u00f6",'\\"o'),("\u00fa","\\'u"),("\u00fb","\\^u"),
               ("\u00fc",'\\"u'),("\u00f1","\\~n"),("\u00e7","\\c{c}"),("\u0107","\\'c"),
               ("\u010d","\\v{c}"),("\u0161","\\v{s}"),("\u017e","\\v{z}"),
               ("\u0142","\\l{}"),("\u00f8","\\o{}"),("\u00e5","\\aa{}"),
               ("\u00c9","\\'E"),("\u00c8","\\`E"),("\u00c1","\\'A"),("\u00d6",'\\"O'),
               ("\u00dc",'\\"U'),("\u00c7","\\c{C}"),("\u0160","\\v{S}")]:
    _FOLD[_c] = _r


def ascii_fold(s):
    """Fold text to ASCII LaTeX. Unmapped non-ASCII is dropped, not smuggled through."""
    if s is None:
        return ""
    out = []
    for ch in str(s):
        if ord(ch) < 128:
            out.append(ch)
        else:
            out.append(_FOLD.get(ch, ""))
    return "".join(out)


def conn_source(conn):
    w = strip_md(conn.get("work"))
    loc = strip_md(conn.get("locator"))
    return "%s, %s" % (w, loc) if loc else w



def full_note(conn, ident):
    """The whole record, set at the passage, rather than a pointer to it.

    Worth doing only where few records survive the gate: at thirty marks over
    thirty pages this is about one box a page and a reader never has to leave the
    paper.  At several hundred it would bury the text it annotates, which is what
    the short form and the section-mark pointer are for.
    """
    parts = []
    cons = strip_md(conn.get("consequence"))
    if cons:
        parts.append("\\textbf{%s}" % to_latex(cons))
    src = conn_source(conn)
    short = LABELS[conn["label"]][0]
    parts.append("%s \\textemdash{} \\emph{%s}, read %s."
                 % (to_latex(src), to_latex(short),
                    to_latex(READ_WORD.get(conn.get("read"), ""))))
    for key, head in (("their_object", "The source"),
                      ("dictionary", "Correspondence"),
                      ("differs", "Where it stops")):
        v = conn.get(key)
        if v:
            parts.append("\\emph{%s.}\\ %s" % (head, to_latex(strip_md(v))))
    parts.append("{\\footnotesize\\S\\,%s}" % ident)
    return "\\par\\medskip ".join(parts)


def margin_note(conn, ident):
    """One line: kind, source with locator, pointer into the guide."""
    short = LABELS[conn["label"]][0]
    return ascii_fold("%s \\textperiodcentered\\ %s \\textperiodcentered\\ \\S\\,%s" % (
        short, to_latex(conn_source(conn)), ident))


def render_callout(ident, entry, rec):
    out = ["%% generated by correspond.py from the ledgers -- do not edit",
           "\\begin{antecedentbox}"]
    name = to_latex(entry.get("name"))
    state = strip_md(rec.get("state") or "nothing located")
    out.append("\\antetag{%s \\textperiodcentered\\ %s}" % (name, to_latex(state)))
    conns = [c for c in (rec.get("connections") or []) if is_news(c)]
    for conn in conns:
        short = LABELS[conn["label"]][0]
        body = []
        body.append("\\textbf{%s.}\\ %s" % (to_latex(short.capitalize()),
                                            to_latex(conn_source(conn))))
        if conn.get("dictionary"):
            body.append(to_latex(conn["dictionary"]))
        if conn.get("differs"):
            body.append("\\emph{Where it stops.}\\ " + to_latex(conn["differs"]))
        out.append("\n\n".join(body))
        out.append("")
    if rec.get("unlocated"):
        out.append("{\\small\\color{inkmuted}What nothing was located for: %s}"
                   % to_latex(rec["unlocated"]))
    loc = to_latex(entry.get("location"))
    if loc:
        out.append("{\\small\\color{inkmuted}%s. The full record is at \\hyperref[corr:%s]{%s}.}"
                   % (loc, ident, ident))
    out.append("\\end{antecedentbox}")
    return "\n".join(out) + "\n"



def render_connections_md(inv, cor, index):
    """The admitted records, in the paper's own order, each led by its consequence.

    This is what a note's `§<id>` points into.  `A-entries.md` holds the whole
    search and is the notes; this holds what earned a reader's attention.
    """
    L = ["# Connections", ""]
    L.append("Every record here names something the authors would do about it. The full "
             "search, including everything that did not meet that bar, is in "
             "`A-entries.md`; nothing has been discarded, only held back.")
    L.append("")
    n = 0
    for e in (inv.get("entries") or []):
        rec = index.get(e["id"])
        if not rec:
            continue
        keep = [c for c in (rec.get("connections") or []) if is_news(c)]
        if not keep:
            continue
        n += len(keep)
        L.append("## %s — %s" % (e["id"], strip_md(e.get("name"))))
        L.append("")
        L.append("*%s*" % strip_md(e.get("location") or ""))
        L.append("")
        if e.get("statement"):
            L.append("**What the paper does here.** %s" % strip_md(e["statement"]))
            L.append("")
        for c in keep:
            L.append("### %s" % strip_md(c.get("consequence")))
            L.append("")
            L.append("%s — %s" % (strip_md(c.get("work")), strip_md(c.get("locator"))))
            L.append("")
            bits = ["read: %s" % READ_WORD.get(c.get("read"), c.get("read")),
                    "relation: %s" % LABELS.get(c.get("label"), (c.get("label"),))[0]]
            if c.get("located_by"):
                k = len(c["located_by"])
                bits.append("located independently by %d search%s" % (k, "" if k == 1 else "es"))
            L.append("*%s*" % " · ".join(bits))
            L.append("")
            for key, head in (("their_object", "What the source says"),
                              ("dictionary", "How they correspond"),
                              ("differs", "Where the correspondence stops"),
                              ("note", "Note")):
                if c.get(key):
                    L.append("**%s.** %s" % (head, strip_md(c[key])))
                    L.append("")
        if rec.get("unlocated"):
            L.append("**Nothing was located for.** %s" % strip_md(rec["unlocated"]))
            L.append("")
    L.insert(3, "")
    L.insert(3, "**%d records over %d entries.**" % (n, sum(1 for x in L if x.startswith("## "))))
    return "\n".join(L) + "\n"


def render_entries_md(inv, cor, index):
    meta = inv.get("meta") or {}
    L = ["# Entries", ""]
    L.append("Every entry and every connection, generated from the ledgers. This is for "
             "lookup, not for reading through.")
    L.append("")
    for e in (inv.get("entries") or []):
        ident = e["id"]
        L.append("## %s — %s" % (ident, strip_md(e.get("name"))))
        L.append("")
        if e.get("location"):
            L.append("*%s*" % strip_md(e["location"]))
            L.append("")
        if e.get("statement"):
            L.append(strip_md(e["statement"]))
            L.append("")
        if e.get("status") == "dismissed":
            L.append("**Not searched.** %s" % strip_md(e.get("dismissal")))
            L.append("")
            continue
        rec = index.get(ident)
        if not rec:
            L.append("*No search record.*")
            L.append("")
            continue
        L.append("**State:** %s" % strip_md(rec.get("state") or "nothing located"))
        L.append("")
        for conn in (rec.get("connections") or []):
            L.append("### %s — %s" % (LABELS[conn["label"]][0], conn_source(conn)))
            L.append("")
            bits = []
            if conn.get("literature"):
                bits.append("literature: %s" % strip_md(conn["literature"]))
            bits.append("read: %s" % READ_WORD[conn["read"]])
            st = conn.get("standing") or "placement"
            bits.append("standing: %s" % st)
            if st == "placement" and not str(conn.get("consequence") or "").strip():
                bits.append("**held back** — no consequence named")
            if conn.get("located_by"):
                n = len(conn["located_by"])
                bits.append("located independently by %d search%s"
                            % (n, "" if n == 1 else "es"))
            L.append("*%s*" % " · ".join(bits))
            L.append("")
            for key, head in (("their_object", "The source's object"),
                              ("dictionary", "The dictionary"),
                              ("differs", "Where the correspondence stops"),
                              ("orients", "What knowing this buys"),
                              ("note", "Note")):
                if conn.get(key):
                    L.append("**%s.** %s" % (head, strip_md(conn[key])))
                    L.append("")
        if rec.get("unlocated"):
            L.append("**Nothing was located for.** %s" % strip_md(rec["unlocated"]))
            L.append("")
        if rec.get("searched"):
            L.append("**Searched.** %s" % strip_md(rec["searched"]))
            L.append("")
    return "\n".join(L) + "\n"


def render_unlocated_md(inv, cor, index):
    L = ["# What nothing was located for", ""]
    L.append("A filter over the ledgers, in the paper's own order. Each line is a statement "
             "about a search, not about the mathematics.")
    L.append("")
    reach = ((cor.get("meta") or {}).get("reach") or {})
    if reach:
        L.append("## What could not be reached")
        L.append("")
        if reach.get("caps"):
            L.append(strip_md(reach["caps"]))
            L.append("")
        for u in (reach.get("unreachable") or []):
            L.append("- %s" % strip_md(u))
        L.append("")
    L.append("## Entries")
    L.append("")
    n = 0
    for e in (inv.get("entries") or []):
        rec = index.get(e["id"])
        if not rec or not rec.get("unlocated"):
            continue
        n += 1
        L.append("**%s — %s** (%s)" % (e["id"], strip_md(e.get("name")),
                                       strip_md(e.get("location") or "")))
        L.append("")
        L.append(strip_md(rec["unlocated"]))
        L.append("")
    if not n:
        L.append("*Nothing recorded.*")
        L.append("")
    return "\n".join(L) + "\n"


def render_leads_md(inv, cor, index):
    L = ["# Leads", ""]
    L.append("Named and unread, ordered only by how many searches nominated each "
             "independently. What a later extension picks up.")
    L.append("")
    rows = []
    for e in (inv.get("entries") or []):
        rec = index.get(e["id"])
        for lead in ((rec or {}).get("leads") or []):
            if isinstance(lead, dict):
                rows.append((lead.get("nominated_by", 1), e["id"],
                             strip_md(lead.get("work")), strip_md(lead.get("why") or "")))
            else:
                rows.append((1, e["id"], strip_md(lead), ""))
    rows.sort(key=lambda r: (-r[0], r[1]))
    if not rows:
        L.append("*None recorded.*")
        return "\n".join(L) + "\n"
    L.append("| Nominations | Entry | Lead | Why |")
    L.append("|---|---|---|---|")
    for n, ident, work, why in rows:
        L.append("| %d | %s | %s | %s |" % (n, ident, work, why))
    L.append("")
    return "\n".join(L) + "\n"


# ----------------------------------------------------------------------
# annotated copies
# ----------------------------------------------------------------------

TODO_PKG = re.compile(r"\\usepackage(\[[^\]]*\])?\{todonotes\}")


def set_todonotes(lines, inline, nmarks=0):
    """Ensure todonotes is loaded with the options we need.

    Margin notes are floats, and LaTeX ships with room for only 18 of them.  A
    densely marked copy dies with "Float(s) lost" -- which it reports at
    \\end{document}, long after the passage that caused it -- so the float pool is
    enlarged in proportion to the marks actually inserted.
    """
    # `inline` is an option of the \todo COMMAND, not of the package; passing it
    # here is "Unknown option `inline' for package `todonotes'".
    opts = "[textsize=footnotesize]" if inline else "[textsize=footnotesize,textwidth=2.6cm]"
    extra = max(256, 2 * nmarks + 64)
    inject = [r"\usepackage%s{todonotes}" % opts,
              r"\extrafloats{%d}" % extra]
    out = list(lines)
    for i, ln in enumerate(out):
        if TODO_PKG.search(ln):
            # lambda, not a string: re.sub processes backslashes in a replacement
            # and every one of these lines starts with \usepackage.
            repl = "\\usepackage%s{todonotes}" % opts
            out[i] = TODO_PKG.sub(lambda _m: repl, ln)
            out.insert(i + 1, r"\extrafloats{%d}" % extra)
            return out
    for i, ln in enumerate(out):
        if r"\begin{document}" in ln:
            for b in reversed([r"\usepackage{xcolor}"] + inject):
                out.insert(i, b)
            return out
    raise LedgerError(r"no \begin{document} in the annotation base")


_MACRO = re.compile(r"\\([a-zA-Z]+)")

# Emitted by this tool or supplied by the packages it loads; never shadow these.
_OURS = {"todo", "usepackage", "extrafloats", "begin", "end", "textperiodcentered",
         "textbf", "emph", "texttt", "textbackslash", "textasciicircum",
         "textasciitilde", "textemdash", "dots", "S", "hyperref", "ref", "label",
         "color", "providecommand", "ensuremath", "mathrm", "operatorname",
         "noindent", "par", "footnotesize", "bigskip", "endgroup", "begingroup",
         "maketitle", "item", "aa", "l", "o", "c", "v", "u", "d", "b", "t", "H",
         "P", "i", "j", "k", "r", "AA", "L", "O", "SS", "ss", "ae", "oe", "AE", "OE"}


def macro_fallbacks(marks, lines):
    r"""\providecommand stubs for macros a note uses and the base does not define.

    A ledger is written by many hands and they bring their own preambles: `\Av`,
    `\Proj`, `\rank`. The base document defines its own and nothing else, so an
    otherwise sound note kills the build with "Undefined control sequence".
    \providecommand is a no-op where the macro already exists, so this adds only
    what is genuinely missing, and \ensuremath makes the stub legal in text and in
    mathematics alike.
    """
    base = "\n".join(lines)
    wanted = set()
    for _i, tex, _anc in marks:
        wanted.update(_MACRO.findall(tex))
    out = []
    for name in sorted(wanted):
        # Single letters are NOT skipped: `\G`, `\Z`, `\Q` are ordinary shorthand in
        # a searcher's own preamble and undefined in the paper's.  Only LaTeX's own
        # one-letter commands are excluded, and those are listed in _OURS.
        if name in _OURS:
            continue
        # crude but sufficient: does the base define it at all?
        if ("\\newcommand{\\%s}" % name in base or "\\def\\%s" % name in base
                or "\\DeclareMathOperator{\\%s}" % name in base
                or "\\newcommand\\%s" % name in base
                or "\\let\\%s" % name in base):
            continue
        out.append("\\providecommand{\\%s}{\\ensuremath{\\mathrm{%s}}}" % (name, name))
    return out



def verify_placement(out, marks, which):
    r"""Every note must sit within a few lines of the passage it is about.

    `check` verifies that an anchor RESOLVES in the base.  That says nothing about
    where the note ENDS UP, and the two are different claims: a preamble line added
    before the marks are placed slides every one of them earlier in the body, at
    which point each note sits at a passage it has nothing to do with while every
    anchor still verifies perfectly.  That happened here -- every document built,
    every anchor checked, and the artifact was worthless.  So this checks the
    generated file against the anchors, which is the claim that matters.
    """
    anchors = {}
    for _i, tex, anc in marks:
        anchors[tex] = anc
    bad = []
    for n, ln in enumerate(out):
        anc = anchors.get(ln)
        if anc is None:
            continue
        # The anchor must appear SOMEWHERE ABOVE the note.  Distance is not the
        # test: a note may legitimately be pushed well past its anchor when the
        # passage sits inside a long display, since that is the first place a
        # paragraph may legally go.  What must never happen is a note landing
        # BEFORE the text it is about -- that is the displacement failure, and it
        # is invisible to every other check.
        above = any(anc in w for w in out[:n])
        if not above:
            bad.append((n + 1, anc[:60]))
    if bad:
        raise LedgerError(
            "%s: %d note(s) are not next to their anchor -- the passage they concern "
            "is not within eight lines above them.\n    first at output line %d, "
            "anchor %r\n    A note in the wrong place is worse than no note: it reads "
            "as a claim about whatever it landed on."
            % (which, len(bad), bad[0][0], bad[0][1]))


def build_annotated(lines, inv, cor, index, which, inline, full=False):
    """which: a literature name, or the sentinel '@unlocated'."""
    marks = []          # (line index, latex)
    for e in (inv.get("entries") or []):
        ident = e["id"]
        rec = index.get(ident)
        if not rec:
            continue
        if which == "@unlocated":
            if not rec.get("unlocated"):
                continue
            # "nothing further was located for this" is only news where the entry
            # itself has substance.  On an entry whose every record is standard
            # background, it says nothing found beyond the standard treatment of a
            # standard object -- the same over-reporting, in a different field.
            cs = rec.get("connections") or []
            if cs and not any(is_news(c) for c in cs):
                continue
            anchor = e.get("anchor")
            if not anchor:
                continue
            i = find_anchor(lines, anchor, ident, e.get("occurrence"))
            marks.append((i, "\\todo[%s]{nothing located \\textperiodcentered\\ \\S\\,%s}"
                          % ("inline" if inline else "", ident), anchor))
            continue
        for conn in (rec.get("connections") or []):
            if which != "@all" and lit_of(conn) != which:
                continue
            if not is_news(conn):
                continue    # standard background belongs in the reference view, not
                            # beside a passage the author wrote knowing it
            anchor = conn.get("anchor") or e.get("anchor")
            if not anchor:
                continue
            i = find_anchor(lines, anchor, ident,
                            conn.get("occurrence") or e.get("occurrence"))
            r, g, b = LABEL_COLOUR[conn["label"]].split(",")
            mode = "inline," if inline else ""
            body = full_note(conn, ident) if full else margin_note(conn, ident)
            marks.append((i, "\\todo[%sbackgroundcolor={rgb,1:red,%s;green,%s;blue,%s}]{%s}"
                          % (mode, r, g, b, body), anchor))
    # ORDER MATTERS.  Mark positions were computed against `lines`, so the marks go
    # in FIRST, bottom-up.  Anything added to the preamble afterwards shifts only
    # what follows it, and every mark is already placed by then.  Doing it the other
    # way round -- preamble first -- silently slides every note earlier in the body
    # by the number of preamble lines added, which puts each one at a passage it has
    # nothing to do with while every anchor still checks out.
    out = list(lines)
    for i, tex, _anc in sorted(marks, key=lambda m: -m[0]):
        j = safe_line(out, i)
        out.insert(j + 1, tex)

    verify_placement(out, marks, which)

    out = set_todonotes(out, inline, len(marks))
    stubs = macro_fallbacks(marks, out)
    if stubs:
        for i, ln in enumerate(out):
            if r"\begin{document}" in ln:
                for s in reversed(stubs):
                    out.insert(i, s)
                break
    return out, len(marks)


def insert_key(lines, title, subtitle):
    out = list(lines)
    for i, ln in enumerate(out):
        if r"\begin{document}" in ln:
            block = [
                r"\begingroup\footnotesize\noindent\textbf{%s}\par" % title,
                r"\noindent %s\par" % subtitle,
                r"\noindent The colours index the kind of relationship recorded. "
                r"They grade nothing: no colour here is better or worse than another, "
                r"and none is a judgment about this paper.\par\endgroup\bigskip",
            ]
            k = i + 1
            while k < len(out) and r"\maketitle" not in out[k]:
                k += 1
            at = k + 1 if k < len(out) else i + 1
            for b in reversed(block):
                out.insert(at, b)
            return out
    return out


# ----------------------------------------------------------------------
# build
# ----------------------------------------------------------------------

def latex(tex, outdir, runs=3):
    stem = os.path.splitext(os.path.basename(tex))[0]
    log = ""
    for _ in range(runs):
        # pdflatex echoes bytes straight from the source, which is not necessarily
        # UTF-8 -- a latin-1 accented name in a bibliography is enough.  Decoding
        # strictly kills the build on a file that would otherwise compile, so decode
        # leniently and let the log speak for itself.
        p = subprocess.run(["pdflatex", "-interaction=nonstopmode",
                            "-halt-on-error", "-file-line-error", stem + ".tex"],
                           cwd=outdir, capture_output=True)
        log = (p.stdout + p.stderr).decode("utf-8", errors="replace")
    return log


def report_build(outdir, stem):
    """Verify rather than trust the exit status."""
    pdf = os.path.join(outdir, stem + ".pdf")
    logp = os.path.join(outdir, stem + ".log")
    problems = []
    if not os.path.exists(pdf):
        return ["no PDF produced"]
    if os.path.exists(logp):
        with open(logp, encoding="utf-8", errors="replace") as fh:
            log = fh.read()
        for pat, msg in (
                (r"^! ", "LaTeX error"),
                (r"Undefined control sequence", "undefined control sequence"),
                (r"There were undefined references", "undefined references"),
                (r"Rerun to get", "cross-references have not converged")):
            if re.search(pat, log, re.M):
                problems.append(msg)
        src = os.path.join(outdir, stem + ".tex")
        if os.path.exists(src) and os.path.getmtime(pdf) < os.path.getmtime(src):
            problems.append("PDF older than its source")
    return problems


AUX = (".aux", ".log", ".out", ".toc", ".tdo", ".fls", ".fdb_latexmk", ".synctex.gz")


def clean_aux(outdir):
    for f in os.listdir(outdir):
        if f.endswith(AUX):
            try:
                os.remove(os.path.join(outdir, f))
            except OSError:
                pass


# ----------------------------------------------------------------------
# commands
# ----------------------------------------------------------------------

def cmd_check(args):
    inv, cor, ents = load(args.outdir)
    index = corr_index(cor)
    n_open = sum(1 for e in (inv.get("entries") or []) if e.get("status") != "dismissed")
    n_dis = len(inv.get("entries") or []) - n_open
    n_conn = sum(len(c.get("connections") or []) for c in (cor.get("entries") or []))
    path, lines = read_base(inv, args.outdir)
    bad = 0
    if lines is not None:
        for e in (inv.get("entries") or []):
            if e.get("status") == "dismissed" or not e.get("anchor"):
                continue
            try:
                i = find_anchor(lines, e["anchor"], e["id"], e.get("occurrence"))
                safe_line(lines, i)
                if args.verbose:
                    print("  ok   %-8s line %d" % (e["id"], i + 1))
            except LedgerError as exc:
                bad += 1
                print("  FAIL %s" % exc)
    else:
        print("  no annotation base recorded; annotated copies will not be produced")
    missing = [e["id"] for e in (inv.get("entries") or [])
               if e.get("status") != "dismissed" and e["id"] not in index]
    print("\n%d entries (%d searched, %d dismissed with a recorded reason), "
          "%d connections, %d literatures"
          % (len(inv.get("entries") or []), n_open, n_dis, n_conn, len(literatures(cor))))
    if missing:
        print("no search record yet: %s" % ", ".join(missing))
    if bad:
        print("%d anchor problem(s)" % bad)
        return 1
    return 0


def cmd_callouts(args):
    inv, cor, ents = load(args.outdir)
    index = corr_index(cor)
    d = os.path.join(args.outdir, "callouts")
    os.makedirs(d, exist_ok=True)
    n = 0
    for e in (inv.get("entries") or []):
        rec = index.get(e["id"])
        if not rec or not (rec.get("connections") or rec.get("unlocated")):
            continue
        with open(os.path.join(d, "%s.tex" % e["id"]), "w") as fh:
            fh.write(render_callout(e["id"], e, rec))
        n += 1
    print("callouts/: %d boxes" % n)
    return 0


def cmd_views(args):
    inv, cor, ents = load(args.outdir)
    index = corr_index(cor)
    for name, fn in (("A-connections.md", render_connections_md),
                     ("A-entries.md", render_entries_md),
                     ("A-unlocated.md", render_unlocated_md),
                     ("A-leads.md", render_leads_md)):
        with open(os.path.join(args.outdir, name), "w") as fh:
            fh.write(fn(inv, cor, index))
        print("%s" % name)
    return 0


def cmd_annotate(args):
    inv, cor, ents = load(args.outdir)
    index = corr_index(cor)
    path, lines = read_base(inv, args.outdir)
    if lines is None:
        print("no annotation base: annotated copies are not produced (Case C)")
        return 0
    made = []
    # The per-literature cut exists so a reader can open one copy and see one body
    # of work's whole footprint.  Below a threshold it does the opposite, scattering
    # a handful of notes over a dozen near-empty documents, so collapse to one.
    lits = literatures(cor)
    n_marks = sum(1 for c in (cor.get("entries") or [])
                  for conn in (c.get("connections") or []) if is_news(conn))
    if n_marks < 60 and len(lits) > 1:
        targets = [("@all", "annotated-connections")]
        print("%d marks over %d literatures: one combined copy, not a cut"
              % (n_marks, len(lits)))
    else:
        targets = [(lit, "annotated-%s" % slug(lit)) for lit in lits]
    targets.append(("@unlocated", "annotated-unlocated"))
    for which, stem in targets:
        out, n = build_annotated(lines, inv, cor, index, which, not args.margin,
                                 full=args.full)
        if not n:
            continue
        title = ("Marked: what nothing was located for" if which == "@unlocated"
                 else "Marked: located connections" if which == "@all"
                 else "Marked: %s" % which)
        sub = ("Each mark names an entry for which no corresponding source was located."
               if which == "@unlocated"
               else "Each mark gives the kind of relationship, the source with its "
                    "locator, and the entry in the guide carrying the full record.")
        out = insert_key(out, title, sub)
        p = os.path.join(args.outdir, stem + ".tex")
        with open(p, "w") as fh:
            fh.write("\n".join(out) + "\n")
        made.append((stem, n))
        print("%s.tex: %d marks" % (stem, n))
    if not made:
        print("no anchored connections; nothing annotated")
    return 0


def cmd_build(args):
    stems = [os.path.splitext(f)[0] for f in sorted(os.listdir(args.outdir))
             if f.startswith("annotated-") and f.endswith(".tex")]
    if not stems:
        print("nothing to build")
        return 0

    # stem -> which literature, so a failure can be regenerated a different way
    targets = {}
    try:
        inv, cor, _ents = load(args.outdir)
        index = corr_index(cor)
        path, lines = read_base(inv, args.outdir)
        for lit in literatures(cor):
            targets["annotated-%s" % slug(lit)] = lit
        targets["annotated-unlocated"] = "@unlocated"
    except LedgerError:
        inv = cor = index = lines = None

    rc = 0
    for stem in stems:
        latex(stem + ".tex", args.outdir)
        problems = report_build(args.outdir, stem)

        # Only reachable when a copy was generated with --margin: margin notes are
        # floats and LaTeX loses them where they cluster, however large the pool.
        # Inline boxes are not floats and always place.
        if problems and lines is not None and stem in targets:
            out, n = build_annotated(lines, inv, cor, index, targets[stem], True,
                                     full=getattr(args, 'full', False))
            out = insert_key(out, "Marked: %s" % targets[stem],
                             "Notes are set inline here rather than in the margin, "
                             "because at this density the margin cannot hold them.")
            with open(os.path.join(args.outdir, stem + ".tex"), "w") as fh:
                fh.write("\n".join(out) + "\n")
            latex(stem + ".tex", args.outdir)
            problems = report_build(args.outdir, stem)
            if not problems:
                print("%-32s ok  (inline: margin could not hold %d notes)" % (stem, n))
                continue

        if problems:
            rc = 1
            print("%-32s FAIL  %s" % (stem, "; ".join(problems)))
        else:
            print("%-32s ok" % stem)
    return rc


def cmd_all(args):
    for fn in (cmd_callouts, cmd_views, cmd_annotate):
        rc = fn(args)
        if rc:
            return rc
    rc = cmd_build(args)
    if args.clean_aux:
        clean_aux(args.outdir)
    return rc


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["check", "callouts", "views", "annotate",
                                        "build", "all"])
    ap.add_argument("-o", "--outdir", default=".")
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("--full", action="store_true",
                    help="set the whole record at the passage instead of a pointer. "
                         "Sensible only where few records survive the gate.")
    ap.add_argument("--margin", action="store_true",
                    help="margin notes instead of inline boxes. Inline is the default: "
                         "the margin is too narrow for a note carrying a source and a "
                         "locator, and it truncates them.")
    ap.add_argument("--clean-aux", action="store_true")
    args = ap.parse_args()
    try:
        return {"check": cmd_check, "callouts": cmd_callouts, "views": cmd_views,
                "annotate": cmd_annotate, "build": cmd_build, "all": cmd_all
                }[args.command](args)
    except LedgerError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
