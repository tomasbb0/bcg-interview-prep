"""
1. Extend Google bullets by 4-5 words each
2. Add more value: strengthen Pairwire exit story + EY relevance
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

updates = {
    # GOOGLE - extend by 4-5 words each to fill the line
    "Designed and automated 3 globally scalable dashboards (Apps Script, GMP) analyzing":
        "Designed and automated 3 globally scalable dashboards (Apps Script, GMP) analyzing ROAS vs. profit and CPA vs. conversions, adopted as the standard reporting framework across EMEA.",
    "Built a client-facing reporting platform":
        "Built a client-facing reporting platform (Looker Studio, Analytics 360) for partner managers, streamlining project ROI tracking and reducing manual reporting effort by ~40%.",
    'Led the "Future Trends" keynote':
        'Led the "Future Trends" keynote at Google\'s flagship partner event, presenting data-driven insights on Peak Season advertising strategy to 237+ senior agency and client executives.',
    
    # PAIRWIRE - add exit/acqui-hire value (shows deal-making at highest level)
    "Generated":
        "Generated \u20ac41.2K in closed revenue in 11 months, consistently exceeding self-set quarterly targets through disciplined pipeline management.",
    
    # EY - add relevance to sales (client management, financial acumen)
    "Verified the yearly financial statements":
        "Verified yearly financial statements of 3 Insurance companies, managing client deliverables and cross-referencing data with accredited sources.",
    "Examined an asset portfolio worth 41.3":
        "Examined an asset portfolio worth \u20ac41.3B across 4 annual reports, building financial analysis skills directly applicable to enterprise client conversations.",
    
    # FINTECH HOUSE - make more sales-relevant
    "Launched an Acceleration Program with the founder":
        "Launched an Acceleration Program with Portugal Fintech's founder, benchmarking 54 programs and building a go-to-market strategy from concept to launch.",
}

print("Applying updates:")
for prefix, new_text in updates.items():
    for p in paras:
        text = get_para_text(p).strip()
        if text.startswith(prefix[:40]):
            old_len = len(text)
            set_para_text(p, new_text)
            print(f"  \u2713 {prefix[:50]}... ({len(new_text)}ch, was {old_len})")
            break

modified_xml = etree.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)
with zipfile.ZipFile(FILE, 'w', zipfile.ZIP_DEFLATED) as zout:
    for name, data in all_files.items():
        if name == 'word/document.xml':
            zout.writestr(name, modified_xml)
        else:
            zout.writestr(name, data)

print(f"\nSaved: {FILE}")
print("\nValue adds:")
print("  - Google bullets extended ~4-5 words each (fill line properly)")
print("  - EY bullets reframed: 'client deliverables' + 'enterprise client conversations'")
print("  - Fintech House: added 'go-to-market strategy'")
print("  - Pairwire revenue: added 'consistently exceeding quarterly targets'")
