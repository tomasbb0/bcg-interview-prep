"""
Analyze and normalize bullet indentation across all sections.
The space between dash and text is controlled by paragraph indent (w:ind) in the XML.
"""
import zipfile
import os
from lxml import etree

FILE = os.path.expanduser("~/Downloads/TomásBatalha_Resume_02_2026_GOOGLE_AE.docx")
NSMAP = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


def qn(tag):
    prefix, name = tag.split(':')
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    return f'{{{ns[prefix]}}}{name}'


def get_para_text(p):
    return ''.join(t.text for t in p.findall('.//w:t', NSMAP) if t.text)


with zipfile.ZipFile(FILE, 'r') as z:
    doc_xml = z.read('word/document.xml')
    all_files = {name: z.read(name) for name in z.namelist()}

tree = etree.fromstring(doc_xml)
paras = tree.findall('.//w:p', NSMAP)

# =================================================================
# STEP 1: ANALYZE - Show indentation for all bullet-like paragraphs
# =================================================================
print("=== BULLET INDENTATION ANALYSIS ===\n")

current_section = ""
for p in paras:
    text = get_para_text(p).strip()
    
    # Track section
    if text in ['WORK EXPERIENCE', 'EDUCATION', 'LEADERSHIP EXPERIENCE', 'SKILLS']:
        current_section = text
        print(f"\n--- {current_section} ---")
        continue
    
    if not text or len(text) < 20:
        continue
    
    # Check if this looks like a bullet (not a company or role line)
    if '|' in text and len(text) < 100:
        print(f"  HEADER: {text[:80]}")
        continue
    
    # Get paragraph properties
    pPr = p.find('w:pPr', NSMAP)
    
    # Get indentation
    ind = pPr.find('w:ind', NSMAP) if pPr is not None else None
    left = ind.get(qn('w:left'), '?') if ind is not None else 'none'
    hanging = ind.get(qn('w:hanging'), '?') if ind is not None else 'none'
    firstLine = ind.get(qn('w:firstLine'), '?') if ind is not None else 'none'
    
    # Get numbering (list format)
    numPr = pPr.find('w:numPr', NSMAP) if pPr is not None else None
    numId = ""
    ilvl = ""
    if numPr is not None:
        nid = numPr.find('w:numId', NSMAP)
        ilv = numPr.find('w:ilvl', NSMAP)
        numId = nid.get(qn('w:val'), '?') if nid is not None else '?'
        ilvl = ilv.get(qn('w:val'), '?') if ilv is not None else '?'
    
    # Get tab stops
    tabs = pPr.find('w:tabs', NSMAP) if pPr is not None else None
    tab_info = ""
    if tabs is not None:
        for tab in tabs.findall('w:tab', NSMAP):
            pos = tab.get(qn('w:pos'), '?')
            tab_info += f" tab={pos}"
    
    print(f"  BULLET: left={left} hang={hanging} firstLine={firstLine} numId={numId} ilvl={ilvl}{tab_info}")
    print(f"          {text[:80]}")


def qn(tag):
    prefix, name = tag.split(':')
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    return f'{{{ns[prefix]}}}{name}'
