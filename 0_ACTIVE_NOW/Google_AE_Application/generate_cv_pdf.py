#!/usr/bin/env python3
"""Generate the Google AE tailored CV as a clean 1-page PDF using fpdf2."""

import os
from fpdf import FPDF

class CVPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_page()
        self.set_auto_page_break(auto=False, margin=10)
        self.set_margins(14, 10, 14)
        self.set_y(10)
    
    def section_header(self, text):
        self.set_font("Helvetica", "B", 9.5)
        self.cell(0, 5, text, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(0, 0, 0)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(1.5)
    
    def company_line(self, text):
        self.ln(1.5)
        self.set_font("Helvetica", "B", 8.5)
        self.cell(0, 4, text, new_x="LMARGIN", new_y="NEXT")
    
    def role_line(self, text):
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 4, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(0.3)
    
    def bullet(self, text):
        self.set_font("Helvetica", "", 7.5)
        x = self.get_x()
        self.set_x(x + 3)
        # Replace special chars that fpdf2 might not handle
        text = text.replace("\u2013", "-").replace("\u2014", "-").replace("\u201c", '"').replace("\u201d", '"').replace("\u2019", "'")
        self.multi_cell(0, 3.5, "- " + text, new_x="LMARGIN", new_y="NEXT")
        self.ln(0.2)
    
    def skill_line(self, label, content):
        self.set_font("Helvetica", "B", 7.5)
        label_w = self.get_string_width(label + " ") + 1
        self.cell(label_w, 3.5, label + " ")
        self.set_font("Helvetica", "", 7.5)
        remaining_w = self.w - self.r_margin - self.get_x()
        self.multi_cell(remaining_w, 3.5, content, new_x="LMARGIN", new_y="NEXT")
        self.ln(0.3)


def create_cv():
    pdf = CVPDF()
    
    # Header - Name
    pdf.set_font("Helvetica", "B", 15)
    pdf.cell(0, 7, "Tomas Maria Burnay Batalha", align="C", new_x="LMARGIN", new_y="NEXT")
    
    # Contact
    pdf.set_font("Helvetica", "", 7.5)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 4, "Lisbon, Portugal (Open to Relocation to Dublin) | (+351) 936 124 118 | tomas.b.batalha@gmail.com | linkedin.com/in/tomasmbatalha", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)
    
    # Professional Summary
    pdf.section_header("PROFESSIONAL SUMMARY")
    pdf.set_font("Helvetica", "", 7.5)
    pdf.multi_cell(0, 3.5, "Former Google intern and startup Co-Founder with full-cycle new business sales experience. Built a E147K B2B pipeline from zero through outbound prospecting, cold outreach, and enterprise deal closing. Managed a 2,311-account territory at Amazon, outperforming full-time colleagues. Seeking to bring builder mentality and commercial execution to Google's New Business Sales team.", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    
    # Work Experience
    pdf.section_header("WORK EXPERIENCE")
    
    # Pairwire
    pdf.company_line("Pairwire | New York, USA (Remote)")
    pdf.role_line("Co-Founder and Head of Sales | February 2024 - December 2025")
    pdf.bullet("Built E147K pipeline of contracted enterprise pilots from zero in 11 months pre-funding through outbound prospecting, cold calling, consulting, and relationship management")
    pdf.bullet("Closed 23 enterprise engagements including Fortune 500 and Big 4 firms across 6-9 month full-cycle sales processes")
    pdf.bullet("Designed an AI-powered outbound engine processing 7,000+ leads, automating 80% of prospecting via custom tech stack (Python, Expand.io, AI-enhanced workflows)")
    pdf.bullet("Led end-to-end deal management from first touch to contract close, managing entire funnel with no sales team or brand recognition")
    pdf.bullet("Created partnership and investor pitch materials; led negotiations with Google, Web Summit, and enterprise decision-makers")
    
    # Google
    pdf.company_line("Google | Lisbon, Portugal")
    pdf.role_line("Business Analyst Intern (Large Customer Sales) | May 2024 - August 2024")
    pdf.bullet('Led the "Future Trends" segment at Google\'s flagship partner event, presenting personally researched insights on Peak Season activation and media readiness to 237+ senior advertising clients')
    pdf.bullet("Designed and automated three globally scalable dashboards using Apps Script and GMP tools to analyze ROAS vs. profit and CPA vs. conversions, projecting $1.41M in annual savings for media spend decisions")
    pdf.bullet("Built a reporting platform for Partner Managers using Looker Studio, Analytics 360, and Apps Script, delivering an estimated E315K in annual efficiency gains")
    
    # Amazon
    pdf.company_line("Amazon | Madrid, Spain")
    pdf.role_line("Business Development Intern (Amazon Business) | May 2022 - November 2022")
    pdf.bullet("Led the B2B retail expansion into Portugal, managing a portfolio of 2,311 companies through prospecting, outreach, and account activation")
    pdf.bullet("Outperformed KPI benchmarks by 21x in company account configurations during the Portugal B2B rollout")
    pdf.bullet("Raised territory share from 56% below to 25% above team average, outperforming full-time colleagues in the region")
    pdf.bullet("Compiled a 19-page strategic report on B2B eCommerce based on 8 company territories and 54 targeted client interviews")
    
    # EY
    pdf.company_line("EY | Lisbon, Portugal")
    pdf.role_line("Assurance Associate (Financial Services) | February 2022 - April 2022")
    pdf.bullet("Audited asset portfolios worth E41.3 billion across 3 insurance firms, developing rigorous data verification and attention to detail")
    
    pdf.ln(1.5)
    
    # Education
    pdf.section_header("EDUCATION")
    
    pdf.company_line("Rotterdam School of Management | Rotterdam, Netherlands")
    pdf.role_line("MSc in Strategic Management | GPA: 8/10")
    pdf.bullet("Relevant Courses: Applied Machine Learning to Strategy (9.3/10), Python Fundamentals (8.3/10)")
    
    pdf.company_line("National University of Singapore | Singapore")
    pdf.role_line("MSc Curriculum Term | MBA-aligned coursework in Strategy and Innovation")
    pdf.bullet("Built a commercial and financial plan for a NUS PhD venture: 70% energy savings, 45% unit margins, 278% ROI in a $1.5B market")
    
    pdf.company_line("Nova School of Business and Economics | Lisbon, Portugal")
    pdf.role_line("BSc in Management | GPA: 16/20")
    pdf.bullet("Statistics (20/20), Procurement Management (19/20), Economics of the European Union (19/20)")
    
    pdf.ln(1.5)
    
    # Leadership & Activities
    pdf.section_header("LEADERSHIP & ACTIVITIES")
    
    leadership = [
        ("Nova Thirst Project", "Founder & President: Led 23 volunteers, raised E2,539 for water access, organized 4 events including one with 35 NGOs (2020-2021)"),
        ("Nova Tech Club", "Digital Transformation Consultant: Designed a job platform prototype and organized corporate events and workshops (2020-2021)"),
        ("Nova Social Consulting (WWF)", "Pro Bono Consultant: Assessed organizational structure, identified 155 improvement areas, delivered 6 presentations to senior management (2020-2021)"),
    ]
    
    for name, desc in leadership:
        pdf.set_font("Helvetica", "B", 7.5)
        name_w = pdf.get_string_width(name + " - ") + 1
        pdf.cell(name_w, 3.5, name + " - ")
        pdf.set_font("Helvetica", "", 7.5)
        remaining_w = pdf.w - pdf.r_margin - pdf.get_x()
        pdf.multi_cell(remaining_w, 3.5, desc, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(0.3)
    
    pdf.ln(1.5)
    
    # Skills
    pdf.section_header("SKILLS")
    
    pdf.skill_line("Sales & Marketing:", "Google Ads, YouTube Ads, Google Display Network, CRM (Salesforce), LinkedIn Sales Navigator, Apollo, Full-Cycle Sales, Pipeline Management, Cold Outreach, Consultative Selling")
    pdf.skill_line("Technical:", "Python, Apps Script, Visual Basic for Applications (VBA), SQL, Looker Studio, Power BI, DAX")
    pdf.skill_line("Certifications:", "Google Ads Certified, Bloomberg Market Concepts, Microsoft Excel Specialist, TOEFL iBT")
    pdf.skill_line("Languages:", "Portuguese (Native), English (Fluent), Spanish (Fluent), French (Beginner)")
    
    # Save
    output = os.path.expanduser("~/Downloads/TomásBatalha_Resume_02_2026_GOOGLE_AE.pdf")
    pdf.output(output)
    print(f"PDF saved to: {output}")


if __name__ == "__main__":
    create_cv()
