"""
Additional CV modifications:
1. Ensure NUS is first in Education (most recent)
2. Condense Leadership Experience bullets
"""
import zipfile
import os
import shutil
from lxml import etree

SOURCE = os.path.expanduser("~/Downloads/TomásBatalha_Resume_02_2026_GOOGLE_AE.docx")
OUTPUT = SOURCE  # Overwrite in place

NSMAP = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
}


def get_paragraph_text(p):
    texts = p.findall('.//w:t', NSMAP)
    return ''.join(t.text for t in texts if t.text)


def replace_paragraph_text(p, new_text):
    runs = p.findall('.//w:r', NSMAP)
    if not runs:
        return False
    first_run = runs[0]
    for run in runs[1:]:
        run.getparent().remove(run)
    t_elem = first_run.find('.//w:t', NSMAP)
    if t_elem is not None:
        t_elem.text = new_text
        t_elem.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    return True


# Read
with zipfile.ZipFile(SOURCE, 'r') as z:
    doc_xml = z.read('word/document.xml')
    all_files = {name: z.read(name) for name in z.namelist()}

tree = etree.fromstring(doc_xml)
paragraphs = tree.findall('.//w:p', NSMAP)

# =============================================================================
# 1. CHECK EDUCATION ORDER
# =============================================================================
print("=== EDUCATION ORDER CHECK ===")
edu_start = False
edu_entries = []
for p in paragraphs:
    text = get_paragraph_text(p).strip()
    if 'EDUCATION' == text.strip():
        edu_start = True
        continue
    if edu_start and text:
        if 'LEADERSHIP' in text or 'SKILLS' in text:
            break
        edu_entries.append(text[:80])

print("Current Education order:")
for e in edu_entries:
    print(f"  {e}")

# NUS should already be first - verify
nus_first = any('Singapore' in e for e in edu_entries[:3])
print(f"\nNUS is first: {nus_first}")

# =============================================================================
# 2. CONDENSE LEADERSHIP EXPERIENCE
# =============================================================================
print("\n=== CONDENSING LEADERSHIP ===")

# Find and condense leadership bullets
leadership_replacements = [
    # Nova Tech Club - condense 2 bullets into 1
    (
        "Designed an online job platform app",
        "Designed an online job platform for underserved professionals and organized 6 events including Fintech Day and Hack Google Sheets."
    ),
    # Remove the second Nova Tech Club bullet (Planned 2 corporate events) 
    # by making it empty - but that might break formatting
    # Better: merge into the first one (done above)
    (
        "Planned 2 corporate events",
        None  # We'll handle this separately
    ),
    
    # Nova Social Consulting - condense 2 bullets into 1
    (
        "Assessed the association",
        "Assessed organizational structure for WWF-partnered project, identifying 155 pain points across 7 workstreams; delivered 6 presentations to senior management."
    ),
    (
        "Executed 8 interviews",
        None  # Merged into above
    ),
    
    # Nova Thirst Project - condense 2 bullets into 1
    (
        "Initiated a team of 23",
        "Founded and led a team of 23 volunteers, raising \u20ac2,539 and chairing 4 major events including one with 35 NGOs."
    ),
    (
        "Chaired 4 major events",
        None  # Merged into above
    ),
]

for search_start, new_text in leadership_replacements:
    for p in paragraphs:
        text = get_paragraph_text(p).strip()
        if text.startswith(search_start):
            if new_text is not None:
                replace_paragraph_text(p, new_text)
                print(f"  ✓ Replaced: '{search_start[:40]}...'")
            else:
                # Make the paragraph text minimal (can't safely remove without breaking table)
                # Set to a single space or very short text
                replace_paragraph_text(p, " ")
                print(f"  ✓ Blanked: '{search_start[:40]}...' (merged into previous bullet)")
            break

# Also blank the duplicate Amazon bullet if it's still there
for p in paragraphs:
    text = get_paragraph_text(p).strip()
    if text.startswith("Raised the bottom-line territory share"):
        replace_paragraph_text(p, " ")
        print(f"  ✓ Blanked duplicate Amazon bullet")
        break

# =============================================================================
# SAVE
# =============================================================================
modified_xml = etree.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)

with zipfile.ZipFile(OUTPUT, 'w', zipfile.ZIP_DEFLATED) as zout:
    for name, data in all_files.items():
        if name == 'word/document.xml':
            zout.writestr(name, modified_xml)
        else:
            zout.writestr(name, data)

print(f"\n✓ Saved to: {OUTPUT}")

# =============================================================================
# VERIFY
# =============================================================================
print("\n--- VERIFICATION: Full document text ---")
with zipfile.ZipFile(OUTPUT, 'r') as z:
    verify_xml = z.read('word/document.xml')

verify_tree = etree.fromstring(verify_xml)
for p in verify_tree.findall('.//w:p', NSMAP):
    text = get_paragraph_text(p).strip()
    if text and len(text) > 1:
        print(f"  {text[:130]}")
