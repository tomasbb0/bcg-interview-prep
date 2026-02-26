"""Fix date range dashes that were accidentally replaced with commas"""
import zipfile
import os
import re
from lxml import etree

FILE = os.path.expanduser("~/Downloads/TomásBatalha_Resume_02_2026_GOOGLE_AE.docx")
NSMAP = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

with zipfile.ZipFile(FILE, 'r') as z:
    doc_xml = z.read('word/document.xml')
    all_files = {name: z.read(name) for name in z.namelist()}

tree = etree.fromstring(doc_xml)

# Fix date ranges: "Month YYYY, Month YYYY" or "Month YYYY, Present" -> "Month YYYY – Month YYYY"
date_pattern = re.compile(
    r'((?:January|February|March|April|May|June|July|August|September|October|November|December|'
    r'Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}),\s*'
    r'((?:January|February|March|April|May|June|July|August|September|October|November|December|'
    r'Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}|Present)'
)

fixed = 0
for t in tree.findall('.//w:t', NSMAP):
    if t.text and re.search(date_pattern, t.text):
        old = t.text
        t.text = re.sub(date_pattern, '\\1 \u2013 \\2', t.text)
        if old != t.text:
            print(f"Fixed: {t.text[:80]}")
            fixed += 1
    
    # Also fix "2020, " that was broken (from "2020 – ")
    if t.text and re.search(r'\d{4},\s+\d{4}', t.text):
        # This is likely a broken date range within a paragraph
        pass  # Let the main pattern handle it

# Special fix for any remaining broken date patterns
for t in tree.findall('.//w:t', NSMAP):
    if t.text:
        # Fix " 2020, Feb" pattern
        t.text = re.sub(r'(\d{4}),\s*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)', 
                        '\\1 \u2013 \\2', t.text)

print(f"\nFixed {fixed} date ranges")

modified_xml = etree.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)
with zipfile.ZipFile(FILE, 'w', zipfile.ZIP_DEFLATED) as zout:
    for name, data in all_files.items():
        if name == 'word/document.xml':
            zout.writestr(name, modified_xml)
        else:
            zout.writestr(name, data)

print(f"Saved: {FILE}")

# Verify all date ranges
print("\nVerification - all lines with dates:")
for p in tree.findall('.//w:p', NSMAP):
    texts = p.findall('.//w:t', NSMAP)
    full = ''.join(t.text for t in texts if t.text)
    if re.search(r'20\d{2}', full) and ('|' in full or 'Present' in full):
        print(f"  {full[:100]}")
