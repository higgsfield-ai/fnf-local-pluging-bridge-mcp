import argparse
from pathlib import Path
parser = argparse.ArgumentParser(description='Install the local After Effects entry skill without overwriting existing files.')
parser.add_argument('--skills-dir', type=Path, default=Path.home() / '.agents/skills')
args = parser.parse_args()
source = Path(__file__).resolve().parents[1] / 'skills/use-after-effects'
target = args.skills_dir.expanduser().absolute() / 'use-after-effects'
if target.exists() or target.is_symlink():
    if target.resolve() != source:
        raise SystemExit(f'Refusing to overwrite existing skill: {target}')
    print(f'Already installed: {target}')
else:
    target.parent.mkdir(parents=True, exist_ok=True)
    target.symlink_to(source, target_is_directory=True)
    print(f'Installed: {target} -> {source}')
