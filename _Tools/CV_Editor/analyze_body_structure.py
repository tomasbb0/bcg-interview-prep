#!/usr/bin/env python3
"""Analyze the body-level structure of the consulting CV docx.
Shows every top-level element in the document body, whether it's a paragraph or table,
and its text content."""

import zipfile
from lxml import etree
import sys

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NSMAP = {'w': W}

def qn(tag):
    return f'{{{W}}}{tag}'

def get_all_text(elem):
    """Get ALL text from an element (including nested tables)."""
    texts = []
    for t in elem.iter(qn('t')):
        if t.text:
            texts.append(t.text)
    return ''.join(texts)

def get_para_text(p):
    """Get text from a single paragraph (not nested)."""
    texts = []
    for r in p.findall(f'{qn("r")}'):
        for t in r.findall(f'{qn("t")}'):
            if t.text:
                texts.append(t.text)
    return ''.join(texts)

def analyze_table(tbl, indent=0):
    """Recursively analyze a table and its contents."""
    prefix = "  " * indent
    
    # Get table indent
    tblInd = tbl.find(f'.//{qn("tblPr")}/{qn("tblInd")}')
    ind_val = tblInd.get(qn('w')) if tblInd is not None else '?'
    
    rows = tbl.findall(f'{qn("tr")}')
    print(f"{prefix}TABLE (tblInd={ind_val}, {len(rows)} rows)")
    
    for ri, row in enumerate(rows):
        cells = row.findall(f'{qn("tc")}')
        for ci, cell in enumerate(cells):
            # Check for nested tables
            nested_tables = cell.findall(f'{qn("tbl")}')
            paras = cell.findall(f'{qn("p")}')
            
            for p in paras:
                text = get_para_text(p).strip()
                if text:
                    # Check if it's bold (section header)
                    is_bold = p.find(f'.//{qn("b")}') is not None
                    marker = "**" if is_bold else ""
                    print(f"{prefix}  Row{ri} Cell{ci}: {marker}{text[:80]}{marker}")
            
            for nt in nested_tables:
                print(f"{prefix}  Row{ri} Cell{ci}: [NESTED TABLE]")
                analyze_table(nt, indent + 2)

def main():
    src = sys.argv[1] if len(sys.argv) > 1 else \
        "/Users/tomasbatalha/Downloads/TomásBatalha_Resume_CONSULTING_v2.docx"
    
    with zipfile.ZipFile(src) as z:
        doc_xml = z.read('word/document.xml')
    
    tree = etree.fromstring(doc_xml)
    body = tree.find(qn('body'))
    
    print(f"=== Body-level elements ===\n")
    
    tbl_count = 0
    for i, elem in enumerate(body):
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        
        if tag == 'p':
            text = get_para_text(elem).strip()
            is_bold = elem.find(f'.//{qn("b")}') is not None
            marker = "**" if is_bold else ""
            print(f"[{i}] PARAGRAPH: {marker}{text[:100]}{marker}")
        elif tag == 'tbl':
            all_text = get_all_text(elem)[:100]
            print(f"\n[{i}] === TABLE #{tbl_count} ===")
            analyze_table(elem)
            tbl_count += 1
            print()
        elif tag == 'sectPr':
            print(f"[{i}] SECTION PROPERTIES")
        else:
            print(f"[{i}] {tag}")

if __name__ == '__main__':
    main()
