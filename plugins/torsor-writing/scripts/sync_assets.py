#!/usr/bin/env python3
"""Refresh reference and converter snapshots after sanitizing and auditing a staging copy."""
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

PLUGIN = Path(__file__).resolve().parents[1]


def main():
    rules_path = PLUGIN / 'scripts/sanitize.local'
    if not rules_path.is_file() or not rules_path.read_text().strip():
        raise RuntimeError('scripts/sanitize.local is required and must contain rules; no assets changed')
    rules = rules_path.read_text()
    # Check the private Perl program before reading or replacing any snapshot.
    subprocess.run(['perl', '-pe', rules], input=b'', capture_output=True, check=True)
    lab = Path(os.environ.get('LAB', str(Path.home() / 'lab')))
    sources = {
        'shelf-main.tex': lab / 'software/shelf/refactor/manual/latex/main.tex',
        'shelf-00-preface.tex': lab / 'software/shelf/refactor/manual/latex/chapters/00-preface.tex',
        'artifacts.tex': lab / 'research/artifacts/src/artifacts.tex',
    }
    converter = lab / 'software/environs/envtools/manual/tex2torsor'
    if not all(p.is_file() for p in sources.values()) or not converter.is_dir():
        raise RuntimeError('LAB is missing required sources; no assets changed')
    article = sources['artifacts.tex'].read_text()
    start = re.search(r'(?m)^[ \t]*\\begin\{document\}', article)
    if not start:
        raise RuntimeError('artifacts source has no document boundary; no assets changed')
    with tempfile.TemporaryDirectory(prefix='.asset-sync-', dir=PLUGIN) as temporary:
        stage = Path(temporary)
        payload = stage / 'payload'
        refs = payload / 'assets/reference'
        refs.mkdir(parents=True)
        for name, source in sources.items():
            if name == 'artifacts.tex':
                (refs / name).write_text(article[:start.start()])
            else:
                shutil.copy2(source, refs / name)
        shutil.copytree(converter, payload / 'tools/tex2torsor', symlinks=True,
                        ignore=shutil.ignore_patterns('.git', '.DS_Store', '__pycache__', '*.pyc'))
        for p in payload.rglob('*'):
            if p.is_file() and not p.is_symlink():
                result = subprocess.run(['perl', '-pe', rules], input=p.read_bytes(),
                                        capture_output=True, check=True)
                p.write_bytes(result.stdout)
        audit_args = [sys.executable, str(PLUGIN / 'scripts/audit_public.py'),
                      '--directory', str(payload)]
        repo = PLUGIN.parents[1]
        if not os.environ.get('TORSOR_AUDIT_DENYLIST') and (repo / '.git').exists():
            config = subprocess.run(['git', '-C', str(repo), 'config', '--local', '--get',
                                     'torsor.auditDenylist'], capture_output=True, text=True)
            if config.returncode == 0:
                if not config.stdout.strip():
                    raise RuntimeError('configured private denylist path is empty')
                audit_args.extend(['--denylist', config.stdout.strip()])
            elif config.returncode != 1 or config.stderr:
                raise RuntimeError('cannot read private audit configuration')
        subprocess.run(audit_args, check=True)
        replaced = []
        try:
            for index, relative in enumerate(('assets/reference', 'tools/tex2torsor')):
                destination = PLUGIN / relative
                previous = stage / ('previous-' + str(index))
                had_previous = destination.exists()
                if had_previous:
                    os.replace(destination, previous)
                replaced.append((destination, previous, had_previous))
                destination.parent.mkdir(parents=True, exist_ok=True)
                os.replace(payload / relative, destination)
        except OSError:
            for destination, previous, had_previous in reversed(replaced):
                if destination.exists():
                    shutil.rmtree(destination)
                if had_previous:
                    os.replace(previous, destination)
            raise
    print('Snapshots sanitized and checked. Review the diff before staging. Prose was not synced.')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, RuntimeError, subprocess.CalledProcessError) as error:
        # The private sanitizer program and its stderr must not be echoed into a log.
        message = 'sanitizer or publication check failed; no staged import was installed' if isinstance(error, subprocess.CalledProcessError) else str(error)
        print('sync-assets: ERROR — ' + message, file=sys.stderr)
        sys.exit(1)
