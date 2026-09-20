#!/usr/bin/env python3
"""Capture actual lockfile audits without fixing, ignoring or concealing findings."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

REPOSITORIES = frozenset({
    'cineharbor-addon-sdk', 'cineharbor-core', 'cineharbor-web',
    'cineharbor-desktop', 'cineharbor-worker', 'cineharbor-download-site',
})
RUST = ('cineharbor-addon-sdk', 'cineharbor-core', 'cineharbor-desktop')
NODE = ('cineharbor-web', 'cineharbor-desktop', 'cineharbor-download-site', 'cineharbor-worker')
ROOT = Path(__file__).resolve().parents[1]


def validate_inputs(value: Any) -> dict[str, str]:
    if not isinstance(value, dict) or value.get('schema_version') != 1:
        raise ValueError('Unsupported audit input schema')
    repositories = value.get('repositories')
    if not isinstance(repositories, dict) or set(repositories) != REPOSITORIES:
        raise ValueError('Expected the six canonical product repositories')
    if any(not isinstance(sha, str) or not re.fullmatch(r'[a-f0-9]{40}', sha)
           for sha in repositories.values()):
        raise ValueError('All audit inputs must be immutable full commit SHAs')
    return repositories


def audit_is_clean(kind: str, code: int, report: Any) -> bool:
    """A failed process, malformed schema, advisory, or warning cannot be a pass."""
    if code != 0 or not isinstance(report, dict) or report.get('error'):
        return False
    if kind == 'rust':
        v = report.get('vulnerabilities')
        return (isinstance(v, dict) and v.get('found') is False
                and type(v.get('count')) is int and v['count'] == 0
                and v.get('list') == [] and isinstance(report.get('warnings'), dict)
                and not any(report['warnings'].values()))
    if kind == 'node':
        metadata = report.get('metadata')
        counts = metadata.get('vulnerabilities') if isinstance(metadata, dict) else None
        required = {'info', 'low', 'moderate', 'high', 'critical'}
        return (isinstance(counts, dict) and required <= counts.keys()
                and all(type(n) is int and n == 0 for n in counts.values())
                and not report.get('advisories') and not report.get('vulnerabilities'))
    return False


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(['git', '-C', str(root), *args], text=True, timeout=120).strip()


def checkout(workspace: Path, name: str, sha: str) -> Path:
    if name not in REPOSITORIES or not re.fullmatch(r'[a-f0-9]{40}', sha):
        raise ValueError('Invalid repository or revision')
    target = workspace / name
    if not target.exists():
        target.mkdir(parents=True)
        git(target, 'init')
        git(target, 'remote', 'add', 'origin', f'https://github.com/CineHarbor/{name}.git')
        git(target, 'fetch', '--depth', '1', 'origin', sha)
        git(target, 'checkout', '--detach', 'FETCH_HEAD')
    if git(target, 'rev-parse', 'HEAD') != sha or git(target, 'status', '--porcelain', '--untracked-files=no'):
        raise RuntimeError('Audit checkout is not the exact clean pinned revision')
    return target


def capture(command: list[str], cwd: Path, out: Path, label: str, timeout: int = 600) -> tuple[dict, Any]:
    """Keep both output streams and status, including timeout/tooling failures."""
    try:
        result = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, timeout=timeout, check=False)
        code, stdout, stderr = result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired as exc:
        code, stdout, stderr = 124, exc.stdout or b'', exc.stderr or b''
    except OSError:
        code, stdout, stderr = 127, b'', b'Audit executable unavailable\n'
    out.mkdir(parents=True, exist_ok=True)
    (out / f'{label}.stdout').write_bytes(stdout)
    (out / f'{label}.stderr').write_bytes(stderr)
    try:
        parsed = json.loads(stdout)
    except (ValueError, UnicodeError):
        parsed = None
    return ({'command': command, 'exit_code': code,
             'stdout_sha256': hashlib.sha256(stdout).hexdigest(),
             'stderr_sha256': hashlib.sha256(stderr).hexdigest()}, parsed)


def run(kind: str, name: str, target: Path, out: Path, sha: str, database: Path | None) -> bool:
    out.mkdir(parents=True, exist_ok=True)
    lock_name = 'Cargo.lock' if kind == 'rust' else ('package-lock.json' if name == 'cineharbor-worker' else 'pnpm-lock.yaml')
    lock = target / lock_name
    before = hashlib.sha256(lock.read_bytes()).hexdigest()
    record: dict[str, Any] = {'schema_version': 1, 'repository': f'CineHarbor/{name}',
        'revision': sha, 'tree': git(target, 'rev-parse', 'HEAD^{tree}'),
        'kind': kind, 'lock_file': lock_name, 'lock_sha256': before,
        'observed_at': datetime.now(timezone.utc).isoformat(), 'steps': [],
        'license_review_approved': False, 'release_ready': False}
    install_ok = True
    if kind == 'node':
        npm = name == 'cineharbor-worker'
        command = ['npm', 'ci', '--ignore-scripts', '--no-audit', '--no-fund'] if npm else ['pnpm', 'install', '--frozen-lockfile', '--ignore-scripts']
        step, _ = capture(command, target, out, 'install')
        record['steps'].append(step)
        install_ok = step['exit_code'] == 0
        audit_command = ['npm' if npm else 'pnpm', 'audit', '--json']
        audit_cwd = target
        if not npm and install_ok:
            step, licenses = capture(['pnpm', 'licenses', 'list', '--json'], target, out, 'license-inventory')
            record['steps'].append(step)
            record['license_inventory_collected'] = step['exit_code'] == 0 and isinstance(licenses, (dict, list))
    else:
        if database is None:
            raise ValueError('Rust audits require an explicitly captured advisory database')
        record['advisory_db_revision'] = git(database, 'rev-parse', 'HEAD')
        # Independent working directory avoids adopting repository audit ignore settings.
        audit_cwd = out.resolve()
        audit_command = ['cargo', 'audit', '--json', '--deny', 'warnings', '--no-fetch',
                         '--db', str(database.resolve()), '--file', str(lock.resolve())]
    step, report = capture(audit_command, audit_cwd, out, 'audit')
    record['steps'].append(step)
    record['source_unchanged'] = (before == hashlib.sha256(lock.read_bytes()).hexdigest()
                                and not git(target, 'status', '--porcelain', '--untracked-files=no'))
    clean = install_ok and record['source_unchanged'] and audit_is_clean(kind, step['exit_code'], report)
    record['status'] = 'PASS' if clean else 'FINDINGS_OR_ERROR'
    (out / 'summary.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({'repository': name, 'kind': kind, 'status': record['status']}))
    return clean


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('kind', choices=['node', 'rust'])
    parser.add_argument('--repository', choices=sorted(REPOSITORIES))
    parser.add_argument('--workspace', type=Path, default=ROOT / 'audit-workspace')
    parser.add_argument('--output', type=Path, default=ROOT / 'audit-evidence')
    parser.add_argument('--database', type=Path)
    args = parser.parse_args()
    inputs = validate_inputs(json.loads((ROOT / 'docs/releases/1.0.0/audit-inputs.json').read_text()))
    names = [args.repository] if args.repository else list(RUST if args.kind == 'rust' else NODE)
    if any(name not in (RUST if args.kind == 'rust' else NODE) for name in names):
        parser.error('Repository does not have the requested package ecosystem')
    ok = True
    for name in names:
        out = args.output.resolve() / f'{name}-{args.kind}'
        try:
            target = checkout(args.workspace.resolve(), name, inputs[name])
            ok = run(args.kind, name, target, out, inputs[name], args.database) and ok
        except Exception as exc:
            out.mkdir(parents=True, exist_ok=True)
            (out / 'failure.json').write_text(json.dumps({'status': 'ERROR', 'error_type': type(exc).__name__,
                'repository': name, 'revision': inputs[name], 'release_ready': False}) + '\n')
            print(f'{name}: ERROR ({type(exc).__name__})', file=sys.stderr)
            ok = False
    return 0 if ok else 1

if __name__ == '__main__':
    raise SystemExit(main())
