#!/usr/bin/env python3
"""Extract text from the latest .docx CV to see current bullet content."""
from docx import Document
from lxml import etree

NSMAP = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

paths = [
    '/Users/tomasbatalha/Library/Mobile Documents/com~apple~CloudDocs/Professional/2 - My Stuff/CV/TomásBatalha_Resume_01_2026_GoogleDocs.docx',
    '/Users/tomasbatalha/Projects/Planning and Advisory/Tomas_Batalha_Future_Plan/0_ACTIVE_NOW/Google_AE_Application/TomásBatalha_Resume_02_2026_GOOGLE_AE.docx',
    '/Users/tomasbatalha/Projects/Planning and Advisory/Tomas_Batalha_Future_Plan/1_Current_Priorities/CV/TomásBatalha_Resume_12_2025_POLISHED.docm',
]

for p in paths:
    try:
        doc = Document(p)
        fname = p.split("/")[-1]
        print(f"=== FILE: {fname} ===\n")
        
        # Use lxml to get ALL text including deeply nested tables
        import zipfile
        with zipfile.ZipFile(p, 'r') as z:
            doc_xml = z.read('word/document.xml')
        
        tree = etree.fromstring(doc_xml)
        paras = tree.findall('.//w:p', NSMAP)
        
        for i, para in enumerate(paras):
            text = ''.join(t.text for t in para.findall('.//w:t', NSMAP) if t.text).strip()
            if text and len(text) > 3:
                print(f"[{i:3d}] {text}")
        
        print(f"\nTotal paragraphs with text: {sum(1 for p in paras if ''.join(t.text for t in p.findall('.//w:t', NSMAP) if t.text).strip())}")
        break
    except Exception as e:
        print(f"Could not open {p.split('/')[-1]}: {e}")
