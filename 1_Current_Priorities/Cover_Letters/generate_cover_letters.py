from fpdf import FPDF
import os

class CoverLetterPDF(FPDF):
    def header(self):
        pass
    
    def footer(self):
        pass

def create_cover_letter(company, role_focus, body_paragraphs, filename):
    pdf = CoverLetterPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=25)
    
    # Header - Name
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, "Tomás Maria Burnay Batalha", ln=True, align="C")
    
    # Contact info
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, "tomas.b.batalha@gmail.com | (+351) 936 124 118 | linkedin.com/in/tomasmbatalha", ln=True, align="C")
    pdf.ln(10)
    
    # Date
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, "February 5, 2026", ln=True)
    pdf.ln(5)
    
    # Company address
    pdf.cell(0, 6, f"{company} Recruiting Team", ln=True)
    pdf.cell(0, 6, f"{company}", ln=True)
    pdf.ln(10)
    
    # Greeting
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, f"Dear {company} Hiring Team,", ln=True)
    pdf.ln(5)
    
    # Body paragraphs
    pdf.set_font("Helvetica", "", 11)
    for para in body_paragraphs:
        pdf.multi_cell(0, 6, para)
        pdf.ln(3)
    
    # Closing
    pdf.ln(5)
    pdf.cell(0, 6, "Sincerely,", ln=True)
    pdf.ln(8)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 6, "Tomás Batalha", ln=True)
    
    # Save
    pdf.output(filename)
    print(f"Created: {filename}")

# Square Cover Letter
square_paragraphs = [
    "I am writing to express my strong interest in joining Square. As someone who has built commercial infrastructure from the ground up at an early-stage fintech and scaled enterprise sales at Amazon and Google, I am deeply aligned with Square's mission to make commerce and financial services accessible to everyone.",
    
    "At Pairwire, I co-founded and led the commercial function, building a $160K pipeline of enterprise pilots with Fortune 500 and Big 4 firms in under 11 months--all pre-funding. I designed an AI-powered outbound engine processing 7,000+ leads and automating 80% of our pipeline, demonstrating my ability to blend technical automation with strategic sales execution. This experience taught me what it takes to build trust with enterprise buyers in complex, high-stakes environments.",
    
    "Previously at Google, I built globally scalable analytics dashboards that projected $1.41M in annual savings and presented strategic insights to 237+ senior clients at Google's flagship partner event. At Amazon, I led the B2B expansion into Portugal, managing 2,311 companies and outperforming KPIs by 21x--turning a territory from 56% below average to 25% above. These experiences gave me a deep appreciation for how operational excellence and customer obsession drive growth at scale.",
    
    "What draws me to Square is the intersection of financial infrastructure and seller empowerment. My background in fintech (starting at Fintech House in Lisbon, where I helped launch an acceleration program), combined with my enterprise sales experience and technical proficiency in Python, SQL, and data automation, positions me to contribute meaningfully to Square's growth. I understand both the seller's journey and the technical systems that power seamless commerce.",
    
    "I would be thrilled to bring my builder's mindset, commercial acumen, and passion for democratizing access to financial tools to Square. Thank you for considering my application."
]

# Okta Cover Letter  
okta_paragraphs = [
    "I am writing to express my enthusiasm for joining Okta. As someone who has navigated enterprise sales cycles with Fortune 500 companies and built technical solutions that drive business outcomes, I am deeply drawn to Okta's mission of enabling secure identity for everyone.",
    
    "At Pairwire, I co-founded and led commercial operations, securing 23 enterprise pilots with major firms including Big 4 consultancies across 6-9 month sales cycles. I built our entire sales infrastructure from scratch, designing an AI-enhanced outbound engine that processed 7,000+ leads and automated 80% of pipeline generation. This experience taught me how to communicate complex technical value propositions to enterprise buyers who demand both security and simplicity.",
    
    "My time at Google reinforced this foundation. I built automated analytics platforms using Apps Script and GMP tools that delivered $1.41M in projected annual savings, while also presenting to 237+ senior clients on strategic activation. At Amazon, I led the B2B expansion into a new market, managing relationships with 2,311 companies and consistently outperforming territory benchmarks. These roles sharpened my ability to translate technical capabilities into business impact--a skill essential for selling identity and access management solutions.",
    
    "What excites me about Okta is the criticality of the problem you solve. In an era where every organization is becoming a technology company, secure and seamless identity is foundational. My technical proficiency (Python, SQL, data automation) combined with my enterprise sales experience positions me to help customers understand how Okta's platform protects their most valuable asset: trust.",
    
    "I am eager to contribute to Okta's growth by bringing my blend of technical depth, commercial rigor, and genuine belief that security should be an enabler, not a barrier. Thank you for considering my application."
]

# Create output directory
output_dir = "/Users/tomasbatalha/Projects/Planning and Advisory/Tomas_Batalha_Future_Plan/1_Current_Priorities/Cover_Letters"
os.makedirs(output_dir, exist_ok=True)

# Generate PDFs
create_cover_letter(
    "Square",
    "Business Development / Sales",
    square_paragraphs,
    f"{output_dir}/Tomas_Batalha_Cover_Letter_Square.pdf"
)

create_cover_letter(
    "Okta", 
    "Business Development / Sales",
    okta_paragraphs,
    f"{output_dir}/Tomas_Batalha_Cover_Letter_Okta.pdf"
)

print("\nDone! Cover letters saved to:")
print(f"  {output_dir}/")
