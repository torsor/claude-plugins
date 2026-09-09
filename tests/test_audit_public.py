import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
REL = Path('plugins/torsor-writing/scripts')
GIT = shutil.which('git')
# Assemble intentionally rejected values without putting paper identifiers in this source.
BAD_ID = '.'.join(('0000', '00001'))
BAD_PERSON = 'Example Person'


class PublicationAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'repo'
        self.root.mkdir()
        (self.root / REL).mkdir(parents=True)
        for name in ('audit-public.sh', 'audit_public.py'):
            shutil.copy2(ROOT / REL / name, self.root / REL / name)
        self.git('init', '-q')
        self.git('config', 'user.name', 'Fixture Author')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.put('example.md', 'Synthetic documentation.\n')
        self.git('add', '.')
        self.git('commit', '-qm', 'Initial fixture')

    def git(self, *args, data=None):
        p = subprocess.run([GIT, '-C', str(self.root), *args], input=data, text=True, capture_output=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        return p.stdout.strip()

    def put(self, name, text):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)

    def audit(self, *args, expected=1, env=None):
        e = os.environ.copy()
        e.pop('TORSOR_AUDIT_DENYLIST', None)
        if env:
            e.update(env)
        p = subprocess.run([sys.executable, str(self.root / REL / 'audit_public.py'), *args],
                           capture_output=True, text=True, env=e)
        self.assertEqual(p.returncode, expected, p.stdout + p.stderr)
        if expected:
            self.assertNotIn('checks passed', p.stdout)
        return p

    def test_clean_placeholders(self):
        self.put('example.md', 'arXiv:0000.00000v1\nauthors: ["A. Author", "B. Coauthor"]\n')
        self.audit('--history', expected=0)

    def test_basic_patterns(self):
        samples = ['arXiv:' + BAD_ID, '10.' + '12345/synthetic', '-'.join(('TEST','D','26','12345')),
                   'authors: ' + json.dumps([BAD_PERSON]), '/'.join(('', 'Users', 'fixture', 'note'))]
        for sample in samples:
            with self.subTest(sample=sample):
                self.put('example.md', sample)
                self.audit()

    def test_allowlisted_author_does_not_hide_identifier(self):
        self.put('example.md', 'A. Author cites arXiv:' + BAD_ID)
        self.audit()

    def test_allowlisted_author_does_not_hide_another_author(self):
        self.put('example.md', 'authors: ' + json.dumps(['A. Author', BAD_PERSON]))
        self.audit()

    def test_tracked_private_file_is_rejected(self):
        self.put('.gitignore', '*.local\n')
        self.put('example.local', 'Nothing identifying is needed to trigger this check.\n')
        self.git('add', '-f', 'example.local')
        self.audit()

    def test_detector_name_in_prose_is_not_exempt(self):
        self.put('example.md', 'See audit-public.sh for arXiv:' + BAD_ID)
        self.audit()

    def test_bare_identifier_and_url(self):
        for value in (BAD_ID + 'v1', 'https://arxiv.org/abs/' + BAD_ID):
            self.put('example.md', value)
            self.audit()

    def test_staged_content_is_checked(self):
        self.put('example.md', 'arXiv:' + BAD_ID)
        self.git('add', 'example.md')
        self.put('example.md', 'The working file is harmless.\n')
        self.audit()

    def test_git_read_failure_is_an_error(self):
        bindir = Path(self.temp.name) / 'bin'
        bindir.mkdir()
        wrapper = bindir / 'git'
        wrapper.write_text('#!/bin/sh\nif [ "$3" = cat-file ]; then exit 2; fi\nexec ' + shlex.quote(GIT) + ' "$@"\n')
        wrapper.chmod(0o755)
        self.audit('--history', expected=2, env={'PATH': str(bindir) + os.pathsep + os.environ['PATH']})

    def test_commit_messages(self):
        self.git('commit', '--allow-empty', '-qm', 'arXiv:' + BAD_ID)
        self.audit('--history')

    def test_tag_messages(self):
        self.git('tag', '-a', 'fixture', '-m', 'arXiv:' + BAD_ID)
        self.audit('--history')

    def test_historical_content_after_deletion(self):
        self.put('example.md', 'arXiv:' + BAD_ID)
        self.git('add', 'example.md')
        self.git('commit', '-qm', 'Fixture change')
        self.git('rm', '-q', 'example.md')
        self.git('commit', '-qm', 'Remove fixture')
        self.audit(expected=0)
        self.audit('--history')

    def test_identifier_in_filename(self):
        self.put(BAD_ID + '.md', 'Synthetic text')
        self.audit()

    def test_credential_pattern(self):
        self.put('example.md', 'ghp_' + 'x' * 36)
        p = self.audit()
        self.assertNotIn('x' * 36, p.stdout)

    def test_split_name_private_denylist(self):
        denylist = Path(self.temp.name) / 'terms.txt'
        denylist.write_text(BAD_PERSON + '\n')
        self.put('example.md', BAD_PERSON.replace(' ', '\n'))
        p = self.audit('--denylist', str(denylist))
        self.assertNotIn(BAD_PERSON, p.stdout)

    def test_missing_denylist_is_error(self):
        self.audit('--denylist', str(Path(self.temp.name) / 'missing'), expected=2)

    def test_configured_denylist_is_enforced(self):
        denylist = Path(self.temp.name) / 'terms.txt'
        denylist.write_text(BAD_PERSON + '\n')
        self.git('config', '--local', 'torsor.auditDenylist', str(denylist))
        self.put('example.md', BAD_PERSON)
        self.audit()
        denylist.unlink()
        self.audit(expected=2)

    def test_outgoing_object_without_ref(self):
        self.put('example.md', 'arXiv:' + BAD_ID)
        self.git('add', 'example.md')
        tree = self.git('write-tree')
        oid = self.git('commit-tree', tree, data='Synthetic outgoing fixture\n')
        self.git('restore', '--source=HEAD', '--staged', '--worktree', 'example.md')
        self.audit('--history', expected=0)
        self.audit('--history', '--revision', oid)

    def test_historical_path_on_other_branch(self):
        before = self.git('rev-parse', 'HEAD')
        self.git('checkout', '-qb', 'fixture-branch')
        self.put(BAD_ID + '.md', 'Synthetic text')
        self.git('add', '.')
        self.git('commit', '-qm', 'Fixture branch')
        self.git('checkout', '-q', '--detach', before)
        self.audit('--history')

    def test_binary_is_not_silently_skipped(self):
        (self.root / 'binary.dat').write_bytes(b'\x00example')
        self.audit()

    def test_snapshot_directory(self):
        snapshot = Path(self.temp.name) / 'snapshot'
        snapshot.mkdir()
        (snapshot / 'example.md').write_text('Synthetic documentation')
        self.audit('--directory', str(snapshot), expected=0)
        (snapshot / 'example.md').write_text('arXiv:' + BAD_ID)
        self.audit('--directory', str(snapshot))


if __name__ == '__main__':
    unittest.main()
