import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
REL = Path('plugins/torsor-writing')


class AssetSyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.plugin = self.base / 'repo' / REL
        (self.plugin / 'scripts').mkdir(parents=True)
        for name in ('sync_assets.py', 'audit_public.py'):
            shutil.copy2(ROOT / REL / 'scripts' / name, self.plugin / 'scripts' / name)
        for name in ('assets/reference', 'tools/tex2torsor', 'assets/prose'):
            p = self.plugin / name
            p.mkdir(parents=True)
            (p / 'existing.txt').write_text('Existing snapshot')
        self.lab = self.base / 'source'
        self.source('software/shelf/refactor/manual/latex/main.tex', 'SOURCE_PERSON')
        self.source('software/shelf/refactor/manual/latex/chapters/00-preface.tex', 'Generic preface')
        self.source('research/artifacts/src/artifacts.tex', '\\documentclass{article}\n\\begin{document}\nPRIVATE_BODY\n')
        self.source('software/environs/envtools/manual/tex2torsor/converter.py', '# SOURCE_PERSON\n')

    def source(self, relative, content):
        p = self.lab / relative
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)

    def run_sync(self, expected):
        env = os.environ.copy()
        env.pop('TORSOR_AUDIT_DENYLIST', None)
        env['LAB'] = str(self.lab)
        p = subprocess.run([sys.executable, str(self.plugin / 'scripts/sync_assets.py')],
                           env=env, capture_output=True, text=True)
        self.assertEqual(p.returncode, expected, p.stdout + p.stderr)

    def rules(self, text='s/SOURCE_PERSON/torsor lab/g;'):
        (self.plugin / 'scripts/sanitize.local').write_text(text)

    def unchanged(self):
        for relative in ('assets/reference', 'tools/tex2torsor', 'assets/prose'):
            p = self.plugin / relative
            self.assertEqual([f.name for f in p.iterdir()], ['existing.txt'])

    def test_missing_or_empty_rules_do_not_modify_assets(self):
        self.run_sync(1)
        self.unchanged()
        self.rules('')
        self.run_sync(1)
        self.unchanged()

    def test_invalid_rules_do_not_modify_assets(self):
        self.rules('this is not valid Perl {')
        self.run_sync(1)
        self.unchanged()

    def test_failed_audit_does_not_modify_assets(self):
        self.rules()
        self.source('software/shelf/refactor/manual/latex/main.tex', 'arXiv:' + '.'.join(('0000', '00001')))
        self.run_sync(1)
        self.unchanged()

    def test_sanitized_import_excludes_body_and_preserves_prose(self):
        self.rules()
        self.run_sync(0)
        self.assertEqual((self.plugin / 'assets/reference/shelf-main.tex').read_text(), 'torsor lab')
        self.assertNotIn('PRIVATE_BODY', (self.plugin / 'assets/reference/artifacts.tex').read_text())
        self.assertEqual((self.plugin / 'tools/tex2torsor/converter.py').read_text(), '# torsor lab\n')
        self.assertTrue((self.plugin / 'assets/prose/existing.txt').is_file())

    def test_local_denylist_is_used_for_imports(self):
        self.rules()
        repo = self.plugin.parents[1]
        subprocess.run(['git', '-C', str(repo), 'init', '-q'], check=True)
        terms = self.base / 'private-terms.txt'
        terms.write_text('Generic preface\n')
        subprocess.run(['git', '-C', str(repo), 'config', 'torsor.auditDenylist', str(terms)], check=True)
        self.run_sync(1)
        self.unchanged()


if __name__ == '__main__':
    unittest.main()
