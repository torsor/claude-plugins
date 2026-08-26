#!/usr/bin/env python3
"""Pandoc filter: replace math with embedded SVG (LaTeX + dvisvgm).

Reads a pandoc JSON AST on stdin, renders every Math element to a standalone
SVG via `latex` + `dvisvgm`, and rewrites each Math element as an <img>
referencing the SVG so the EPUB embeds it. Equations then render on readers
that do not support MathML.

SVGs are written to $MATHSVG_OUTDIR (default: .build/mathsvg relative to the
pandoc working directory) and cached by content hash across builds. If a
snippet fails to render, its Math element is left unchanged so the build still
produces a (partially MathML) EPUB instead of aborting.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

DOC_PT = 12.0  # snippet font size; em = pt / DOC_PT

PAGE_RE = re.compile(r"processing page (\d+)")
DIM_RE = re.compile(r"width=([0-9.]+)pt, height=([0-9.]+)pt, depth=([0-9.]+)pt")

PREAMBLE = r"""\documentclass[12pt]{article}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{amsfonts}
\usepackage{mathtools}
\usepackage{mathrsfs}
\usepackage[active,tightpage]{preview}
\setlength\PreviewBorder{0pt}
\begin{document}
"""


def log(msg: str) -> None:
    print(f"mathsvg_filter: {msg}", file=sys.stderr)


def outdir() -> Path:
    d = Path(os.environ.get("MATHSVG_OUTDIR", ".build/mathsvg")).resolve()
    d.mkdir(parents=True, exist_ok=True)
    return d


def key_of(mode: str, tex: str) -> str:
    return hashlib.sha1((mode + "\0" + tex).encode("utf-8")).hexdigest()[:16]


def snippet_body(mode: str, tex: str) -> str:
    if mode == "DisplayMath":
        return "\\begin{preview}\\[%s\\]\\end{preview}\n" % tex
    return "\\begin{preview}$%s$\\end{preview}\n" % tex


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )


def parse_dims(text: str) -> dict[int, tuple[float, float, float]]:
    dims: dict[int, tuple[float, float, float]] = {}
    page = None
    for line in text.splitlines():
        m = PAGE_RE.search(line)
        if m:
            page = int(m.group(1))
            continue
        d = DIM_RE.search(line)
        if d and page is not None:
            dims[page] = (float(d.group(1)), float(d.group(2)), float(d.group(3)))
    return dims


def render_group(items: list[tuple[str, str, str]], od: Path, index: dict) -> dict | None:
    """items: list of (key, mode, tex). Render as one LaTeX doc.

    Returns {key: record} on success, or None to signal the caller to fall
    back to per-snippet rendering.
    """
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        tex = PREAMBLE + "".join(snippet_body(mode, t) for _, mode, t in items) + "\\end{document}\n"
        (work / "m.tex").write_text(tex, encoding="utf-8")
        latex = run(["latex", "-interaction=nonstopmode", "-halt-on-error", "m.tex"], work)
        if latex.returncode != 0 or not (work / "m.dvi").exists():
            return None
        dv = run(["dvisvgm", "--no-fonts", "--page=1-", "--output=s-%p.svg", "m.dvi"], work)
        dims = parse_dims(dv.stdout)
        svgs = [work / f"s-{i}.svg" for i in range(1, len(items) + 1)]
        if dv.returncode != 0 or not all(s.exists() for s in svgs) or len(dims) != len(items):
            return None
        out: dict = {}
        for i, (key, mode, _tex) in enumerate(items, 1):
            w, h, dp = dims[i]
            dest = od / f"{key}.svg"
            shutil.copyfile(svgs[i - 1], dest)
            rec = {
                "file": str(dest),
                "w": w / DOC_PT,
                "h": (h + dp) / DOC_PT,
                "d": dp / DOC_PT,
                "mode": mode,
            }
            index[key] = rec
            out[key] = rec
        return out


def load_index(od: Path) -> dict:
    p = od / "index.json"
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            return {}
    return {}


def save_index(od: Path, index: dict) -> None:
    (od / "index.json").write_text(json.dumps(index), encoding="utf-8")


def collect(node, acc: dict) -> None:
    if isinstance(node, list):
        for x in node:
            collect(x, acc)
    elif isinstance(node, dict):
        if node.get("t") == "Math":
            mode = node["c"][0]["t"]
            tex = node["c"][1]
            acc[key_of(mode, tex)] = (mode, tex)
        else:
            for v in node.values():
                collect(v, acc)


def render_all(snippets: dict, od: Path, index: dict) -> None:
    todo = [
        (key, mode, tex)
        for key, (mode, tex) in snippets.items()
        if not (index.get(key) and (od / f"{key}.svg").exists())
    ]
    if not todo:
        return
    if render_group(todo, od, index) is None:
        for item in todo:
            if render_group([item], od, index) is None:
                log(f"failed to render (kept as MathML): {item[2][:60]!r}")
                index[item[0]] = None
    save_index(od, index)


def make_image(rec: dict, tex: str) -> dict:
    if rec["mode"] == "DisplayMath":
        style = (
            "display:block;margin:0.7em auto;width:%.4fem;max-width:100%%;height:auto;"
            % rec["w"]
        )
        classes = ["math", "display"]
    else:
        style = "height:%.4fem;width:auto;vertical-align:-%.4fem;" % (rec["h"], rec["d"])
        classes = ["math", "inline"]
    attr = ["", classes, [["style", style]]]
    return {"t": "Image", "c": [attr, [], [rec["file"], ""]]}


def transform(node, index: dict):
    if isinstance(node, list):
        return [transform(x, index) for x in node]
    if isinstance(node, dict):
        if node.get("t") == "Math":
            mode = node["c"][0]["t"]
            tex = node["c"][1]
            rec = index.get(key_of(mode, tex))
            if rec:
                return make_image(rec, tex)
            return node
        return {k: transform(v, index) for k, v in node.items()}
    return node


def main() -> None:
    doc = json.load(sys.stdin)
    od = outdir()
    index = load_index(od)
    snippets: dict = {}
    collect(doc.get("blocks", []), snippets)
    if snippets:
        render_all(snippets, od, index)
    doc = transform(doc, index)
    json.dump(doc, sys.stdout)


if __name__ == "__main__":
    main()
