#!/usr/bin/env python3
"""Replace sections in index.html with new EN/PT bilingual content from PDFs."""
import re
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
        if f'id="{section_id}"' in line and 'class="section"' in line:
            start = i
            break
    if start is None:
        return None, None
    
    # Find the closing </div> that matches this section's opening <div>
    depth = 0
    for i in range(start, len(lines)):
        depth += lines[i].count("<div") - lines[i].count("</div>")
        if depth == 0:
            return start, i
    return start, None

# Replace frameworks section
new_frameworks_path = os.path.join(SECTIONS_DIR, "frameworks_new.html")
with open(new_frameworks_path, "r", encoding="utf-8") as f:
    new_frameworks = f.read()

start, end = find_section_bounds(lines, "frameworks")
if start is not None and end is not None:
    print(f"Frameworks section: lines {start+1} to {end+1}")
    new_lines = new_frameworks.split("\n")
    lines = lines[:start] + new_lines + lines[end+1:]
    print(f"Replaced {end-start+1} old lines with {len(new_lines)} new lines")
else:
    print(f"ERROR: Could not find frameworks section bounds: start={start}, end={end}")

# Write back
html = "\n".join(lines)
with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Total lines: {len(lines)}")
print("Done!")
