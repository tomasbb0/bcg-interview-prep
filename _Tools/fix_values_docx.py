"""Fix values in both .docx CVs: remove Big 4, 155→50+, 65%→40%"""
import zipfile
from lxml import etree
import shutil
import os

NSMAP = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

def fix_docx(src, replacements):
    tmp = src + '.tmp'
    shutil.copy2(src, tmp)
    
    with zipfile.ZipFile(tmp, 'r') as zin:
        xml_bytes = zin.read('word/document.xml')
    
    tree = etree.fromstring(xml_bytes)
    
    count = 0
    for para in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
        runs = para.findall('.//w:r/w:t', NSMAP)
        full_text = ''.join(r.text or '' for r in runs)
        
        for old, new in replacements:
            if old in full_text:
                new_text = full_text.replace(old, new)
                first_run = True
                for r in runs:
                    if first_run:
                        r.text = new_text
                        r.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
                        first_run = False
                    else:
                        r.text = ''
                count += 1
                print(f'  \u2713 "{old}" \u2192 "{new}"')
                break
    
    new_xml = etree.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)
    
    with zipfile.ZipFile(tmp, 'r') as zin:
        with zipfile.ZipFile(src, 'w', zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == 'word/document.xml':
                    zout.writestr(item, new_xml)
                else:
                    zout.writestr(item, zin.read(item.filename))
    
    os.remove(tmp)
    print(f'  Total: {count} replacements')

# Fix Google AE FIXED
print('=== Google AE CV ===')
fix_docx(
    os.path.expanduser('~/Downloads/Tom\u00e1sBatalha_Resume_02_2026_GOOGLE_AE_FIXED.docx'),
    [
        ('Fortune 500 and Big 4 firms', 'Fortune 500 firms'),
    ]
)

# Fix Consulting v4
print('\n=== Consulting CV ===')
fix_docx(
    os.path.expanduser('~/Downloads/Tom\u00e1sBatalha_Resume_CONSULTING_v4.docx'),
    [
        ('Fortune 500 and Big 4 clients', 'Fortune 500 clients'),
        ('155 pain points and improvement areas', '50+ pain points and improvement areas'),
        ('65%', '40%'),
    ]
)

print('\n\u2705 Both .docx files updated')
