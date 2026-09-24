"""Verify the immutable SFCP release and recovered source; optionally package it.

This intentionally does not publish a Spriggit rebuild: conversion differences
remain unresolved. Any source edit fails the frozen-baseline gate.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / 'baseline' / 'manifest.json'


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def source_digest(path):
    # Git may check text out with CRLF on Windows and LF on Linux.
    if path.suffix.lower() in ('.yaml', '.json', '.psc', '.cmd', '.meta', '.afx') or path.name == '.spriggit':
        return hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest()
    return digest(path)


def checked_path(relative):
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError(f'Path outside repository: {relative}')
    return path


def verify():
    manifest = json.loads(LOCK.read_text(encoding='utf-8'))
    problems = []
    expected = manifest['recovered_source_sha256']
    actual_paths = set()
    for relative in manifest['source_roots']:
        path = checked_path(relative)
        if path.is_dir():
            actual_paths.update(p.relative_to(ROOT).as_posix() for p in path.rglob('*') if p.is_file())
        elif path.is_file():
            actual_paths.add(relative)
    for relative in sorted(actual_paths - expected.keys()):
        problems.append(f'Unexpected source file: {relative}')
    for relative, sha in expected.items():
        path = checked_path(relative)
        if not path.is_file() or source_digest(path) != sha:
            problems.append(f'Missing or modified source: {relative}')
    for entry in manifest['release_files']:
        path = checked_path(entry['path'])
        if not path.is_file() or digest(path) != entry['sha256']:
            problems.append(f'Release file mismatch: {entry["path"]}')
    if problems:
        raise ValueError('\n'.join(problems) + '\nBaseline verification failed. Do not refresh the lock to approve gameplay changes; first resolve the source-build gate documented in Docs/BASELINE.md.')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package', type=Path, help='Write a ZIP of the verified original ESM and BA2')
    args = parser.parse_args()
    try:
        manifest = verify()
        if args.package:
            output = args.package.resolve()
            protected = [checked_path(e['path']) for e in manifest['release_files']] + [LOCK]
            protected.extend(checked_path(p) for p in manifest['source_roots'])
            if any(output == p or (p.is_dir() and output.is_relative_to(p)) for p in protected):
                raise ValueError('Output would overwrite baseline evidence')
            output.parent.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
                for entry in manifest['release_files']:
                    path = checked_path(entry['path'])
                    info = zipfile.ZipInfo(path.name, date_time=(2024, 9, 30, 0, 0, 0))
                    info.compress_type = zipfile.ZIP_DEFLATED
                    archive.writestr(info, path.read_bytes())
            print(f'Packaged verified SFCP 1.0.0 reference: {output}')
        print(f'PASS: {len(manifest["release_files"])} release files and {len(manifest["recovered_source_sha256"])} source files match the frozen baseline.')
        print('Source conversion is NOT approved for gameplay publication; see Docs/BASELINE.md.')
        return 0
    except (ValueError, OSError, KeyError) as error:
        print(error, file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
