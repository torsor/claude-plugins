#!/usr/bin/env python3
"""Assemble a self-contained torsor deliverable from a build manifest.

    assemble.py MANIFEST.yaml OUT_DIR [--core CORE_DIR]

The manifest (also copied into the deliverable as build.yaml for provenance)
declares the source, genre, metadata, voice, and enabled features. The assembler
is a *stitcher*, not a brancher:

  - main.tex  = base/preamble.tex + each enabled feature's preamble.tex + body
  - Makefile, formats/, check-build.py, tex2torsor/  are vendored verbatim
  - each enabled feature dir is vendored under features/<name>/
  - each feature's tex2torsor mappings + CSS slices are merged into the vendored
    tex2torsor (assembled, not branched)

Adding a format or feature is a new file/dir in the core; this script does not
change. See docs/specs/2026-07-15-unified-builder-contract-design.md.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import yaml


def fail(msg: str) -> None:
    print(f"assemble: {msg}", file=sys.stderr)
    sys.exit(1)


LATEX_SPECIAL = {
    "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
    "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
    "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
}


def latex_escape(text: str) -> str:
    return "".join(LATEX_SPECIAL.get(ch, ch) for ch in text)


def makefile_escape(text: str) -> str:
    # Make expands $(...); '#' starts a comment. Neutralize both.
    return text.replace("$", "$$").replace("#", r"\#").replace('"', '\\"')


def build_bodymatter(chapters_spec, chapters_dir: Path) -> str:
    """Emit \\frontmatter…\\backmatter from the manifest's chapters spec.

    dict  -> {frontmatter, mainmatter, appendix, backmatter} lists (order kept)
    list  -> all mainmatter
    None  -> glob fallback (00-* is frontmatter, the rest mainmatter)
    """
    def inputs(stems):
        return "\n".join(f"\\input{{chapters/{s}}}" for s in stems)

    if isinstance(chapters_spec, dict):
        front = chapters_spec.get("frontmatter", []) or []
        main = chapters_spec.get("mainmatter", []) or []
        app = chapters_spec.get("appendix", []) or []
        back = chapters_spec.get("backmatter", []) or []
    elif isinstance(chapters_spec, list):
        front, main, app, back = [], chapters_spec, [], []
    else:
        stems = sorted(p.stem for p in chapters_dir.glob("*.tex"))
        front = [s for s in stems if s.startswith("00")]
        main = [s for s in stems if not s.startswith("00")]
        app, back = [], []

    parts = ["\\frontmatter", "\\setcounter{tocdepth}{1}", "\\tableofcontents"]
    if front:
        parts.append(inputs(front))
    parts.append("\\mainmatter")
    if main:
        parts.append(inputs(main))
    if app:
        parts += ["\\appendix", inputs(app)]
    if back:
        parts += ["\\backmatter", inputs(back)]
    return "\n".join(parts)


def assemble_main_tex(core: Path, features: list[str], meta: dict, out_latex: Path,
                      titlepage_path: Path, chapters_spec) -> None:
    preamble = (core / "base" / "preamble.tex").read_text(encoding="utf-8")
    preamble = preamble.replace("@@PDFTITLE@@", latex_escape(meta["title"]))
    preamble = preamble.replace("@@PDFAUTHOR@@", latex_escape(meta["author"]))

    parts = [preamble]
    for feat in features:
        frag = core / "features" / feat / "preamble.tex"
        if frag.exists():
            parts.append(f"\n% ==== feature: {feat} ====\n" + frag.read_text(encoding="utf-8"))

    cover = meta.get("cover_rel")
    if cover:
        cover_block = f"  \\vspace{{0.75cm}}\n  \\includegraphics[width=2.35in]{{{cover}}}\\par\n"
        top_space, spacer = "2cm", "0.75cm"
    else:
        cover_block, top_space, spacer = "", "3cm", "3cm"

    titlepage = titlepage_path.read_text(encoding="utf-8")
    for k, v in {
        "@@TITLE@@": latex_escape(meta["title"]),
        "@@SUBTITLE@@": latex_escape(meta.get("subtitle", "")),
        "@@TAGLINE@@": latex_escape(meta.get("tagline", "")),
        "@@BLURB@@": latex_escape(meta.get("blurb", meta["title"])),
        "@@TOPSPACE@@": top_space,
        "@@SPACER@@": spacer,
        "@@COVER_BLOCK@@": cover_block,
    }.items():
        titlepage = titlepage.replace(k, v)

    body = (core / "base" / "body.tex.tmpl").read_text(encoding="utf-8")
    body = body.replace("@@TITLEPAGE@@", titlepage)
    body = body.replace("@@BODYMATTER@@", build_bodymatter(chapters_spec, out_latex / "chapters"))

    (out_latex / "main.tex").write_text("\n".join(parts) + "\n" + body, encoding="utf-8")


def write_style(out: Path, core: Path, prose_base: str | None, voice: str) -> None:
    """Assemble out/latex/STYLE.md: a header comment recording the voice, then the
    base prose file, then the chosen voice file (both optional — skip if missing).

    The prose library lives at core.parent.parent / "assets" / "prose"
    (tools/../assets/prose = plugins/torsor-writing/assets/prose). Missing prose
    files are skipped gracefully; STYLE.md always gets at least the header."""
    prose = core.parent.parent / "assets" / "prose"
    parts = [f"<!-- Voice: {voice}. Assembled by the torsor unified builder. -->", ""]

    if prose_base:
        base_file = prose / f"{prose_base}.md"
        if base_file.exists():
            parts.append(base_file.read_text(encoding="utf-8").rstrip("\n"))
            parts.append("")

    voice_file = prose / "voices" / f"{voice}.md"
    if voice_file.exists():
        parts.append(voice_file.read_text(encoding="utf-8").rstrip("\n"))
        parts.append("")

    (out / "latex" / "STYLE.md").write_text("\n".join(parts), encoding="utf-8")


def fresh_tree(dst: Path, src: Path) -> None:
    """Copy a directory tree, replacing any existing dst (idempotent re-vendoring)."""
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def merge_html_slices(core: Path, features: list[str], out: Path) -> None:
    """Build the deliverable's tex2torsor mappings/CSS from the clean core base +
    each enabled feature's slice, overwriting the vendored (legacy) copies."""
    mappings_path = out / "tex2torsor" / "mappings.yaml"
    mappings = yaml.safe_load((core / "base" / "mappings.yaml").read_text(encoding="utf-8")) or {}
    mappings.setdefault("mappings", {})
    css_path = out / "tex2torsor" / "css" / "doc.css"

    for feat in features:
        fdir = core / "features" / feat
        fmap = fdir / "mappings.yaml"
        if fmap.exists():
            extra = yaml.safe_load(fmap.read_text(encoding="utf-8")) or {}
            for section, entries in (extra.get("mappings") or {}).items():
                mappings["mappings"].setdefault(section, {}).update(entries or {})
        fcss = fdir / "style.css"
        if fcss.exists():
            with css_path.open("a", encoding="utf-8") as f:
                f.write(f"\n/* ==== feature: {feat} ==== */\n")
                f.write(fcss.read_text(encoding="utf-8"))

    mappings_path.write_text(yaml.safe_dump(mappings, sort_keys=False), encoding="utf-8")


def write_config_mk(out: Path, stem: str, meta: dict) -> None:
    cover = meta.get("cover_rel")
    epub_cover = f"--epub-cover-image={cover}" if cover else ""
    lines = [
        "# Per-document build values (generated by assemble.py). Edit the manifest, re-assemble.",
        f"STEM := {stem}",
        f"DOC_TITLE := {makefile_escape(meta['title'])}",
        f"DOC_AUTHOR := {makefile_escape(meta['author'])}",
        f"EPUB_COVER := {epub_cover}",
    ]
    (out / "config.mk").write_text("\n".join(lines) + "\n", encoding="utf-8")


GITIGNORE = """# Built outputs
html/
epub/
markdown/

# PDF + LaTeX intermediates
latex/*.pdf
latex/*.aux
latex/*.log
latex/*.out
latex/*.toc
latex/*.fls
latex/*.fdb_latexmk
latex/*.synctex.gz
latex/chapters/*.aux
latex/.build/

.DS_Store
"""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("manifest", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--core", type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--in-place", action="store_true",
                    help="assemble around chapters already at OUT/latex/chapters "
                         "(the authoring flow): do not wipe OUT, do not copy a source")
    args = ap.parse_args()

    core = args.core.resolve()
    tools = core.parent
    manifest = yaml.safe_load(args.manifest.read_text(encoding="utf-8")) or {}

    # Paths in the manifest (cover, bibliography, source) are resolved relative to
    # the manifest's own directory, not the process cwd. For --in-place that dir is
    # the doc dir, so a natural `cover: latex/icon.png` resolves as authors expect.
    manifest_dir = args.manifest.resolve().parent

    def resolve_rel(p: str) -> Path:
        q = Path(p).expanduser()
        return q if q.is_absolute() else (manifest_dir / q)

    out = args.out.resolve()
    src = None
    if args.in_place:
        if not (out / "latex" / "chapters").is_dir():
            fail(f"--in-place: expected authored chapters at {out}/latex/chapters")
    else:
        source = manifest.get("source", {})
        if source.get("kind") != "latex":
            fail("assemble.py handles source.kind: latex (authored chapters) or "
                 "--in-place; for Markdown use frontend_markdown.py.")
        src = resolve_rel(source["path"]).resolve()
        if not (src / "chapters").is_dir():
            fail(f"source has no chapters/ directory: {src}")
        if out.exists() and any(out.iterdir()):
            if not args.force:
                fail(f"output dir not empty: {out} (pass --force or --in-place)")
            shutil.rmtree(out)

    stem = manifest.get("stem") or out.name
    meta = {
        "title": manifest.get("title") or stem,
        "subtitle": manifest.get("subtitle", ""),
        "tagline": manifest.get("tagline", ""),
        "blurb": manifest.get("blurb", ""),
        "author": manifest.get("author", "torsor lab"),
    }

    # Resolve genre: default features + title page (a genre may override the base one).
    titlepage_path = core / "base" / "titlepage.tex"
    default_features: list[str] = []
    prose_base: str | None = None
    genre_name = manifest.get("genre")
    if genre_name:
        gdir = core / "genres" / genre_name
        if not gdir.is_dir():
            fail(f"unknown genre: {genre_name}")
        gy = yaml.safe_load((gdir / "genre.yaml").read_text(encoding="utf-8")) or {} \
            if (gdir / "genre.yaml").exists() else {}
        default_features = list(gy.get("default_features") or [])
        prose_base = gy.get("prose_base")
        # Title page precedence: genre's own file > genre.yaml `titlepage` pointer > base.
        if (gdir / "titlepage.tex").exists():
            titlepage_path = gdir / "titlepage.tex"
        elif gy.get("titlepage"):
            cand = core / gy["titlepage"]
            if not cand.exists():
                fail(f"genre {genre_name}: titlepage not found: {gy['titlepage']}")
            titlepage_path = cand

    # features: manifest `features` replaces the genre default; `extra_features`
    # appends to it (so e.g. a manual that also needs math sets extra_features: [math]).
    features = list(manifest["features"]) if manifest.get("features") is not None else list(default_features)
    for f in (manifest.get("extra_features") or []):
        if f not in features:
            features.append(f)
    chapters_spec = manifest.get("chapters")

    # Layout
    (out / "latex" / "chapters").mkdir(parents=True, exist_ok=True)
    (out / "latex" / "assets").mkdir(parents=True, exist_ok=True)
    if src is not None:  # copy-from-source mode (in-place leaves existing chapters be)
        shutil.copytree(src / "chapters", out / "latex" / "chapters", dirs_exist_ok=True)
        if (src / "assets").is_dir():
            shutil.copytree(src / "assets", out / "latex" / "assets", dirs_exist_ok=True)

    # Opt-in table-fitting (front-end normalization; off by default so authored
    # LaTeX is never silently rewritten — from-markdown turns it on).
    if manifest.get("fit_tables"):
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from normalize_tables import normalize_tables
        for tex in (out / "latex" / "chapters").glob("*.tex"):
            tex.write_text(normalize_tables(tex.read_text(encoding="utf-8")), encoding="utf-8")

    cover = manifest.get("cover")
    if cover:
        cov = resolve_rel(cover).resolve()
        if not cov.is_file():
            fail(f"cover not found: {cov}")
        dest = out / "latex" / "assets" / f"cover{cov.suffix.lower() or '.png'}"
        if cov.resolve() != dest.resolve():  # in-place: cover may already be at dest
            shutil.copy2(cov, dest)
        meta["cover_rel"] = f"assets/{dest.name}"

    # Bibliography: vendor the .bib as references.bib and turn on the bib feature.
    bib = manifest.get("bibliography")
    if bib:
        bibp = resolve_rel(bib).resolve()
        if not bibp.is_file():
            fail(f"bibliography not found: {bibp}")
        bibdest = out / "latex" / "references.bib"
        if bibp.resolve() != bibdest.resolve():  # in-place: bib may already be at dest
            shutil.copy2(bibp, bibdest)
        if "bib" not in features:
            features.append("bib")

    # Vendor the core verbatim (idempotent, so --in-place can re-run)
    shutil.copy2(core / "Makefile", out / "Makefile")
    fresh_tree(out / "formats", core / "formats")
    fresh_tree(out / "tex2torsor", tools / "tex2torsor")
    shutil.copy2(tools / "check-build.py", out / "check-build.py")
    for feat in features:
        fdir = core / "features" / feat
        if not fdir.is_dir():
            fail(f"unknown feature: {feat}")
        fresh_tree(out / "features" / feat, fdir)

    # Assemble (stitch, don't branch)
    assemble_main_tex(core, features, meta, out / "latex", titlepage_path, chapters_spec)
    write_style(out, core, prose_base, manifest.get("voice", "01-direct"))
    merge_html_slices(core, features, out)
    write_config_mk(out, stem, meta)
    (out / ".gitignore").write_text(GITIGNORE, encoding="utf-8")
    if args.manifest.resolve() != (out / "build.yaml").resolve():  # provenance
        shutil.copy2(args.manifest, out / "build.yaml")

    print(f"Assembled deliverable: {out}")
    print(f"  stem: {stem}   features: {features or '(none)'}")
    print("Next: cd into it and run `make all`.")


if __name__ == "__main__":
    main()
