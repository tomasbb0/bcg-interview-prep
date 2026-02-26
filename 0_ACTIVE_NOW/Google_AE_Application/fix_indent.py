"""Normalize all bullet indentation to match Google/Amazon format (left=674, hanging=425, numId=2)"""
import zipfile
import os
from lxml import etree

FILE = os.path.expanduser("~/Downloads/TomásBatalha_Resume_02_2026_GOOGLE_AE.docx")
NSMAP = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def qn(tag):
    return f'{{{W}}}{tag}'


def get_para_text(p):
    return ''.join(t.text for t in p.findall('.//w:t', NSMAP) if t.text)


def is_bullet_para(p, text):
    """Check if this paragraph is a bullet (not a header/company/role/section)"""
    if not text or len(text) < 20:
        return False
    if text in ['WORK EXPERIENCE', 'EDUCATION', 'LEADERSHIP EXPERIENCE', 'SKILLS']:
        return False
    if '|' in text and len(text) < 100:  # company or role line
        return False
    # Check if it has numPr (list formatting)
    pPr = p.find('w:pPr', NSMAP)
    if pPr is not None:
        numPr = pPr.find('w:numPr', NSMAP)
        if numPr is not None:
            return True
    return False


with zipfile.ZipFile(FILE, 'r') as z:
    doc_xml = z.read('word/document.xml')
    all_files = {name: z.read(name) for name in z.namelist()}

tree = etree.fromstring(doc_xml)
paras = tree.findall('.//w:p', NSMAP)

# Target format: left=674, hanging=425, numId=2, ilvl=0
TARGET_LEFT = '674'
TARGET_HANGING = '425'
TARGET_NUMID = '2'
TARGET_ILVL = '0'

fixed = 0
for p in paras:
    text = get_para_text(p).strip()
    if not is_bullet_para(p, text):
        continue
    
    pPr = p.find('w:pPr', NSMAP)
    if pPr is None:
        continue
    
    # Fix numPr (list style)
    numPr = pPr.find('w:numPr', NSMAP)
    if numPr is not None:
        numId = numPr.find('w:numId', NSMAP)
        ilvl = numPr.find('w:ilvl', NSMAP)
        
        current_numId = numId.get(qn('val'), '') if numId is not None else ''
        
        if current_numId != TARGET_NUMID:
            if numId is not None:
                numId.set(qn('val'), TARGET_NUMID)
            if ilvl is not None:
                ilvl.set(qn('val'), TARGET_ILVL)
            fixed += 1
            print(f"  Fixed numId {current_numId}->{TARGET_NUMID}: {text[:60]}...")
    
    # Fix indentation
    ind = pPr.find('w:ind', NSMAP)
    if ind is not None:
        current_left = ind.get(qn('left'), '')
        current_hanging = ind.get(qn('hanging'), '')
        
        needs_fix = False
        if current_left != TARGET_LEFT:
            needs_fix = True
        if current_hanging != TARGET_HANGING:
            needs_fix = True
        
        if needs_fix:
            ind.set(qn('left'), TARGET_LEFT)
            ind.set(qn('hanging'), TARGET_HANGING)
            # Remove firstLine if present (conflicts with hanging)
            if qn('firstLine') in ind.attrib:
                del ind.attrib[qn('firstLine')]
            fixed += 1
            print(f"  Fixed indent left={current_left}->{TARGET_LEFT}, hang={current_hanging}->{TARGET_HANGING}: {text[:50]}...")
    else:
        # No indentation set — add it
        ind = etree.SubElement(pPr, qn('ind'))
        ind.set(qn('left'), TARGET_LEFT)
        ind.set(qn('hanging'), TARGET_HANGING)
        fixed += 1
        print(f"  Added indent: {text[:60]}...")

print(f"\nTotal fixes: {fixed}")

# Save
modified_xml = etree.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)
with zipfile.ZipFile(FILE, 'w', zipfile.ZIP_DEFLATED) as zout:
    for name, data in all_files.items():
        if name == 'word/document.xml':
            zout.writestr(name, modified_xml)
        else:
            zout.writestr(name, data)

print(f"Saved: {FILE}")
