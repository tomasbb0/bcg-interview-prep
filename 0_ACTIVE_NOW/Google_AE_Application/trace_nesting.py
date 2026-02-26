#!/usr/bin/env python3
"""Trace the full table nesting chain for every bullet paragraph."""

import zipfile
from lxml import etree
from pathlib import Path

SRC = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/Professional/2 - My Stuff/CV/TomásBatalha_Resume_02_2026.docx"

ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

def qn(tag):
    return f'{{{W}}}{tag}'

def get_text(p):
    return ''.join(t.text for t in p.findall('.//w:t', ns) if t.text)

with zipfile.ZipFile(SRC) as z:
    xml = z.read('word/document.xml')

tree = etree.fromstring(xml)

# Number all tables for reference
all_tables = tree.findall('.//w:tbl', ns)
table_ids = {id(t): i for i, t in enumerate(all_tables)}

# Get table indent
def get_tbl_ind(tbl):
    tblPr = tbl.find('w:tblPr', ns)
    if tblPr is None:
        return 0
    tblInd = tblPr.find('w:tblInd', ns)
    if tblInd is None:
        return 0
    try:
        return int(tblInd.get(qn('w'), '0'))
    except ValueError:
        return 0

# Get cell's left margin
def get_cell_margin(tc):
    tcPr = tc.find('w:tcPr', ns)
    if tcPr is None:
        return 0
    tcMar = tcPr.find('w:tcMar', ns)
    if tcMar is None:
        return 0
    left = tcMar.find('w:left', ns) or tcMar.find('w:start', ns)
    if left is None:
        return 0
    try:
        return int(left.get(qn('w'), '0'))
    except ValueError:
        return 0

# For each cell, determine its position within the row
# We need to find which column it starts at based on preceding cells
def get_cell_start_offset(tc):
    """Get the left offset of a cell within its row (position of preceding cells)."""
    tr = tc.getparent()
    if tr is None or tr.tag != qn('tr'):
        return 0
    
    # This is tricky - we'd need to trace grid columns. 
    # Instead, just check if it's the first cell in the row.
    cells = tr.findall('w:tc', ns)
    if cells and cells[0] is tc:
        return 0  # First cell - starts at left edge of table
    else:
        # Not first cell - we'd need grid info. But bullet content should always be in first cell.
        return -1  # Flag: not first cell

print("=== BULLET PARAGRAPH ANCESTRY TRACE ===\n")

for p in tree.findall('.//w:p', ns):
    text = get_text(p).strip()
    if not text or len(text) < 10:
        continue
    
    pPr = p.find('w:pPr', ns)
    if pPr is None:
        continue
    if pPr.find('w:numPr', ns) is None:
        continue
    
    # Get paragraph indent
    ind = pPr.find('w:ind', ns)
    p_left = ind.get(qn('left'), 'none') if ind is not None else 'none'
    p_hang = ind.get(qn('hanging'), 'none') if ind is not None else 'none'
    
    # Walk up the entire ancestor chain
    ancestors = []
    node = p.getparent()
    while node is not None:
        tag = node.tag.split('}')[-1] if '}' in node.tag else node.tag
        
        if node.tag == qn('tbl'):
            tbl_ind = get_tbl_ind(node)
            tbl_num = table_ids.get(id(node), '?')
            ancestors.append(f"tbl#{tbl_num}(ind={tbl_ind})")
        elif node.tag == qn('tc'):
            cell_offset = get_cell_start_offset(node)
            cell_margin = get_cell_margin(node)
            ancestors.append(f"tc(offset={cell_offset},margin={cell_margin})")
        elif node.tag == qn('tr'):
            ancestors.append("tr")
        
        node = node.getparent()
    
    ancestors.reverse()
    
    # Calculate total offset
    total_tbl_indent = 0
    chain_str = " > ".join(ancestors)
    for node2 in p.iterancestors():
        if node2.tag == qn('tbl'):
            total_tbl_indent += get_tbl_ind(node2)
    
    try:
        abs_dash = total_tbl_indent + int(p_left) - int(p_hang)
        abs_text = total_tbl_indent + int(p_left)
    except ValueError:
        abs_dash = '?'
        abs_text = '?'
    
    print(f"Para: {text[:65]}...")
    print(f"  Indent: left={p_left}, hanging={p_hang}")
    print(f"  Chain: {chain_str}")
    print(f"  Total tblInd: {total_tbl_indent} → abs_dash={abs_dash}, abs_text={abs_text}")
    print()
