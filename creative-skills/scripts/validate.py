from pathlib import Path
import re
import json
import hashlib
root = Path(__file__).resolve().parents[1]
errors = []
for skill in sorted((root / 'skills').iterdir()):
    entry = skill / 'SKILL.md'
    text = entry.read_text()
    if not text.startswith('---\nname: ' + skill.name + '\n') or '\ndescription: ' not in text:
        errors.append(f'{entry}: invalid metadata')
    for doc in skill.rglob('*.md'):
        for link in re.findall(r'\]\(([^)]+)\)', doc.read_text()):
            if '://' in link or link.startswith('#'):
                continue
            target = (doc.parent / link.split('#')[0]).resolve()
            if not target.is_relative_to(skill.resolve()) or not target.is_file():
                errors.append(f'{doc}: invalid link {link}')
provenance = json.loads((root / 'provenance.json').read_text())
for name, expected in provenance['originalFiles'].items():
    path = root / 'archive/bridge-ae' / name
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        errors.append(f'Archived source differs from recorded provenance: {name}')
if errors:
    raise SystemExit('\n'.join(errors))
skills = sorted((root / 'skills').iterdir())
print(f'Validated {len(skills)} skills and their local reference links.')
