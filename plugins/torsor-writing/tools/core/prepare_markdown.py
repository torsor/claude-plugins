#!/usr/bin/env python3
"""Prepare LaTeX chapter files from a Markdown source (the from-markdown front-end).

Vendored into the core so from-markdown has no external dependency. Strips export
artifacts, splits a leading `# Preface` into front matter, and converts the body
Markdown to LaTeX via pandoc (`--no-highlight`, so code renders in the house
verbatim style rather than pandoc's undefined Shaded/Highlighting). Wide-table
fitting is handled downstream by the core's `fit_tables` normalization, not here.

    prepare_markdown.py SOURCE.md LATEX_DIR [--title TITLE]

Writes LATEX_DIR/chapters/00-preface.tex (if a preface exists) and 01-body.tex.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
GENERATED_DIV_RE = re.compile(r'\A\s*<div class="(?:titlepage|center)">.*?</div>\s*', re.S)
HTML_ANCHOR_RE = re.compile(r"<a\b[^>]*>(.*?)</a>", re.S | re.I)


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def run(cmd: list[str]) -> None:
    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        fail(f"required command not found: {cmd[0]}")
    except subprocess.CalledProcessError as exc:
        fail(f"command failed with exit {exc.returncode}: {' '.join(cmd)}")


def split_frontmatter(markdown: str) -> tuple[str, str]:
    if not markdown.startswith("---\n"):
        return "", markdown
    end = markdown.find("\n---", 4)
    if end == -1:
        return "", markdown
    after = markdown.find("\n", end + 4)
    if after == -1:
        return markdown, ""
    return markdown[: after + 1], markdown[after + 1 :]


def normalize(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[`*_{}\[\]()]|\\", "", text)
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def strip_generated_title_blocks(markdown: str) -> str:
    text = markdown
    while True:
        text, count = GENERATED_DIV_RE.subn("", text, count=1)
        if count == 0:
            return text


def strip_leading_export_artifacts(markdown: str) -> str:
    frontmatter, body = split_frontmatter(markdown)
    body = re.sub(r"\A\s*(?:=[^\n]*\n)+\s*", "", body)
    return frontmatter + body


def strip_exported_html_refs(markdown: str) -> str:
    def replace(match: re.Match[str]) -> str:
        return match.group(1).strip()

    return HTML_ANCHOR_RE.sub(replace, markdown).replace(" ", " ")


def strip_leading_document_title(markdown: str, title: str) -> str:
    frontmatter, body = split_frontmatter(markdown)
    lines = body.splitlines()
    index = 0
    while index < len(lines) and not lines[index].strip():
        index += 1
    if index < len(lines):
        match = re.match(r"^#\s+(.+?)\s*$", lines[index])
        if match and normalize(match.group(1)) == normalize(title):
            del lines[index]
            while index < len(lines) and not lines[index].strip():
                del lines[index]
    return frontmatter + "\n".join(lines).strip() + "\n"


def split_preface(markdown: str) -> tuple[str, str]:
    _, body = split_frontmatter(markdown)
    body = body.strip() + "\n"
    lines = body.splitlines()
    index = 0
    while index < len(lines) and not lines[index].strip():
        index += 1
    if index >= len(lines):
        return "", ""
    match = HEADING_RE.match(lines[index])
    if not match:
        return "", body
    title = match.group(2).strip()
    if not title.lower().startswith("preface"):
        return "", body
    level = len(match.group(1))
    end = len(lines)
    for pos in range(index + 1, len(lines)):
        next_heading = HEADING_RE.match(lines[pos])
        if next_heading and len(next_heading.group(1)) <= level:
            end = pos
            break
    preface_lines = lines[index:end]
    preface_lines[0] = "# " + title
    body_lines = lines[end:]
    return "\n".join(preface_lines).strip() + "\n", "\n".join(body_lines).strip() + "\n"


def make_preface_unnumbered(tex: str) -> str:
    def replace(match: re.Match[str]) -> str:
        title = match.group(1)
        label = match.group(2) or ""
        return "\\chapter*{" + title + "}\n\\addcontentsline{toc}{chapter}{" + title + "}" + label

    return re.sub(r"\\chapter\{([^}]*)\}(\\label\{[^}]+\})?", replace, tex, count=1)


def pandoc_to_latex(markdown_path: Path, out_path: Path, source_dir: Path, document_root: Path) -> None:
    resource_path = f"{source_dir}:{document_root}:{Path.cwd()}"
    run(
        [
            "pandoc",
            str(markdown_path),
            "-f",
            "gfm+yaml_metadata_block+smart",
            "-t",
            "latex",
            "--top-level-division=chapter",
            "--no-highlight",
            f"--resource-path={resource_path}",
            "-o",
            str(out_path),
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_markdown", type=Path)
    parser.add_argument("latex_dir", type=Path)
    parser.add_argument("--title", default="")
    args = parser.parse_args()

    source_markdown = args.source_markdown.resolve()
    latex_dir = args.latex_dir.resolve()
    document_root = latex_dir.parent
    chapters_dir = latex_dir / "chapters"
    build_dir = latex_dir / ".build"
    chapters_dir.mkdir(parents=True, exist_ok=True)
    build_dir.mkdir(parents=True, exist_ok=True)

    markdown = source_markdown.read_text(encoding="utf-8")
    markdown = strip_leading_export_artifacts(markdown)
    markdown = strip_generated_title_blocks(markdown)
    markdown = strip_exported_html_refs(markdown)
    if args.title:
        markdown = strip_leading_document_title(markdown, args.title)
    preface_md, body_md = split_preface(markdown)

    preface_tex = chapters_dir / "00-preface.tex"
    body_tex = chapters_dir / "01-body.tex"

    if preface_md.strip():
        preface_src = build_dir / "preface.md"
        preface_src.write_text(preface_md, encoding="utf-8")
        pandoc_to_latex(preface_src, preface_tex, source_markdown.parent.resolve(), document_root)
        preface_tex.write_text(
            make_preface_unnumbered(preface_tex.read_text(encoding="utf-8")),
            encoding="utf-8",
        )
    else:
        preface_tex.write_text("", encoding="utf-8")

    body_src = build_dir / "body.md"
    body_src.write_text(body_md, encoding="utf-8")
    pandoc_to_latex(body_src, body_tex, source_markdown.parent.resolve(), document_root)


if __name__ == "__main__":
    main()
