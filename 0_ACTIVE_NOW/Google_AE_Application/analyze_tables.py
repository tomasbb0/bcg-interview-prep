#!/usr/bin/env python3
"""Analyze table structure in the DOCX to understand why bullets don't align."""

import zipfile
from lxml import etree
from pathlib import Path

SRC = Path.home() / "Downloads" / "TomásBatalha_Resume_02_2026_GOOGLE_AE.docx"

ns = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
}

with zipfile.ZipFile(SRC) as z:
    xml = z.read('word/document.xml')

tree = etree.fromstring(xml)

# Find all tables
tables = tree.findall('.//w:tbl', ns)
print(f"Total tables: {len(tables)}\n")

for i, tbl in enumerate(tables):
    print(f"=== TABLE {i} ===")
    
    # Table properties
    tblPr = tbl.find('w:tblPr', ns)
    if tblPr is not None:
        # Table width
        tblW = tblPr.find('w:tblW', ns)
        if tblW is not None:
            print(f"  Table width: {tblW.get(f'{{{ns["w"]}}}w')} type={tblW.get(f'{{{ns["w"]}}}type')}")
        
        # Table layout
        tblLayout = tblPr.find('w:tblLayout', ns)
        if tblLayout is not None:
            print(f"  Layout: {tblLayout.get(f'{{{ns["w"]}}}type')}")
        
        # Table indent
        tblInd = tblPr.find('w:tblInd', ns)
        if tblInd is not None:
            print(f"  Table indent: {tblInd.get(f'{{{ns["w"]}}}w')} type={tblInd.get(f'{{{ns["w"]}}}type')}")
        
        # Table cell margin
        tblCellMar = tblPr.find('w:tblCellMar', ns)
        if tblCellMar is not None:
            for side in ['top', 'left', 'bottom', 'right', 'start', 'end']:
                el = tblCellMar.find(f'w:{side}', ns)
                if el is not None:
                    print(f"  Cell margin {side}: {el.get(f'{{{ns["w"]}}}w')} type={el.get(f'{{{ns["w"]}}}type')}")
    
    # Grid columns
    tblGrid = tbl.find('w:tblGrid', ns)
    if tblGrid is not None:
        cols = tblGrid.findall('w:gridCol', ns)
        widths = [c.get(f'{{{ns["w"]}}}w') for c in cols]
        print(f"  Grid columns: {widths}")
    
    # First row cells — check cell widths and margins
    rows = tbl.findall('w:tr', ns)
    print(f"  Rows: {len(rows)}")
    
    for j, row in enumerate(rows):
        cells = row.findall('w:tc', ns)
        for k, cell in enumerate(cells):
            tcPr = cell.find('w:tcPr', ns)
            if tcPr is not None:
                tcW = tcPr.find('w:tcW', ns)
                w_val = tcW.get(f'{{{ns["w"]}}}w') if tcW is not None else 'N/A'
                
                # Cell margins override
                tcMar = tcPr.find('w:tcMar', ns)
                mar_info = ""
                if tcMar is not None:
                    for side in ['left', 'right', 'start', 'end']:
                        el = tcMar.find(f'w:{side}', ns)
                        if el is not None:
                            w_ns = ns['w']
                            mar_info += f" {side}={el.get('{' + w_ns + '}w')}"
                
                # Check for paragraphs with bullets
                paras = cell.findall('w:p', ns)
                for p in paras:
                    pPr = p.find('w:pPr', ns)
                    numPr = pPr.find('w:numPr', ns) if pPr is not None else None
                    if numPr is not None:
                        numId = numPr.find('w:numId', ns)
                        ilvl = numPr.find('w:ilvl', ns)
                        nid = numId.get(f'{{{ns["w"]}}}val') if numId is not None else '?'
                        lvl = ilvl.get(f'{{{ns["w"]}}}val') if ilvl is not None else '?'
                        
                        # Paragraph indent
                        ind = pPr.find('w:ind', ns) if pPr is not None else None
                        if ind is not None:
                            left = ind.get(f'{{{ns["w"]}}}left', 'N/A')
                            hang = ind.get(f'{{{ns["w"]}}}hanging', 'N/A')
                        else:
                            left = 'none'
                            hang = 'none'
                        
                        # Get text preview
                        runs = p.findall('.//w:r/w:t', ns)
                        text = ''.join(r.text or '' for r in runs)[:60]
                        
                        print(f"  Row{j} Cell{k} (w={w_val}{mar_info}): numId={nid} ilvl={lvl} left={left} hang={hang}")
                        print(f"    Text: {text}")

print("\n\n=== NUMBERING DEFINITIONS ===")
with zipfile.ZipFile(SRC) as z:
    try:
        nxml = z.read('word/numbering.xml')
        ntree = etree.fromstring(nxml)
        
        # Get all abstractNum
        for an in ntree.findall('.//w:abstractNum', ns):
            anid = an.get(f'{{{ns["w"]}}}abstractNumId')
            lvl0 = an.find('w:lvl[@w:ilvl="0"]', ns)
            if lvl0 is not None:
                pPr = lvl0.find('w:pPr', ns)
                ind = pPr.find('w:ind', ns) if pPr is not None else None
                if ind is not None:
                    left = ind.get(f'{{{ns["w"]}}}left', 'N/A')
                    hang = ind.get(f'{{{ns["w"]}}}hanging', 'N/A')
                else:
                    left = 'none'
                    hang = 'none'
                numFmt = lvl0.find('w:numFmt', ns)
                fmt = numFmt.get(f'{{{ns["w"]}}}val') if numFmt is not None else '?'
                lvlText = lvl0.find('w:lvlText', ns)
                txt = lvlText.get(f'{{{ns["w"]}}}val') if lvlText is not None else '?'
                print(f"  abstractNum {anid}: fmt={fmt} text='{txt}' left={left} hang={hang}")
        
        # Get num -> abstractNum mapping
        print("\n  Num mappings:")
        for num in ntree.findall('.//w:num', ns):
            nid = num.get(f'{{{ns["w"]}}}numId')
            anRef = num.find('w:abstractNumId', ns)
            anid = anRef.get(f'{{{ns["w"]}}}val') if anRef is not None else '?'
            print(f"    numId={nid} -> abstractNumId={anid}")
    except KeyError:
        print("  No numbering.xml found")
