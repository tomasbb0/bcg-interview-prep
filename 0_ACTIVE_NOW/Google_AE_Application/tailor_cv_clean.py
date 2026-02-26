"""
CLEAN VERSION - Start from original, ONLY replace bullet text. NO structural changes.
"""
import zipfile
import os
import shutil
from lxml import etree

SOURCE = os.path.expanduser(
    "~/Library/Mobile Documents/com~apple~CloudDocs/Professional/2 - My Stuff/CV/TomásBatalha_Resume_02_2026.docx"
)
OUTPUT = os.path.expanduser("~/Downloads/TomásBatalha_Resume_02_2026_GOOGLE_AE.docx")

NSMAP = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


def get_para_text(p):
    return ''.join(t.text for t in p.findall('.//w:t', NSMAP) if t.text)


def set_para_text(p, new_text):
    """Replace text in paragraph, keeping first run's formatting."""
    runs = p.findall('.//w:r', NSMAP)
    if not runs:
        return
    for run in runs[1:]:
        run.getparent().remove(run)
    t = runs[0].find('.//w:t', NSMAP)
    if t is not None:
        t.text = new_text
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')


# Copy original
shutil.copy2(SOURCE, OUTPUT)

# Read
with zipfile.ZipFile(SOURCE, 'r') as z:
    doc_xml = z.read('word/document.xml')
    all_files = {name: z.read(name) for name in z.namelist()}

tree = etree.fromstring(doc_xml)
paras = tree.findall('.//w:p', NSMAP)

# =================================================================
# TEXT-ONLY REPLACEMENTS (prefix match → new text)
# All bullets kept SHORT to preserve 1-page fit
# =================================================================
replacements = {
    # PAIRWIRE - light tailoring for sales language
    "Built automated GTM workflows":
        "Built automated GTM workflows (Python + OpenAI API) processing 10,847+ leads; pure outbound, zero marketing spend.",
    "Ran 147 discovery calls":
        "Ran 147+ discovery calls with enterprise prospects, closing 34 engagements across 6\u20139 month sales cycles.",
    "Generated \u20ac41.2K in closed revenue in 11 months. Zero":
        "Generated \u20ac41.2K in closed revenue in 11 months through pure outbound; managed full pipeline to signed contract.",
    "Managed entire sales funnel: automated":
        "Managed entire sales funnel: prospecting, qualification, demo, negotiation, and close \u2014 all built from scratch.",
    
    # GOOGLE - light tailoring
    "Designed and automated three globally":
        "Designed and automated 3 globally scalable dashboards using Apps Script and GMP tools to analyze ROAS vs. profit and CPA vs. conversions, adopted as EMEA\u2019s standard reporting framework.",
    "Built a reporting platform for partner managers to track financial":
        "Built a reporting platform for partner managers to track ROI using Looker Studio, Analytics 360, and Apps Script; reduced manual reporting by ~40%.",
    "Led the \u201cFuture Trends\u201d segment at Google\u2019s flagship partner event, presenting personally":
        "Led the \u201cFuture Trends\u201d segment at Google\u2019s flagship partner event, presenting insights to 237+ senior clients on Peak Season advertising strategy.",
    
    # AMAZON - light tailoring
    "Led and executed the project of expansion":
        "Led the expansion of Amazon\u2019s B2B retail segment into Portugal, managing a portfolio of 2,311 companies from prospecting to onboarding.",
    "Outperformed KPI benchmarks by 21x in company account config":
        "Outperformed KPI benchmarks by 21x in account configurations, driving territory share from 56% below to 25% above team average.",
    "Raised the bottom-line territory share from 56% below":
        "Raised territory revenue share from 56% below to 25% above team average, outperforming full-time colleagues in the region.",
    "Compiled a 19-pager consulting report":
        "Compiled a 19-page consulting report assessing B2B eCommerce across 8 territories and 54 client interviews, informing regional GTM strategy.",
    
    # SKILLS
    "Python, Apps Script, Virtual Basic":
        "Salesforce, HubSpot CRM, Google Ads, Looker Studio, Python, Apps Script, SQL, Power BI, DAX.",
}

print("Applying text replacements:")
for prefix, new_text in replacements.items():
    found = False
    for p in paras:
        text = get_para_text(p).strip()
        if text.startswith(prefix[:35]):
            set_para_text(p, new_text)
            print(f"  \u2713 {prefix[:50]}... -> ({len(new_text)} chars)")
            found = True
            break
    if not found:
        print(f"  \u2717 NOT FOUND: {prefix[:50]}")

# Save
modified_xml = etree.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)
with zipfile.ZipFile(OUTPUT, 'w', zipfile.ZIP_DEFLATED) as zout:
    for name, data in all_files.items():
        if name == 'word/document.xml':
            zout.writestr(name, modified_xml)
        else:
            zout.writestr(name, data)

print(f"\n\u2713 Saved: {OUTPUT}")
print("\nAll sections, titles, and structure preserved. Only bullet TEXT changed.")
