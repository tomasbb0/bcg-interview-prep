"""
FINAL: Start from original, apply text changes AND normalize ALL bullet indentation.
Set every bullet paragraph to left=674, hanging=425 (Google/Amazon standard).
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
    # Normalize character spacing on the remaining run
    # Most of the CV uses charSpacing=-1 and width=105
    rPr = runs[0].find('w:rPr', NSMAP)
    if rPr is not None:
        # Set w:spacing val="-1" (character spacing)
        sp = rPr.find('w:spacing', NSMAP)
        if sp is None:
            sp = etree.SubElement(rPr, qn('spacing'))
        sp.set(qn('val'), '-1')
        # Set w:w val="105" (character width scaling)
        w_elem = rPr.find('w:w', NSMAP)
        if w_elem is None:
            w_elem = etree.SubElement(rPr, qn('w'))
        w_elem.set(qn('val'), '105')


# Fresh copy
shutil.copy2(SOURCE, OUTPUT)

with zipfile.ZipFile(SOURCE, 'r') as z:
    doc_xml = z.read('word/document.xml')
    all_files = {name: z.read(name) for name in z.namelist()}

tree = etree.fromstring(doc_xml)
paras = tree.findall('.//w:p', NSMAP)

# ===================================================================
# PART 1: TEXT REPLACEMENTS
# ===================================================================
replacements = {
    "Built automated GTM workflows (Pytho":
        "Built automated outbound workflows (Python + OpenAI API) processing 10,847+ leads into a qualified new-business pipeline, driving scalable prospecting with zero marketing spend.",
    "Ran 147 discovery calls with enterpr":
        "Ran 147+ consultative discovery calls with C-level and VP-level buyers, closing 34 engagements across 6-9 month sales cycles through needs-based, multi-stakeholder selling.",
    "Generated \u20ac41.2K in closed reven":
        "Generated \u20ac41.2K in closed revenue in 11 months, consistently exceeding quarterly targets through CRM-tracked pipeline management and structured sales follow-ups.",
    "Managed entire sales funnel: automat":
        "Managed entire sales funnel end-to-end: lead generation, CRM tracking, qualification, demo, negotiation, and close \u2014 all built from scratch with no prior commercial infrastructure.",
    "Designed and automated three globall":
        "Designed and automated 3 globally scalable dashboards (Apps Script, GMP) analyzing ROAS vs. profit and CPA vs. conversions, projecting $1.41M in annual media spend savings across EMEA.",
    "Built a reporting platform for partn":
        "Built a client-facing reporting platform (Looker Studio, Analytics 360) for partner managers to track financial impact and streamline ROI reporting, delivering an estimated \u20ac315K in annual efficiency gains.",
    "Led the \u201cFuture Trends\u201d seg":
        'Led the "Future Trends" keynote at Google\'s flagship partner event, presenting personally researched, data-driven insights on Peak Season strategy and media readiness to 237+ senior executives.',
    "Led and executed the project of expa":
        "Led Amazon's B2B retail expansion into Portugal, managing a pipeline of 2,311 target companies from prospecting to onboarding.",
    "Outperformed KPI benchmarks by 21x i":
        "Outperformed KPI benchmarks by 21x in account acquisition, raising territory share from 56% below to 25% above team average.",
    "Raised the bottom-line territory sha":
        "Drove highest conversion rate in the region, outperforming full-time colleagues across all account configuration metrics.",
    "Compiled a 19-pager consulting repor":
        "Authored a 19-page market intelligence report across 8 territories and 54 client interviews, shaping regional GTM strategy.",
    "Verified the yearly financial statem":
        "Verified yearly financial statements of 3 Insurance companies, managing client deliverables and cross-referencing accredited sources.",
    "Examined an asset portfolio worth 41":
        "Examined an \u20ac41.3B asset portfolio across 4 annual reports, building financial acumen applicable to enterprise conversations.",
    "Launched an Acceleration Program wit":
        "Launched an Acceleration Program with Portugal Fintech's founder, benchmarking 54 programs and building a GTM strategy from concept to launch.",
    "Python, Apps Script, Virtual Basic f":
        "Salesforce, HubSpot CRM, Google Ads, Looker Studio, Python, Apps Script, SQL, Power BI, DAX.",
}

print("=== TEXT REPLACEMENTS ===")
applied = 0
for prefix, new_text in replacements.items():
    for p in paras:
        text = get_para_text(p).strip()
        if text.startswith(prefix):
            set_para_text(p, new_text)
            applied += 1
            print(f"  \u2713 {new_text[:80]}...")
            break
print(f"  {applied}/{len(replacements)} applied\n")

# ===================================================================
# PART 2: NORMALIZE ALL BULLET INDENTATION
# Problem: Tables are NESTED (up to 3 levels deep). The absolute page
# position of a bullet depends on the SUM of ALL ancestor table indents.
#
# Example nesting (NOVA Education): tbl#3(142) > tbl#4(0) > tbl#5(117) = 259 total
#
# Fix: For each bullet paragraph, sum ALL ancestor table indents,
# then set paragraph_left = TARGET - total_indent
#
# Target absolute position (matching Google/Amazon in tbl#0, tblInd=180):
#   Text position = 854, Dash position = 429
# ===================================================================
print("=== INDENT NORMALIZATION (nested table compensation) ===")

TARGET_ABS_TEXT = 854   # Absolute text start position on page (twips)
TARGET_HANGING = 425    # Constant hanging indent


def get_tbl_ind(tbl):
    """Get a table's tblInd value."""
    tblPr = tbl.find('w:tblPr', NSMAP)
    if tblPr is None:
        return 0
    tblInd = tblPr.find('w:tblInd', NSMAP)
    if tblInd is None:
        return 0
    try:
        return int(tblInd.get(qn('w'), '0'))
    except ValueError:
        return 0


def get_total_table_indent(elem):
    """Sum tblInd from ALL ancestor tables (handles nesting)."""
    total = 0
    node = elem.getparent()
    while node is not None:
        if node.tag == qn('tbl'):
            total += get_tbl_ind(node)
        node = node.getparent()
    return total


indent_fixed = 0
for p in tree.findall('.//w:p', NSMAP):
    text = get_para_text(p).strip()
    if not text or len(text) < 5:
        continue

    pPr = p.find('w:pPr', NSMAP)
    if pPr is None:
        continue

    numPr = pPr.find('w:numPr', NSMAP)
    if numPr is None:
        continue

    # Sum ALL ancestor table indents
    total_tbl_ind = get_total_table_indent(p)

    # Compute needed paragraph left
    para_left = TARGET_ABS_TEXT - total_tbl_ind
    para_left_str = str(para_left)
    hang_str = str(TARGET_HANGING)

    # Set/update w:ind
    ind = pPr.find('w:ind', NSMAP)
    if ind is None:
        ind = etree.SubElement(pPr, qn('ind'))

    current_left = ind.get(qn('left'), '')
    current_hanging = ind.get(qn('hanging'), '')

    if current_left != para_left_str or current_hanging != hang_str:
        ind.set(qn('left'), para_left_str)
        ind.set(qn('hanging'), hang_str)
        if qn('firstLine') in ind.attrib:
            del ind.attrib[qn('firstLine')]
        indent_fixed += 1
        abs_dash = total_tbl_ind + para_left - TARGET_HANGING
        print(f"  \u2713 totalTblInd={total_tbl_ind} left={current_left or 'none'}->{para_left_str}: {text[:55]}...")

print(f"\n  {indent_fixed} bullets adjusted (all target: abs_dash=429, abs_text=854)")

# ===================================================================
# PART 3: NORMALIZE CHARACTER SPACING ON ALL BULLET RUNS
# The original CV has inconsistent charSpacing and width across runs.
# Some runs have charSpacing=-1 width=105, others have defaults.
# This causes visible letter spacing differences between sections.
# Fix: Set charSpacing=-1 and width=105 on ALL runs in bullet paragraphs.
# ===================================================================
print("\n=== CHARACTER SPACING NORMALIZATION ===")
spacing_fixed = 0

for p in tree.findall('.//w:p', NSMAP):
    pPr = p.find('w:pPr', NSMAP)
    if pPr is None:
        continue
    if pPr.find('w:numPr', NSMAP) is None:
        continue

    for run in p.findall('.//w:r', NSMAP):
        rPr = run.find('w:rPr', NSMAP)
        if rPr is None:
            continue

        changed = False

        # Normalize w:spacing val to -1
        sp = rPr.find('w:spacing', NSMAP)
        if sp is None:
            sp = etree.SubElement(rPr, qn('spacing'))
            sp.set(qn('val'), '-1')
            changed = True
        elif sp.get(qn('val')) != '-1':
            sp.set(qn('val'), '-1')
            changed = True

        # Normalize w:w val to 105
        w_elem = rPr.find('w:w', NSMAP)
        if w_elem is None:
            w_elem = etree.SubElement(rPr, qn('w'))
            w_elem.set(qn('val'), '105')
            changed = True
        elif w_elem.get(qn('val')) != '105':
            w_elem.set(qn('val'), '105')
            changed = True

        if changed:
            spacing_fixed += 1

print(f"  {spacing_fixed} runs normalized to charSpacing=-1, width=105")


# Save
modified_xml = etree.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)
with zipfile.ZipFile(OUTPUT, 'w', zipfile.ZIP_DEFLATED) as zout:
    for name, data in all_files.items():
        if name == 'word/document.xml':
            zout.writestr(name, modified_xml)
        else:
            zout.writestr(name, data)

print(f"\nSaved: {OUTPUT}")
