#!/usr/bin/env python3
"""Inject inline-tree data + renderer into index.html.

1. Reads _inline_tree.js (pure UTF-8, no Python escaping issues)
2. Injects it just before 'var FWM_DATA = {' inside the existing IIFE
3. Replaces the old flat generic-example rendering with hierarchical inline-tree rendering
"""

import pathlib, sys

ROOT = pathlib.Path(__file__).parent
HTML = ROOT / "index.html"
JS   = ROOT / "_inline_tree.js"

src  = HTML.read_text(encoding="utf-8")
js   = JS.read_text(encoding="utf-8")

# ── Step 1: inject the JS data just before FWM_DATA ──────────────────────

MARKER_A = "        var FWM_DATA = {"
if MARKER_A not in src:
    sys.exit("ERROR: cannot find FWM_DATA marker")

# Only inject once
if "FWM_INLINE_TREE" in src:
    print("FWM_INLINE_TREE already present — skipping data injection")
else:
    src = src.replace(MARKER_A, js + "\n" + MARKER_A, 1)
    print("Injected inline-tree data before FWM_DATA")

# ── Step 2: replace old flat example rendering ───────────────────────────

OLD_RENDER = '''              // Build generic examples & prompt from FW_EXAMPLES general data
              var exDiv = document.getElementById("fwm-examples-display");
              var genData =
                typeof FW_EXAMPLES !== "undefined" &&
                FW_EXAMPLES[key] &&
                FW_EXAMPLES[key].examples &&
                FW_EXAMPLES[key].examples.general
                  ? FW_EXAMPLES[key].examples.general
                  : null;
              if (genData) {
                var html =
                  '<div style="background:#f1f8e9;border-radius:8px;padding:12px 16px;border-left:3px solid #7cb342;">';
                html +=
                  '<p style="margin:0 0 8px;font-weight:700;font-size:0.9em;color:#33691e;">💡 Generic Examples (Template)</p>';
                if (genData.lvl2 && genData.lvl2.length > 0) {
                  html +=
                    '<p style="margin:0 0 4px;font-size:0.82em;color:#558b2f;font-weight:600;">Level 2 (branches):</p>';
                  html +=
                    '<ul style="margin:0 0 8px;padding-left:18px;font-size:0.82em;color:#555;">';
                  genData.lvl2.forEach(function (ex) {
                    html += '<li style="margin-bottom:2px;">' + ex + "</li>";
                  });
                  html += "</ul>";
                }
                if (genData.lvl3 && genData.lvl3.length > 0) {
                  html +=
                    '<p style="margin:0 0 4px;font-size:0.82em;color:#558b2f;font-weight:600;">Level 3 (drivers — MECE lists):</p>';
                  html +=
                    '<ul style="margin:0 0 8px;padding-left:18px;font-size:0.82em;color:#555;">';
                  genData.lvl3.forEach(function (ex) {
                    html += '<li style="margin-bottom:2px;">' + ex + "</li>";
                  });
                  html += "</ul>";
                }
                if (genData.prompts && genData.prompts.length > 0) {
                  var randPrompt =
                    genData.prompts[
                      Math.floor(Math.random() * genData.prompts.length)
                    ];
                  html +=
                    '<p style="margin:8px 0 4px;font-size:0.82em;color:#558b2f;font-weight:600;">📋 Sample Case Prompt:</p>';
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

NEW_RENDER = '''              // Build inline tree + prompt from FWM_INLINE_TREE data
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

if OLD_RENDER in src:
    src = src.replace(OLD_RENDER, NEW_RENDER, 1)
    print("Replaced flat example rendering with inline-tree rendering")
elif "FWM_INLINE_TREE[key]" in src:
    print("Inline-tree rendering already present — skipping")
else:
    sys.exit("ERROR: could not find old flat rendering block to replace")

HTML.write_text(src, encoding="utf-8")
print(f"Done — wrote {len(src):,} chars to {HTML.name}")
