"""Fix em dashes: replace Unicode em dash with en dash (which already works in the doc)"""
import zipfile
import os
from lxml import etree

FILE = os.path.expanduser("~/Downloads/TomásBatalha_Resume_02_2026_GOOGLE_AE.docx")
NSMAP = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

with zipfile.ZipFile(FILE, 'r') as z:
    doc_xml = z.read('word/document.xml')
    all_files = {name: z.read(name) for name in z.namelist()}

tree = etree.fromstring(doc_xml)

# Replace all em dashes (U+2014) with en dashes (U+2013) which the doc already uses
count = 0
for t in tree.findall('.//w:t', NSMAP):
    if t.text and '\u2014' in t.text:
        t.text = t.text.replace('\u2014', ' \u2013 ')
        count += 1
    # Also fix smart quotes if broken
    if t.text and '\u2019' in t.text:
        # Smart apostrophe - replace with regular if causing issues
        pass  # Keep smart quotes, they usually work

print(f"Fixed {count} em dashes -> en dashes")

modified_xml = etree.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)
with zipfile.ZipFile(FILE, 'w', zipfile.ZIP_DEFLATED) as zout:
    for name, data in all_files.items():
        if name == 'word/document.xml':
            zout.writestr(name, modified_xml)
        else:
            zout.writestr(name, data)

print(f"Saved: {FILE}")
