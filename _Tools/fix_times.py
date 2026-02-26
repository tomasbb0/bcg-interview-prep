#!/usr/bin/env python3
"""Adjust Tuesday times to 15:30 start, 00:30 end."""

f = "/Users/tomasbatalha/Projects/Planning and Advisory/Tomas_Batalha_Future_Plan/0_ACTIVE_NOW/BCG_Interview_Prep/index.html"
with open(f, 'r', encoding='utf-8') as fh:
    c = fh.read()

changes = 0

# Badge
old = 'LATE START 15:00'
new = 'LATE START 15:30'
if old in c:
    c = c.replace(old, new)
    changes += 1
    print("Badge updated")

# Times - use >time< pattern to match inside td tags, count=1
time_map = [
    ('>15:00-15:10<', '>15:30-15:40<'),
    ('>15:10-15:55<', '>15:40-16:00<'),
    ('>20:00-20:50<', '>20:15-21:00<'),
    ('>20:50-21:30<', '>21:00-21:40<'),
    ('>21:30-22:30<', '>21:40-22:40<'),
    ('>22:30-23:00<', '>22:40-23:10<'),
    ('>23:00-00:00<', '>23:10-00:30<'),
]

for old, new in time_map:
    if old in c:
        c = c.replace(old, new, 1)
        changes += 1
        print(f"  {old} -> {new}")
    else:
        print(f"  NOT FOUND: {old}")

# Propranolol standalone time cell
old_prop = '20:00\n                  </td>'
new_prop = '20:15\n                  </td>'
if old_prop in c:
    c = c.replace(old_prop, new_prop, 1)
    changes += 1
    print("Propranolol cell time updated")

# Med card time
old_card = 'Propranolol 10mg \u00e0s 20:00'
new_card = 'Propranolol 10mg \u00e0s 20:15'
if old_card in c:
    c = c.replace(old_card, new_card)
    changes += 1
    print("Med card time updated")

# Description line
old_desc = 'In\u00edcio tardio \u2014 Bloco'
new_desc = 'In\u00edcio tardio 15:30 \u2014 Bloco'
if old_desc in c:
    c = c.replace(old_desc, new_desc, 1)
    changes += 1
    print("Description updated")

old_mid = 'at\u00e9 meia-noite'
new_mid = 'at\u00e9 00:30'
if old_mid in c:
    c = c.replace(old_mid, new_mid, 1)
    changes += 1
    print("Midnight -> 00:30")

with open(f, 'w', encoding='utf-8') as fh:
    fh.write(c)
print(f"\nTotal changes: {changes}")
