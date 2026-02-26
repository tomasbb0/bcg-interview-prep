#!/usr/bin/env python3
"""
Fix Google AE resume to match the tailored plan in CV_TAILORED_GOOGLE_AE.md.
Uses lxml + zipfile (proven approach from CV_DOCX_CHEAT_SHEET.md).

Changes:
1. Pairwire title: "Co-Founder" → "Co-Founder and Head of Sales"
2. Pairwire dates: "December 2024 – Present" → "February 2024 – December 2025"
3. Pairwire bullet 1: rewrite (pipeline focus)
4. Pairwire bullet 2: rewrite (enterprise engagements)
5. Pairwire bullet 3: rewrite (AI outbound engine)
6. Pairwire bullet 4: rewrite (end-to-end deal management)
7. Google title: add "(Large Customer Sales)"
8. Google bullet order: put "Future Trends" first (keynote = strongest for AE)
9. Google bullet 1 (now dashboards): rewrite
10. Google bullet 2 (reporting platform): rewrite
11. Google bullet 3 (Future Trends): rewrite + move to first position
12. EY: condense to 1 bullet
13. Fintech: delete all bullets (keep structure minimal)
14. Skills: update to include sales tools
15. Delete "Hobbies:" / "Interests:" artifact
"""

import zipfile
from lxml import etree
import copy

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NSMAP = {'w': W}

def qn(tag):
    return f'{{{W}}}{tag}'

def get_para_text(p):
    return ''.join(t.text for t in p.iter(qn('t')) if t.text)

def set_para_text(p, new_text):
    """Replace ALL text in a paragraph. Keeps first run's formatting."""
    runs = p.findall(f'.//{qn("r")}')
    if not runs:
        return
    for run in runs[1:]:
        run.getparent().remove(run)
    t_elem = runs[0].find(f'.//{qn("t")}')
    if t_elem is not None:
        t_elem.text = new_text
        t_elem.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')

def delete_para_text(p):
    """Clear all text from paragraph (makes it invisible)."""
    for t_elem in p.iter(qn('t')):
        t_elem.text = ''
    # Also set spacing to minimum to hide the empty line
    pPr = p.find(qn('pPr'))
    if pPr is None:
        pPr = etree.SubElement(p, qn('pPr'))
    spacing = pPr.find(qn('spacing'))
    if spacing is None:
        spacing = etree.SubElement(pPr, qn('spacing'))
    spacing.set(qn('before'), '0')
    spacing.set(qn('after'), '0')
    spacing.set(qn('line'), '20')
    spacing.set(qn('lineRule'), 'exact')
    # Also set font size to 1pt
    rPr = pPr.find(qn('rPr'))
    if rPr is None:
        rPr = etree.SubElement(pPr, qn('rPr'))
    sz = rPr.find(qn('sz'))
    if sz is None:
        sz = etree.SubElement(rPr, qn('sz'))
    sz.set(qn('val'), '2')

# --- Configuration ---
SOURCE = '/Users/tomasbatalha/Downloads/TomásBatalha_Resume_02_2026_GOOGLE_AE.docx'
OUTPUT = '/Users/tomasbatalha/Downloads/TomásBatalha_Resume_02_2026_GOOGLE_AE_FIXED.docx'

# --- Load ---
with zipfile.ZipFile(SOURCE) as z:
    doc_xml = z.read('word/document.xml')
    all_files = {name: z.read(name) for name in z.namelist()}

tree = etree.fromstring(doc_xml)

# --- Build paragraph index ---
replacements = 0
deletions = 0

for p in tree.iter(qn('p')):
    text = get_para_text(p).strip()
    
    # === PAIRWIRE FIXES ===
    
    # Title fix
    if text == 'Co-Founder | December 2024 \u2013 Present' or text.startswith('Co-Founder | December 2024'):
        set_para_text(p, 'Co-Founder and Head of Sales | February 2024 \u2013 December 2025')
        print(f"✓ Pairwire title+dates fixed")
        replacements += 1
    
    # Bullet 1: outbound workflows → pipeline
    elif text.startswith('Built automated outbound workflows'):
        set_para_text(p, 'Built \u20ac147K pipeline of contracted enterprise pilots from zero in 11 months pre-funding through outbound prospecting, cold calling, consulting, and relationship management.')
        print(f"✓ Pairwire bullet 1: pipeline focus")
        replacements += 1
    
    # Bullet 2: discovery calls → enterprise engagements
    elif text.startswith('Ran 147+ consultative discovery'):
        set_para_text(p, 'Closed 23 enterprise engagements including Fortune 500 and Big 4 firms across 6\u20139 month full-cycle sales processes.')
        print(f"✓ Pairwire bullet 2: enterprise engagements")
        replacements += 1
    
    # Bullet 3: revenue → AI outbound engine
    elif text.startswith('Generated \u20ac41.2K in closed revenue') or text.startswith('Generated'):
        set_para_text(p, 'Designed an AI-powered outbound engine processing 7,000+ leads, automating 80% of prospecting via custom tech stack (Python, Expand.io, AI-enhanced workflows).')
        print(f"✓ Pairwire bullet 3: AI outbound engine")
        replacements += 1
    
    # Bullet 4: sales funnel → deal management
    elif text.startswith('Managed entire sales funnel'):
        set_para_text(p, 'Led end-to-end deal management from first touch to contract close, managing entire funnel with no sales team or brand recognition.')
        print(f"✓ Pairwire bullet 4: deal management")
        replacements += 1
    
    # === GOOGLE FIXES ===
    
    # Title: add (Large Customer Sales)
    elif text.startswith('Business Analyst Intern | May 2024'):
        set_para_text(p, 'Business Analyst Intern, Large Customer Sales | May 2024 \u2013 August 2024')
        print(f"✓ Google title: added (Large Customer Sales)")
        replacements += 1
    
    # Google bullet 1 (dashboards): rewrite for AE framing
    elif text.startswith('Designed and automated 3 globally scalable'):
        set_para_text(p, 'Designed and automated three globally scalable dashboards using Apps Script and GMP tools to analyze ROAS vs. profit and CPA vs. conversions, projecting $1.41M in annual savings for media spend decisions.')
        print(f"✓ Google bullet 1: AE-framed dashboards")
        replacements += 1
    
    # Google bullet 2 (reporting platform): rewrite
    elif text.startswith('Built a client-facing reporting platform'):
        set_para_text(p, 'Built a reporting platform for Partner Managers using Looker Studio, Analytics 360, and Apps Script, delivering an estimated \u20ac315K in annual efficiency gains.')
        print(f"✓ Google bullet 2: reporting platform")
        replacements += 1
    
    # Google bullet 3 (Future Trends): rewrite
    elif text.startswith('Led the \u201cFuture Trends\u201d keynote') or text.startswith('Led the "Future Trends"'):
        set_para_text(p, 'Led the \u201cFuture Trends\u201d segment at Google\u2019s flagship partner event, presenting personally researched insights on Peak Season activation and media readiness to 237+ senior advertising clients.')
        print(f"✓ Google bullet 3: Future Trends")
        replacements += 1
    
    # === AMAZON FIXES ===
    
    # Amazon bullet 1: minor
    elif text.startswith("Led Amazon's B2B retail expansion") or text.startswith("Led Amazon\u2019s B2B retail"):
        set_para_text(p, 'Led the B2B retail expansion into Portugal, managing a portfolio of 2,311 companies through prospecting, outreach, and account activation.')
        print(f"✓ Amazon bullet 1: fixed")
        replacements += 1
    
    # Amazon bullet 3: "Drove highest conversion" → delete (not in tailored plan)
    elif text.startswith('Drove highest conversion rate'):
        delete_para_text(p)
        print(f"✓ Amazon bullet 3: deleted (not in plan)")
        deletions += 1
    
    # Amazon bullet 4: market report
    elif text.startswith('Authored a 19-page market intelligence'):
        set_para_text(p, 'Compiled a 19-page strategic report on B2B eCommerce based on 8 company territories and 54 targeted client interviews.')
        print(f"✓ Amazon bullet 4: report rewrite")
        replacements += 1
    
    # === EY FIXES ===
    
    # EY title: simplify
    elif text.startswith('Financial Services Office Assurance Associate'):
        set_para_text(p, 'Assurance Associate, Financial Services | Feb 2022 \u2013 Apr 2022')
        print(f"✓ EY title: simplified")
        replacements += 1
    
    # EY bullet 1: rewrite + condense
    elif text.startswith('Verified yearly financial'):
        set_para_text(p, 'Audited asset portfolios worth \u20ac41.3 billion across 3 insurance firms, developing rigorous data verification and attention to detail.')
        print(f"✓ EY bullet 1: condensed")
        replacements += 1
    
    # EY bullet 2: delete (plan has only 1 bullet)
    elif text.startswith('Examined an') and '41.3B' in text:
        delete_para_text(p)
        print(f"✓ EY bullet 2: deleted")
        deletions += 1
    
    # === FINTECH FIXES ===
    # Delete all Fintech bullets (not in tailored plan)
    elif text.startswith('Launched an Acceleration Program'):
        delete_para_text(p)
        print(f"✓ Fintech bullet 1: deleted")
        deletions += 1
    elif text.startswith('Conceptualized and built an onboarding'):
        delete_para_text(p)
        print(f"✓ Fintech bullet 2: deleted")
        deletions += 1
    elif text.startswith('Co-ordinated, on a daily basis'):
        delete_para_text(p)
        print(f"✓ Fintech bullet 3: deleted")
        deletions += 1
    
    # Delete Fintech header and role too
    elif text == 'Fintech House | Lisbon, Portugal':
        delete_para_text(p)
        print(f"✓ Fintech header: deleted")
        deletions += 1
    elif text.startswith('Business Development Intern | May 2020'):
        delete_para_text(p)
        print(f"✓ Fintech role line: deleted")
        deletions += 1
    
    # === EDUCATION FIXES ===
    
    # Rotterdam: simplify description
    elif text.startswith('MSc in Strategic Management | Advanced coursework'):
        set_para_text(p, 'MSc in Strategic Management | GPA: 8/10')
        print(f"✓ Rotterdam: simplified to just degree + GPA")
        replacements += 1
    
    # Delete "Final GPA: 8/10" (now in title line)
    elif text == 'Final GPA: 8/10':
        delete_para_text(p)
        print(f"✓ Rotterdam GPA line: deleted (merged into title)")
        deletions += 1
    
    # Strategy Case grade: remove (not in plan)
    elif text.startswith('Relevant Courses: Applied Machine Learning') and 'Strategy Case' in text:
        set_para_text(p, 'Relevant Courses: Applied Machine Learning to Strategy (9.3/10), Python Fundamentals (8.3/10)')
        print(f"✓ Rotterdam courses: removed Strategy Case")
        replacements += 1
    
    # Nova degree: simplify
    elif text == 'Bachelor of Science in Management':
        set_para_text(p, 'BSc in Management | GPA: 16/20')
        print(f"✓ Nova: simplified degree line")
        replacements += 1
    
    # Delete "Final GPA: 16/20" (now in title line)
    elif text == 'Final GPA: 16/20':
        delete_para_text(p)
        print(f"✓ Nova GPA line: deleted (merged into title)")
        deletions += 1
    
    # Nova courses: simplify
    elif text.startswith('Relevant Courses: Statistics'):
        set_para_text(p, 'Statistics (20/20), Procurement Management (19/20), Economics of the European Union (19/20)')
        print(f"✓ Nova courses: simplified")
        replacements += 1
    
    # NUS: simplify description
    elif text.startswith('Completed advanced coursework in venture'):
        delete_para_text(p)
        print(f"✓ NUS extra coursework line: deleted")
        deletions += 1
    
    # === SKILLS FIXES ===
    
    # Proficiencies → Sales tools + Technical
    elif text.startswith('Salesforce, HubSpot CRM'):
        set_para_text(p, 'Salesforce, LinkedIn Sales Navigator, Apollo, Google Ads, Looker Studio, Python, Apps Script, SQL, Power BI.')
        print(f"✓ Skills: updated with sales tools")
        replacements += 1
    
    # Certifications: simplify
    elif text.startswith('Bloomberg Market Concepts Certificate'):
        set_para_text(p, 'Google Ads Certified, Bloomberg Market Concepts, Microsoft Excel Specialist, TOEFL iBT.')
        print(f"✓ Certifications: Google Ads first")
        replacements += 1
    
    # === DELETE HOBBIES/INTERESTS ARTIFACT ===
    elif text == 'Hobbies:':
        delete_para_text(p)
        print(f"✓ Hobbies label: deleted")
        deletions += 1
    elif text == 'Interests:':
        delete_para_text(p)
        print(f"✓ Interests label: deleted")
        deletions += 1
    elif text.startswith('Piano, Tennis, Hiking'):
        delete_para_text(p)
        print(f"✓ Hobbies content: deleted")
        deletions += 1
    elif text.startswith('AFS Intercultural Programs'):
        delete_para_text(p)
        print(f"✓ Interests content: deleted")
        deletions += 1

# --- Save ---
modified_xml = etree.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)
with zipfile.ZipFile(OUTPUT, 'w', zipfile.ZIP_DEFLATED) as zout:
    for name, data in all_files.items():
        if name == 'word/document.xml':
            zout.writestr(name, modified_xml)
        else:
            zout.writestr(name, data)

print(f"\n{'='*50}")
print(f"Replacements: {replacements}")
print(f"Deletions:    {deletions}")
print(f"Total edits:  {replacements + deletions}")
print(f"\n✅ Saved to: {OUTPUT}")
