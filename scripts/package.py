"""Copy the sole application HTML and supporting release artifacts without assembly."""
import argparse
import hashlib
import pathlib
import re
import shutil
import subprocess
from check_artifact_names import check, expected_names


def package(source, destination):
    """Validate source/version, copy exact HTML bytes and emit a checked inventory."""
    source, destination = pathlib.Path(source), pathlib.Path(destination)
    version = (source/'VERSION').read_text().strip()
    names = expected_names(version)
    html = (source/'tetris.html').read_text()
    match = re.search(r'<meta name="app-version" content="([^"]+)">', html)
    if not match or match[1] != version:
        raise ValueError('HTML app-version and VERSION must agree')
    required = {'tetris.html':source/'tetris.html', 'README.md':source/'README.md'}
    if 'session.schema.json' in names:
        required['session.schema.json'] = source/'docs/dev/contracts/session.schema.json'
    if any(not p.is_file() or p.is_symlink() for p in required.values()):
        raise ValueError('Required ordinary source artifact is missing')
    destination.mkdir(parents=True, exist_ok=True)
    for name, path in required.items():
        shutil.copyfile(path, destination/name)
    result = subprocess.run(['git','rev-parse','HEAD'],cwd=source,text=True,capture_output=True)
    revision = result.stdout.strip() if result.returncode == 0 else 'main'
    readme = (destination/'README.md').read_text()
    def link(match):
        label, target = match.groups()
        if '://' in target or target.startswith('#') or target in names:
            return match[0]
        return '['+label+'](https://github.com/pchemguy/SDD-Manager-Demo-Tetris-ChatGPT-SinglePage-Autodoc-V3/blob/'+revision+'/'+target+')'
    (destination/'README.md').write_text(re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link, readme))
    sums = ''.join(hashlib.sha256((destination/name).read_bytes()).hexdigest()+'  '+name+'\n' for name in sorted(required))
    (destination/'SHA256SUMS').write_text(sums)
    check(destination, version)
    return version


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parents[1])
    parser.add_argument('--out',type=pathlib.Path,default=pathlib.Path('dist'))
    args = parser.parse_args()
    try:
        version = package(args.source,args.out)
    except (OSError, ValueError) as error:
        parser.exit(1,str(error)+'\n')
    print('Packaged version '+version+'; stable names and checksums passed.')
