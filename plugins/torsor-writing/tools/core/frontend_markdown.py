#!/usr/bin/env python3
"""The from-markdown front-end for the torsor unified document builder.

    frontend_markdown.py MANIFEST.yaml OUT_DIR [--force]

This is a *preprocessor*, not a builder. A manifest whose source is Markdown

    source: { kind: markdown, path: SOME.md }

is turned into the canonical torsor intermediate — a LaTeX chapter tree
(``chapters/*.tex`` + ``assets/``) — and then handed to ``assemble.py``, which
owns everything downstream (preamble stitching, feature vendoring, ``make``).

Steps:
  1. Convert the Markdown to LaTeX chapters via the core's vendored
     ``prepare_markdown.py`` (+ ``copy_markdown_and_images`` here): strip export
     artifacts, split a leading ``# Preface`` into front matter, convert body
     Markdown -> LaTeX via pandoc (``--no-highlight``). Wide-table fitting is
     handled downstream by the core's ``fit_tables`` normalization.
  2. Copy local Markdown images into the staging ``assets/``.
  3. Write a staging source dir (a temp dir) holding ``chapters/`` (+ ``assets/``).
  4. Build an effective manifest = the input manifest with ``source`` rewritten
     to ``{kind: latex, path: <staging dir>}`` (genre/title/features/etc kept).
  5. Delegate to ``assemble.py`` on the effective manifest + OUT_DIR.

Adding this front-end is a new file in the core; ``assemble.py`` is not touched.
See docs/specs/2026-07-15-unified-builder-contract-design.md.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

CORE = Path(__file__).resolve().parent
ASSEMBLE = CORE / "assemble.py"
PREPARE = CORE / "prepare_markdown.py"

IMAGE_PATTERN = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def fail(msg: str) -> None:
    print(f"frontend_markdown: {msg}", file=sys.stderr)
    sys.exit(1)


def copy_markdown_and_images(source: Path, dest_source_dir: Path, latex_assets_dir: Path) -> Path:
    """Copy the Markdown to dest_source_dir/doc.md, copying any local images it
    references into assets/ (and into latex_assets_dir for the build) and
    rewriting the links. Remote and anchor links are left untouched."""
    text = source.read_text(encoding="utf-8")
    assets_dir = dest_source_dir / "assets"
    copied: dict[Path, str] = {}

    def replace(match: re.Match[str]) -> str:
        alt = match.group(1)
        raw_path = match.group(2)
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", raw_path) or raw_path.startswith("#"):
            return match.group(0)
        image_path = (source.parent / raw_path).resolve()
        if not image_path.exists() or not image_path.is_file():
            return match.group(0)
        assets_dir.mkdir(parents=True, exist_ok=True)
        if image_path not in copied:
            target = assets_dir / image_path.name
            counter = 2
            while target.exists() and target.resolve() != image_path:
                target = assets_dir / f"{image_path.stem}-{counter}{image_path.suffix}"
                counter += 1
            shutil.copy2(image_path, target)
            latex_assets_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(image_path, latex_assets_dir / target.name)
            copied[image_path] = f"assets/{target.name}"
        return f"![{alt}]({copied[image_path]})"

    dest = dest_source_dir / "doc.md"
    dest.write_text(IMAGE_PATTERN.sub(replace, text), encoding="utf-8")
    return dest


# Macros pandoc defines in its *standalone* LaTeX template but omits from the
# body fragments we emit here. The torsor preamble (built for hand-authored
# chapters) does not provide them, so the front-end supplies them, guarded by
# \providecommand so they never clash with anything the core already defines.
PANDOC_COMPAT = (
    "% pandoc-fragment compatibility (injected by frontend_markdown.py)\n"
    "\\providecommand{\\tightlist}{"
    "\\setlength{\\itemsep}{0pt}\\setlength{\\parskip}{0pt}}\n"
    "\\providecommand{\\pandocbounded}[1]{#1}\n"
    "\\providecommand{\\passthrough}[1]{#1}\n"
)


def inject_pandoc_compat(staging: Path) -> None:
    """Prepend the pandoc-fragment macro shim to each generated chapter, so the
    body \\input{}s build against the torsor preamble. \\providecommand keeps it
    inert where the core (or an earlier chapter) already defined a macro."""
    for tex in sorted((staging / "chapters").glob("*.tex")):
        body = tex.read_text(encoding="utf-8")
        tex.write_text(PANDOC_COMPAT + body, encoding="utf-8")


def markdown_to_chapters(source_md: Path, staging: Path, title: str) -> None:
    """Populate ``staging`` with ``chapters/00-preface.tex``, ``01-body.tex`` and
    ``assets/`` from ``source_md``, using the core's vendored prepare pipeline."""
    # 1. Copy the Markdown + rewrite/copy its local images. The rewritten copy
    #    lives in staging/source (its assets/ feeds pandoc's resource path); the
    #    images also land in staging/assets for the final LaTeX build.
    src_stage = staging / "source"
    src_stage.mkdir(parents=True, exist_ok=True)
    doc_md = copy_markdown_and_images(source_md, src_stage, staging / "assets")

    # 2. Run the vendored core prepare script to emit the chapters.
    try:
        subprocess.run(
            [sys.executable, str(PREPARE), str(doc_md), str(staging), "--title", title],
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        fail(f"markdown preparation failed (exit {exc.returncode})")

    if not (staging / "chapters").is_dir():
        fail("prepare step produced no chapters/ directory")

    inject_pandoc_compat(staging)


def write_effective_manifest(manifest: dict, staging: Path, dest: Path) -> None:
    """The input manifest, with ``source`` rewritten to the LaTeX staging dir.

    Table-fitting defaults ON for Markdown sources (there is no hand-tuned LaTeX
    to preserve), unless the manifest set it explicitly."""
    effective = dict(manifest)
    effective["source"] = {"kind": "latex", "path": str(staging)}
    effective.setdefault("fit_tables", True)
    dest.write_text(yaml.safe_dump(effective, sort_keys=False), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("manifest", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    if shutil.which("pandoc") is None:
        fail("pandoc is required to convert Markdown to LaTeX (not found on PATH)")

    manifest = yaml.safe_load(args.manifest.read_text(encoding="utf-8")) or {}
    source = manifest.get("source", {})
    if source.get("kind") != "markdown":
        fail("this front-end handles source.kind: markdown "
             "(for authored LaTeX, run assemble.py directly)")
    src_path = source.get("path")
    if not src_path:
        fail("manifest source.path is required")
    source_md = Path(src_path).expanduser().resolve()
    if not source_md.is_file():
        fail(f"source Markdown not found: {source_md}")

    stem = manifest.get("stem") or args.out.resolve().name
    title = manifest.get("title") or stem

    # Staging must live OUTSIDE OUT_DIR: assemble.py --force wipes OUT_DIR before
    # it reads the (latex) source, so a staging dir under OUT_DIR would vanish.
    staging = Path(tempfile.mkdtemp(prefix="torsor-mdsrc-"))
    try:
        markdown_to_chapters(source_md, staging, title)

        eff_manifest = staging / "build.effective.yaml"
        write_effective_manifest(manifest, staging, eff_manifest)

        cmd = [sys.executable, str(ASSEMBLE), str(eff_manifest), str(args.out)]
        if args.force:
            cmd.append("--force")
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as exc:
            fail(f"assemble.py failed (exit {exc.returncode})")
    finally:
        shutil.rmtree(staging, ignore_errors=True)


if __name__ == "__main__":
    main()
