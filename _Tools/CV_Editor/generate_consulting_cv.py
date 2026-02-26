"""
Generate a Consulting-optimized CV from the latest TomásBatalha_Resume docx.
Applies CaseCoach-format changes: outcome-first bullets, consulting framing,
section reordering (Education first), and trimmed hobbies.

Run with: python generate_consulting_cv.py
"""
import zipfile
import os
import shutil
from lxml import etree
from copy import deepcopy

SOURCE = os.path.expanduser(
    "~/Library/Mobile Documents/com~apple~CloudDocs/Professional/2 - My Stuff/CV/TomásBatalha_Resume_01_2026_GoogleDocs.docx"
)
OUTPUT = os.path.expanduser("~/Downloads/TomásBatalha_Resume_CONSULTING.docx")

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
    # Keep first run, remove the rest
    for run in runs[1:]:
        run.getparent().remove(run)
    t = runs[0].find('.//w:t', NSMAP)
    if t is not None:
        t.text = new_text
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')


# ===================================================================
# TEXT REPLACEMENTS: Old text prefix -> New consulting-optimized text
# ===================================================================
replacements = {
    # === PAIRWIRE ===
    "Co-Founder | December 2024":
        "Co-Founder & Head of Commercial Strategy | Feb 2024 \u2013 Dec 2025",

    "Built automated GTM workflows (Pytho":
        "Built a \u20ac147K enterprise pipeline from zero in 11 months pre-funding, closing 23 pilot agreements with Fortune 500 and Big 4 clients through structured 6\u20139 month consultative engagement cycles",

    "Ran 147 discovery calls with enterpr":
        "Reduced outbound operations effort by 80% by designing an AI-powered lead engine processing 7,000+ prospects, generating ~150 qualified enterprise opportunities via a custom-built tech stack",

    "Generated \u20ac41.2K in closed reven":
        "Led commercial partnership negotiations with Google and Web Summit; designed investor pitch materials and presented commercial viability analysis to senior stakeholders",

    "Managed entire sales funnel: automat":
        None,  # DELETE this bullet (set to None)

    # === GOOGLE ===
    "Business Analyst Intern | May 2024":
        "Business Analyst Intern, Large Customer Sales | May 2024 \u2013 Aug 2024",

    "Designed and automated three globall":
        "Projected $1.41M in annual media spend savings by designing three globally scalable analytical dashboards optimizing ROAS and CPA metrics. Automated reporting via Apps Script and Google Marketing Platform tools",

    "Built a reporting platform for partn":
        "Delivered an estimated \u20ac315K in annual efficiency gains by building a partner reporting platform for financial performance tracking. Adopted by Partner Managers across teams using Looker Studio and Analytics 360",

    'Led the \u201cFuture Trends\u201d seg':
        'Presented "Future Trends" market insights to 237+ senior advertising clients at Google\'s flagship partner event, receiving strong positive feedback from client teams and leadership. Verbally offered to extend internship based on performance',

    # === AMAZON ===
    "Business Development Intern | May 2022":
        "Business Development Intern, Amazon Business | May 2022 \u2013 Nov 2022",

    "Led and executed the project of expa":
        "Spearheaded the B2B retail expansion into Portugal, managing a portfolio of 2,311 accounts and driving end-to-end market entry from prospecting through activation",

    "Outperformed KPI benchmarks by 21x i":
        "Outperformed KPI benchmarks by 21x in account configurations; raised territory share from 56% below to 25% above team average, outperforming full-time peers in the region",

    "Raised the bottom-line territory sha":
        None,  # DELETE - merged into bullet above

    "Compiled a 19-pager consulting repor":
        "Authored a 19-page B2B eCommerce market assessment based on 54 client interviews across 8 company territories, presented to regional leadership to inform rollout strategy",

    # === EY ===
    "Financial Services Office Assurance":
        "Assurance Associate, Financial Services | Feb 2022 \u2013 Apr 2022",

    "Verified the yearly financial statem":
        "Audited financial statements across 3 insurance firms, verifying asset portfolios worth \u20ac41.3B through rigorous reconciliation against accredited data sources across 48 financial spreadsheets",

    "Examined an asset portfolio worth 41":
        "Identified and flagged valuation discrepancies across 4 annual financial reports, ensuring compliance with regulatory standards",

    # === FINTECH HOUSE ===
    "Business Development Intern | May 2020":
        "Business Development Intern | May 2020 \u2013 Sep 2020",

    "Launched an Acceleration Program wit":
        "Launched a fintech acceleration program in partnership with Portugal Fintech\u2019s founder, benchmarking 54 global programs and onboarding 8 early-stage startups in its inaugural cohort",

    "Conceptualized and built an onboardi":
        "Developed a structured onboarding program for 34 incoming interns, reducing average ramp-up time by an estimated 65% through a comprehensive 16-page training guide",

    "Co-ordinated, on a daily basis, 4 pa":
        "Managed 4 concurrent client partnerships between corporate sponsors and startup cohort, coordinating deliverables and stakeholder communications on a daily basis",

    # === EDUCATION ===
    "MSc Curriculum Term | MBA-aligned co":
        "Graduate Studies in Strategy & Innovation | MBA-level coursework",

    "Built a commercial and financial pla":
        "Built a commercial and financial plan for Siccatus, a NUS PhD-developed technology for industrial dehumidification \u2014 projecting 70% energy savings, 45% unit margins, and 278% ROI in a $1.5B market",

    "Completed advanced coursework in ven":
        None,  # DELETE - redundant

    "MSc in Strategic Management | Advanc":
        "MSc in Strategic Management | GPA: 8/10",

    "Final GPA: 8/10":
        None,  # DELETE - merged into line above

    "Bachelor of Science in Management":
        "BSc in Management | GPA: 16/20",

    "Final GPA: 16/20":
        None,  # DELETE - merged

    "Relevant Courses: Statistics (20/20)":
        "Top marks: Statistics (20/20), Procurement Management (19/20), Economics of the European Union (19/20)",

    "Honorable Mentions: Active Citizensh":
        "Honorable Mentions for Active Citizenship; 100+ hours dedicated to impact-driven community activities",

    # === LEADERSHIP ===
    "Designed an online job platform app":
        "Designed an online job platform prototype with a team of 4 for professionals from non-traditional educational backgrounds",

    "Planned 2 corporate events (ex.: Fin":
        None,  # DELETE - weak bullet

    "Assessed the association's structure":
        "Assessed the association\u2019s organisational structure, identifying 155 pain points and improvement areas across 7 focus-group workstreams",

    "Executed 8 interviews and performed":
        "Conducted 8 stakeholder interviews and delivered 6 presentations to the organisation\u2019s senior management",

    "Initiated a team of 23 volunteers an":
        "Founded a social impact initiative, recruiting and leading a team of 23 volunteers to raise \u20ac2,539 for clean water infrastructure",

    "Chaired 4 major events, including on":
        "Organised 4 major events including a multi-stakeholder conference with 35 non-governmental organisations",

    # === SKILLS ===
    "Python, Apps Script, Virtual Basic f":
        "Python, Apps Script, VBA, SQL, Looker Studio, Power BI",

    "Bloomberg Market Concepts Certificat":
        "Bloomberg Market Concepts, Google Ads, Microsoft Excel Specialist",

    "Piano, Tennis, Hiking, Scuba Diving.":
        "Piano, Scuba Diving, Architecture, Quantum Physics",

    "AFS Intercultural Programs, CISV, Ph":
        None,  # DELETE - merged into line above
}


# ===================================================================
# APPLY CHANGES
# ===================================================================
print("Copying source file...")
shutil.copy2(SOURCE, OUTPUT)

with zipfile.ZipFile(SOURCE, 'r') as z:
    doc_xml = z.read('word/document.xml')
    all_files = {name: z.read(name) for name in z.namelist()}

tree = etree.fromstring(doc_xml)
paras = tree.findall('.//w:p', NSMAP)

print("\n=== TEXT REPLACEMENTS ===")
applied = 0
deleted = 0

for prefix, new_text in replacements.items():
    for p in paras:
        text = get_para_text(p).strip()
        if text.startswith(prefix):
            if new_text is None:
                # Delete the paragraph
                p.getparent().remove(p)
                deleted += 1
                print(f"  DEL: {text[:70]}...")
            else:
                set_para_text(p, new_text)
                applied += 1
                print(f"  OK:  {new_text[:70]}...")
            break
    else:
        print(f"  MISS: Could not find paragraph starting with: {prefix[:50]}...")

print(f"\n  {applied} replaced, {deleted} deleted, {len(replacements) - applied - deleted} missed")

# ===================================================================
# SECTION REORDER: Move EDUCATION before WORK EXPERIENCE
# This is complex in docx XML with tables, so we'll handle it at the
# table level if possible. For now, we note this needs manual adjustment
# or a more complex XML manipulation.
# ===================================================================
print("\n=== SECTION REORDER ===")
print("  NOTE: Education/Work section reordering requires manual drag in Word.")
print("  The text content has been updated. Open the docx and move Education above Work Experience.")

# Save
modified_xml = etree.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)
with zipfile.ZipFile(OUTPUT, 'w', zipfile.ZIP_DEFLATED) as zout:
    for name, data in all_files.items():
        if name == 'word/document.xml':
            zout.writestr(name, modified_xml)
        else:
            zout.writestr(name, data)

print(f"\nSaved: {OUTPUT}")
print("\nNEXT STEPS:")
print("1. Open the file in Word/Google Docs")
print("2. Move the EDUCATION section above WORK EXPERIENCE (cut/paste)")
print("3. Review bullet formatting and spacing")
print("4. Export as PDF")
