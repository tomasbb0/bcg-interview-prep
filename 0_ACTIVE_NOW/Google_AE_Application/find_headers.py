#!/usr/bin/env python3
"""Find section headers and job titles in the CV."""
import zipfile
from lxml import etree
from pathlib import Path

SRC = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/Professional/2 - My Stuff/CV/TomásBatalha_Resume_02_2026.docx"
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

def qn(tag): return f'{{{W}}}{tag}'

with zipfile.ZipFile(SRC) as z:
    xml = z.read('word/document.xml')

tree = etree.fromstring(xml)

print("=== ALL TEXT IN DOCUMENT (with formatting) ===\n")

for p in tree.findall('.//w:p', ns):
    runs = p.findall('.//w:r', ns)
    if not runs:
        continue
    
    text_parts = []
    is_bold = False
    font_size = None
    font_name = None
    
    for r in runs:
        t = r.find('w:t', ns)
        if t is not None and t.text:
            text_parts.append(t.text)
        
        # Check formatting
        rPr = r.find('w:rPr', ns)
        if rPr is not None:
            b = rPr.find('w:b', ns)
            if b is not None:
                # Bold (unless val="0")
                val = b.get(qn('val'), 'true')
                if val != '0' and val != 'false':
                    is_bold = True
            
            sz = rPr.find('w:sz', ns)
            if sz is not None:
                font_size = int(sz.get(qn('val'), '0')) / 2  # half-points to points
            
            rFonts = rPr.find('w:rFonts', ns)
            if rFonts is not None:
                font_name = rFonts.get(qn('ascii'), rFonts.get(qn('cs'), ''))
    
    full_text = ''.join(text_parts).strip()
    if not full_text:
        continue
    
    # Only show non-bullet content OR short bold text (likely headers/titles)
    numPr = None
    pPr = p.find('w:pPr', ns)
    if pPr is not None:
        numPr = pPr.find('w:numPr', ns)
    
    if numPr is None or is_bold or (font_size and font_size > 8):
        fmt = []
        if is_bold: fmt.append("BOLD")
        if font_size: fmt.append(f"{font_size}pt")
        if font_name: fmt.append(font_name)
        fmt_str = f" [{', '.join(fmt)}]" if fmt else ""
        
        if len(full_text) < 150:
            print(f"{full_text}{fmt_str}")
