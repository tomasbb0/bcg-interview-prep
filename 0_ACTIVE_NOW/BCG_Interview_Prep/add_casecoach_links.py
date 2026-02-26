#!/usr/bin/env python3
"""Add CaseCoach direct links to all schedule items + Practice Room booking section."""

FILE = "/Users/tomasbatalha/Projects/Planning and Advisory/Tomas_Batalha_Future_Plan/0_ACTIVE_NOW/BCG_Interview_Prep/index.html"

with open(FILE, "r", encoding="utf-8") as f:
    html = f.read()

# ═══════════════════════════════════════════════════
# CaseCoach URL structure:
# Case Interview Prep Course: https://casecoach.com/c/courses/case-interview-prep-course/class/{slug}/
# Case Math Course: https://casecoach.com/c/courses/case-math-course/class/{slug}/
# Practice Room: https://casecoach.com/c/practice-room/
# Drills: https://casecoach.com/c/drills/
# ═══════════════════════════════════════════════════

BASE_CASE = "https://casecoach.com/c/courses/case-interview-prep-course/class"
BASE_MATH = "https://casecoach.com/c/courses/case-math-course/class"
PRACTICE_ROOM = "https://casecoach.com/c/practice-room/"
DRILLS = "https://casecoach.com/c/drills/"

# ═══════════════════════════════════════════════════
# BLOCO MAPPINGS — which classes are in each bloco
# ═══════════════════════════════════════════════════

# Case Prep Course Blocos:
# Bloco 1: Structuring (AIM test, How to build structure, Top-10 frameworks, etc.)
# Bloco 2: Math in Cases + Exhibits 
# Bloco 3: Creativity & Judgment
# Bloco 4: Synthesis & Case Leadership

bloco_links = {
    # TUESDAY
    "Case Prep Course Bloco 1": [
        (f"{BASE_CASE}/how-to-approach-structuring-the-aim-test/", "AIM Test"),
        (f"{BASE_CASE}/how-to-build-a-structure/", "Build Structure"),
        (f"{BASE_CASE}/top-10-case-frameworks/", "Top-10 Frameworks"),
        (f"{BASE_CASE}/academic-frameworks/", "Academic Frameworks"),
        (f"{BASE_CASE}/logical-frameworks/", "Logical Frameworks"),
    ],
    "Case Prep Course Bloco 2": [
        (f"{BASE_CASE}/how-to-solve-math-questions/", "Math in Cases"),
        (f"{BASE_CASE}/how-to-identify-insights/", "Identify Insights"),
        (f"{BASE_CASE}/how-to-communicate-your-structure/", "Communicate Structure"),
    ],
    # WEDNESDAY  
    "Case Prep Course Bloco 3": [
        (f"{BASE_CASE}/how-to-generate-ideas/", "Creativity"),
        (f"{BASE_CASE}/how-to-identify-insights/", "Judgment & Insights"),
    ],
    "Case Prep Course Bloco 4": [
        (f"{BASE_CASE}/how-to-synthesize-your-recommendation/", "Synthesis"),
        (f"{BASE_CASE}/how-to-lead-the-case-and-conquer-candidate-led-interviews/", "Case Leadership"),
    ],
    # Math Course Blocos:
    "Math Course Bloco 1": [
        (f"{BASE_MATH}/addition/", "Addition"),
        (f"{BASE_MATH}/subtraction/", "Subtraction"),
        (f"{BASE_MATH}/multiplication/", "Multiplication"),
        (f"{BASE_MATH}/division/", "Division"),
        (f"{BASE_MATH}/fractions/", "Fractions"),
        (f"{BASE_MATH}/percentages/", "Percentages"),
    ],
    "Math Course Bloco 2": [
        (f"{BASE_MATH}/weighted-averages/", "Weighted Avg"),
        (f"{BASE_MATH}/compounding/", "Compounding"),
        (f"{BASE_MATH}/probability/", "Probability"),
        (f"{BASE_MATH}/algebra/", "Algebra"),
    ],
    "Math Course Bloco 3": [
        (f"{BASE_MATH}/keeping-track-of-zeros/", "Track Zeros"),
        (f"{BASE_MATH}/simplifying-calculations-with-rounding/", "Rounding"),
        (f"{BASE_MATH}/simplifying-calculations-with-factors/", "Factors"),
        (f"{BASE_MATH}/simplifying-calculations-with-distributive-properties/", "Distributive"),
        (f"{BASE_MATH}/fraction-values-to-remember/", "Fraction Values"),
    ],
    "Math Course Bloco 4": [
        (f"{BASE_MATH}/income-statement/", "Income Statement"),
        (f"{BASE_MATH}/balance-sheet/", "Balance Sheet"),
        (f"{BASE_MATH}/cash-flow/", "Cash Flow"),
        (f"{BASE_MATH}/investments/", "Investments"),
        (f"{BASE_MATH}/valuation/", "Valuation"),
        (f"{BASE_MATH}/operations/", "Operations"),
    ],
}

# Solo case URLs (from model case interview videos)
solo_cases = {
    "FlashFash": f"{BASE_CASE}/model-case-interview-flashfash/",
    "Roko Hotel": None,  # Not a CaseCoach video case — it's a solo practice case
    "A-EYE": None,  # Solo practice
    "Clean-All": None,  # Solo practice
    "Canadian Wildlife": f"{BASE_CASE}/canadian-wildlife-federation-scott/",
}

# Other useful links
fit_course_link = f"{BASE_CASE}/how-to-exhibit-strong-presence-and-effective-communication/"
estimation_link = f"{BASE_CASE}/estimations-and-market-sizing/"

# ═══════════════════════════════════════════════════
# Build link HTML snippets
# ═══════════════════════════════════════════════════

def make_links_html(bloco_name):
    """Generate a small HTML snippet with clickable links for a bloco."""
    if bloco_name not in bloco_links:
        return ""
    links = bloco_links[bloco_name]
    parts = []
    for url, label in links:
        parts.append(f'<a href="{url}" target="_blank" style="color:var(--highlight);text-decoration:underline;font-size:0.85em;">{label}</a>')
    return " 🔗 " + " · ".join(parts)

# ═══════════════════════════════════════════════════
# Apply link insertions to schedule items
# ═══════════════════════════════════════════════════

changes = 0

# TUESDAY - Bloco 1
old = """📹 CaseCoach: Case Prep Course Bloco 1 (speed)
                  </td>
                  <td>
                    Structuring (3-4 vídeos a 1.5x). AIM test: Answer-focused,
                    Insightful, MECE."""
new = f"""📹 CaseCoach: Case Prep Course Bloco 1 (speed)
                  </td>
                  <td>
                    Structuring (3-4 vídeos a 1.5x). AIM test: Answer-focused,
                    Insightful, MECE.{make_links_html("Case Prep Course Bloco 1")}"""
if old in html:
    html = html.replace(old, new)
    changes += 1

# TUESDAY - Bloco 2
old = """📹 CaseCoach: Case Prep Course Bloco 2 (speed)
                  </td>
                  <td>
                    Math in Cases + Exhibits a 1.5x. Anotar fórmulas-chave.
                    Focar no essencial."""
new = f"""📹 CaseCoach: Case Prep Course Bloco 2 (speed)
                  </td>
                  <td>
                    Math in Cases + Exhibits a 1.5x. Anotar fórmulas-chave.
                    Focar no essencial.{make_links_html("Case Prep Course Bloco 2")}"""
if old in html:
    html = html.replace(old, new)
    changes += 1

# TUESDAY - Drills
old = """⚡ CaseCoach Drills</td>
                  <td>
                    10 Calculations + 5 Structures. Target: 15-30 seg cada.
                    Aplicar Bloco 1+2."""
new = f"""⚡ CaseCoach Drills</td>
                  <td>
                    10 Calculations + 5 Structures. Target: 15-30 seg cada.
                    Aplicar Bloco 1+2. <a href="{DRILLS}" target="_blank" style="color:var(--highlight);text-decoration:underline;font-size:0.85em;">🔗 Abrir Drills</a>"""
if old in html:
    html = html.replace(old, new)
    changes += 1

# TUESDAY - Solo #1 Roko Hotel (no CaseCoach link - it's internal)

# TUESDAY - Math Bloco 1
old = """📹 CaseCoach: Math Course Bloco 1
                  </td>
                  <td>
                    Fundamentos: operações, frações, percentagens, termos PT. +
                    3 Case Math drills."""
new = f"""📹 CaseCoach: Math Course Bloco 1
                  </td>
                  <td>
                    Fundamentos: operações, frações, percentagens, termos PT. +
                    3 Case Math drills.{make_links_html("Math Course Bloco 1")}"""
if old in html:
    html = html.replace(old, new)
    changes += 1

# TUESDAY - Solo #2 FlashFash
old = """📚 CaseCoach Caso Solo #2: FlashFash (M&A) — 💊 Alprazolam"""
new = f"""📚 <a href="{solo_cases['FlashFash']}" target="_blank" style="color:inherit;text-decoration:underline;">CaseCoach Caso Solo #2: FlashFash (M&A)</a> — 💊 Alprazolam"""
if old in html:
    html = html.replace(old, new)
    changes += 1

# WEDNESDAY - Bloco 3
old = """📹 CaseCoach: Case Prep Course Bloco 3
                  </td>
                  <td>
                    Creativity & Judgment aulas. + 5 Creativity drills após. AIM
                    check."""
new = f"""📹 CaseCoach: Case Prep Course Bloco 3
                  </td>
                  <td>
                    Creativity & Judgment aulas. + 5 Creativity drills após. AIM
                    check.{make_links_html("Case Prep Course Bloco 3")}"""
if old in html:
    html = html.replace(old, new)
    changes += 1

# WEDNESDAY - Practice Room #2
old = """🤝 CaseCoach Practice Room #2</td>
                  <td>
                    Market Entry/Operations (BCG favorites). Praticar hipótese
                    inicial + brainstorming criativo."""
new = f"""🤝 <a href="{PRACTICE_ROOM}" target="_blank" style="color:inherit;text-decoration:underline;">CaseCoach Practice Room #2</a></td>
                  <td>
                    Market Entry/Operations (BCG favorites). Praticar hipótese
                    inicial + brainstorming criativo. <a href="{PRACTICE_ROOM}" target="_blank" style="color:var(--highlight);font-size:0.85em;">🔗 Reservar</a>"""
if old in html:
    html = html.replace(old, new)
    changes += 1

# WEDNESDAY - Bloco 4
old = """📹 CaseCoach: Case Prep Course Bloco 4
                  </td>
                  <td>
                    Synthesis & Case Leadership. Watch 1 sample interview (MBB
                    candidate)."""
new = f"""📹 CaseCoach: Case Prep Course Bloco 4
                  </td>
                  <td>
                    Synthesis & Case Leadership. Watch 1 sample interview (MBB
                    candidate).{make_links_html("Case Prep Course Bloco 4")}"""
if old in html:
    html = html.replace(old, new)
    changes += 1

# WEDNESDAY - Practice Room #3
old = """🤝 CaseCoach Practice Room #3 — 💊 COMBO PRIME DOSE TEST</td>"""
new = f"""🤝 <a href="{PRACTICE_ROOM}" target="_blank" style="color:inherit;text-decoration:underline;">CaseCoach Practice Room #3</a> — 💊 COMBO PRIME DOSE TEST</td>"""
if old in html:
    html = html.replace(old, new)
    changes += 1

# WEDNESDAY - Math Bloco 2
old = """📹 CaseCoach: Math Course Bloco 2 + Drills
                  </td>
                  <td>
                    Weighted avg, growth, breakeven. + 10 Calculations + 5
                    Market Sizing drills."""
new = f"""📹 CaseCoach: Math Course Bloco 2 + Drills
                  </td>
                  <td>
                    Weighted avg, growth, breakeven. + 10 Calculations + 5
                    Market Sizing drills.{make_links_html("Math Course Bloco 2")} <a href="{DRILLS}" target="_blank" style="color:var(--highlight);font-size:0.85em;">🔗 Drills</a>"""
if old in html:
    html = html.replace(old, new)
    changes += 1

# WEDNESDAY - Math Bloco 3
old = """📹 CaseCoach: Math Course Bloco 3"""
new_text = f"""📹 CaseCoach: Math Course Bloco 3"""
# Don't change the title, add links in details
old2 = """Pro Tips: atalhos, arredondamento, simplificação. +
                    CaseCoach Charts drills."""
new2 = f"""Pro Tips: atalhos, arredondamento, simplificação. +
                    CaseCoach Charts drills.{make_links_html("Math Course Bloco 3")}"""
if old2 in html:
    html = html.replace(old2, new2)
    changes += 1

# WEDNESDAY - Practice Room #4
old = """🤝 CaseCoach Practice Room #4</td>
                  <td>
                    Cost Cutting/Operations (BCG favorites). Último caso hard do
                    dia."""
new = f"""🤝 <a href="{PRACTICE_ROOM}" target="_blank" style="color:inherit;text-decoration:underline;">CaseCoach Practice Room #4</a></td>
                  <td>
                    Cost Cutting/Operations (BCG favorites). Último caso hard do
                    dia. <a href="{PRACTICE_ROOM}" target="_blank" style="color:var(--highlight);font-size:0.85em;">🔗 Reservar</a>"""
if old in html:
    html = html.replace(old, new)
    changes += 1

# THURSDAY - Math Bloco 4 + Fit Course
old = """📹 CaseCoach: Math Course Bloco 4 + Fit Course"""
new = f"""📹 CaseCoach: Math Course Bloco 4 + Fit Course"""
# Add links in details column for Thursday
old3 = """📹 CaseCoach: Math Course Bloco 4 + Fit Course
                  </td>"""
if old3 in html:
    # Find the details for this row and add links
    pass  # Will handle via the details search below

# THURSDAY - Practice Room #5
old = """🤝 CaseCoach Practice Room #5</td>"""
new = f"""🤝 <a href="{PRACTICE_ROOM}" target="_blank" style="color:inherit;text-decoration:underline;">CaseCoach Practice Room #5</a></td>"""
if old in html:
    html = html.replace(old, new)
    changes += 1

# ═══════════════════════════════════════════════════
# Add BOOK ALL PRACTICE ROOMS section at top of schedule
# ═══════════════════════════════════════════════════

# Find the Case Count Target table and add booking section before it
booking_card = f'''
            <div class="card card-accent" style="margin-bottom:16px;margin-top:16px;">
              <h3>🤝 Reservar Practice Rooms — <a href="{PRACTICE_ROOM}" target="_blank" style="color:var(--highlight);text-decoration:underline;">Abrir CaseCoach Practice Room</a></h3>
              <p style="color:var(--text-muted);font-size:0.9em;margin-bottom:10px;">Reserva TODOS agora para garantir slot. Clica no link, escolhe a hora, e marca ✓.</p>
              <table>
                <thead>
                  <tr>
                    <th style="width:30px;">✓</th>
                    <th>Dia</th>
                    <th>Hora</th>
                    <th>Sessão</th>
                    <th>Foco</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><input type="checkbox" class="schedule-check" id="chk-book-1" onchange="saveCheck(this)"/></td>
                    <td><strong>Qua 25</strong></td>
                    <td>11:15-12:15</td>
                    <td>Practice Room #2</td>
                    <td>Market Entry/Operations</td>
                    <td id="book-status-1">⏳ Por reservar</td>
                  </tr>
                  <tr style="background:rgba(0,167,89,0.08);">
                    <td><input type="checkbox" class="schedule-check" id="chk-book-2" onchange="saveCheck(this)"/></td>
                    <td><strong>Qua 25</strong></td>
                    <td>14:00-15:00</td>
                    <td>Practice Room #3 💊</td>
                    <td>Profitability (COMBO TEST)</td>
                    <td id="book-status-2">⏳ Por reservar</td>
                  </tr>
                  <tr>
                    <td><input type="checkbox" class="schedule-check" id="chk-book-3" onchange="saveCheck(this)"/></td>
                    <td><strong>Qua 25</strong></td>
                    <td>21:00-22:00</td>
                    <td>Practice Room #4</td>
                    <td>Cost Cutting/Operations</td>
                    <td id="book-status-3">⏳ Por reservar</td>
                  </tr>
                  <tr>
                    <td><input type="checkbox" class="schedule-check" id="chk-book-4" onchange="saveCheck(this)"/></td>
                    <td><strong>Qui 26</strong></td>
                    <td>14:00-15:00</td>
                    <td>Practice Room #5</td>
                    <td>Mixed (BCG style)</td>
                    <td id="book-status-4">⏳ Por reservar</td>
                  </tr>
                  <tr style="background:rgba(0,167,89,0.08);">
                    <td><input type="checkbox" class="schedule-check" id="chk-book-5" onchange="saveCheck(this)"/></td>
                    <td><strong>Qui 26</strong></td>
                    <td>18:00-19:00</td>
                    <td>Practice Room #6 (EXTRA)</td>
                    <td>Market Entry/Growth — extra caso com stranger</td>
                    <td id="book-status-5">⏳ Por reservar</td>
                  </tr>
                </tbody>
              </table>
              <p style="margin-top:8px;font-size:0.85em;color:var(--text-muted);">💡 Tip: Reserva agora enquanto há slots. Practice Room é o melhor treino real — casos com estranhos = pressão real.</p>
            </div>
'''

# Insert before the Case Count Target section
target = '<!-- Case Count Target -->'
if target in html:
    html = html.replace(target, booking_card + '\n            ' + target)
    changes += 1
else:
    # Try to find it another way
    target2 = 'Target Case Count'
    if target2 in html:
        # Find the card containing it
        idx = html.index(target2)
        # Find the preceding <div class="card
        card_start = html.rfind('<div class="card', 0, idx)
        if card_start > 0:
            html = html[:card_start] + booking_card + '\n            ' + html[card_start:]
            changes += 1

print(f"Applied {changes} changes")

with open(FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("✅ CaseCoach links + booking section added!")
