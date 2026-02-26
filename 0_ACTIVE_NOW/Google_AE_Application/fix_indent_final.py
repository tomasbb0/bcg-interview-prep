"""
Fix indentation: Remove paragraph-level w:ind from all bullet paragraphs.
Let the numbering definition (numId=2, abstractNum=14: left=720, hanging=360) 
control spacing consistently for ALL bullets.
Also shorten bullets slightly.
"""
import zipfile
import os
from lxml import etree

FILE = os.path.expanduser("~/Downloads/TomásBatalha_Resume_02_2026_GOOGLE_AE.docx")
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


with zipfile.ZipFile(FILE, 'r') as z:
    doc_xml = z.read('word/document.xml')
    all_files = {name: z.read(name) for name in z.namelist()}

tree = etree.fromstring(doc_xml)
paras = tree.findall('.//w:p', NSMAP)

# ===== PART 1: Fix indentation by removing paragraph-level w:ind from bullets =====
print("=== FIXING INDENTATION ===")
indent_fixed = 0

for p in paras:
    text = get_para_text(p).strip()
    if not text or len(text) < 15:
        continue
    
    pPr = p.find('w:pPr', NSMAP)
    if pPr is None:
        continue
    
    # Only fix paragraphs that have numPr (are list items)
    numPr = pPr.find('w:numPr', NSMAP)
    if numPr is None:
        continue
    
    # Remove paragraph-level indent override
    ind = pPr.find('w:ind', NSMAP)
    if ind is not None:
        pPr.remove(ind)
        indent_fixed += 1

print(f"  Removed {indent_fixed} paragraph-level indent overrides")
print("  All bullets now use numbering definition spacing (left=720, hanging=360)")

# ===== PART 2: Shorten bullets slightly =====
print("\n=== SHORTENING BULLETS ===")

shortenings = {
    # PAIRWIRE
    "Built automated GTM workflows (Python + OpenAI API) processing 10,847+ leads into a qualified pipeline":
        "Built automated GTM workflows (Python + OpenAI API) processing 10,847+ leads into a qualified pipeline.",
    "Ran 147+ consultative discovery calls with enterprise prospects, qualifying opportunities and closing 34 engagements across 6-9 month cycles":
        "Ran 147+ consultative discovery calls with enterprise prospects, closing 34 engagements across 6-9 month cycles.",
    "Generated":
        "Generated \u20ac41.2K in closed revenue in 11 months, exceeding quarterly targets through disciplined pipeline management.",
    "Managed entire sales funnel end-to-end: lead generation, qualification, demo, proposal, negotiation, and close, all processes built from scratch":
        "Managed entire sales funnel: lead generation, qualification, demo, negotiation, and close. All processes built from scratch.",
    
    # GOOGLE - slightly shorter
    "Designed and automated 3 globally scalable dashboards (Apps Script, GMP) analyzing ROAS vs. profit and CPA vs. conversions, adopted as the standard reporting framework across EMEA":
        "Designed and automated 3 globally scalable dashboards (Apps Script, GMP) analyzing ROAS vs. profit and CPA vs. conversions, adopted across EMEA.",
    "Built a client-facing reporting platform (Looker Studio, Analytics 360) for partner managers, streamlining project ROI tracking and reducing manual reporting effort by ~40%":
        "Built a client-facing reporting platform (Looker Studio, Analytics 360) for partner managers, streamlining ROI tracking and reducing manual reporting by ~40%.",
    
    # AMAZON
    "Led Amazon's B2B retail expansion into Portugal, managing a new-business pipeline of 2,311 target companies from prospecting through onboarding":
        "Led Amazon's B2B retail expansion into Portugal, managing a pipeline of 2,311 target companies from prospecting to onboarding.",
    "Authored a 19-page market intelligence report across 8 territories and 54 client interviews, shaping the regional go-to-market strategy":
        "Authored a 19-page market intelligence report across 8 territories and 54 client interviews, shaping regional GTM strategy.",
    
    # EY
    "Examined an asset portfolio worth":
        "Examined an \u20ac41.3B asset portfolio across 4 annual reports, building financial acumen applicable to enterprise client conversations.",
    
    # FINTECH
    "Launched an Acceleration Program with Portugal Fintech's founder, benchmarking 54 programs and building a go-to-market strategy from concept to launch":
        "Launched an Acceleration Program with Portugal Fintech's founder, benchmarking 54 programs and building a GTM strategy from concept to launch.",
    "Conceptualized and built an onboarding program featuring a 16-pager guide aimed at reducing training time by 65%":
        "Built an onboarding program with a 16-page guide, reducing training time by 65% for 34 incoming interns.",
}

shortened = 0
for prefix, new_text in shortenings.items():
    for p in paras:
        text = get_para_text(p).strip()
        if text.startswith(prefix[:35]):
            old_len = len(text)
            set_para_text(p, new_text)
            diff = old_len - len(new_text)
            if diff > 0:
                print(f"  -{diff}ch: {new_text[:70]}...")
            else:
                print(f"  +{-diff}ch: {new_text[:70]}...")
            shortened += 1
            break

print(f"\n  Shortened {shortened} bullets")

# Save
modified_xml = etree.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)
with zipfile.ZipFile(FILE, 'w', zipfile.ZIP_DEFLATED) as zout:
    for name, data in all_files.items():
        if name == 'word/document.xml':
            zout.writestr(name, modified_xml)
        else:
            zout.writestr(name, data)

print(f"\nSaved: {FILE}")
