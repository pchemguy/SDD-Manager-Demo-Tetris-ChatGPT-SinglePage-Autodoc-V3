"""Independently check stable release basenames, inventory and actual byte hashes."""
import argparse
import hashlib
import pathlib
import re


def expected_names(version):
    """Derive the contract's asset set from the delivered capability version."""
    if not re.fullmatch(r'\d+\.\d+\.\d+', version):
        raise ValueError('Expected a stable semantic version')
    major, minor, _ = map(int, version.split('.'))
    names = {'tetris.html', 'README.md', 'SHA256SUMS'}
    if (major, minor) >= (0, 6):
        names.add('session.schema.json')
    return names


def check(directory, version):
    """Reject unexpected/versioned names, links, duplicate entries or altered bytes."""
    directory = pathlib.Path(directory)
    expected = expected_names(version)
    actual = {p.name for p in directory.iterdir()}
    if actual != expected:
        raise ValueError('Artifact names differ from stable contract: ' + ', '.join(sorted(actual)))
    for name in expected:
        p = directory / name
        if p.is_symlink() or not p.is_file():
            raise ValueError('Artifact must be an ordinary file: ' + name)
    entries = {}
    for line in (directory/'SHA256SUMS').read_text().splitlines():
        match = re.fullmatch(r'([0-9a-f]{64})  ([A-Za-z0-9._-]+)', line)
        if not match or match[2] in entries:
            raise ValueError('Malformed or duplicate checksum entry')
        entries[match[2]] = match[1]
    if set(entries) != expected - {'SHA256SUMS'}:
        raise ValueError('Checksum inventory differs from artifact contract')
    for name, digest in entries.items():
        if hashlib.sha256((directory/name).read_bytes()).hexdigest() != digest:
            raise ValueError('Checksum mismatch: ' + name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=pathlib.Path)
    parser.add_argument('--version', required=True)
    args = parser.parse_args()
    try:
        check(args.directory, args.version)
    except (OSError, ValueError) as error:
        parser.exit(1, str(error) + '\n')
    print('Stable artifact names and actual byte hashes verified.')
