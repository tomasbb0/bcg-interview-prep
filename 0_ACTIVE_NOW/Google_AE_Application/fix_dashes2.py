"""Remove all en/em dashes used as punctuation (not in date ranges or bullet markers)"""
import zipfile
import os
from lxml import etree

FILE = os.path.expanduser("~/Downloads/TomásBatalha_Resume_02_2026_GOOGLE_AE.docx")
NSMAP = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

with zipfile.ZipFile(FILE, 'r') as z:
    doc_xml = z.read('word/document.xml')
    all_files = {name: z.read(name) for name in z.namelist()}

tree = etree.fromstring(doc_xml)

# Find the specific bullet with the dash and rewrite it
for t in tree.findall('.//w:t', NSMAP):
    if t.text and 'Managed entire sales funnel' in t.text:
        # Rewrite without any dashes
        t.text = "Managed entire sales funnel: prospecting, qualification, demo, negotiation, and close, all processes and tooling built from scratch."
        print(f"Fixed: {t.text[:80]}...")
    
    # Also check for any other stray em/en dashes in bullet text (not date ranges)
    if t.text and (' \u2013 ' in t.text or ' \u2014 ' in t.text):
        # This is a dash used as punctuation (with spaces around it)
        old = t.text
        t.text = t.text.replace(' \u2013 ', ', ').replace(' \u2014 ', ', ')
        if old != t.text:
            print(f"Fixed stray dash: {t.text[:80]}...")
    
    # Fix smart quotes if needed (EMEA's -> EMEA's)
    if t.text and 'EMEA\u2019s' in t.text:
        t.text = t.text.replace('\u2019', "'")
        print(f"Fixed smart apostrophe: {t.text[:80]}...")

modified_xml = etree.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)
with zipfile.ZipFile(FILE, 'w', zipfile.ZIP_DEFLATED) as zout:
    for name, data in all_files.items():
        if name == 'word/document.xml':
            zout.writestr(name, modified_xml)
        else:
            zout.writestr(name, data)

print(f"Saved: {FILE}")
