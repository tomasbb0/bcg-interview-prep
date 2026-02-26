"""Fix NOVA Education bullet indent: add paragraph-level indent back to match other sections visually"""
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


with zipfile.ZipFile(FILE, 'r') as z:
    doc_xml = z.read('word/document.xml')
    all_files = {name: z.read(name) for name in z.namelist()}

tree = etree.fromstring(doc_xml)

# Find tables that contain NOVA Education bullets
# These are any bullets containing "Statistics", "Honorable", or "Relevant Courses"
# They're in tables 3, 4, 5

# Find the specific tables by looking for text content
tables = tree.findall('.//w:tbl', NSMAP)

nova_identifiers = ['Statistics (20/20)', 'Honorable Mentions', 'Relevant Courses: Applied'] 
# Plus any other education bullets that might be in different tables

fixed = 0
for tbl in tables:
    # Check all paragraphs in this table
    for p in tbl.findall('.//w:p', NSMAP):
        text = get_para_text(p).strip()
        
        # Check if this is a bullet in an education table that needs fixing
        pPr = p.find('w:pPr', NSMAP)
        if pPr is None:
            continue
        numPr = pPr.find('w:numPr', NSMAP)
        if numPr is None:
            continue
        
        # Check if indent is missing (we removed it) 
        ind = pPr.find('w:ind', NSMAP)
        
        # Check if this is in a table that also contains NOVA identifiers
        tbl_text = ''.join(t.text for t in tbl.findall('.//w:t', NSMAP) if t.text)
        is_nova_table = any(nid in tbl_text for nid in nova_identifiers)
        
        # Also check for NUS and Rotterdam education tables
        is_edu_table = 'EDUCATION' in tbl_text or 'Singapore' in tbl_text or 'Rotterdam' in tbl_text
        
        if (is_nova_table or is_edu_table) and ind is None and len(text) > 15:
            # Add indent matching the original NOVA values  
            # Original had left=552, hanging=426 for NOVA
            # But we need to match visually with Google bullets in Table 0
            # Let's try: use same indent as originally used for NOVA bullets
            ind = etree.SubElement(pPr, qn('ind'))
            # Use values that align visually with the wider tables
            # Google (Table 0, wide) uses numId definition: left=720, hanging=360 → dash at 360
            # NOVA (Table 3/4/5, narrower) needs explicit smaller values
            # Original was left=552, hanging=426 → dash at 126
            # Let me try left=360, hanging=360 → dash at 0 (leftmost)
            ind.set(qn('left'), '360')
            ind.set(qn('hanging'), '360')
            fixed += 1
            print(f"  Fixed: {text[:70]}...")

        # Also check for Leadership tables - they were in separate tables too
        is_leadership_table = 'Nova Tech Club' in tbl_text or 'Nova Social' in tbl_text or 'Thirst' in tbl_text
        if is_leadership_table and ind is None and len(text) > 15:
            ind = etree.SubElement(pPr, qn('ind'))
            ind.set(qn('left'), '360')
            ind.set(qn('hanging'), '360')
            fixed += 1
            print(f"  Fixed (leadership): {text[:70]}...")

print(f"\nTotal fixed: {fixed}")

modified_xml = etree.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)
with zipfile.ZipFile(FILE, 'w', zipfile.ZIP_DEFLATED) as zout:
    for name, data in all_files.items():
        if name == 'word/document.xml':
            zout.writestr(name, modified_xml)
        else:
            zout.writestr(name, data)

print(f"Saved: {FILE}")
