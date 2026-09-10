from pathlib import Path
import re
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
if errors:
    raise SystemExit('\n'.join(errors))
print('Validated 10 skills and their local reference links.')
