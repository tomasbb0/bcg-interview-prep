#!/usr/bin/env python3
"""Comprehensive update: black highlighted lines, merged gray box,
   pill restyling, PT/EN gray box, prompt-first ordering."""

import pathlib, sys, re

ROOT = pathlib.Path(__file__).parent
HTML = ROOT / "index.html"

src = HTML.read_text(encoding="utf-8")
changes = 0

# ═══════════════════════════════════════════════════════════
# 1. RESTYLE ACADEMIC PILLS → black fill, white text
#    RESTYLE LOGICAL PILLS  → white fill, black border/text
# ═══════════════════════════════════════════════════════════

ACADEMIC_IDS = {
    "fwm-n-supply-demand": ("📊 Supply &amp; Demand", "📊 Oferta e Procura"),
    "fwm-n-three-cs":      ("🔺 Three Cs",           "🔺 Três Cs"),
    "fwm-n-porters-five":  ("⭐ Porter's 5 Forces",  "⭐ 5 Forças de Porter"),
    "fwm-n-four-ps":       ("🎯 Four Ps",            "🎯 Quatro Ps"),
}

LOGICAL_IDS = {
    "fwm-n-equations":     ("🔢 Equations",     "🔢 Equações"),
    "fwm-n-key-questions": ("❓ Key Questions",  "❓ Questões-chave"),
    "fwm-n-hypotheses":    ("🧪 Hypotheses",     "🧪 Hipóteses"),
    "fwm-n-root-causes":   ("🔍 Root Causes",    "🔍 Causas-raiz"),
    "fwm-n-process-map":   ("🗺️ Process Map",   "🗺️ Mapa de Processo"),
    "fwm-n-from-to":       ("➡️ From-To",       "➡️ De-Para"),
}

# Replace academic pill styles
for pill_id, (en, pt) in ACADEMIC_IDS.items():
    # Find the pill div and replace its style
    pat = re.compile(
        r'(<div class="fwm-pill" id="' + re.escape(pill_id) + r'"[^>]*?)style="[^"]*"',
        re.DOTALL,
    )
    new_style = 'style="background:#222;color:#fff;border-color:#222;font-size:12px;"'
    m = pat.search(src)
    if m:
        old = m.group(0)
        new = m.group(1) + new_style
        src = src.replace(old, new, 1)
        changes += 1
        print(f"  Restyled {pill_id} → black fill")
    else:
        print(f"  WARNING: could not find {pill_id}")

# Replace logical pill styles
for pill_id, (en, pt) in LOGICAL_IDS.items():
    pat = re.compile(
        r'(<div class="fwm-pill" id="' + re.escape(pill_id) + r'"[^>]*?)style="[^"]*"',
        re.DOTALL,
    )
    new_style = 'style="background:#fff;color:#222;border-color:#222;font-size:11px;"'
    m = pat.search(src)
    if m:
        old = m.group(0)
        new = m.group(1) + new_style
        src = src.replace(old, new, 1)
        changes += 1
        print(f"  Restyled {pill_id} → white fill/black border")
    else:
        print(f"  WARNING: could not find {pill_id}")

print(f"[1/5] Restyled pills ({changes} changes)")

# ═══════════════════════════════════════════════════════════
# 2. MODIFY drawFwmLines TO HIGHLIGHT PATH TO SELECTED PILL
# ═══════════════════════════════════════════════════════════

OLD_DRAW = '''        window.drawFwmLines = function () {
          var c = document.getElementById("fwm-tree-container");
          var svg = document.getElementById("fwm-lines");
          if (!c || !svg) return;
          // Check if fw-map section is visible
          var fwMap = document.getElementById("fw-map");
          if (fwMap && !fwMap.classList.contains("active")) return;

          svg.innerHTML = "";
          var cr = c.getBoundingClientRect();

          FWM_CONNS.forEach(function (conn) {
            var fe = document.getElementById(conn.f);
            var te = document.getElementById(conn.t);
            if (!fe || !te) return;
            var fr = fe.getBoundingClientRect();
            var tr = te.getBoundingClientRect();
            // From bottom-center of parent pill to top-center of child pill
            var x1 = fr.left + fr.width / 2 - cr.left;
            var y1 = fr.bottom - cr.top;
            var x2 = tr.left + tr.width / 2 - cr.left;
            var y2 = tr.top - cr.top;

            // Use curved paths for cleaner look
            var midY = (y1 + y2) / 2;
            var path = document.createElementNS(
              "http://www.w3.org/2000/svg",
              "path",
            );
            var d =
              "M" +
              x1 +
              "," +
              y1 +
              " C" +
              x1 +
              "," +
              midY +
              " " +
              x2 +
              "," +
              midY +
              " " +
              x2 +
              "," +
              y2;
            path.setAttribute("d", d);
            path.setAttribute("fill", "none");
            path.setAttribute("stroke", conn.d ? "#ccc" : "#aaa");
            path.setAttribute("stroke-width", "2");
            if (conn.d) path.setAttribute("stroke-dasharray", "6,4");
            svg.appendChild(path);
          });
        };'''

NEW_DRAW = '''        /* Global: which pill is highlighted? null = none */
        window.fwmHighlightPill = null;

        window.drawFwmLines = function () {
          var c = document.getElementById("fwm-tree-container");
          var svg = document.getElementById("fwm-lines");
          if (!c || !svg) return;
          var fwMap = document.getElementById("fw-map");
          if (fwMap && !fwMap.classList.contains("active")) return;

          svg.innerHTML = "";
          var cr = c.getBoundingClientRect();

          /* Build ancestor set for highlighted pill */
          var hlSet = {};
          if (window.fwmHighlightPill) {
            /* Build parent map from current FWM_CONNS */
            var parentMap = {};
            FWM_CONNS.forEach(function (conn) {
              if (!conn.d) { /* only solid connections */
                parentMap[conn.t] = conn.f;
              }
            });
            /* Walk up from highlighted pill to root */
            var cur = window.fwmHighlightPill;
            while (cur && parentMap[cur]) {
              var p = parentMap[cur];
              hlSet[p + "|" + cur] = true;
              cur = p;
            }
          }

          FWM_CONNS.forEach(function (conn) {
            var fe = document.getElementById(conn.f);
            var te = document.getElementById(conn.t);
            if (!fe || !te) return;
            var fr = fe.getBoundingClientRect();
            var tr = te.getBoundingClientRect();
            var x1 = fr.left + fr.width / 2 - cr.left;
            var y1 = fr.bottom - cr.top;
            var x2 = tr.left + tr.width / 2 - cr.left;
            var y2 = tr.top - cr.top;

            var midY = (y1 + y2) / 2;
            var path = document.createElementNS("http://www.w3.org/2000/svg", "path");
            var d = "M" + x1 + "," + y1 + " C" + x1 + "," + midY + " " + x2 + "," + midY + " " + x2 + "," + y2;
            path.setAttribute("d", d);
            path.setAttribute("fill", "none");

            /* Determine color: black if on highlight path, else gray */
            var connKey = conn.f + "|" + conn.t;
            var isHighlighted = window.fwmHighlightPill && hlSet[connKey];
            if (isHighlighted) {
              path.setAttribute("stroke", "#222");
              path.setAttribute("stroke-width", "3");
            } else {
              path.setAttribute("stroke", "#ddd");
              path.setAttribute("stroke-width", "2");
            }
            if (conn.d) path.setAttribute("stroke-dasharray", "6,4");
            svg.appendChild(path);
          });
        };'''

if OLD_DRAW in src:
    src = src.replace(OLD_DRAW, NEW_DRAW, 1)
    print("[2/5] Replaced drawFwmLines with path-highlighting version")
else:
    print("[2/5] WARNING: could not find drawFwmLines to replace")

# ═══════════════════════════════════════════════════════════
# 3. UPDATE CLICK HANDLER: set fwmHighlightPill + merged gray box
# ═══════════════════════════════════════════════════════════

# 3a. On pill click, set highlight and redraw lines
OLD_CLICK_ACTIVE = '''              pill.classList.add("active");
              currentFwmNode = key;

              // Build chain'''

NEW_CLICK_ACTIVE = '''              pill.classList.add("active");
              currentFwmNode = key;

              // Highlight connector lines path
              window.fwmHighlightPill = "fwm-n-" + key.replace("competitive-response","comp-resp").replace("cost-reduction","cost-red").replace("fixed-costs","fc").replace("variable-costs","vc").replace("market-entry","market-entry").replace("new-product","new-product").replace("m-and-a","m-and-a").replace("process-optimization","process-opt");
              window.drawFwmLines();

              // Build chain'''

if OLD_CLICK_ACTIVE in src:
    src = src.replace(OLD_CLICK_ACTIVE, NEW_CLICK_ACTIVE, 1)
    print("[3a/5] Added fwmHighlightPill on pill click")
else:
    print("[3a/5] WARNING: could not find click active block")

# 3b. On toggle-close (same pill clicked), clear highlight
OLD_TOGGLE_CLOSE = '''              if (currentFwmNode === key && panel.classList.contains("show")) {
                panel.classList.remove("show");
                pill.classList.remove("active");
                currentFwmNode = null;
                return;
              }'''

NEW_TOGGLE_CLOSE = '''              if (currentFwmNode === key && panel.classList.contains("show")) {
                panel.classList.remove("show");
                pill.classList.remove("active");
                currentFwmNode = null;
                window.fwmHighlightPill = null;
                window.drawFwmLines();
                return;
              }'''

if OLD_TOGGLE_CLOSE in src:
    src = src.replace(OLD_TOGGLE_CLOSE, NEW_TOGGLE_CLOSE, 1)
    print("[3b/5] Added highlight clear on toggle-close")
else:
    print("[3b/5] WARNING: could not find toggle close block")

# 3c. On panel close button, clear highlight
OLD_CLOSE_BTN = '''onclick="this.parentElement.classList.remove('show');document.querySelectorAll('.fwm-pill.active').forEach(function(p){p.classList.remove('active')});"'''

NEW_CLOSE_BTN = '''onclick="this.parentElement.classList.remove('show');document.querySelectorAll('.fwm-pill.active').forEach(function(p){p.classList.remove('active')});window.fwmHighlightPill=null;if(window.drawFwmLines)window.drawFwmLines();"'''

if OLD_CLOSE_BTN in src:
    src = src.replace(OLD_CLOSE_BTN, NEW_CLOSE_BTN, 1)
    print("[3c/5] Updated close button to clear highlight")
else:
    print("[3c/5] WARNING: could not find close button onclick")

# ═══════════════════════════════════════════════════════════
# 4. MERGE GRAY BOX: prompt first, then inline tree, hide FWM_DATA tree
# ═══════════════════════════════════════════════════════════

OLD_RENDER = '''              // Build framework tree if available
              if (data.tree) {
                treeEl.innerHTML = fwmRenderTree(data.tree);
                treeEl.style.display = "block";
              } else {
                treeEl.style.display = "none";
              }

              // Build inline tree + prompt from FWM_INLINE_TREE data
              var exDiv = document.getElementById("fwm-examples-display");
              var treeNode = (typeof window.FWM_INLINE_TREE !== "undefined") ? window.FWM_INLINE_TREE[key] : null;
              var genData =
                typeof FW_EXAMPLES !== "undefined" &&
                FW_EXAMPLES[key] &&
                FW_EXAMPLES[key].examples &&
                FW_EXAMPLES[key].examples.general
                  ? FW_EXAMPLES[key].examples.general
                  : null;
              if (treeNode || genData) {
                var html =
                  '<div style="background:#f1f8e9;border-radius:8px;padding:12px 16px;border-left:3px solid #7cb342;">';
                html +=
                  '<p style="margin:0 0 8px;font-weight:700;font-size:0.9em;color:#33691e;">💡 Inline Tree (Hints & Structure)</p>';
                if (treeNode && window.fwmRenderInlineTree) {
                  html += window.fwmRenderInlineTree(treeNode, 0);
                }
                if (genData && genData.prompts && genData.prompts.length > 0) {
                  var randPrompt =
                    genData.prompts[
                      Math.floor(Math.random() * genData.prompts.length)
                    ];
                  html +=
                    '<p style="margin:12px 0 4px;font-size:0.82em;color:#558b2f;font-weight:600;">📋 Sample Case Prompt:</p>';
                  html +=
                    "<p style=\\"margin:0;font-size:0.85em;font-family:'Courier New',monospace;color:#333;line-height:1.5;padding:8px;background:#fff;border-radius:4px;border:1px solid #c5e1a5;\\">&ldquo;" +
                    randPrompt +
                    "&rdquo;</p>";
                }
                html += "</div>";
                exDiv.innerHTML = html;
                exDiv.style.display = "block";
              } else {
                exDiv.style.display = "none";
              }'''

NEW_RENDER = '''              // Hide separate framework tree — inline tree replaces it
              treeEl.style.display = "none";

              // Build merged gray box: prompt first, then inline tree with hints
              var exDiv = document.getElementById("fwm-examples-display");
              var treeNode = (typeof window.FWM_INLINE_TREE !== "undefined") ? window.FWM_INLINE_TREE[key] : null;
              var genData =
                typeof FW_EXAMPLES !== "undefined" &&
                FW_EXAMPLES[key] &&
                FW_EXAMPLES[key].examples &&
                FW_EXAMPLES[key].examples.general
                  ? FW_EXAMPLES[key].examples.general
                  : null;
              if (treeNode || genData) {
                var html =
                  '<div style="background:#f1f8e9;border-radius:8px;padding:12px 16px;border-left:3px solid #7cb342;">';
                // PROMPT FIRST
                if (genData && genData.prompts && genData.prompts.length > 0) {
                  var randPrompt =
                    genData.prompts[
                      Math.floor(Math.random() * genData.prompts.length)
                    ];
                  html +=
                    '<p style="margin:0 0 4px;font-size:0.82em;color:#558b2f;font-weight:600;">📋 Sample Case Prompt:</p>';
                  html +=
                    "<p style=\\"margin:0 0 12px;font-size:0.85em;font-family:'Courier New',monospace;color:#333;line-height:1.5;padding:8px;background:#fff;border-radius:4px;border:1px solid #c5e1a5;\\">&ldquo;" +
                    randPrompt +
                    "&rdquo;</p>";
                }
                // THEN INLINE TREE
                if (treeNode && window.fwmRenderInlineTree) {
                  html += window.fwmRenderInlineTree(treeNode, 0);
                }
                html += "</div>";
                exDiv.innerHTML = html;
                exDiv.style.display = "block";
              } else {
                exDiv.style.display = "none";
              }'''

if OLD_RENDER in src:
    src = src.replace(OLD_RENDER, NEW_RENDER, 1)
    print("[4/5] Merged gray box: prompt first + inline tree (no separate framework tree)")
else:
    print("[4/5] WARNING: could not find old render block")

# ═══════════════════════════════════════════════════════════
# 5. UPDATE fwmRenderInlineTree TO RESPECT PT/EN TOGGLE
# ═══════════════════════════════════════════════════════════

OLD_RENDERER = '''      window.fwmRenderInlineTree = function (node, depth) {
        depth = depth || 0;
        var html = "";
        var indent = depth * 16;
        var subs = node.subs || [];

        if (depth === 0 && node.label) {
          html += '<div style="font-weight:700;font-size:0.95em;margin-bottom:8px;color:#2e7d32;">' + node.label + '</div>';
          if (node.hint) {
            html += '<div style="font-size:0.82em;color:#666;margin-bottom:10px;">💡 ' + node.hint + '</div>';
          }
        }

        subs.forEach(function (sub) {
          html += '<div style="margin-left:' + indent + 'px;margin-bottom:6px;">';
          html += '<span style="font-weight:600;font-size:0.88em;color:#333;">' + sub.label + '</span>';
          if (sub.hint) {
            html += '<br><span style="font-size:0.82em;color:#666;margin-left:4px;">💡 ' + sub.hint + '</span>';
          }
          if (sub.subs && sub.subs.length > 0) {
            html += window.fwmRenderInlineTree(sub, depth + 1);
          }
          html += '</div>';
        });
        return html;
      };'''

NEW_RENDERER = '''      /* Pick the right half of "EN / PT" labels based on current language */
      function fwmLangLabel(label) {
        if (!label) return "";
        var parts = label.split(" / ");
        if (parts.length < 2) return label;
        return (window.fwmLang === "pt") ? parts[parts.length - 1] : parts[0];
      }

      window.fwmRenderInlineTree = function (node, depth) {
        depth = depth || 0;
        var html = "";
        var indent = depth * 16;
        var subs = node.subs || [];

        if (depth === 0 && node.label) {
          html += '<div style="font-weight:700;font-size:0.95em;margin-bottom:8px;color:#2e7d32;">' + fwmLangLabel(node.label) + '</div>';
          if (node.hint) {
            html += '<div style="font-size:0.82em;color:#666;margin-bottom:10px;">' + String.fromCodePoint(0x1f4a1) + ' ' + node.hint + '</div>';
          }
        }

        subs.forEach(function (sub) {
          html += '<div style="margin-left:' + indent + 'px;margin-bottom:6px;">';
          html += '<span style="font-weight:600;font-size:0.88em;color:#333;">' + fwmLangLabel(sub.label) + '</span>';
          if (sub.hint) {
            html += '<br><span style="font-size:0.82em;color:#666;margin-left:4px;">' + String.fromCodePoint(0x1f4a1) + ' ' + sub.hint + '</span>';
          }
          if (sub.subs && sub.subs.length > 0) {
            html += window.fwmRenderInlineTree(sub, depth + 1);
          }
          html += '</div>';
        });
        return html;
      };'''

if OLD_RENDERER in src:
    src = src.replace(OLD_RENDERER, NEW_RENDERER, 1)
    print("[5/5] Updated fwmRenderInlineTree with PT/EN-aware labels")
else:
    print("[5/5] WARNING: could not find old renderer")

HTML.write_text(src, encoding="utf-8")
print(f"\nDone — wrote {len(src):,} chars to {HTML.name}")
