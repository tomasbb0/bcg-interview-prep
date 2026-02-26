#!/usr/bin/env python3
"""
Swap Education section above Work Experience in the consulting CV v2.

Current body structure:
  [0-3] Name, contact, empty paragraphs
  [4]   TABLE #0 (tblInd=180) — WORK EXPERIENCE + Pairwire/Google/Amazon
  [5]   separator ¶
  [6]   TABLE #1 (tblInd=113) — EY
  [7]   separator ¶
  [8]   TABLE #2 (tblInd=142) — Fintech + nested EDUCATION table (tblInd=117)
  [9-]  Leadership tables, Skills, etc.

Desired output:
  [0-3] Name, contact, empty paragraphs
  [NEW] Education table (extracted from nested, tblInd=180)
  [NEW] separator ¶
  [4]   TABLE #0 — WORK EXPERIENCE + Pairwire/Google/Amazon
  ... rest unchanged (EY, Fintech WITHOUT education, Leadership, Skills)
"""

import zipfile
import copy
from lxml import etree

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NSMAP = {'w': W}

def qn(tag):
    return f'{{{W}}}{tag}'

def get_para_text(p):
    texts = []
    for t in p.iter(qn('t')):
        if t.text:
            texts.append(t.text)
    return ''.join(texts)

# --- Configuration ---
SOURCE = '/Users/tomasbatalha/Downloads/TomásBatalha_Resume_CONSULTING_v2.docx'
OUTPUT = '/Users/tomasbatalha/Downloads/TomásBatalha_Resume_CONSULTING_v3.docx'
TARGET_ABS_TEXT = 854
TARGET_HANGING = 425
NEW_EDU_TBLIND = 180  # Match Work Experience table indent

# --- Load document ---
with zipfile.ZipFile(SOURCE) as z:
    doc_xml = z.read('word/document.xml')
    all_files = {name: z.read(name) for name in z.namelist()}

tree = etree.fromstring(doc_xml)
body = tree.find(qn('body'))
body_elements = list(body)

# === 1. FIND KEY TABLES ===
work_exp_idx = None
fintech_idx = None
separator_elem = None

for i, elem in enumerate(body_elements):
    if elem.tag == qn('tbl'):
        all_text = ''.join([get_para_text(p) for p in elem.iter(qn('p'))])
        if 'WORK EXPERIENCE' in all_text and work_exp_idx is None:
            work_exp_idx = i
            print(f"[{i}] WORK EXPERIENCE table")
        if 'EDUCATION' in all_text and ('intech' in all_text.lower()):
            fintech_idx = i
            print(f"[{i}] Fintech+Education table")
    elif elem.tag == qn('p') and separator_elem is None and i > 3:
        # First separator paragraph after headers
        separator_elem = elem

assert work_exp_idx is not None, "Could not find WORK EXPERIENCE table"
assert fintech_idx is not None, "Could not find Fintech+Education table"

fintech_tbl = body_elements[fintech_idx]

# === 2. FIND NESTED EDUCATION TABLE INSIDE FINTECH ===
edu_nested_table = None
edu_cell = None
edu_row = None

for row in fintech_tbl.findall(f'{qn("tr")}'):
    for cell in row.findall(f'{qn("tc")}'):
        for nested_tbl in cell.findall(f'{qn("tbl")}'):
            nested_text = ''.join([get_para_text(p) for p in nested_tbl.iter(qn('p'))])
            if 'EDUCATION' in nested_text:
                edu_nested_table = nested_tbl
                edu_cell = cell
                edu_row = row
                break
        if edu_nested_table:
            break
    if edu_nested_table:
        break

assert edu_nested_table is not None, "Could not find nested EDUCATION table"
print("Found nested EDUCATION table inside Fintech")

# Print Education content
print("\nEducation content found:")
for p in edu_nested_table.iter(qn('p')):
    text = get_para_text(p).strip()
    if text:
        print(f"  {text[:80]}")

# === 3. DEEP COPY + ADJUST TABLE INDENT ===
edu_copy = copy.deepcopy(edu_nested_table)

# Change tblInd to match Work Experience table
tbl_pr = edu_copy.find(f'{qn("tblPr")}')
if tbl_pr is not None:
    tbl_ind_elem = tbl_pr.find(f'{qn("tblInd")}')
    if tbl_ind_elem is not None:
        old_ind = tbl_ind_elem.get(qn('w'), '0')
        tbl_ind_elem.set(qn('w'), str(NEW_EDU_TBLIND))
        print(f"\nEducation table tblInd: {old_ind} → {NEW_EDU_TBLIND}")
    else:
        # Create tblInd element
        tbl_ind_elem = etree.SubElement(tbl_pr, qn('tblInd'))
        tbl_ind_elem.set(qn('w'), str(NEW_EDU_TBLIND))
        tbl_ind_elem.set(qn('type'), 'dxa')
        print(f"\nCreated Education table tblInd: {NEW_EDU_TBLIND}")

# === 4. RECALCULATE BULLET INDENTS ===
def recalc_bullet_indents(tbl_elem, total_tblInd):
    """Recalculate indent for bullet paragraphs at this table level."""
    for row in tbl_elem.findall(f'{qn("tr")}'):
        for cell in row.findall(f'{qn("tc")}'):
            # Process direct paragraphs (not in nested tables)
            for p in cell.findall(f'{qn("p")}'):
                pPr = p.find(f'{qn("pPr")}')
                if pPr is None:
                    continue
                
                numPr = pPr.find(f'{qn("numPr")}')
                ind = pPr.find(f'{qn("ind")}')
                
                if ind is not None and numPr is not None:
                    # This is a bullet paragraph — recalculate
                    old_left = ind.get(qn('left'), '0')
                    new_left = max(0, TARGET_ABS_TEXT - total_tblInd)
                    
                    ind.set(qn('left'), str(new_left))
                    ind.set(qn('hanging'), str(TARGET_HANGING))
                    
                    # Remove firstLine if present (conflicts with hanging)
                    if ind.get(qn('firstLine')):
                        del ind.attrib[qn('firstLine')]
                    
                    text = get_para_text(p).strip()[:50]
                    print(f"  Bullet indent {old_left}→{new_left} (total={total_tblInd}): {text}")
            
            # Recurse into nested tables
            for nested_tbl in cell.findall(f'{qn("tbl")}'):
                nested_pr = nested_tbl.find(f'{qn("tblPr")}')
                nested_ind = 0
                if nested_pr is not None:
                    ni = nested_pr.find(f'{qn("tblInd")}')
                    if ni is not None:
                        nested_ind = int(ni.get(qn('w'), '0'))
                recalc_bullet_indents(nested_tbl, total_tblInd + nested_ind)

print("\nRecalculating bullet indents:")
recalc_bullet_indents(edu_copy, NEW_EDU_TBLIND)

# === 5. CREATE SEPARATOR PARAGRAPH ===
# Find the existing separator between TABLE #0 and next table
sep_idx = work_exp_idx + 1
if sep_idx < len(body_elements) and body_elements[sep_idx].tag == qn('p'):
    separator_copy = copy.deepcopy(body_elements[sep_idx])
    print(f"\nCopied separator paragraph from index {sep_idx}")
else:
    # Create a minimal empty paragraph
    separator_copy = etree.Element(qn('p'))
    pPr = etree.SubElement(separator_copy, qn('pPr'))
    rPr = etree.SubElement(pPr, qn('rPr'))
    etree.SubElement(rPr, qn('b'))
    print("\nCreated new separator paragraph")

# === 6. INSERT EDUCATION TABLE + SEPARATOR BEFORE WORK EXPERIENCE ===
# Insert order matters: edu_table first, then separator, so final order is:
# edu_table → separator → WORK EXPERIENCE table

body.insert(work_exp_idx, edu_copy)
body.insert(work_exp_idx + 1, separator_copy)

print(f"\nInserted Education table + separator before WORK EXPERIENCE")

# Note: all indices after work_exp_idx have shifted by 2

# === 7. REMOVE NESTED EDUCATION TABLE FROM FINTECH ===
# Remove the nested table from the cell
edu_cell.remove(edu_nested_table)
print("Removed nested Education table from Fintech cell")

# Check if the cell is now empty (no content paragraphs either)
# Every Word cell must have at least one paragraph
remaining_paras = edu_cell.findall(f'{qn("p")}')
remaining_text = ''.join([get_para_text(p).strip() for p in remaining_paras])
if not remaining_text:
    print("Fintech row with Education is now empty — minimizing row height")
    # Make the empty paragraph very small (2pt font) to minimize whitespace
    for p in remaining_paras:
        pPr = p.find(f'{qn("pPr")}')
        if pPr is None:
            pPr = etree.SubElement(p, qn('pPr'))
        # Set spacing to 0
        spacing = pPr.find(f'{qn("spacing")}')
        if spacing is None:
            spacing = etree.SubElement(pPr, qn('spacing'))
        spacing.set(qn('before'), '0')
        spacing.set(qn('after'), '0')
        spacing.set(qn('line'), '20')  # Minimal line spacing (twips)
        spacing.set(qn('lineRule'), 'exact')
        
        # Set font size to 2pt (smallest reasonable)
        rPr = pPr.find(f'{qn("rPr")}')
        if rPr is None:
            rPr = etree.SubElement(pPr, qn('rPr'))
        sz = rPr.find(f'{qn("sz")}')
        if sz is None:
            sz = etree.SubElement(rPr, qn('sz'))
        sz.set(qn('val'), '2')  # Half-points: 2 = 1pt

# === 8. SAVE ===
modified_xml = etree.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)
with zipfile.ZipFile(OUTPUT, 'w', zipfile.ZIP_DEFLATED) as zout:
    for name, data in all_files.items():
        if name == 'word/document.xml':
            zout.writestr(name, modified_xml)
        else:
            zout.writestr(name, data)

print(f"\n✅ Saved to: {OUTPUT}")
print("\nVerify in Word:")
print("  1. EDUCATION section appears FIRST (before Work Experience)")
print("  2. Bullet indents align with Work Experience bullets")
print("  3. No extra whitespace where Education used to be")
print("  4. Still fits on 1 page")
