#!/usr/bin/env python3
"""
Apply all section replacements to index.html:
1. Insert case examples after frameworks section (before math)
2. Replace math section with new EN/PT version
3. Add drills header (CaseCoach drill types + chart types) before existing exercises
4. Insert scoring rubric into BCG Patterns section
5. Update Portuguese section subtitle
6. Update Creativity section subtitle
"""
import os

BASE = os.path.join(os.path.dirname(__file__), "..", "0_ACTIVE_NOW", "BCG_Interview_Prep")
HTML_PATH = os.path.join(BASE, "index.html")
SECTIONS_DIR = os.path.join(BASE, "sections")

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

lines = html.split("\n")

def find_section_bounds(lines, section_id):
    """Find the start and end line indices for a section."""
    start = None
    for i, line in enumerate(lines):
        if f'id="{section_id}"' in line and ('class="section"' in line or "class='section'" in line):
            start = i
            break
    if start is None:
        return None, None
    depth = 0
    for i in range(start, len(lines)):
        depth += lines[i].count("<div") - lines[i].count("</div>")
        if depth == 0:
            return start, i
    return start, None

def load_section(name):
    path = os.path.join(SECTIONS_DIR, name)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# Track changes
changes = []

# ═══════════════════════════════════════════════════════════════
# 1. Insert case examples BEFORE the math section comment
# ═══════════════════════════════════════════════════════════════
case_examples = load_section("case_examples.html")
case_lines = case_examples.split("\n")

# Find the line just before the math section 
math_start, math_end = find_section_bounds(lines, "math")
if math_start is not None:
    # Look for the comment line above math
    insert_at = math_start
    for i in range(math_start - 1, max(math_start - 10, 0), -1):
        if "SECTION: MATH" in lines[i] or "═══" in lines[i]:
            insert_at = i
            break
    
    lines = lines[:insert_at] + case_lines + [""] + lines[insert_at:]
    changes.append(f"Inserted case examples ({len(case_lines)} lines) at line {insert_at}")
else:
    print("ERROR: Could not find math section")

# ═══════════════════════════════════════════════════════════════
# 2. Replace math section
# ═══════════════════════════════════════════════════════════════
math_new = load_section("math_new.html")
math_new_lines = math_new.split("\n")

math_start, math_end = find_section_bounds(lines, "math")
if math_start is not None and math_end is not None:
    lines = lines[:math_start] + math_new_lines + lines[math_end+1:]
    changes.append(f"Replaced math section (lines {math_start}-{math_end}) with {len(math_new_lines)} new lines")
else:
    print(f"ERROR: Could not find math section bounds: {math_start}, {math_end}")

# ═══════════════════════════════════════════════════════════════
# 3. Replace drills section header (keep existing exercises)
# ═══════════════════════════════════════════════════════════════
drills_header = load_section("drills_header.html")
drills_header_lines = drills_header.split("\n")

drills_start, drills_end = find_section_bounds(lines, "drills")
if drills_start is not None:
    # Find where the first exercise collapsible starts (Nível 1)
    first_exercise = None
    for i in range(drills_start, min(drills_start + 40, len(lines))):
        if "Nível 1" in lines[i] or "Aquecimento" in lines[i]:
            first_exercise = i
            break
    
    if first_exercise is not None:
        # Replace from drills_start to just before first exercise
        lines = lines[:drills_start] + drills_header_lines + [""] + lines[first_exercise:]
        changes.append(f"Replaced drills header (lines {drills_start}-{first_exercise-1}) with {len(drills_header_lines)} new lines")
    else:
        print("WARN: Could not find first exercise in drills, inserting header only")
else:
    print("ERROR: Could not find drills section")

# ═══════════════════════════════════════════════════════════════
# 4. Insert scoring rubric into BCG Patterns (before Red Flags)
# ═══════════════════════════════════════════════════════════════
scoring = load_section("scoring_rubric.html")
scoring_lines = scoring.split("\n")

bcg_start, bcg_end = find_section_bounds(lines, "bcg-patterns")
if bcg_start is not None:
    # Find "Red Flags" or "⚠️ Red Flags" heading
    red_flags = None
    for i in range(bcg_start, bcg_end or len(lines)):
        if "Red Flags" in lines[i]:
            red_flags = i
            break
    
    if red_flags is not None:
        lines = lines[:red_flags] + scoring_lines + [""] + lines[red_flags:]
        changes.append(f"Inserted scoring rubric ({len(scoring_lines)} lines) before Red Flags at line {red_flags}")
    else:
        # Insert before end of section
        lines = lines[:bcg_end] + scoring_lines + lines[bcg_end:]
        changes.append(f"Inserted scoring rubric at end of BCG Patterns")
else:
    print("ERROR: Could not find bcg-patterns section")

# ═══════════════════════════════════════════════════════════════
# 5. Update section subtitles to indicate EN/PT
# ═══════════════════════════════════════════════════════════════
for i in range(len(lines)):
    if "Vocabulário de negócios PT-PT para a entrevista" in lines[i]:
        lines[i] = '          Business vocabulary EN/PT for the interview / Vocabulário de negócios EN/PT para a entrevista'
        changes.append(f"Updated Portuguese section subtitle at line {i}")
    if "Como brilhar nas perguntas de brainstorming" in lines[i]:
        lines[i] = '          How to shine in brainstorming questions / Como brilhar nas perguntas de brainstorming — EN/PT'
        changes.append(f"Updated Creativity section subtitle at line {i}")

# ═══════════════════════════════════════════════════════════════
# Write back
# ═══════════════════════════════════════════════════════════════
html = "\n".join(lines)
with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\nTotal lines: {len(lines)}")
print(f"\nChanges applied ({len(changes)}):")
for c in changes:
    print(f"  ✅ {c}")
