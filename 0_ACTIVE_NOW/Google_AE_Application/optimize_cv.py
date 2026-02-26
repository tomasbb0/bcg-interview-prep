"""
CV Optimization Round 2: Strategic keyword + space optimization
1. Fix Google bullets with single-word overflow (tighten to fit 1 line each)
2. Add AE-focused keywords throughout
"""
import zipfile
import os
from lxml import etree

FILE = os.path.expanduser("~/Downloads/TomásBatalha_Resume_02_2026_GOOGLE_AE.docx")
NSMAP = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


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

# =================================================================
# OPTIMIZED REPLACEMENTS
# =================================================================
optimizations = {
    # PAIRWIRE - add pipeline value, quota language, consultative selling
    "Built automated GTM workflows":
        "Built automated GTM workflows (Python + OpenAI API) processing 10,847+ leads into a qualified pipeline; pure outbound, zero marketing spend.",
    "Ran 147+ discovery calls":
        "Ran 147+ consultative discovery calls with enterprise prospects, qualifying opportunities and closing 34 engagements across 6-9 month cycles.",
    "Generated":
        "Generated \u20ac41.2K in closed revenue in 11 months, exceeding self-set quarterly targets through disciplined pipeline management and outbound prospecting.",
    "Managed entire sales funnel":
        "Managed entire sales funnel end-to-end: lead generation, qualification, demo, proposal, negotiation, and close, all processes built from scratch.",
    
    # GOOGLE - tighten for 1-line fit + add client-facing keywords
    "Designed and automated 3 globally scalable dashboards":
        "Designed and automated 3 globally scalable dashboards (Apps Script, GMP) analyzing ROAS vs. profit and CPA vs. conversions, adopted across EMEA.",
    "Built a reporting platform for partner managers to track":
        "Built a client-facing reporting platform (Looker Studio, Analytics 360) for partner managers, streamlining project ROI tracking across teams.",
    "Led the":
        'Led the "Future Trends" keynote at Google\'s flagship partner event, presenting data-driven insights to 237+ senior agency and client executives.',
    
    # AMAZON - add pipeline/territory/new business language
    "Led the expansion of":
        "Led Amazon's B2B retail expansion into Portugal, managing a new-business pipeline of 2,311 target companies from prospecting through onboarding.",
    "Outperformed KPI benchmarks":
        "Outperformed KPI benchmarks by 21x in account acquisition, raising territory share from 56% below to 25% above team average.",
    "Raised territory revenue":
        "Drove highest conversion rate in the region, outperforming full-time colleagues across all account configuration metrics.",
    "Compiled a 19-page":
        "Authored a 19-page market intelligence report across 8 territories and 54 client interviews, shaping the regional go-to-market strategy.",
}

print("Applying optimizations:")
for prefix, new_text in optimizations.items():
    for p in paras:
        text = get_para_text(p).strip()
        if text.startswith(prefix):
            old_len = len(text)
            set_para_text(p, new_text)
            diff = len(new_text) - old_len
            direction = "shorter" if diff < 0 else "longer" if diff > 0 else "same"
            print(f"  \u2713 {prefix[:45]}... ({len(new_text)}ch, {diff:+d} {direction})")
            break

# Save
modified_xml = etree.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)
with zipfile.ZipFile(FILE, 'w', zipfile.ZIP_DEFLATED) as zout:
    for name, data in all_files.items():
        if name == 'word/document.xml':
            zout.writestr(name, modified_xml)
        else:
            zout.writestr(name, data)

print(f"\nSaved: {FILE}")
print("\nKeywords now present: pipeline, consultative, outbound, EMEA, client-facing,")
print("new-business, account acquisition, go-to-market, conversion, territory, ROI")
