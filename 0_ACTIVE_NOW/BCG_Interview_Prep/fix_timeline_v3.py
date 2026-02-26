#!/usr/bin/env python3
"""Fix pill timeline: prefill expected times, show pill names on bars,
make drag work, fix day navigation, color bars only when NOW passes them."""

import re

FILE = "/Users/tomasbatalha/Projects/Planning and Advisory/Tomas_Batalha_Future_Plan/0_ACTIVE_NOW/BCG_Interview_Prep/index.html"

with open(FILE, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Fix changeDay — remove the "don't allow future days" guard
# The user wants to navigate to Wed/Thu/Fri to see expected schedules
old_changeDay = '''      function changeDay(delta) {
        viewDate = new Date(viewDate.getTime() + delta * 86400000);
        // Don't allow future days
        const now = getNow();
        if (viewDate > now) viewDate = new Date(now);
        updateDayLabel();
        // Reset button states then reload UI for the viewed day
        ["concerta", "rubifen", "propranolol", "alprazolam"].forEach((id) => {
          const btn = document.getElementById("btn-" + id);
          btn.textContent = "Tomei";
          btn.style.background = PILL_DATA[id].color;
          btn.disabled = false;
          document.getElementById(id + "-time").textContent = "";
          document.getElementById("bar-" + id).style.display = "none";
        });
        updatePillUI();
      }'''

new_changeDay = '''      function changeDay(delta) {
        viewDate = new Date(viewDate.getTime() + delta * 86400000);
        // Allow navigation up to Fri 27 Feb (interview day)
        const maxDate = new Date(2026, 1, 28); // Feb 28
        const minDate = new Date(2026, 1, 22); // Feb 22
        if (viewDate > maxDate) viewDate = new Date(maxDate);
        if (viewDate < minDate) viewDate = new Date(minDate);
        updateDayLabel();
        // Reset button states then reload UI for the viewed day
        ["concerta", "rubifen", "propranolol", "alprazolam"].forEach((id) => {
          const btn = document.getElementById("btn-" + id);
          btn.textContent = "Tomei";
          btn.style.background = PILL_DATA[id].color;
          btn.disabled = false;
          document.getElementById(id + "-time").textContent = "";
          document.getElementById("bar-" + id).style.display = "none";
        });
        updatePillUI();
      }'''

html = html.replace(old_changeDay, new_changeDay)

# 2. Add EXPECTED pill schedules + update updatePillUI to show expected bars
# Find the "// Initialize pill tracker on load" line and add expected schedules before it
# Also fix the duplicate initialization

old_init = '''      // Initialize pill tracker on load
      updatePillUI();
      // Update NOW indicator every 10 seconds
      setInterval(updateNowIndicator, 10000);

      // Initialize pill tracker on load
      updatePillUI();
      // Update NOW indicator every 10 seconds
      setInterval(updateNowIndicator, 10000);'''

new_init = '''      // ═══════════════════════════════════════════════════
      // EXPECTED PILL SCHEDULES (pre-filled for each day)
      // ═══════════════════════════════════════════════════
      const EXPECTED_PILLS = {
        "2026-02-24": { // Terça - DAY 1
          rubifen:     { time: "15:30", dose: "20mg" },
          propranolol: { time: "15:30", dose: "10mg" },
          alprazolam:  { time: "21:00", dose: "0,25mg" }
        },
        "2026-02-25": { // Quarta - DAY 2
          concerta:    { time: "10:00", dose: "27mg" },
          rubifen:     { time: "12:30", dose: "20mg" },
          propranolol: { time: "13:00", dose: "20mg" },
          alprazolam:  { time: "13:00", dose: "0,5mg" }
        },
        "2026-02-26": { // Quinta - DAY 3
          concerta:    { time: "09:30", dose: "27mg" },
          rubifen:     { time: "13:00", dose: "20mg" }
        },
        "2026-02-27": { // Sexta - GAME DAY
          concerta:    { time: "09:30", dose: "27mg" },
          rubifen:     { time: "12:30", dose: "20mg" },
          propranolol: { time: "14:30", dose: "?mg" },
          alprazolam:  { time: "14:30", dose: "?mg" }
        }
      };

      function getExpectedForDay() {
        const d = viewDate;
        const key = d.getFullYear() + "-" +
          String(d.getMonth() + 1).padStart(2, "0") + "-" +
          String(d.getDate()).padStart(2, "0");
        return EXPECTED_PILLS[key] || {};
      }

      // Initialize pill tracker on load
      updatePillUI();
      // Update NOW indicator every 10 seconds
      setInterval(updateNowIndicator, 10000);'''

html = html.replace(old_init, new_init)

# 3. Replace the ENTIRE updatePillUI function to:
#    - Show expected bars (grey/dashed) for pills not yet taken  
#    - Show pill name INSIDE each bar
#    - Color bars only for past/present (before NOW), grey for future
#    - Make bars bigger and more draggable

old_updatePillUI = '''      function updatePillUI() {
        const log = getPillLog();
        const hasPills = Object.keys(log.pills).length > 0;

        document.getElementById("timeline-empty").style.display = hasPills
          ? "none"
          : "block";
        document.getElementById("effects-table").style.display = hasPills
          ? "block"
          : "none";

        const tbody = document.getElementById("effects-tbody");
        tbody.innerHTML = "";

        Object.keys(log.pills).forEach((pillId) => {
          const pill = log.pills[pillId];
          const data = PILL_DATA[pillId];
          const taken = new Date(pill.time);
          const takenTZ = getTimeInLisbon(taken);
          const takenH = takenTZ.fractionalHours;

          const onsetH = takenH + data.onsetMin / 60;
          const peakH = takenH + data.peakMin / 60;
          const fadeH = takenH + data.durationMin / 60;

          // Update button — show registered, allow re-click
          const btn = document.getElementById("btn-" + pillId);
          btn.textContent = "\\u2705 " + pill.timeStr;
          btn.style.background = "#666";
          btn.disabled = false;

          // Update time display
          const timeSpan = document.getElementById(pillId + "-time");
          timeSpan.textContent = "\\u23f0 " + pill.timeStr;

          // Show bar
          const barEl = document.getElementById("bar-" + pillId);
          barEl.style.display = "block";

          const fillEl = document.getElementById("bar-" + pillId + "-fill");
          const startPct = hourToPercent(takenH);
          const endPct = hourToPercent(fadeH);
          const peakStartPct = hourToPercent(onsetH);
          const peakEndPct = hourToPercent(peakH);

          fillEl.style.left = startPct + "%";
          fillEl.style.width = endPct - startPct + "%";
          fillEl.style.background = `linear-gradient(90deg, 
            ${data.color}33 0%, 
            ${data.color}33 ${((peakStartPct - startPct) / (endPct - startPct)) * 100}%, 
            ${data.color} ${((peakStartPct - startPct) / (endPct - startPct)) * 100}%, 
            ${data.color} ${((peakEndPct - startPct) / (endPct - startPct)) * 100}%, 
            ${data.color}33 ${((peakEndPct - startPct) / (endPct - startPct)) * 100}%, 
            ${data.color}33 100%)`;

          // Effects table row
          const fmt = (h) => {
            let hh = Math.floor(h) % 24;
            let mm = Math.round((h % 1) * 60);
            return (
              String(hh).padStart(2, "0") + ":" + String(mm).padStart(2, "0")
            );
          };
          const row = document.createElement("tr");
          row.innerHTML = `
            <td style="color:${data.color};font-weight:bold;">${data.name}</td>
            <td>${pill.dose}</td>
            <td><strong>${pill.timeStr}</strong></td>
            <td>${fmt(onsetH)} (${data.onsetMin}min)</td>
            <td style="color:${data.color};font-weight:bold;">${fmt(onsetH)}\\u2013${fmt(peakH)}</td>
            <td>${fmt(fadeH)}</td>
          `;
          tbody.appendChild(row);
        });

        // Update NOW indicator
        updateNowIndicator();

        // Render symptoms
        renderSymptoms();

        // Re-attach drag listeners (bars now visible)
        setTimeout(attachDragListeners, 50);

        // Schedule check-in based on pill peaks
        scheduleCheckin();
      }'''

new_updatePillUI = '''      function updatePillUI() {
        const log = getPillLog();
        const expected = getExpectedForDay();
        const allPillIds = new Set([...Object.keys(log.pills), ...Object.keys(expected)]);
        const hasPills = allPillIds.size > 0;

        document.getElementById("timeline-empty").style.display = hasPills ? "none" : "block";
        document.getElementById("effects-table").style.display = hasPills ? "block" : "none";

        const tbody = document.getElementById("effects-tbody");
        tbody.innerHTML = "";

        const now = getNow();
        const nowTZ = getTimeInLisbon(now);
        const nowH = nowTZ.fractionalHours;

        const fmt = (h) => {
          let hh = Math.floor(h) % 24;
          let mm = Math.round((h % 1) * 60);
          return String(hh).padStart(2, "0") + ":" + String(mm).padStart(2, "0");
        };

        // Hide all bars first
        ["concerta", "rubifen", "propranolol", "alprazolam"].forEach(id => {
          document.getElementById("bar-" + id).style.display = "none";
        });

        allPillIds.forEach((pillId) => {
          const data = PILL_DATA[pillId];
          const isTaken = !!log.pills[pillId];
          const exp = expected[pillId];
          let takenH, dose, timeStr;

          if (isTaken) {
            const pill = log.pills[pillId];
            const taken = new Date(pill.time);
            const takenTZ = getTimeInLisbon(taken);
            takenH = takenTZ.fractionalHours;
            dose = pill.dose;
            timeStr = pill.timeStr;
          } else if (exp) {
            // Expected but not yet taken
            const [hh, mm] = exp.time.split(":").map(Number);
            takenH = hh + mm / 60;
            dose = exp.dose;
            timeStr = exp.time;
          } else {
            return;
          }

          const onsetH = takenH + data.onsetMin / 60;
          const peakH = takenH + data.peakMin / 60;
          const fadeH = takenH + data.durationMin / 60;

          // Update button
          const btn = document.getElementById("btn-" + pillId);
          if (isTaken) {
            btn.textContent = "\\u2705 " + timeStr;
            btn.style.background = "#666";
          } else {
            btn.textContent = "Tomei";
            btn.style.background = data.color;
          }
          btn.disabled = false;

          // Update time display
          const timeSpan = document.getElementById(pillId + "-time");
          if (isTaken) {
            timeSpan.textContent = "\\u2705 " + timeStr;
            timeSpan.style.color = data.color;
          } else if (exp) {
            timeSpan.textContent = "\\u23f0 esperado " + exp.time;
            timeSpan.style.color = "var(--text-muted)";
          }

          // Show bar
          const barEl = document.getElementById("bar-" + pillId);
          barEl.style.display = "block";

          const fillEl = document.getElementById("bar-" + pillId + "-fill");
          const startPct = hourToPercent(takenH);
          const endPct = hourToPercent(fadeH);
          const peakStartPct = hourToPercent(onsetH);
          const peakEndPct = hourToPercent(peakH);
          const widthPct = endPct - startPct;

          fillEl.style.left = startPct + "%";
          fillEl.style.width = widthPct + "%";
          fillEl.style.height = "100%";
          fillEl.style.position = "absolute";
          fillEl.style.borderRadius = "4px";
          fillEl.style.cursor = isTaken ? "grab" : "default";
          fillEl.style.minWidth = "40px";

          // Add pill name label inside bar
          const shortName = pillId.charAt(0).toUpperCase() + pillId.slice(1);
          const labelText = shortName + " " + dose;

          if (isTaken) {
            // Determine how much of the bar the NOW line has passed
            const nowPct = hourToPercent(nowH);
            const barEndPct = startPct + widthPct;
            const peakOnsetPct = ((peakStartPct - startPct) / widthPct) * 100;
            const peakEndRelPct = ((peakEndPct - startPct) / widthPct) * 100;

            if (isToday(viewDate) && nowPct < startPct) {
              // Pill taken but effect hasn't started yet (just taken)
              fillEl.style.background = data.color + "33";
              fillEl.style.border = "2px dashed " + data.color;
              fillEl.innerHTML = '<span style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);font-size:0.7em;font-weight:bold;color:' + data.color + ';white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:90%;">' + labelText + '</span>';
            } else if (!isToday(viewDate) || nowPct >= barEndPct) {
              // Full bar colored (past day or NOW past the bar)
              fillEl.style.border = "none";
              fillEl.style.background = 'linear-gradient(90deg, ' +
                data.color + '55 0%, ' +
                data.color + '55 ' + peakOnsetPct + '%, ' +
                data.color + ' ' + peakOnsetPct + '%, ' +
                data.color + ' ' + peakEndRelPct + '%, ' +
                data.color + '55 ' + peakEndRelPct + '%, ' +
                data.color + '55 100%)';
              fillEl.innerHTML = '<span style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);font-size:0.7em;font-weight:bold;color:white;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:90%;text-shadow:0 1px 2px rgba(0,0,0,0.5);">' + labelText + '</span>';
            } else {
              // NOW is somewhere in the middle of this bar — partial coloring
              const progressPct = ((nowPct - startPct) / widthPct) * 100;
              fillEl.style.border = "none";
              fillEl.style.background = 'linear-gradient(90deg, ' +
                data.color + '55 0%, ' +
                data.color + '55 ' + Math.min(peakOnsetPct, progressPct) + '%, ' +
                data.color + ' ' + Math.min(peakOnsetPct, progressPct) + '%, ' +
                data.color + ' ' + Math.min(peakEndRelPct, progressPct) + '%, ' +
                data.color + '55 ' + Math.min(peakEndRelPct, progressPct) + '%, ' +
                data.color + '55 ' + progressPct + '%, ' +
                data.color + '1a ' + progressPct + '%, ' +
                data.color + '1a 100%)';
              fillEl.innerHTML = '<span style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);font-size:0.7em;font-weight:bold;color:white;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:90%;text-shadow:0 1px 2px rgba(0,0,0,0.5);">' + labelText + '</span>';
            }
          } else {
            // Expected / not yet taken — grey dashed outline
            fillEl.style.background = "transparent";
            fillEl.style.border = "2px dashed " + data.color + "80";
            fillEl.innerHTML = '<span style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);font-size:0.7em;font-weight:bold;color:' + data.color + '80;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:90%;">' + labelText + ' (esperado)</span>';
          }

          // Effects table row
          const status = isTaken ? "\\u2705" : "\\u23f0";
          const row = document.createElement("tr");
          row.style.opacity = isTaken ? "1" : "0.5";
          row.innerHTML =
            '<td style="color:' + data.color + ';font-weight:bold;">' + status + ' ' + data.name + '</td>' +
            '<td>' + dose + '</td>' +
            '<td><strong>' + timeStr + '</strong>' + (isTaken ? '' : ' (esperado)') + '</td>' +
            '<td>' + fmt(onsetH) + ' (' + data.onsetMin + 'min)</td>' +
            '<td style="color:' + data.color + ';font-weight:bold;">' + fmt(onsetH) + '\\u2013' + fmt(peakH) + '</td>' +
            '<td>' + fmt(fadeH) + '</td>';
          tbody.appendChild(row);
        });

        // Update NOW indicator
        updateNowIndicator();

        // Render symptoms
        renderSymptoms();

        // Re-attach drag listeners (bars now visible)
        setTimeout(attachDragListeners, 50);

        // Schedule check-in based on pill peaks
        scheduleCheckin();
      }'''

html = html.replace(old_updatePillUI, new_updatePillUI)

# 4. Fix the bar container overflow: hidden → visible so drag grab area works
# Change all 4 bar track containers from overflow:hidden to overflow:visible
html = html.replace(
    '''                      height: 32px;
                      background: var(--border);
                      border-radius: 4px;
                      overflow: hidden;''',
    '''                      height: 32px;
                      background: var(--border);
                      border-radius: 4px;
                      overflow: visible;'''
)
# There may be multiple instances — do it until all are changed  
while 'overflow: hidden;' in html and 'height: 32px;\n                      background: var(--border);\n                      border-radius: 4px;\n                      overflow: hidden;' in html:
    html = html.replace(
        'height: 32px;\n                      background: var(--border);\n                      border-radius: 4px;\n                      overflow: hidden;',
        'height: 32px;\n                      background: var(--border);\n                      border-radius: 4px;\n                      overflow: visible;'
    )

# 5. Update the NOW indicator to also update bar colors every tick
old_now_update = '''      // Update NOW indicator every 10 seconds
      setInterval(updateNowIndicator, 10000);'''
new_now_update = '''      // Update NOW indicator + bar colors every 10 seconds
      setInterval(function() { updateNowIndicator(); updatePillUI(); }, 10000);'''
html = html.replace(old_now_update, new_now_update)

# 6. Fix the "timeline-empty" message  
html = html.replace(
    'Clica "Tomei" para ativar timeline',
    'Nenhum medicamento agendado para este dia'
)

print(f"File length: {len(html)} chars")

with open(FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("✅ All fixes applied!")

# Verify changes
checks = [
    ("Expected pills", "EXPECTED_PILLS" in html),
    ("changeDay fixed", "maxDate" in html),
    ("updatePillUI updated", "getExpectedForDay" in html),
    ("No duplicate init", html.count("// Initialize pill tracker on load") == 1),
    ("Overflow visible", "overflow: visible;" in html),
]
for name, ok in checks:
    print(f"  {'✅' if ok else '❌'} {name}")
