#!/usr/bin/env python3
"""Math feature — HTML slice. Inject MathJax into generated HTML when TeX
fallback math is present. Idempotent (skips if the loader is already there)."""

from __future__ import annotations

import sys
from pathlib import Path


SCRIPT = (
    '<script>window.MathJax={tex:{'
    'inlineMath:[["$","$"],["\\\\(","\\\\)"]],'
    'displayMath:[["$$","$$"],["\\\\[","\\\\]"]]}};</script>\n'
    '<script id="MathJax-script" async '
    'src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>\n'
)


def main(path: str) -> None:
    html_path = Path(path)
    html = html_path.read_text(encoding="utf-8")
    if "MathJax-script" in html:
        return
    html_path.write_text(html.replace("</head>", SCRIPT + "</head>", 1), encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1])
