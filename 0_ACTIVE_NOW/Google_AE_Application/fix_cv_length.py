"""
Fix CV to fit 1 page:
1. Shorten tailored bullets to match original lengths
2. Remove blanked paragraph rows from XML
"""
import zipfile
import os
from lxml import etree

SOURCE = os.path.expanduser("~/Downloads/TomásBatalha_Resume_02_2026_GOOGLE_AE.docx")
OUTPUT = SOURCE

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
# 1. SHORTEN TAILORED BULLETS (match original lengths ~80-100 chars)
# =============================================================================
print("=== SHORTENING BULLETS ===")

shortenings = [
    # Pairwire - originals were ~80-100 chars each
    (
        "Built automated GTM workflows (Python + OpenAI API) processing 10,847+",
        "Built automated GTM workflows (Python + OpenAI API) processing 10,847+ leads; pure outbound, zero marketing spend."
    ),
    (
        "Ran 147+ discovery calls with enterprise and mid-market",
        "Ran 147+ discovery calls with enterprise prospects, closing 34 engagements across 6\u20139 month sales cycles."
    ),
    (
        "Generated \u20ac41.2K in closed revenue within 11 months",
        "Generated \u20ac41.2K in closed revenue in 11 months through pure outbound, managing full pipeline to signed contract."
    ),
    (
        "Managed the entire sales funnel end-to-end",
        "Managed entire sales funnel: prospecting, qualification, demo, negotiation, and close \u2014 all processes built from scratch."
    ),
    
    # Google - trim to match originals (~130-150 chars)
    (
        "Designed and automated 3 globally scalable performance dashboards using Apps Script and GMP tools, enabling partner managers to track ROAS vs. profit and CPA vs. conversions",
        "Designed and automated 3 globally scalable dashboards using Apps Script and GMP tools to analyze ROAS vs. profit and CPA vs. conversions, adopted as EMEA\u2019s standard reporting framework."
    ),
    (
        "Built a cross-functional reporting platform for partner managers using Looker Studio and Analytics 360, streamlining project ROI tracking and reducing manual reporting effort",
        "Built a reporting platform for partner managers to track financial impact and streamline project ROI, using Looker Studio, Analytics 360, and Apps Script."
    ),
    (
        'Led the \u201cFuture Trends\u201d keynote segment at Google\u2019s flagship partner event, presenting data-driven insights on Peak Season',
        'Led the \u201cFuture Trends\u201d segment at Google\u2019s flagship partner event, presenting insights to 237+ senior clients on Peak Season advertising strategy.'
    ),

    # Amazon - trim
    (
        "Led the end-to-end expansion of Amazon\u2019s B2B retail segment into Portugal, managing a pipeline of 2,311 target companies from prospecting",
        "Led the expansion of Amazon\u2019s B2B retail segment into Portugal, managing a portfolio of 2,311 companies from prospecting through onboarding."
    ),
    (
        "Outperformed KPI benchmarks by 21x in account configurations, driving territory revenue share from 56% below to 25% above team average",
        "Outperformed KPI benchmarks by 21x in account configurations; raised territory share from 56% below to 25% above team average."
    ),
    (
        "Compiled a 19-page market intelligence report assessing B2B eCommerce opportunity across 8 territories and 54 targeted client interviews, directly informing",
        "Compiled a 19-page consulting report assessing B2B eCommerce across 8 territories and 54 client interviews, informing regional GTM strategy."
    ),

    # Leadership - trim condensed bullets
    (
        "Designed an online job platform for underserved professionals and organized 6 events",
        "Designed a job platform app for underserved professionals; organized 6 events including Fintech Day."
    ),
    (
        "Assessed organizational structure for WWF-partnered project, identifying 155 pain points across 7 workstreams; delivered 6 presentations",
        "Assessed organizational structure for WWF-partnered project, identifying 155 pain points across 7 workstreams."
    ),
    (
        "Founded and led a team of 23 volunteers, raising \u20ac2,539 and chairing 4 major events including one with 35 NGOs",
        "Founded a team of 23 volunteers, raised \u20ac2,539, and chaired 4 events including one with 35 NGOs."
    ),
]

for search_start, new_text in shortenings:
    for p in paragraphs:
        text = get_paragraph_text(p).strip()
        if text.startswith(search_start[:40]):
            replace_paragraph_text(p, new_text)
            print(f"  \u2713 Shortened: '{new_text[:60]}...' ({len(new_text)} chars)")
            break

# =============================================================================
# 2. REMOVE BLANKED PARAGRAPHS (those with just " " space)
# =============================================================================
print("\n=== REMOVING EMPTY ROWS ===")

removed = 0
for p in list(paragraphs):
    text = get_paragraph_text(p).strip()
    if text == "" or text == " ":
        # Check if this is in a table cell - if so we need to be careful
        parent = p.getparent()
        # Check if parent is a table cell (w:tc)
        if parent is not None and parent.tag.endswith('}tc'):
            # Check if this is the ONLY paragraph in the cell
            cell_paras = parent.findall('.//w:p', NSMAP)
            if len(cell_paras) == 1:
                # This is the only paragraph in a table cell - can't remove it
                # But we can try to remove the entire table row
                tc = parent
                tr = tc.getparent()
                if tr is not None and tr.tag.endswith('}tr'):
                    tbl = tr.getparent()
                    if tbl is not None:
                        tbl.remove(tr)
                        removed += 1
                        print(f"  \u2713 Removed empty table row")
            else:
                # Multiple paragraphs in cell - safe to remove this one
                parent.remove(p)
                removed += 1
                print(f"  \u2713 Removed empty paragraph in cell")

print(f"  Total removed: {removed}")

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

print(f"\n\u2713 Saved to: {OUTPUT}")

# Count total characters
print("\n=== CHARACTER COUNT CHECK ===")
with zipfile.ZipFile(OUTPUT, 'r') as z:
    verify_xml = z.read('word/document.xml')
verify_tree = etree.fromstring(verify_xml)
total_chars = 0
for p in verify_tree.findall('.//w:p', NSMAP):
    text = get_paragraph_text(p).strip()
    if text:
        total_chars += len(text)
print(f"  Total text characters: {total_chars}")
