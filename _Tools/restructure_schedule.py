#!/usr/bin/env python3
"""
Restructure the Schedule tab:
1. Move Schedule (day tabs) to the very top of master-plan
2. Move Medication/Wellness/Sleep to a new Wellness tab
3. Add persistent checkboxes to all schedule activity rows
4. Add localStorage JS for checkbox persistence
"""
import re

with open('0_ACTIVE_NOW/BCG_Interview_Prep/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ═══════════════════════════════════════════
# 1. Add Wellness nav item in sidebar
# ═══════════════════════════════════════════
content = content.replace(
    '''        <a href="#" onclick="showSection('game-day')" data-section="game-day">
          <span class="icon">🏆</span> Game Day
        </a>''',
    '''        <a href="#" onclick="showSection('game-day')" data-section="game-day">
          <span class="icon">🏆</span> Game Day
        </a>
        <a href="#" onclick="showSection('wellness')" data-section="wellness">
          <span class="icon">💊</span> Wellness & Meds
        </a>'''
)
print("1. Added Wellness nav item")

# ═══════════════════════════════════════════
# 2. Find and extract the sections we need to move
# ═══════════════════════════════════════════

# Find the markers
situation_start = content.index('<div class="card card-accent">\n          <h3>Situation Assessment</h3>')
med_start = content.index('<!-- MEDICATION -->')
schedule_start = content.index('<!-- SCHEDULE TABS -->')
case_target_start = content.index('<!-- CASE TARGETS -->')

# Find the end of the master-plan section (the closing </div> before FRAMEWORKS comment)
frameworks_comment = content.index('<!-- ═══════════════════════════════════════════════════════ -->\n      <!-- SECTION: FRAMEWORKS -->')
# The </div> right before frameworks comment closes master-plan
master_plan_end = content.rindex('</div>', 0, frameworks_comment)

# Extract the blocks
# Situation Assessment block: from situation_start to med_start
situation_block = content[situation_start:med_start].rstrip()

# Medication & Wellness block: from med_start to schedule_start  
wellness_block = content[med_start:schedule_start].rstrip()

# Schedule block: from schedule_start to case_target_start
schedule_block = content[schedule_start:case_target_start].rstrip()

# Case target block: from case_target_start to master_plan_end
case_target_block = content[case_target_start:master_plan_end].rstrip()

print("2. Extracted all blocks")

# ═══════════════════════════════════════════
# 3. Rebuild master-plan section content
# ═══════════════════════════════════════════

# The master-plan section header (title + subtitle)
mp_header = '''      <div class="section active" id="master-plan">
        <div class="section-title">📋 Schedule</div>
        <div class="section-subtitle">
          Plano hora-a-hora — Domingo 22 Feb → Sexta 27 Feb
        </div>'''

# New master-plan content: Schedule at top, then Case Target, then Situation Assessment
new_master_plan = f'''{mp_header}

{schedule_block}

{case_target_block}

        <h2>📋 Situation Assessment</h2>
{situation_block}
      </div>'''

# ═══════════════════════════════════════════
# 4. Create Wellness section
# ═══════════════════════════════════════════

new_wellness_section = f'''
      <!-- ═══════════════════════════════════════════════════════ -->
      <!-- SECTION: WELLNESS -->
      <!-- ═══════════════════════════════════════════════════════ -->
      <div class="section" id="wellness">
        <div class="section-title">💊 Wellness & Meds</div>
        <div class="section-subtitle">
          Medicação, sono, energia — Protocolo para a semana
        </div>

{wellness_block.replace("<!-- MEDICATION -->", "").strip()}
      </div>'''

# ═══════════════════════════════════════════
# 5. Replace the old master-plan section with new
# ═══════════════════════════════════════════

old_master_plan_start = content.index('      <div class="section active" id="master-plan">')
old_master_plan_section = content[old_master_plan_start:frameworks_comment]

# Replace
content = content[:old_master_plan_start] + new_master_plan + '\n\n' + new_wellness_section + '\n\n      ' + content[frameworks_comment:]
print("3. Restructured master-plan + created wellness section")

# ═══════════════════════════════════════════
# 6. Add checkboxes to schedule table rows
# ═══════════════════════════════════════════

# Add a ✓ column header to each schedule table
content = content.replace(
    '''                <tr>
                  <th>Hora</th>
                  <th>Atividade</th>
                  <th>Detalhes</th>
                </tr>''',
    '''                <tr>
                  <th style="width:30px">✓</th>
                  <th>Hora</th>
                  <th>Atividade</th>
                  <th>Detalhes</th>
                </tr>'''
)
print("4. Added checkbox column headers")

# Now add checkbox cells to each <tr> in schedule tables
# We need to find all <tr> rows inside day-content divs that have <td class="time-col">
# Strategy: find each <td class="time-col"> row and prepend a checkbox <td>

day_ids = {'tue': 'Ter', 'wed': 'Qua', 'thu': 'Qui', 'fri': 'Sex'}
checkbox_counter = {}

# Use regex to find tbody rows with time-col in schedule sections
# Pattern: find <tr>\n...<td class="time-col"... inside day-content divs

lines = content.split('\n')
new_lines = []
in_day_content = False
current_day = None
row_index = 0

i = 0
while i < len(lines):
    line = lines[i]
    
    # Track which day we're in
    if 'class="day-content"' in line or 'class="day-content active"' in line:
        in_day_content = True
        if 'id="day-tue"' in line:
            current_day = 'tue'
        elif 'id="day-wed"' in line:
            current_day = 'wed'
        elif 'id="day-thu"' in line:
            current_day = 'thu'
        elif 'id="day-fri"' in line:
            current_day = 'fri'
        else:
            current_day = None
        row_index = 0
    
    # Detect end of day-content
    if in_day_content and line.strip() == '</div>' and i > 0:
        # Check if this closes day-content
        pass
    
    # Check for <tbody> to reset row counter
    if '<tbody>' in line:
        row_index = 0
    
    # Add checkbox to rows with time-col
    if in_day_content and current_day and 'class="time-col"' in line:
        row_index += 1
        chk_id = f"chk-{current_day}-{row_index}"
        
        # Find the <tr> that contains this line (look back for <tr>)
        # The <tr> should be 1 line before or at the line
        tr_found = False
        for back in range(min(3, len(new_lines))):
            idx = len(new_lines) - 1 - back
            if '<tr>' in new_lines[idx] and '</tr>' not in new_lines[idx]:
                # Insert checkbox td after <tr>
                indent = '                  '
                new_lines.insert(idx + 1, f'{indent}<td><input type="checkbox" class="schedule-check" id="{chk_id}" onchange="saveCheck(this)"></td>')
                tr_found = True
                break
        
        if not tr_found:
            # If tr is on same line or structure is different, skip
            pass
    
    # Track end of day sections
    if in_day_content and '<!-- CASE TARGETS -->' in line:
        in_day_content = False
        current_day = None
    
    new_lines.append(line)
    i += 1

content = '\n'.join(new_lines)
print("5. Added checkboxes to schedule rows")

# ═══════════════════════════════════════════
# 7. Add checkbox CSS and localStorage JS
# ═══════════════════════════════════════════

# Add CSS for checkboxes
checkbox_css = '''
      /* SCHEDULE CHECKBOXES */
      .schedule-check {
        width: 18px;
        height: 18px;
        cursor: pointer;
        accent-color: var(--bcg-green);
      }
      .schedule-check:checked {
        opacity: 1;
      }
      tr:has(.schedule-check:checked) td {
        text-decoration: line-through;
        opacity: 0.5;
      }
      tr:has(.schedule-check:checked) td:first-child {
        text-decoration: none;
        opacity: 1;
      }'''

content = content.replace(
    '      /* SIDEBAR */',
    f'{checkbox_css}\n\n      /* SIDEBAR */'
)
print("6. Added checkbox CSS")

# Add localStorage JS
checkbox_js = '''
      // Schedule checkbox persistence
      function saveCheck(cb) {
        const checks = JSON.parse(localStorage.getItem('bcg-prep-checks') || '{}');
        checks[cb.id] = cb.checked;
        localStorage.setItem('bcg-prep-checks', JSON.stringify(checks));
      }
      function loadChecks() {
        const checks = JSON.parse(localStorage.getItem('bcg-prep-checks') || '{}');
        Object.keys(checks).forEach(id => {
          const cb = document.getElementById(id);
          if (cb) cb.checked = checks[id];
        });
      }
      loadChecks();'''

# Insert before the closing </script>
content = content.replace(
    '      setInterval(updateCountdown, 60000);',
    '      setInterval(updateCountdown, 60000);\n' + checkbox_js
)
print("7. Added localStorage JS")

# ═══════════════════════════════════════════
# 8. Update keyboard nav sections array
# ═══════════════════════════════════════════

content = content.replace(
    '''          "fit",
          "game-day",
        ];''',
    '''          "fit",
          "game-day",
          "wellness",
        ];'''
)
print("8. Updated keyboard nav sections array")

# ═══════════════════════════════════════════
# 9. Write output
# ═══════════════════════════════════════════
with open('0_ACTIVE_NOW/BCG_Interview_Prep/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nDone! Total lines: {content.count(chr(10)) + 1}")
