#!/usr/bin/env python3
"""
tex2torsor — Convert LaTeX documentation to styled HTML via Pandoc.

Usage:
  tex2torsor INPUT.tex [options]

The script:
  1. Reads a mappings YAML config (default: mappings.yaml next to this script).
  2. Writes a temporary Pandoc metadata file from the config.
  3. Invokes Pandoc with filter.lua and template.html from the same directory.
  4. Emits a self-contained or linked HTML file.

To reuse for other projects, point --config at a different mappings YAML.
"""

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional

import json
import yaml


TOOL_DIR = Path(__file__).parent


def die(msg: str) -> None:
    print(f"tex2torsor: {msg}", file=sys.stderr)
    sys.exit(1)


def build_pandoc_cmd(
    input_path: Path,
    output_path: Optional[Path],
    meta_file: Path,
    css_files: list[str],
    toc: bool,
    embed: bool,
    template: Path,
    filter_path: Path,
    resource_path: Path,
    citeproc: bool = False,
    bibliographies: Optional[list[str]] = None,
) -> list[str]:
    cmd = [
        "pandoc",
        str(input_path),
        "--from=latex-smart",
        "--to=html5",
        f"--lua-filter={filter_path}",
        f"--metadata-file={meta_file}",
        f"--template={template}",
        f"--resource-path={resource_path}",
        "--standalone",
        "--number-sections",
    ]

    if toc:
        cmd += ["--toc", "--toc-depth=2"]

    if embed:
        cmd.append("--embed-resources")

    if citeproc:
        cmd.append("--citeproc")
    for bib in bibliographies or []:
        cmd.append(f"--bibliography={bib}")

    for css in css_files:
        cmd.append(f"--css={css}")

    if output_path:
        cmd += ["-o", str(output_path)]

    return cmd


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert LaTeX docs to styled HTML",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input", help="Input .tex file")
    parser.add_argument("-o", "--output", help="Output HTML file (default: stdout)")
    parser.add_argument(
        "-c", "--config",
        default=str(TOOL_DIR / "mappings.yaml"),
        help="Mappings config YAML (default: mappings.yaml beside this script)",
    )
    parser.add_argument(
        "--css", action="append", default=None, metavar="FILE",
        help="CSS file to link (repeatable; overrides config css list)",
    )
    parser.add_argument(
        "--template",
        default=str(TOOL_DIR / "template.html"),
        help="Pandoc HTML template",
    )
    parser.add_argument(
        "--toc", action=argparse.BooleanOptionalAction, default=True,
        help="Include table of contents (default: on)",
    )
    parser.add_argument(
        "--embed", action="store_true", default=False,
        help="Embed CSS inline for a single-file output",
    )
    parser.add_argument(
        "--citeproc", action="store_true", default=False,
        help="Resolve citations with pandoc-citeproc (needs --bibliography)",
    )
    parser.add_argument(
        "--bibliography", action="append", default=None, metavar="FILE",
        help="Bibliography file for --citeproc (repeatable)",
    )
    args = parser.parse_args()

    if not shutil.which("pandoc"):
        die("pandoc not found in PATH — install it first")

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        die(f"input file not found: {args.input}")

    config_path = Path(args.config)
    if not config_path.exists():
        die(f"config file not found: {args.config}")

    with config_path.open() as f:
        config = yaml.safe_load(f) or {}

    mappings = config.get("mappings", {})
    css_from_config = config.get("css", [])
    css_files = args.css if args.css is not None else css_from_config

    filter_path = TOOL_DIR / "filter.lua"
    template_path = Path(args.template)
    output_path = Path(args.output).resolve() if args.output else None

    # Write metadata as JSON — avoids Pandoc's smart-typography mangling of
    # strings like "callout--note" when they pass through YAML metadata files.
    meta = {"tex2torsor": mappings}
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, prefix="tex2torsor_meta_"
    ) as mf:
        json.dump(meta, mf)
        meta_file = Path(mf.name)

    try:
        cmd = build_pandoc_cmd(
            input_path=input_path,
            output_path=output_path,
            meta_file=meta_file,
            css_files=css_files,
            toc=args.toc,
            embed=args.embed,
            template=template_path,
            filter_path=filter_path,
            resource_path=input_path.parent,
            citeproc=args.citeproc,
            bibliographies=args.bibliography,
        )

        result = subprocess.run(cmd, cwd=input_path.parent)
        if result.returncode != 0:
            sys.exit(result.returncode)

        if output_path:
            print(f"Written: {output_path}")

    finally:
        meta_file.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
