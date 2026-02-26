#!/usr/bin/env python3
"""V3 Updates:
1. Sidebar collapse toggle button (desktop)
2. Tree connector lines in green inline-tree box
3. No horizontal scroll + wider framework map section
4. Verify black-line path tracing works (already implemented)
"""

import re, sys

FILE = "index.html"

with open(FILE, "r", encoding="utf-8") as f:
    html = f.read()

original = html

# ────────────────────────────────────────────────
# STEP 1: Sidebar collapse toggle on desktop
# ────────────────────────────────────────────────
print("STEP 1: Sidebar collapse toggle...")

# 1a. Add CSS for collapsed state + toggle button
sidebar_css_marker = "/* MOBILE MENU */\n      .menu-toggle {"
sidebar_css_inject = """/* SIDEBAR COLLAPSE TOGGLE (desktop) */
      .sidebar-collapse-btn {
        position: absolute;
        top: 50%;
        right: -14px;
        transform: translateY(-50%);
        width: 28px;
        height: 28px;
        background: #fff;
        border: 1px solid #e5e5e5;
        border-radius: 50%;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        color: #888;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        z-index: 101;
        transition: all 0.2s;
      }
      .sidebar-collapse-btn:hover {
        color: #333;
        background: #f5f5f5;
        box-shadow: 0 2px 8px rgba(0,0,0,0.12);
      }
      body.sidebar-collapsed .sidebar {
        width: 0;
        overflow: hidden;
        border-right: none;
      }
      body.sidebar-collapsed .sidebar > * {
        opacity: 0;
        pointer-events: none;
      }
      body.sidebar-collapsed .sidebar .sidebar-collapse-btn {
        opacity: 1;
        pointer-events: auto;
        right: -40px;
        width: 32px;
        height: 32px;
        font-size: 16px;
      }
      body.sidebar-collapsed .main {
        margin-left: 0;
      }
      body.sidebar-collapsed .menu-toggle {
        display: none;
      }

      """ + sidebar_css_marker

if sidebar_css_marker in html:
    html = html.replace(sidebar_css_marker, sidebar_css_inject)
    print("  1a. CSS injected OK")
else:
    print("  1a. MARKER NOT FOUND!")

# 1b. Add the toggle button inside the sidebar
sidebar_html_marker = '<aside class="sidebar" id="bcg-nav">'
sidebar_html_inject = '<aside class="sidebar" id="bcg-nav">\n      <button class="sidebar-collapse-btn" id="sidebar-collapse-toggle" onclick="toggleSidebarCollapse()" title="Collapse sidebar">&#x276E;</button>'

if sidebar_html_marker in html:
    html = html.replace(sidebar_html_marker, sidebar_html_inject, 1)
    print("  1b. Toggle button HTML injected OK")
else:
    print("  1b. SIDEBAR HTML MARKER NOT FOUND!")

# 1c. Add JS function for toggle
sidebar_js_marker = "function toggleSidebar() {"
sidebar_js_inject = """function toggleSidebarCollapse() {
        var body = document.body;
        body.classList.toggle('sidebar-collapsed');
        var btn = document.getElementById('sidebar-collapse-toggle');
        if (body.classList.contains('sidebar-collapsed')) {
          btn.innerHTML = '&#x276F;'; // right arrow
          btn.title = 'Expand sidebar';
        } else {
          btn.innerHTML = '&#x276E;'; // left arrow
          btn.title = 'Collapse sidebar';
        }
        // Redraw framework map lines after animation
        setTimeout(function() { if (window.drawFwmLines) window.drawFwmLines(); }, 350);
      }

      function toggleSidebar() {"""

if sidebar_js_marker in html:
    html = html.replace(sidebar_js_marker, sidebar_js_inject, 1)
    print("  1c. Toggle JS injected OK")
else:
    print("  1c. SIDEBAR JS MARKER NOT FOUND!")


# ────────────────────────────────────────────────
# STEP 2: Tree connector lines in green box
# ────────────────────────────────────────────────
print("STEP 2: Tree connector lines in inline tree...")

old_render = """window.fwmRenderInlineTree = function (node, depth) {
          depth = depth || 0;
          var html = "";
          var indent = depth * 16;
          var subs = node.subs || [];

          if (depth === 0 && node.label) {
            html +=
              '<div style="font-weight:700;font-size:0.95em;margin-bottom:8px;color:#2e7d32;">' +
              fwmLangLabel(node.label) +
              "</div>";
            if (node.hint) {
              html +=
                '<div style="font-size:0.82em;color:#666;margin-bottom:10px;">' +
                String.fromCodePoint(0x1f4a1) +
                " " +
                node.hint +
                "</div>";
            }
          }

          subs.forEach(function (sub) {
            html +=
              '<div style="margin-left:' + indent + 'px;margin-bottom:6px;">';
            html +=
              '<span style="font-weight:600;font-size:0.88em;color:#333;">' +
              fwmLangLabel(sub.label) +
              "</span>";
            if (sub.hint) {
              html +=
                '<br><span style="font-size:0.82em;color:#666;margin-left:4px;">' +
                String.fromCodePoint(0x1f4a1) +
                " " +
                sub.hint +
                "</span>";
            }
            if (sub.subs && sub.subs.length > 0) {
              html += window.fwmRenderInlineTree(sub, depth + 1);
            }
            html += "</div>";
          });
          return html;
        };"""

new_render = """window.fwmRenderInlineTree = function (node, depth) {
          depth = depth || 0;
          var html = "";
          var subs = node.subs || [];

          if (depth === 0 && node.label) {
            html +=
              '<div style="font-weight:700;font-size:0.95em;margin-bottom:8px;color:#2e7d32;">' +
              fwmLangLabel(node.label) +
              "</div>";
            if (node.hint) {
              html +=
                '<div style="font-size:0.82em;color:#666;margin-bottom:10px;">' +
                String.fromCodePoint(0x1f4a1) +
                " " +
                node.hint +
                "</div>";
            }
          }

          if (subs.length > 0) {
            html += '<ul style="list-style:none;margin:0 0 0 ' + (depth > 0 ? '8' : '0') + 'px;padding:0;border-left:' + (depth > 0 ? '2px solid #c5e1a5' : 'none') + ';">';
            subs.forEach(function (sub, idx) {
              var isLast = idx === subs.length - 1;
              html += '<li style="position:relative;padding:4px 0 4px ' + (depth > 0 ? '16' : '4') + 'px;margin:0;">';
              /* Tree connector: horizontal tee line */
              if (depth > 0) {
                html += '<span style="position:absolute;left:-2px;top:12px;width:14px;height:0;border-top:2px solid #a5d6a7;"></span>';
                /* Vertical line cutoff for last item */
                if (isLast) {
                  html += '<span style="position:absolute;left:-2px;top:12px;bottom:0;width:4px;background:#f1f8e9;"></span>';
                  html += '<span style="position:absolute;left:-2px;top:0;height:12px;width:0;border-left:2px solid #a5d6a7;"></span>';
                }
              }
              html += '<span style="font-weight:600;font-size:0.88em;color:#333;">' + fwmLangLabel(sub.label) + '</span>';
              if (sub.hint) {
                html += '<br><span style="font-size:0.79em;color:#777;margin-left:2px;">' +
                  String.fromCodePoint(0x1f4a1) + ' ' + sub.hint + '</span>';
              }
              if (sub.subs && sub.subs.length > 0) {
                html += window.fwmRenderInlineTree(sub, depth + 1);
              }
              html += '</li>';
            });
            html += '</ul>';
          }
          return html;
        };"""

if old_render in html:
    html = html.replace(old_render, new_render)
    print("  Render function replaced OK")
else:
    print("  RENDER FUNCTION MARKER NOT FOUND! Trying partial match...")
    # Try matching just the function signature and body
    partial = 'window.fwmRenderInlineTree = function (node, depth) {'
    if partial in html:
        # Find the end of the function
        start = html.index(partial)
        # Find the matching closing };
        # Simple approach: find "};" after the function
        end_marker = "        };\n\n        var FWM_DATA"
        if end_marker in html[start:]:
            end = html.index(end_marker, start) + len("        };")
            html = html[:start] + new_render + html[end:]
            print("  Render function replaced via partial match OK")
        else:
            print("  COULD NOT FIND END MARKER!")
    else:
        print("  FUNCTION SIGNATURE NOT FOUND!")


# ────────────────────────────────────────────────
# STEP 3: Wider map + no horizontal scroll
# ────────────────────────────────────────────────
print("STEP 3: Wider layout + no horizontal scroll...")

# 3a. Remove max-width constraint on .main or increase it
old_main_style = """.main {
        margin-left: var(--sidebar-width);
        max-width: 900px;
        padding: 48px 56px;
        flex: 1;
      }"""

new_main_style = """.main {
        margin-left: var(--sidebar-width);
        max-width: 1200px;
        padding: 48px 56px;
        flex: 1;
      }"""

if old_main_style in html:
    html = html.replace(old_main_style, new_main_style)
    print("  3a. Main max-width increased to 1200px OK")
else:
    print("  3a. MAIN STYLE NOT FOUND!")

# 3b. Change overflow-x:auto to overflow-x:hidden on .fwm-tree and make pills shrink
old_fwm_tree = """.fwm-tree {
            position: relative;
            width: 100%;
            overflow-x: auto;
            padding-bottom: 20px;
          }"""

new_fwm_tree = """.fwm-tree {
            position: relative;
            width: 100%;
            overflow-x: hidden;
            padding-bottom: 20px;
          }"""

if old_fwm_tree in html:
    html = html.replace(old_fwm_tree, new_fwm_tree)
    print("  3b. overflow-x changed to hidden OK")
else:
    print("  3b. FWM-TREE STYLE NOT FOUND!")

# 3c. Make pills shrinkable — remove min-width and add flex-shrink
old_pill = """.fwm-pill {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 8px 20px;
            border-radius: 50px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            border: 2px solid;
            transition: all 0.2s;
            position: relative;
            z-index: 1;
            white-space: nowrap;
            min-width: 140px;
            text-align: center;
            user-select: none;
          }"""

new_pill = """.fwm-pill {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 8px 16px;
            border-radius: 50px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            border: 2px solid;
            transition: all 0.2s;
            position: relative;
            z-index: 1;
            white-space: nowrap;
            min-width: 0;
            text-align: center;
            user-select: none;
            flex-shrink: 1;
          }"""

if old_pill in html:
    html = html.replace(old_pill, new_pill)
    print("  3c. Pill min-width removed, flex-shrink added OK")
else:
    print("  3c. PILL STYLE NOT FOUND!")

# 3d. Make fwm-row flex-wrap properly
old_row = """.fwm-row {
            display: flex;
            justify-content: center;
            gap: 16px;
            margin-bottom: 56px;
            position: relative;
          }"""

new_row = """.fwm-row {
            display: flex;
            justify-content: center;
            gap: 12px;
            margin-bottom: 56px;
            position: relative;
            flex-wrap: nowrap;
          }"""

if old_row in html:
    html = html.replace(old_row, new_row)
    print("  3d. Row gap adjusted OK")
else:
    print("  3d. ROW STYLE NOT FOUND!")


# ────────────────────────────────────────────────
# WRITE RESULT
# ────────────────────────────────────────────────
if html != original:
    with open(FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print("\n✅ All changes written to", FILE)
else:
    print("\n⚠️  No changes made!")
