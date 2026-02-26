"""Extract ALL text from the DOCX XML by concatenating runs, searching for Pairwire"""
import zipfile
import os
import re
from lxml import etree

cv_path = os.path.expanduser(
    "~/Library/Mobile Documents/com~apple~CloudDocs/Professional/2 - My Stuff/CV/TomásBatalha_Resume_02_2026.docx"
)

NSMAP = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}

with zipfile.ZipFile(cv_path, 'r') as z:
    xml = z.read('word/document.xml')

tree = etree.fromstring(xml)

# Extract paragraphs by concatenating all w:t elements within each w:p
paragraphs = tree.findall('.//w:p', NSMAP)

print(f"Total paragraphs in document: {len(paragraphs)}")
print("=" * 80)
print("ALL NON-EMPTY PARAGRAPHS (reconstructed from runs):")
print("=" * 80)

for i, p in enumerate(paragraphs):
    # Get all text elements in this paragraph
    texts = p.findall('.//w:t', NSMAP)
    full_text = ''.join(t.text for t in texts if t.text)
    
    if full_text.strip():
        # Check for formatting
        bold_runs = p.findall('.//w:rPr/w:b', NSMAP)
        is_bold = "BOLD" if bold_runs else ""
        
        # Highlight if it contains interesting keywords
        highlight = ""
        for kw in ['airwire', 'Co-Founder', 'EDUCATION', 'Rotterdam', 'NOVA', 'MSc', 'WORK EXP', 'SKILL', 'LEADER']:
            if kw.lower() in full_text.lower():
                highlight = f" *** {kw} ***"
                break
        
        print(f"  P{i:3d} {is_bold:4s}: {full_text[:150]}{highlight}")

# Also search specifically for the word Pairwire across ALL text
print("\n" + "=" * 80)
print("FULL TEXT SEARCH FOR 'PAIRWIRE' (case insensitive):")
print("=" * 80)
all_text = []
for p in paragraphs:
    texts = p.findall('.//w:t', NSMAP)
    full_text = ''.join(t.text for t in texts if t.text)
    all_text.append(full_text)

full_doc_text = '\n'.join(all_text)
for m in re.finditer(r'.{0,50}(pairwire|pair.wire).{0,50}', full_doc_text, re.IGNORECASE):
    print(f"  Found: ...{m.group(0)}...")

if 'pairwire' not in full_doc_text.lower():
    print("  NOT FOUND anywhere in document text!")
    # But let's check what IS near Co-Founder
    print("\n  Searching around 'Co-Founder':")
    idx = full_doc_text.lower().find('co-founder')
    if idx >= 0:
        context = full_doc_text[max(0,idx-200):idx+200]
        print(f"  Context: {context}")
