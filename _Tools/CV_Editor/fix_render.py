#!/usr/bin/env python3
"""Fix corrupted renderPreview lines in cv_platform.html"""

with open('cv_platform.html', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
pad = '                        '

# The correct JavaScript lines for jobs section
jobs_lines = [
    pad + "const [companyName, companyLoc] = splitPipe(job.company);",
    pad + "const [roleTitle, roleDates] = splitPipe(job.role);",
    pad + """html += `<h3 class="cv-company">${esc(companyName)}${companyLoc ? `<span class="cv-location">${esc(companyLoc)}</span>` : ''}</h3>`;""",
    pad + """html += `<p class="cv-role">${esc(roleTitle)}${roleDates ? `<span class="cv-dates">${esc(roleDates)}</span>` : ''}</p>`;""",
]

# The correct JavaScript lines for education section
edu_lines = [
    pad + "const [instName, instLoc] = splitPipe(sch.institution);",
    pad + "const [degName, degExtra] = splitPipe(sch.degree);",
    pad + """html += `<h3 class="cv-company">${esc(instName)}${instLoc ? `<span class="cv-location">${esc(instLoc)}</span>` : ''}</h3>`;""",
    pad + """html += `<p class="cv-role">${esc(degName)}${degExtra ? `<span class="cv-dates">${esc(degExtra)}</span>` : ''}</p>`;""",
]

# Fix jobs section
for i, line in enumerate(lines):
    if 'const [companyName, companyLoc] = esc(companyName)' in line:
        print(f'Found corrupted jobs block at line {i+1}')
        for j in range(4):
            lines[i + j] = jobs_lines[j]
        print(f'Fixed lines {i+1}-{i+4}')
        break

# Fix education section
for i, line in enumerate(lines):
    if 'const [instName, instLoc] = splitPesc(instName)' in line:
        print(f'Found corrupted education block at line {i+1}')
        for j in range(4):
            lines[i + j] = edu_lines[j]
        print(f'Fixed lines {i+1}-{i+4}')
        break

content = '\n'.join(lines)
with open('cv_platform.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
