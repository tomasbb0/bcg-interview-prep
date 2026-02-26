"""
Check numbering.xml to understand bullet list definitions and fix them.
Also shorten all bullets slightly.
"""
import zipfile
import os
from lxml import etree

FILE = os.path.expanduser("~/Downloads/TomásBatalha_Resume_02_2026_GOOGLE_AE.docx")
NSMAP = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def qn(tag):
    return f'{{{W}}}{tag}'


with zipfile.ZipFile(FILE, 'r') as z:
    numbering_xml = z.read('word/numbering.xml')

tree = etree.fromstring(numbering_xml)

# Find all abstract numbering definitions
print("=== ABSTRACT NUMBERING DEFINITIONS ===\n")
for abstract in tree.findall('.//w:abstractNum', NSMAP):
    abstract_id = abstract.get(qn('abstractNumId'), '?')
    
    # Get level 0 (the main bullet level)
    for lvl in abstract.findall('.//w:lvl', NSMAP):
        ilvl = lvl.get(qn('ilvl'), '?')
        if ilvl != '0':
            continue
        
        numFmt_el = lvl.find('w:numFmt', NSMAP)
        numFmt = numFmt_el.get(qn('val'), '?') if numFmt_el is not None else '?'
        
        lvl_text_el = lvl.find('w:lvlText', NSMAP)
        lvl_text = lvl_text_el.get(qn('val'), '?') if lvl_text_el is not None else '?'
        
        pPr = lvl.find('w:pPr', NSMAP)
        ind = pPr.find('w:ind', NSMAP) if pPr is not None else None
        left = ind.get(qn('left'), '?') if ind is not None else 'none'
        hanging = ind.get(qn('hanging'), '?') if ind is not None else 'none'
        
        print(f"  abstractNum {abstract_id}, level 0: fmt={numFmt}, text='{lvl_text}', left={left}, hanging={hanging}")

# Find num -> abstractNum mappings
print("\n=== NUM ID MAPPINGS ===\n")
for num in tree.findall('.//w:num', NSMAP):
    num_id = num.get(qn('numId'), '?')
    abstract_ref = num.find('w:abstractNumId', NSMAP)
    abstract_id = abstract_ref.get(qn('val'), '?') if abstract_ref is not None else '?'
    
    # Check for level overrides
    overrides = num.findall('w:lvlOverride', NSMAP)
    override_info = f" ({len(overrides)} overrides)" if overrides else ""
    
    print(f"  numId={num_id} -> abstractNum={abstract_id}{override_info}")
