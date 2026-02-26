"""Search the RAW XML of the CV for any mention of Pairwire"""
import zipfile
import os
import re

cv_path = os.path.expanduser(
    "~/Library/Mobile Documents/com~apple~CloudDocs/Professional/2 - My Stuff/CV/TomásBatalha_Resume_02_2026.docx"
)

# A DOCX is a ZIP file. Let's search ALL XML files inside it
with zipfile.ZipFile(cv_path, 'r') as z:
    for name in z.namelist():
        data = z.read(name)
        try:
            text = data.decode('utf-8', errors='replace')
        except:
            continue
        
        # Search for Pairwire (case insensitive)
        if re.search(r'pairwire|pair.?wire', text, re.IGNORECASE):
            print(f"\n{'='*60}")
            print(f"FOUND 'Pairwire' in: {name}")
            print(f"{'='*60}")
            # Find and show context around each match
            for m in re.finditer(r'.{0,100}(pairwire|pair.?wire).{0,100}', text, re.IGNORECASE):
                # Clean up XML noise for readability
                snippet = m.group(0)
                # Strip XML tags for readable output
                clean = re.sub(r'<[^>]+>', ' ', snippet)
                clean = re.sub(r'\s+', ' ', clean).strip()
                print(f"  Context: ...{clean}...")
            print()

# Also search for other keywords to understand what's in the doc
print("\n" + "="*60)
print("SEARCHING FOR OTHER CONTENT KEYWORDS")
print("="*60)
keywords = ['Pairwire', 'Co-Founder', 'pairwire', 'EDUCATION', 'Education', 
            'Rotterdam', 'NOVA', 'MSc', 'BSc', 'Summary', 'SUMMARY',
            'Head of Growth', 'acqui-hire', 'exit']

with zipfile.ZipFile(cv_path, 'r') as z:
    doc_xml = z.read('word/document.xml').decode('utf-8', errors='replace')
    
    for kw in keywords:
        if kw.lower() in doc_xml.lower():
            print(f"  FOUND: '{kw}'")
        else:
            print(f"  NOT FOUND: '{kw}'")

# Also check if there are headers/footers or other parts
print("\n" + "="*60)
print("ALL FILES IN DOCX ARCHIVE:")
print("="*60)
with zipfile.ZipFile(cv_path, 'r') as z:
    for name in z.namelist():
        size = z.getinfo(name).file_size
        print(f"  {name} ({size:,} bytes)")
