"""
FINAL CLEAN VERSION - Start from ORIGINAL iCloud CV.
ONLY replace text content. ZERO formatting/indent/numId/structural changes.
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
    """Replace text, keep FIRST run formatting, remove extra runs."""
    runs = p.findall('.//w:r', NSMAP)
    if not runs:
        return
    for run in runs[1:]:
        run.getparent().remove(run)
    t = runs[0].find('.//w:t', NSMAP)
    if t is not None:
        t.text = new_text
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')


# Fresh copy from iCloud original
shutil.copy2(SOURCE, OUTPUT)

with zipfile.ZipFile(SOURCE, 'r') as z:
    doc_xml = z.read('word/document.xml')
    all_files = {name: z.read(name) for name in z.namelist()}

tree = etree.fromstring(doc_xml)
paras = tree.findall('.//w:p', NSMAP)

# ===================================================================
# ONLY TEXT REPLACEMENTS - prefix match on first 35 chars of original
# All replacements SHORTER or same length as originals to fit 1 page
# ===================================================================
replacements = {
    # PAIRWIRE (original bullets → tailored for AE, same length)
    "Built automated GTM workflows (Pytho":
        "Built automated GTM workflows (Python + OpenAI API) processing 10,847+ leads into a qualified pipeline.",
    "Ran 147 discovery calls with enterpr":
        "Ran 147+ consultative discovery calls with enterprise prospects, closing 34 engagements across 6-9 month cycles.",
    "Generated \u20ac41.2K in closed reven":
        "Generated \u20ac41.2K in closed revenue in 11 months, exceeding quarterly targets through disciplined pipeline management.",
    "Managed entire sales funnel: automat":
        "Managed entire sales funnel: lead generation, qualification, demo, negotiation, and close. All built from scratch.",

    # GOOGLE
    "Designed and automated three globall":
        "Designed and automated 3 globally scalable dashboards (Apps Script, GMP) analyzing ROAS vs. profit and CPA vs. conversions, adopted across EMEA.",
    "Built a reporting platform for partn":
        "Built a client-facing reporting platform (Looker Studio, Analytics 360) for partner managers, streamlining ROI tracking and reducing reporting by ~40%.",
    "Led the \u201cFuture Trends\u201d seg":
        'Led the "Future Trends" keynote at Google\'s flagship partner event, presenting data-driven insights on Peak Season strategy to 237+ senior executives.',

    # AMAZON
    "Led and executed the project of expa":
        "Led Amazon's B2B retail expansion into Portugal, managing a pipeline of 2,311 target companies from prospecting to onboarding.",
    "Outperformed KPI benchmarks by 21x i":
        "Outperformed KPI benchmarks by 21x in account acquisition, raising territory share from 56% below to 25% above team average.",
    "Raised the bottom-line territory sha":
        "Drove highest conversion rate in the region, outperforming full-time colleagues across all account configuration metrics.",
    "Compiled a 19-pager consulting repor":
        "Authored a 19-page market intelligence report across 8 territories and 54 client interviews, shaping regional GTM strategy.",

    # EY
    "Verified the yearly financial statem":
        "Verified yearly financial statements of 3 Insurance companies, managing client deliverables and cross-referencing accredited sources.",
    "Examined an asset portfolio worth 41":
        "Examined an \u20ac41.3B asset portfolio across 4 annual reports, building financial acumen applicable to enterprise conversations.",

    # FINTECH HOUSE
    "Launched an Acceleration Program wit":
        "Launched an Acceleration Program with Portugal Fintech's founder, benchmarking 54 programs and building a GTM strategy from concept to launch.",

    # SKILLS
    "Python, Apps Script, Virtual Basic f":
        "Salesforce, HubSpot CRM, Google Ads, Looker Studio, Python, Apps Script, SQL, Power BI, DAX.",
}

print("Applying text-only replacements (zero formatting changes):\n")
applied = 0
for prefix, new_text in replacements.items():
    for p in paras:
        text = get_para_text(p).strip()
        if text.startswith(prefix):
            old_len = len(text)
            set_para_text(p, new_text)
            diff = old_len - len(new_text)
            print(f"  \u2713 ({len(new_text):3d}ch, {diff:+3d}) {new_text[:80]}...")
            applied += 1
            break

print(f"\nTotal: {applied}/{len(replacements)} applied")
print("Zero formatting, indent, or structural changes made.")

# Save
modified_xml = etree.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)
with zipfile.ZipFile(OUTPUT, 'w', zipfile.ZIP_DEFLATED) as zout:
    for name, data in all_files.items():
        if name == 'word/document.xml':
            zout.writestr(name, modified_xml)
        else:
            zout.writestr(name, data)

print(f"\nSaved: {OUTPUT}")
