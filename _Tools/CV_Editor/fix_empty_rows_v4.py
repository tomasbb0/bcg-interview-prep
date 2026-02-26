#!/usr/bin/env python3
"""
Fix empty rows in v3 → produce v4.

Issues fixed:
1. Remove the empty Row4 from Fintech table (created when Education was extracted)
2. Minimize spacer rows in Education table (rows between universities)
3. Minimize spacer rows in NOVA nested table
"""

import zipfile
from lxml import etree

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
def qn(tag): return f'{{{W}}}{tag}'

def get_para_text(p):
    return ''.join(t.text for t in p.iter(qn('t')) if t.text)

def get_table_text(tbl):
    return ''.join(get_para_text(p) for p in tbl.iter(qn('p')))

def is_row_empty(row):
    """Check if a row has no text content and no nested tables."""
    for cell in row.findall(f'{qn("tc")}'):
        for p in cell.findall(f'{qn("p")}'):
            if get_para_text(p).strip():
                return False
        if cell.findall(f'{qn("tbl")}'):
            return False
    return True

def minimize_row(row):
    """Make a row as small as possible (1pt font, minimal line height)."""
    trPr = row.find(f'{qn("trPr")}')
    if trPr is None:
        trPr = etree.SubElement(row, qn('trPr'))
        # Insert trPr as first child
        row.insert(0, trPr)
    
    # Set row height to exact 20 twips (smallest practical)
    trHeight = trPr.find(f'{qn("trHeight")}')
    if trHeight is None:
        trHeight = etree.SubElement(trPr, qn('trHeight'))
    trHeight.set(qn('val'), '20')
    trHeight.set(qn('hRule'), 'exact')
    
    # Also minimize paragraph content in cells
    for cell in row.findall(f'{qn("tc")}'):
        for p in cell.findall(f'{qn("p")}'):
            pPr = p.find(f'{qn("pPr")}')
            if pPr is None:
                pPr = etree.SubElement(p, qn('pPr'))
            
            # Set spacing to 0
            spacing = pPr.find(f'{qn("spacing")}')
            if spacing is None:
                spacing = etree.SubElement(pPr, qn('spacing'))
            spacing.set(qn('before'), '0')
            spacing.set(qn('after'), '0')
            spacing.set(qn('line'), '20')
            spacing.set(qn('lineRule'), 'exact')
            
            # Set font size to 1pt
            rPr = pPr.find(f'{qn("rPr")}')
            if rPr is None:
                rPr = etree.SubElement(pPr, qn('rPr'))
            sz = rPr.find(f'{qn("sz")}')
            if sz is None:
                sz = etree.SubElement(rPr, qn('sz'))
            sz.set(qn('val'), '2')  # Half-points: 2 = 1pt

# --- Config ---
SOURCE = '/Users/tomasbatalha/Downloads/TomásBatalha_Resume_CONSULTING_v3.docx'
OUTPUT = '/Users/tomasbatalha/Downloads/TomásBatalha_Resume_CONSULTING_v4.docx'

# --- Load ---
with zipfile.ZipFile(SOURCE) as z:
    doc_xml = z.read('word/document.xml')
    all_files = {name: z.read(name) for name in z.namelist()}

tree = etree.fromstring(doc_xml)
body = tree.find(qn('body'))

fixes = 0

# Process all body-level tables
for elem in body:
    if elem.tag != qn('tbl'):
        continue
    
    table_text = get_table_text(elem)[:50]
    
    # === Fix 1: Remove empty Row4 from Fintech table ===
    if 'Fintech' in table_text or 'intech' in table_text.lower():
        rows = elem.findall(f'{qn("tr")}')
        for ri, row in enumerate(rows):
            if is_row_empty(row):
                elem.remove(row)
                fixes += 1
                print(f"✓ Removed empty Row{ri} from Fintech table")
    
    # === Fix 2: Minimize spacer rows in Education table ===
    if 'EDUCATION' in table_text:
        rows = elem.findall(f'{qn("tr")}')
        for ri, row in enumerate(rows):
            if is_row_empty(row):
                minimize_row(row)
                fixes += 1
                print(f"✓ Minimized empty Row{ri} in Education table (h→20)")
        
        # Also handle nested NOVA table spacer rows
        for nested_tbl in elem.iter(qn('tbl')):
            nested_text = get_table_text(nested_tbl)[:50]
            if 'Nova School' in nested_text or 'BSc' in nested_text:
                nested_rows = nested_tbl.findall(f'{qn("tr")}')
                for ri, row in enumerate(nested_rows):
                    if is_row_empty(row):
                        minimize_row(row)
                        fixes += 1
                        print(f"✓ Minimized empty Row{ri} in NOVA nested table (h→20)")

print(f"\nTotal fixes: {fixes}")

# --- Save ---
modified_xml = etree.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)
with zipfile.ZipFile(OUTPUT, 'w', zipfile.ZIP_DEFLATED) as zout:
    for name, data in all_files.items():
        if name == 'word/document.xml':
            zout.writestr(name, modified_xml)
        else:
            zout.writestr(name, data)

print(f"\n✅ Saved to: {OUTPUT}")
