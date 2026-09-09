#!/usr/bin/env python3
"""Inspect working files, index, and optionally all Git history for disclosure patterns.

--revision also checks an outgoing object with no local ref. --directory checks an
unversioned import. An optional private UTF-8 denylist contains literal substrings,
one per line. Whitespace is normalized so a name split across lines still matches.
Neither denylist values nor matching content are printed. Provenance needs manual review.
"""
import argparse
import ast
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
IDENTIFIER = re.compile(r"(?<![\d.])([0-9]{4}\.[0-9]{4,5})(?:v[0-9]+)?(?![0-9])", re.I)
PATTERNS = [
    (r"(?:arxiv:|arxiv\.org/(?:abs|pdf|e-print)/)[a-z-]+(?:\.[a-z]+)?/[0-9]{7}", "legacy arXiv identifier"),
    (r"(?<![\w.])10\.[0-9]{4,}/[A-Za-z0-9./_-]+", "DOI"),
    (r"(?<![A-Za-z])[A-Z]{2,}-D-[0-9]{2}-[0-9]{3,}", "submission identifier"),
    (r"/(?:Users|home)/[A-Za-z0-9_.-]+|[A-Z]:\\Users\\[^\\\s]+|CloudStorage[/]Dropbox", "personal path"),
    (r"-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|AKIA[A-Z0-9]{16}|sk-(?:proj-|ant-)?[A-Za-z0-9_-]{25,}|xox[baprs]-[A-Za-z0-9-]{20,}", "credential pattern"),
]
PATTERNS = [(re.compile(p, re.I), label) for p, label in PATTERNS]
AUTHORS = re.compile(r'^\s*(?:authors|"authors")\s*:\s*(.*)$', re.M)
PLACEHOLDER_AUTHORS = {"A. Author", "B. Coauthor", "C. Author", "D. Author", "...", "<AUTHORS>", "torsor lab"}
PRIVATE_FILE = re.compile(r"(?:^|/)(?:[^/]*\.local|[^/]*\.bundle|\.env(?:\.[^/]*)?|[^/]*\.(?:pem|key)|CLEANUP[^/]*|cleanup-(?:audit|private)[^/]*)$", re.I)


class AuditError(Exception):
    pass


def git(*args, data=None):
    try:
        p = subprocess.run(["git", "-C", str(ROOT), *args], input=data, capture_output=True)
    except OSError as e:
        raise AuditError("cannot run git") from e
    if p.returncode:
        raise AuditError("git %s failed (exit %d)" % (args[0], p.returncode))
    return p.stdout


def objects(oids):
    """Validate every response header and byte count in a finite Git object batch."""
    oids = sorted(set(oids))
    if not oids:
        return {}
    data = git("cat-file", "--batch", data=("\n".join(oids) + "\n").encode())
    out, pos = {}, 0
    for expected in oids:
        end = data.find(b"\n", pos)
        if end < 0:
            raise AuditError("truncated git object response")
        header = data[pos:end].decode("ascii").split()
        if len(header) != 3 or header[0] != expected or not header[2].isdigit():
            raise AuditError("missing or invalid git object")
        stop = end + 1 + int(header[2])
        if data[stop:stop + 1] != b"\n":
            raise AuditError("truncated git object body")
        out[expected] = (header[1], data[end + 1:stop])
        pos = stop + 1
    if pos != len(data):
        raise AuditError("unexpected trailing git object data")
    return out


def configured_denylist():
    p = subprocess.run(['git', '-C', str(ROOT), 'config', '--local', '--get',
                        'torsor.auditDenylist'], capture_output=True)
    if p.returncode == 1 and not p.stderr:
        return None
    if p.returncode:
        raise AuditError('cannot read private audit configuration')
    value = p.stdout.decode('utf-8').strip()
    if not value:
        raise AuditError('configured private denylist path is empty')
    return value


class Audit:
    def __init__(self, denylist):
        self.findings, self.checked, self.terms = set(), 0, []
        if denylist:
            try:
                lines = Path(denylist).read_text(encoding="utf-8").splitlines()
            except (OSError, UnicodeError) as e:
                raise AuditError("private denylist could not be read") from e
            self.terms = [" ".join(line.casefold().split()) for line in lines if line.strip()]
            if not self.terms:
                raise AuditError("private denylist is empty")

    def flag(self, location, reason):
        self.findings.add((location, reason))

    def text(self, data, location):
        self.checked += 1
        if b"\0" in data:
            self.flag(location, "binary content requires a separate publication review")
        try:
            text = data.decode("utf-8")
        except UnicodeError:
            self.flag(location, "non-UTF-8 content requires a separate publication review")
            text = data.decode("utf-8", errors="replace")
        for pattern, label in PATTERNS:
            for m in pattern.finditer(text):
                self.flag(location + ":" + str(text.count("\n", 0, m.start()) + 1), label)
        for m in IDENTIFIER.finditer(text):
            if m.group(1) != "0000.00000":
                self.flag(location + ":" + str(text.count("\n", 0, m.start()) + 1), "arXiv-shaped identifier")
        for m in AUTHORS.finditer(text):
            # Exempt exact list elements, never the surrounding line or file.
            value = m.group(1).split("#", 1)[0].strip().rstrip(",")
            try:
                names = ast.literal_eval(value)
            except (SyntaxError, ValueError):
                names = None
            if not isinstance(names, list) or not all(isinstance(n, str) and n in PLACEHOLDER_AUTHORS for n in names):
                self.flag(location + ":" + str(text.count("\n", 0, m.start()) + 1), "non-placeholder authors field")
        normalized = " ".join(text.casefold().split())
        if any(term in normalized for term in self.terms):
            self.flag(location, "private denylist match")

    def path(self, name, location):
        if PRIVATE_FILE.search(name):
            self.flag(location, "private-looking file is included")
        self.text(name.encode("utf-8"), location + " (path)")

    def mode(self, mode, location):
        if mode not in ("100644", "100755"):
            self.flag(location, "symlink, submodule, or unsupported file mode")

    def working_and_index(self):
        entries = []
        for record in git("ls-files", "--stage", "-z").split(b"\0"):
            if not record:
                continue
            meta, raw_path = record.split(b"\t", 1)
            mode, oid, stage = meta.decode("ascii").split()
            name = raw_path.decode("utf-8")
            if stage != "0":
                raise AuditError("unmerged index entries")
            self.mode(mode, "index:" + name)
            self.path(name, "index:" + name)
            if mode != "160000":
                entries.append((oid, name))
        batch = objects(oid for oid, _ in entries)
        for oid, name in entries:
            typ, body = batch[oid]
            if typ != "blob":
                raise AuditError("index entry is not a blob")
            self.text(body, "index:" + name)
        paths = git("ls-files", "--cached", "--others", "--exclude-standard", "-z")
        for raw_path in set(paths.split(b"\0")):
            if not raw_path:
                continue
            name = raw_path.decode("utf-8")
            self.path(name, "working:" + name)
            path = ROOT / name
            if path.is_symlink():
                self.flag("working:" + name, "symlink requires publication review")
            elif path.is_file():
                self.text(path.read_bytes(), "working:" + name)

    def history(self, revisions):
        explicit = [git("rev-parse", "--verify", "--end-of-options", rev + "^{object}").decode().strip() for rev in revisions]
        oids = git("rev-list", "--objects", "--no-object-names", "--all", *explicit).decode().splitlines()
        if not oids:
            raise AuditError("no history to inspect")
        batch, locations = objects(oids), {}
        for oid, (typ, body) in batch.items():
            if typ == "commit":
                for record in git("ls-tree", "-rz", "--full-tree", oid).split(b"\0"):
                    if not record:
                        continue
                    meta, raw_path = record.split(b"\t", 1)
                    mode, kind, blob = meta.decode().split()
                    name = raw_path.decode("utf-8")
                    self.mode(mode, oid[:12] + ":" + name)
                    self.path(name, oid[:12] + ":" + name)
                    locations.setdefault(blob, name)
                self.text(body.split(b"\n\n", 1)[-1], "commit:" + oid[:12])
            elif typ == "tag":
                self.text(body.split(b"\n\n", 1)[-1], "tag:" + oid[:12])
        for oid, (typ, body) in batch.items():
            if typ == "blob":
                self.text(body, oid[:12] + ":" + locations.get(oid, "<object>"))
        for name in git("for-each-ref", "--format=%(refname)").decode().splitlines():
            self.text(name.encode(), "ref:" + name)

    def directory(self, path):
        if not path.is_dir():
            raise AuditError("snapshot directory does not exist")
        files = 0
        for p in sorted(path.rglob("*")):
            name = p.relative_to(path).as_posix()
            if p.is_symlink():
                self.flag(name, "symlink requires publication review")
            elif p.is_file():
                files += 1
                self.path(name, name)
                self.text(p.read_bytes(), name)
        if not files:
            raise AuditError("snapshot contains no files")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--history", action="store_true")
    parser.add_argument("--revision", action="append", default=[])
    parser.add_argument("--directory", type=Path)
    parser.add_argument("--denylist", default=os.environ.get("TORSOR_AUDIT_DENYLIST"))
    args = parser.parse_args()
    try:
        if not args.directory and not args.denylist:
            args.denylist = configured_denylist()
        audit = Audit(args.denylist)
        if args.directory:
            if args.history or args.revision:
                raise AuditError("directory and history modes cannot be combined")
            audit.directory(args.directory)
        else:
            actual_root = Path(git("rev-parse", "--show-toplevel").decode().strip()).resolve()
            if actual_root != ROOT:
                raise AuditError("the audit must be run from a standalone repository")
            audit.working_and_index()
            if args.history or args.revision:
                audit.history(args.revision)
        for location, reason in sorted(audit.findings):
            print("  FAIL %s — %s" % (location, reason))
        if audit.findings:
            print("audit-public: FAILED (%d findings)" % len(audit.findings))
            return 1
        print("audit-public: checks passed (%d items); example provenance needs manual review" % audit.checked)
        return 0
    except (AuditError, OSError, UnicodeError, ValueError) as e:
        print("audit-public: ERROR — %s" % e, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
