#!/usr/bin/env python3
"""Fix all dates in BCG prep HTML to match: Ter 24, Qua 25, Qui 26, Sex 27"""

with open('0_ACTIVE_NOW/BCG_Interview_Prep/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    # Sunday 23 → 22
    ('Domingo 23 Feb', 'Domingo 22 Feb'),
    ('Domingo 23 \u2014', 'Domingo 22 \u2014'),
    ('Dom 23', 'Dom 22'),
    # Monday 24 → 23
    ('Segunda 24 Feb', 'Segunda 23 Feb'),
    ('Segunda 24 \u2014', 'Segunda 23 \u2014'),
    ('Seg 24', 'Seg 23'),
    # Wednesday 26 → 25
    ('Quarta 26 Feb', 'Quarta 25 Feb'),
    ('Quarta 26 \u2014', 'Quarta 25 \u2014'),
    ('Qua 26', 'Qua 25'),
    # Thursday 27 → 26
    ('Quinta 27 Feb', 'Quinta 26 Feb'),
    ('Quinta 27 \u2014', 'Quinta 26 \u2014'),
    ('Qui 27', 'Qui 26'),
    # Friday 28 → 27
    ('Sexta 28 Feb', 'Sexta 27 Feb'),
    ('Sexta 28 \u2014', 'Sexta 27 \u2014'),
    ('Sex 28', 'Sex 27'),
    ('Sexta-feira 28 Feb', 'Sexta-feira 27 Feb'),
]

total = 0
for old, new in replacements:
    count = content.count(old)
    if count > 0:
        content = content.replace(old, new)
        print(f'  OK: "{old}" -> "{new}" ({count}x)')
        total += count

# Also fix range refs
for old, new in [('Ter 24 \u2192 Qui 27', 'Ter 24 \u2192 Qui 26')]:
    count = content.count(old)
    if count > 0:
        content = content.replace(old, new)
        print(f'  OK: "{old}" -> "{new}" ({count}x)')
        total += count

with open('0_ACTIVE_NOW/BCG_Interview_Prep/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f'\nDone! {total} replacements made.')
