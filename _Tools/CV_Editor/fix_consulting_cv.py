"""
Fix the consulting CV:
1. Split Google's last bullet - "Verbally offered to extend" as separate line
2. Swap EDUCATION above WORK EXPERIENCE
3. Trim content to fit 1 page
"""
import zipfile
import os
import shutil
from lxml import etree
from copy import deepcopy

SOURCE = os.path.expanduser("~/Downloads/TomásBatalha_Resume_CONSULTING.docx")
OUTPUT = os.path.expanduser("~/Downloads/TomásBatalha_Resume_CONSULTING_v2.docx")

NSMAP = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def qn(tag):
    return f'{{{W}}}{tag}'


def get_para_text(p):
    return ''.join(t.text for t in p.findall('.//w:t', NSMAP) if t.text)


def set_para_text(p, new_text):
    runs = p.findall('.//w:r', NSMAP)
    if not runs:
        return
    for run in runs[1:]:
        run.getparent().remove(run)
    t = runs[0].find('.//w:t', NSMAP)
    if t is not None:
        t.text = new_text
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')


shutil.copy2(SOURCE, OUTPUT)

with zipfile.ZipFile(SOURCE, 'r') as z:
    doc_xml = z.read('word/document.xml')
    all_files = {name: z.read(name) for name in z.namelist()}

tree = etree.fromstring(doc_xml)
paras = tree.findall('.//w:p', NSMAP)

# ===================================================================
# FIX 1: Split the Google "Future Trends" bullet
# ===================================================================
print("=== FIX 1: Split Google bullet ===")
for p in paras:
    text = get_para_text(p).strip()
    if text.startswith('Presented "Future Trends"') and 'Verbally offered' in text:
        # Set this paragraph to just the Future Trends part
        new_text = 'Presented "Future Trends" market insights to 237+ senior advertising clients at Google\'s flagship partner event, receiving strong positive feedback from client teams and leadership'
        set_para_text(p, new_text)
        
        # Create a new paragraph after this one for the extension offer
        new_p = deepcopy(p)
        set_para_text(new_p, 'Verbally offered to extend internship based on performance')
        
        # Insert after current paragraph
        parent = p.getparent()
        idx = list(parent).index(p)
        parent.insert(idx + 1, new_p)
        
        print("  OK: Split into two bullets")
        break

# ===================================================================
# FIX 2: Swap EDUCATION above WORK EXPERIENCE
# We need to find the top-level table structure and move sections.
# The CV uses tables. Let's find which table cells contain which sections.
# ===================================================================
print("\n=== FIX 2: Reorder sections ===")

# Find all paragraphs and their parent chains to understand structure
work_section_start = None
work_section_end = None
edu_section_start = None
edu_section_end = None
leadership_section_start = None

# Walk through all paragraphs to find section boundaries
all_paras = tree.findall('.//w:p', NSMAP)
section_markers = {}

for i, p in enumerate(all_paras):
    text = get_para_text(p).strip()
    if text == 'WORK EXPERIENCE':
        section_markers['work'] = i
    elif text == 'EDUCATION':
        section_markers['edu'] = i
    elif text == 'LEADERSHIP EXPERIENCE':
        section_markers['leadership'] = i
    elif text == 'SKILLS':
        section_markers['skills'] = i

print(f"  Section positions: {section_markers}")

# The sections might be in separate table rows or cells.
# Let's try to work at the table row level.
# Find the parent table rows for each section header
def find_ancestor_row(elem):
    """Find the ancestor table row (w:tr) of an element."""
    node = elem.getparent()
    while node is not None:
        if node.tag == qn('tr'):
            return node
        node = node.getparent()
    return None

def find_ancestor_table(elem):
    """Find the nearest ancestor table (w:tbl)."""
    node = elem.getparent()
    while node is not None:
        if node.tag == qn('tbl'):
            return node
        node = node.getparent()
    return None

# Find the rows containing each section
work_para = all_paras[section_markers['work']]
edu_para = all_paras[section_markers['edu']]

work_row = find_ancestor_row(work_para)
edu_row = find_ancestor_row(edu_para)
work_table = find_ancestor_table(work_para)
edu_table = find_ancestor_table(edu_para)

if work_row is not None and edu_row is not None:
    print(f"  Work section in row, Edu section in row")
    
    # Check if they're in the same table
    if work_table == edu_table:
        print("  Same parent table - can reorder rows")
        table = work_table
        rows = list(table)
        
        # Find indices
        work_idx = rows.index(work_row)
        edu_idx = rows.index(edu_row)
        
        print(f"  Work row index: {work_idx}, Edu row index: {edu_idx}")
        
        # We need to move all rows from edu_idx to end-of-education
        # above work_idx rows
        # First, identify which rows belong to education vs work
        # Education rows: from edu_idx until we hit LEADERSHIP EXPERIENCE or SKILLS
        
        leadership_para = all_paras[section_markers['leadership']]
        leadership_row = find_ancestor_row(leadership_para)
        
        if leadership_row is not None:
            leadership_idx = rows.index(leadership_row)
        else:
            leadership_idx = len(rows)
        
        print(f"  Leadership row index: {leadership_idx}")
        
        # Education rows are from edu_idx to leadership_idx - 1
        # Work rows are from work_idx to edu_idx - 1
        
        if edu_idx > work_idx:
            # Education is after Work - need to swap
            # Collect the row groups
            work_rows = rows[work_idx:edu_idx]  # Work Experience rows
            edu_rows = rows[edu_idx:leadership_idx]  # Education rows
            
            print(f"  Work rows: {len(work_rows)}, Education rows: {len(edu_rows)}")
            
            # Remove all rows in both groups
            for r in work_rows + edu_rows:
                table.remove(r)
            
            # Re-insert: education first, then work
            insert_point = work_idx
            for r in edu_rows:
                table.insert(insert_point, r)
                insert_point += 1
            for r in work_rows:
                table.insert(insert_point, r)
                insert_point += 1
            
            print("  Sections swapped successfully!")
        else:
            print("  Education already before Work - no swap needed")
    else:
        print("  Different parent tables - need different approach")
        
        # They might be in nested tables. Let's try going up further.
        # Find the common ancestor and swap at that level
        work_parent = work_table.getparent()
        edu_parent = edu_table.getparent()
        
        # Try to swap the tables themselves
        if work_parent == edu_parent:
            parent = work_parent
            children = list(parent)
            wi = children.index(work_table)
            ei = children.index(edu_table)
            
            if ei > wi:
                # Need to identify all elements between
                work_block = []
                edu_block = []
                in_work = False
                in_edu = False
                
                for child in children:
                    if child == work_table:
                        in_work = True
                    if child == edu_table:
                        in_work = False
                        in_edu = True
                    if in_work:
                        work_block.append(child)
                    if in_edu:
                        edu_block.append(child)
                        if child != edu_table:
                            # Check if this contains Leadership
                            texts = [get_para_text(p).strip() for p in child.findall('.//w:p', NSMAP)]
                            if 'LEADERSHIP EXPERIENCE' in texts:
                                in_edu = False
                
                # Simple swap of the two table elements
                parent.remove(edu_table)
                parent.insert(wi, edu_table)
                # work_table has shifted, remove and reinsert after edu
                parent.remove(work_table)
                parent.insert(wi + 1, work_table)
                print("  Swapped table elements!")
            else:
                print("  Education already before Work")
        else:
            print("  WARNING: Complex nesting - could not auto-swap. Do it manually in Word.")
else:
    print("  WARNING: Could not find section rows. Swap manually in Word.")

# ===================================================================
# FIX 3: Trim content to fit 1 page
# Remove/shorten weaker bullets
# ===================================================================
print("\n=== FIX 3: Trim for 1-page fit ===")

# Re-scan paras after modifications
paras = tree.findall('.//w:p', NSMAP)
trimmed = 0

for p in paras:
    text = get_para_text(p).strip()
    
    # Delete Fintech House weakest bullet (daily partnership coordination)
    if text.startswith("Managed 4 concurrent client partnerships"):
        p.getparent().remove(p)
        trimmed += 1
        print("  DEL: Fintech partnerships bullet (weakest)")
    
    # Shorten Nova Tech Club entry
    elif text.startswith("Designed an online job platform prototype"):
        set_para_text(p, "Designed a job platform prototype for underserved professionals with a cross-functional team of 4")
        trimmed += 1
        print("  TRIM: Nova Tech Club bullet shortened")
    
    # Remove "Hobbies:" label if separate from content
    elif text == "Hobbies:":
        p.getparent().remove(p)
        trimmed += 1
        print("  DEL: Hobbies label")
    
    # Remove "Interests:" label if separate
    elif text == "Interests:":
        p.getparent().remove(p)
        trimmed += 1
        print("  DEL: Interests label")
    
    # Combine hobbies into one line under a simpler label
    elif text == "Piano, Scuba Diving, Architecture, Quantum Physics":
        set_para_text(p, "Piano, Scuba Diving, Architecture")
        trimmed += 1
        print("  TRIM: Reduced hobbies to 3")

    # Shorten Fintech benchmark bullet
    elif text.startswith("Launched a fintech acceleration program"):
        set_para_text(p, "Launched a fintech acceleration program with Portugal Fintech\u2019s founder, benchmarking 54 global programs and onboarding 8 startups")
        trimmed += 1
        print("  TRIM: Shortened Fintech launch bullet")

    # Remove French language (beginner - not worth space)
    elif "French (beginner)" in text:
        set_para_text(p, "Portuguese (native), English (fluent), Spanish (fluent)")
        trimmed += 1
        print("  TRIM: Removed French (beginner)")

print(f"\n  {trimmed} changes for space")

# ===================================================================
# SAVE
# ===================================================================
modified_xml = etree.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)
with zipfile.ZipFile(OUTPUT, 'w', zipfile.ZIP_DEFLATED) as zout:
    for name, data in all_files.items():
        if name == 'word/document.xml':
            zout.writestr(name, modified_xml)
        else:
            zout.writestr(name, data)

print(f"\nSaved: {OUTPUT}")

# Verify final content
print("\n=== FINAL CONTENT ===")
tree2 = etree.fromstring(modified_xml)
for i, p in enumerate(tree2.findall('.//w:p', NSMAP)):
    text = ''.join(t.text for t in p.findall('.//w:t', NSMAP) if t.text).strip()
    if text and len(text) > 3:
        print(f"  [{i:3d}] {text}")
