import importlib.util
from pathlib import Path
import tempfile
import types
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / 'plugins/torsor-writing/skills/write-critical-guide/tools/annotate_tex.py'
spec = importlib.util.spec_from_file_location('annotate_tex', TOOL)
annotate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(annotate)
FIXTURE = ROOT / 'tests/fixtures/review'


class ReviewFixtureTests(unittest.TestCase):
    def test_ledger_generates_located_notes_and_issue_list(self):
        ledger = annotate.load_ledger(FIXTURE / 'issues.yaml')
        with tempfile.TemporaryDirectory() as out:
            args = types.SimpleNamespace(outdir=out, verbose=False)
            self.assertEqual(annotate.cmd_check(ledger, args), 0)
            annotate.cmd_annotate(ledger, args)
            annotate.cmd_issues_md(ledger, args)
            issue_list = (Path(out) / '02-issues.md').read_text()
            for issue in ledger['issues']:
                self.assertIn(issue['id'], issue_list)
                filename = ledger['categories'][issue['category']]['output']
                source = (Path(out) / filename).read_text()
                self.assertIn(issue['anchor'], source)
                self.assertIn(issue['id'], source)
            self.assertIn('$n-1$', issue_list)

    def test_documentation_anchor_resolves_in_fixture(self):
        doc = (TOOL.parent.parent / 'references/issue-model.md').read_text()
        schema = yaml.safe_load(doc.split('```yaml\n', 1)[1].split('```', 1)[0])
        source_lines = (FIXTURE / 'paper.tex').read_text().splitlines()
        for issue in schema['issues']:
            self.assertEqual(sum(issue['anchor'] in line for line in source_lines), 1)

    def test_stale_fixture_anchor_is_rejected(self):
        ledger = annotate.load_ledger(FIXTURE / 'issues.yaml')
        ledger['issues'][0]['anchor'] = 'This sentence is absent from the fixture.'
        with self.assertRaises(annotate.LedgerError):
            annotate.cmd_check(ledger, types.SimpleNamespace(verbose=False))


if __name__ == '__main__':
    unittest.main()
