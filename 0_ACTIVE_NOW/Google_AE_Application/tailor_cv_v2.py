"""
Tailored CV for Google AE - CORRECTED VERSION
Strategy: Find paragraphs by their EXISTING text and replace with tailored text.
NO structural changes - only text modifications to preserve formatting perfectly.
"""
import zipfile
import os
import shutil
import re
from lxml import etree

# Paths
SOURCE = os.path.expanduser(
    "~/Library/Mobile Documents/com~apple~CloudDocs/Professional/2 - My Stuff/CV/TomásBatalha_Resume_02_2026.docx"
)
OUTPUT = os.path.expanduser("~/Downloads/TomásBatalha_Resume_02_2026_GOOGLE_AE.docx")

NSMAP = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
}


def get_paragraph_text(p):
    """Reconstruct full text from a paragraph's runs."""
    texts = p.findall('.//w:t', NSMAP)
    return ''.join(t.text for t in texts if t.text)


def replace_paragraph_text(p, new_text):
    """
    Replace ALL text in a paragraph with new_text, keeping the FIRST run's formatting.
    Removes all runs except the first, sets new text on that first run.
    """
    runs = p.findall('.//w:r', NSMAP)
    if not runs:
        return False
    
    # Keep first run, remove the rest
    first_run = runs[0]
    for run in runs[1:]:
        run.getparent().remove(run)
    
    # Set text on first run's w:t element
    t_elem = first_run.find('.//w:t', NSMAP)
    if t_elem is not None:
        t_elem.text = new_text
        # Preserve spaces
        t_elem.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    else:
        # Create a w:t element
        t_elem = etree.SubElement(first_run, qn('w:t'))
        t_elem.text = new_text
        t_elem.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    
    return True


def qn(tag):
    """Convert tag like 'w:t' to full namespace URI."""
    prefix, name = tag.split(':')
    ns = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    }
    return f'{{{ns[prefix]}}}{name}'


# =============================================================================
# STEP 1: Copy original file
# =============================================================================
shutil.copy2(SOURCE, OUTPUT)
print(f"Copied original to: {OUTPUT}")

# =============================================================================
# STEP 2: Open as ZIP and modify document.xml directly
# =============================================================================

# Read the DOCX
with zipfile.ZipFile(SOURCE, 'r') as z:
    doc_xml = z.read('word/document.xml')
    all_files = {name: z.read(name) for name in z.namelist()}

tree = etree.fromstring(doc_xml)
body = tree.find('.//w:body', NSMAP)
paragraphs = tree.findall('.//w:p', NSMAP)

# Build index of paragraphs by their text
para_index = {}
for p in paragraphs:
    text = get_paragraph_text(p).strip()
    if text:
        para_index[text[:80]] = p  # Use first 80 chars as key

# =============================================================================
# DEFINE REPLACEMENTS: (search_prefix, new_text)
# The search_prefix is the first ~40-80 chars of the ORIGINAL text to find it
# =============================================================================

replacements = [
    # --- PAIRWIRE BULLETS (tailor for Google AE - sales language) ---
    (
        "Built automated GTM workflows",
        "Built automated GTM workflows (Python + OpenAI API) processing 10,847+ leads, driving a fully self-built outbound engine from prospecting to close \u2014 zero marketing spend."
    ),
    (
        "Ran 147 discovery calls",
        "Ran 147+ discovery calls with enterprise and mid-market prospects, qualifying opportunities and closing 34 engagements across 6\u20139 month consultative sales cycles."
    ),
    (
        "Generated \u20ac41.2K in closed revenue",
        "Generated \u20ac41.2K in closed revenue within 11 months through pure outbound prospecting, managing the full pipeline from cold outreach to signed contract."
    ),
    (
        "Managed entire sales funnel",
        "Managed the entire sales funnel end-to-end: lead generation, qualification, demo, proposal, negotiation, and close \u2014 building all processes and tooling from scratch."
    ),
    
    # --- GOOGLE BULLETS (tailor for AE - partner/client-facing impact) ---
    (
        "Designed and automated three globally scalable dashboards",
        "Designed and automated 3 globally scalable performance dashboards using Apps Script and GMP tools, enabling partner managers to track ROAS vs. profit and CPA vs. conversions \u2014 adopted as the standard reporting framework across EMEA."
    ),
    (
        "Built a reporting platform for partner managers",
        "Built a cross-functional reporting platform for partner managers using Looker Studio and Analytics 360, streamlining project ROI tracking and reducing manual reporting effort by ~40%."
    ),
    (
        'Led the \u201cFuture Trends\u201d segment',  # smart quotes version
        "Led the \u201cFuture Trends\u201d keynote segment at Google\u2019s flagship partner event, presenting data-driven insights on Peak Season advertising strategy to 237+ senior agency and client executives."
    ),
    
    # --- AMAZON BULLETS (tailor for AE - pipeline/territory language) ---
    (
        "Led and executed the project of expansion",
        "Led the end-to-end expansion of Amazon\u2019s B2B retail segment into Portugal, managing a pipeline of 2,311 target companies from prospecting through onboarding."
    ),
    (
        "Outperformed KPI benchmarks by 21x",
        "Outperformed KPI benchmarks by 21x in account configurations, driving territory revenue share from 56% below to 25% above team average \u2014 outperforming full-time colleagues across the region."
    ),
    (
        "Raised the bottom-line territory share",
        None  # SKIP this one - it's been merged with the above
    ),
    (
        "Compiled a 19-pager consulting report",
        "Compiled a 19-page market intelligence report assessing B2B eCommerce opportunity across 8 territories and 54 targeted client interviews, directly informing regional go-to-market strategy."
    ),
    
    # --- SKILLS: Update proficiencies ---
    (
        "Python, Apps Script, Virtual Basic",
        "Salesforce, HubSpot CRM, Google Ads, Looker Studio, Python, Apps Script, SQL, Power BI, DAX."
    ),
]

# =============================================================================
# STEP 3: Apply replacements
# =============================================================================
print("\nApplying replacements:")

applied = 0
skipped = 0

for search_start, new_text in replacements:
    if new_text is None:
        skipped += 1
        continue
        
    found = False
    for p in paragraphs:
        text = get_paragraph_text(p).strip()
        if text.startswith(search_start):
            if replace_paragraph_text(p, new_text):
                print(f"  \u2713 Replaced: '{search_start[:50]}...'")
                applied += 1
                found = True
                break
    
    if not found:
        # Try partial match
        for p in paragraphs:
            text = get_paragraph_text(p).strip()
            if search_start[:30] in text:
                if replace_paragraph_text(p, new_text):
                    print(f"  \u2713 Replaced (partial): '{search_start[:50]}...'")
                    applied += 1
                    found = True
                    break
    
    if not found:
        print(f"  \u2717 NOT FOUND: '{search_start[:50]}...'")

# Handle the "Raised the bottom-line" bullet - it overlaps with Outperformed
# We want to keep the Outperformed version which now includes this info
# So we can just leave it or remove it
for p in paragraphs:
    text = get_paragraph_text(p).strip()
    if text.startswith("Raised the bottom-line territory share"):
        # Leave as-is for now - removing a paragraph from the table could break layout
        print(f"  ~ Kept duplicate Amazon bullet (safe to remove manually)")
        break

print(f"\nResults: {applied} replaced, {skipped} skipped")

# =============================================================================
# STEP 4: Write modified XML back to DOCX
# =============================================================================
modified_xml = etree.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)

# Rewrite the DOCX with modified document.xml
with zipfile.ZipFile(OUTPUT, 'w', zipfile.ZIP_DEFLATED) as zout:
    for name, data in all_files.items():
        if name == 'word/document.xml':
            zout.writestr(name, modified_xml)
        else:
            zout.writestr(name, data)

print(f"\n{'='*60}")
print(f"SUCCESS: Tailored CV saved to:")
print(f"  {OUTPUT}")
print(f"{'='*60}")

# =============================================================================
# VERIFY
# =============================================================================
print("\n--- VERIFICATION ---")
with zipfile.ZipFile(OUTPUT, 'r') as z:
    verify_xml = z.read('word/document.xml')

verify_tree = etree.fromstring(verify_xml)
verify_paras = verify_tree.findall('.//w:p', NSMAP)

print("Key paragraphs in output:")
for p in verify_paras:
    text = get_paragraph_text(p).strip()
    for kw in ['Pairwire', 'Google', 'Amazon', 'Salesforce', 'Built automated', 'Ran 147', 'Generated', 'Managed the entire']:
        if kw in text:
            print(f"  {text[:120]}")
            break
