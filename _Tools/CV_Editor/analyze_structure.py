"""Analyze table nesting structure of the CV docx."""
import zipfile
from lxml import etree

NSMAP = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

def qn(tag):
    return '{' + W + '}' + tag

p = '/Users/tomasbatalha/Downloads/TomásBatalha_Resume_CONSULTING_v2.docx'
with zipfile.ZipFile(p, 'r') as z:
    doc_xml = z.read('word/document.xml')

tree = etree.fromstring(doc_xml)

sections = ['WORK EXPERIENCE', 'EDUCATION', 'LEADERSHIP EXPERIENCE', 'SKILLS']

for p_el in tree.findall('.//w:p', NSMAP):
    text = ''.join(t.text for t in p_el.findall('.//w:t', NSMAP) if t.text).strip()
    if text in sections:
        path = []
        node = p_el
        while node is not None:
            tag = node.tag.split('}')[-1] if '}' in node.tag else node.tag
            if tag in ('tbl', 'tr', 'tc', 'body'):
                parent = node.getparent()
                if parent is not None and tag == 'tr':
                    idx = list(parent).index(node)
                    total = len(list(parent))
                    path.append('TR[' + str(idx) + '/' + str(total) + ']')
                elif tag == 'tbl':
                    parent = node.getparent()
                    if parent is not None:
                        idx = list(parent).index(node)
                        total = len(list(parent))
                        path.append('TBL[' + str(idx) + '/' + str(total) + ']')
                    else:
                        path.append('TBL')
                else:
                    path.append(tag.upper())
            node = node.getparent()
        path.reverse()
        print(text + ': ' + ' > '.join(path))

# Also show the body's direct children to understand top-level structure
print('\n=== BODY CHILDREN ===')
body = tree.find('.//w:body', NSMAP)
for i, child in enumerate(body):
    tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
    if tag == 'tbl':
        # Get first text in this table
        first_texts = []
        for pp in child.findall('.//w:p', NSMAP):
            t = ''.join(t.text for t in pp.findall('.//w:t', NSMAP) if t.text).strip()
            if t and len(t) > 3:
                first_texts.append(t)
                if len(first_texts) >= 3:
                    break
        print('  [' + str(i) + '] TBL: ' + ' | '.join(first_texts))
    elif tag == 'p':
        t = ''.join(t.text for t in child.findall('.//w:t', NSMAP) if t.text).strip()
        print('  [' + str(i) + '] P: ' + (t[:80] if t else '(empty)'))
    else:
        print('  [' + str(i) + '] ' + tag)
