#!/usr/bin/env python3
"""Find ALL empty rows in every table of the v3 docx."""

import zipfile
from lxml import etree

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
def qn(tag): return f'{{{W}}}{tag}'

def get_para_text(p):
    return ''.join(t.text for t in p.iter(qn('t')) if t.text)

def scan_table(tbl, table_label, indent=0):
    prefix = "  " * indent
    tbl_ind_elem = tbl.find(f'{qn("tblPr")}/{qn("tblInd")}')
    tbl_ind = tbl_ind_elem.get(qn('w'), '?') if tbl_ind_elem is not None else 'none'
    
    rows = tbl.findall(f'{qn("tr")}')
    print(f"{prefix}{table_label} (tblInd={tbl_ind}, {len(rows)} rows)")
    
    empty_rows = []
    for ri, row in enumerate(rows):
        cells = row.findall(f'{qn("tc")}')
        all_text = ''
        has_nested = False
        for cell in cells:
            for p in cell.findall(f'{qn("p")}'):
                all_text += get_para_text(p).strip()
            if cell.findall(f'{qn("tbl")}'):
                has_nested = True
        
        # Get row height if specified
        trPr = row.find(f'{qn("trPr")}')
        trHeight = None
        if trPr is not None:
            h = trPr.find(f'{qn("trHeight")}')
            if h is not None:
                trHeight = h.get(qn('val'))
        
        if not all_text and not has_nested:
            status = "⚠️  EMPTY"
            empty_rows.append(ri)
        elif not all_text and has_nested:
            status = "📦 nested table only"
        else:
            status = all_text[:60]
        
        height_info = f" [h={trHeight}]" if trHeight else ""
        print(f"{prefix}  Row{ri}: {status}{height_info}")
        
        # Recurse into nested tables
        for cell in cells:
            for ni, nt in enumerate(cell.findall(f'{qn("tbl")}')):
                scan_table(nt, f"Nested table", indent + 2)
    
    return empty_rows

import sys
src = sys.argv[1] if len(sys.argv) > 1 else "/Users/tomasbatalha/Downloads/TomásBatalha_Resume_CONSULTING_v3.docx"
with zipfile.ZipFile(src) as z:
    doc_xml = z.read('word/document.xml')
tree = etree.fromstring(doc_xml)
body = tree.find(qn('body'))

tbl_idx = 0
for i, elem in enumerate(body):
    if elem.tag == qn('tbl'):
        first_text = ''.join(get_para_text(p) for p in elem.iter(qn('p')))[:50]
        print(f"\n[{i}] === BODY TABLE #{tbl_idx} ({first_text[:40]}) ===")
        empties = scan_table(elem, f"TABLE #{tbl_idx}")
        if empties:
            print(f"  >>> EMPTY ROWS: {empties}")
        tbl_idx += 1
    elif elem.tag == qn('p'):
        text = get_para_text(elem).strip()
        if not text:
            print(f"[{i}] (empty paragraph)")
