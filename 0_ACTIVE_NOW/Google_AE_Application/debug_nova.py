"""Check specific formatting of NOVA School bullets vs others"""
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

tree = etree.fromstring(doc_xml)
paras = tree.findall('.//w:p', NSMAP)

# Dump FULL XML for paragraphs around NOVA and compare with a Google bullet
print("=== NOVA BULLETS FULL XML ===\n")
for p in paras:
    text = get_para_text(p).strip()
    if text.startswith('Relevant Courses: Statistics') or text.startswith('Honorable Mentions'):
        print(f"TEXT: {text[:80]}")
        # Print full pPr XML
        pPr = p.find('w:pPr', NSMAP)
        if pPr is not None:
            print(f"pPr XML: {etree.tostring(pPr, pretty_print=True).decode()}")
        print()

print("=== GOOGLE BULLET FOR COMPARISON ===\n")
for p in paras:
    text = get_para_text(p).strip()
    if text.startswith('Designed and automated 3'):
        print(f"TEXT: {text[:80]}")
        pPr = p.find('w:pPr', NSMAP)
        if pPr is not None:
            print(f"pPr XML: {etree.tostring(pPr, pretty_print=True).decode()}")
        break

print("=== PAIRWIRE BULLET FOR COMPARISON ===\n")
for p in paras:
    text = get_para_text(p).strip()
    if text.startswith('Built automated GTM'):
        print(f"TEXT: {text[:80]}")
        pPr = p.find('w:pPr', NSMAP)
        if pPr is not None:
            print(f"pPr XML: {etree.tostring(pPr, pretty_print=True).decode()}")
        break

# Also check if NOVA bullets are in a different table with different cell margins
print("\n=== TABLE CONTEXT ===")
tables = tree.findall('.//w:tbl', NSMAP)
for t_idx, tbl in enumerate(tables):
    for p in tbl.findall('.//w:p', NSMAP):
        text = get_para_text(p).strip()
        if 'Statistics (20/20)' in text or 'Honorable Mentions' in text:
            print(f"  NOVA bullet in Table {t_idx}")
            # Check table cell margins
            tc = p.getparent()
            if tc is not None:
                tcPr = tc.find('w:tcPr', NSMAP)
                if tcPr is not None:
                    tcMar = tcPr.find('w:tcMar', NSMAP)
                    if tcMar is not None:
                        print(f"  Cell margins: {etree.tostring(tcMar, pretty_print=True).decode()}")
        if 'Designed and automated 3' in text:
            print(f"  Google bullet in Table {t_idx}")
