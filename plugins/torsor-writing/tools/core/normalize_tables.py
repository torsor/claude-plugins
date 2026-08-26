#!/usr/bin/env python3
"""Table-fitting normalization — a front-end step, not a feature.

Rewrites tabular/longtable column specs so wide tables fit the 6x9 text block
instead of overflowing, in two mechanical modes:

  * bare l/c/r columns        -> equal-width wrapping L{} columns
  * absolute-width p{}/L{}     -> the same widths RESCALED proportionally to
    (e.g. p{5.5cm}p{7.5cm})       \\linewidth, preserving the author's ratios

Column widths already expressed relative to \\linewidth/\\textwidth (or specs
this parser doesn't recognize) are left untouched — allocating widths past these
mechanical defaults is reviewer-tier judgment. Totals are held under 1.0 to
leave room for \\tabcolsep.

Why a front-end step and not a feature: features stay preamble/mappings/CSS;
source transforms belong to the front-ends. Applied opt-in via the manifest
(`fit_tables: true`); the from-markdown front-end enables it by default, while
from-latex leaves it off so authored LaTeX is never silently rewritten.
"""
from __future__ import annotations

import re

ENV_RE = re.compile(r"\\begin\{(?:tabular|longtable)\}")
BARE = set("lcr")
TOTAL = 0.90  # column widths sum to this; the rest is \tabcolsep headroom

LEN_RE = re.compile(r"^\s*([0-9.]+)\s*(cm|mm|in|pt|bp|pc)\s*$")
UNIT_PT = {"cm": 28.4527, "mm": 2.84527, "in": 72.27, "pt": 1.0, "bp": 1.00375, "pc": 12.0}


def _extract_braced(s: str, i: int):
    """s[i] must be '{'. Return (inner, index_after_closing) honoring nesting."""
    if i >= len(s) or s[i] != "{":
        return None
    depth = 0
    for j in range(i, len(s)):
        if s[j] == "{":
            depth += 1
        elif s[j] == "}":
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
    return None


def _strip_noise(spec: str) -> str:
    """Drop @{...} groups, column rules (|), and whitespace; keep column entries."""
    out, k = [], 0
    while k < len(spec):
        c = spec[k]
        if c == "@" and k + 1 < len(spec) and spec[k + 1] == "{":
            g = _extract_braced(spec, k + 1)
            if g is None:
                return spec  # malformed -> treat as non-convertible
            k = g[1]
            continue
        if c in "| \t\n":
            k += 1
            continue
        out.append(c)
        k += 1
    return "".join(out)


def _parse_columns(spec: str):
    """Parse a noise-stripped spec into [(type, arg-or-None)]; None if unparseable."""
    cols, k = [], 0
    while k < len(spec):
        c = spec[k]
        if c in "lcrX":
            cols.append((c, None))
            k += 1
        elif c in "pmbLCR" and k + 1 < len(spec) and spec[k + 1] == "{":
            g = _extract_braced(spec, k + 1)
            if g is None:
                return None
            cols.append((c, g[0]))
            k = g[1]
        else:
            return None
    return cols or None


def _abs_width_pt(arg: str):
    m = LEN_RE.match(arg)
    return float(m.group(1)) * UNIT_PT[m.group(2)] if m else None


def _spec_from_fracs(fracs) -> str:
    return "@{}" + "".join(f"L{{{f:.3f}\\linewidth}}" for f in fracs) + "@{}"


def _fit_spec(spec: str):
    """Return a fitted column spec for this (noise-stripped) spec, or None to leave it."""
    if spec and all(c in BARE for c in spec):
        n = len(spec)
        return _spec_from_fracs([TOTAL / n] * n)
    cols = _parse_columns(spec)
    if cols and all(t in "pmbLCR" and a is not None for t, a in cols):
        widths = [_abs_width_pt(a) for _, a in cols]
        if all(w is not None for w in widths):  # all absolute -> rescale to fit
            total = sum(widths)
            return _spec_from_fracs([TOTAL * w / total for w in widths])
    return None


def normalize_tables(tex: str) -> str:
    result, pos = [], 0
    for m in ENV_RE.finditer(tex):
        k = m.end()
        while k < len(tex) and tex[k] in " \t\n":
            k += 1
        if k < len(tex) and tex[k] == "[":  # optional [pos]
            close = tex.find("]", k)
            if close == -1:
                continue
            k = close + 1
            while k < len(tex) and tex[k] in " \t\n":
                k += 1
        if k >= len(tex) or tex[k] != "{":
            continue
        braced = _extract_braced(tex, k)
        if braced is None:
            continue
        spec, end = braced
        fitted = _fit_spec(_strip_noise(spec))
        if fitted is not None:
            result.append(tex[pos:k])
            result.append("{" + fitted + "}")
            pos = end
    result.append(tex[pos:])
    return "".join(result)
