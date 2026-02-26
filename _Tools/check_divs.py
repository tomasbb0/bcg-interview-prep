#!/usr/bin/env python3
import re

with open('0_ACTIVE_NOW/BCG_Interview_Prep/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

depth = 0
first_neg = None
for i, line in enumerate(lines):
    opens = len(re.findall(r'<div[\s>]', line))
    closes = len(re.findall(r'</div>', line))
    depth += opens - closes
    if depth < 0 and first_neg is None:
        first_neg = i

if first_neg is not None:
    print(f"First negative at L{first_neg+1}")
    # Re-trace depth showing 20 lines before
    d = 0
    for j in range(first_neg + 1):
        opens = len(re.findall(r'<div[\s>]', lines[j]))
        closes = len(re.findall(r'</div>', lines[j]))
        d += opens - closes
    print(f"Cumulative depth at that point: {d}")
    
    # Show divs in nearby lines
    for j in range(max(0, first_neg - 20), min(len(lines), first_neg + 5)):
        opens = len(re.findall(r'<div[\s>]', lines[j]))
        closes = len(re.findall(r'</div>', lines[j]))
        if opens or closes:
            print(f"  L{j+1} +{opens}/-{closes}: {lines[j].rstrip()[:100]}")
else:
    print("No negative depths!")

print(f"\nFinal depth: {depth}")
