"""Fix the remaining broken date range"""
import zipfile
import os
from lxml import etree

FILE = os.path.expanduser("~/Downloads/TomásBatalha_Resume_02_2026_GOOGLE_AE.docx")
NSMAP = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

with zipfile.ZipFile(FILE, 'r') as z:
    doc_xml = z.read('word/document.xml')
    all_files = {name: z.read(name) for name in z.namelist()}

tree = etree.fromstring(doc_xml)

fixed = 0
for t in tree.findall('.//w:t', NSMAP):
    if t.text:
        # Fix any remaining "YYYY, " that should be "YYYY – " in date contexts
        if '2020, ' in t.text and 'Feb' not in t.text and 'Sep' not in t.text:
            # This is likely a broken fragment " 2020, "
            t.text = t.text.replace('2020, ', '2020 \u2013 ')
            print(f"Fixed fragment: {t.text}")
            fixed += 1
        if 'Sep 2020, Feb' in t.text:
            t.text = t.text.replace('Sep 2020, Feb', 'Sep 2020 \u2013 Feb')
            print(f"Fixed: {t.text}")
            fixed += 1
        # Also catch " 2020, " pattern
        if ', Feb 2021' in t.text and 'Consultant' not in t.text:
            t.text = t.text.replace(', Feb 2021', ' \u2013 Feb 2021')
            print(f"Fixed: {t.text}")
            fixed += 1

print(f"\nFixed {fixed} remaining date ranges")

modified_xml = etree.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)
with zipfile.ZipFile(FILE, 'w', zipfile.ZIP_DEFLATED) as zout:
    for name, data in all_files.items():
        if name == 'word/document.xml':
            zout.writestr(name, modified_xml)
        else:
            zout.writestr(name, data)

# Final verification
print("\nFinal verification - all date lines:")
for p in tree.findall('.//w:p', NSMAP):
    texts = p.findall('.//w:t', NSMAP)
    full = ''.join(tt.text for tt in texts if tt.text)
    if '202' in full and '|' in full:
        print(f"  {full[:100]}")

print(f"\nSaved: {FILE}")
