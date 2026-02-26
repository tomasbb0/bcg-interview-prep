#!/usr/bin/env python3
"""Fix Framework Map: replace static SVG connectors with dynamic JS-drawn lines
that actually connect to the pill shapes."""
import re

FILE = '/Users/tomasbatalha/Projects/Planning and Advisory/Tomas_Batalha_Future_Plan/0_ACTIVE_NOW/BCG_Interview_Prep/index.html'

with open(FILE, 'r', encoding='utf-8') as f:
    html = f.read()

original_len = len(html)

# ──────────────────────────────────────────────────
# 1. Add id attributes to each pill (for JS targeting)
# ──────────────────────────────────────────────────
pill_ids = [
    ('data-fwm="profitability"', 'id="fwm-n-profitability" data-fwm="profitability"'),
    ('data-fwm="revenue"',      'id="fwm-n-revenue" data-fwm="revenue"'),
    ('data-fwm="costs"',        'id="fwm-n-costs" data-fwm="costs"'),
    ('data-fwm="volume"',       'id="fwm-n-volume" data-fwm="volume"'),
    ('data-fwm="price"',        'id="fwm-n-price" data-fwm="price"'),
    ('data-fwm="fixed-costs"',  'id="fwm-n-fc" data-fwm="fixed-costs"'),
    ('data-fwm="variable-costs"', 'id="fwm-n-vc" data-fwm="variable-costs"'),
    ('data-fwm="growth"',       'id="fwm-n-growth" data-fwm="growth"'),
    ('data-fwm="pricing"',      'id="fwm-n-pricing" data-fwm="pricing"'),
    ('data-fwm="competitive-response"', 'id="fwm-n-comp-resp" data-fwm="competitive-response"'),
    ('data-fwm="cost-reduction"', 'id="fwm-n-cost-red" data-fwm="cost-reduction"'),
    ('data-fwm="investment"',   'id="fwm-n-investment" data-fwm="investment"'),
    ('data-fwm="market-entry"', 'id="fwm-n-market-entry" data-fwm="market-entry"'),
    ('data-fwm="new-product"',  'id="fwm-n-new-product" data-fwm="new-product"'),
    ('data-fwm="m-and-a"',      'id="fwm-n-m-and-a" data-fwm="m-and-a"'),
    ('data-fwm="process-optimization"', 'id="fwm-n-process-opt" data-fwm="process-optimization"'),
]

for old, new in pill_ids:
    count = html.count(old)
    html = html.replace(old, new, 1)  # Only first occurrence (in the map HTML)
    print(f"  pill id: {old} → found {count}x, replaced 1st")

# ──────────────────────────────────────────────────
# 2. Remove ALL static SVG connector divs
# ──────────────────────────────────────────────────
# Pattern: <div class="fwm-connector">\n  <svg ...>...</svg>\n  </div>
connector_pattern = r'<div class="fwm-connector">\s*<svg[^>]*>.*?</svg>\s*</div>'
n_connectors = len(re.findall(connector_pattern, html, re.DOTALL))
html = re.sub(connector_pattern, '', html, flags=re.DOTALL)
print(f"  Removed {n_connectors} static SVG connector blocks")

# ──────────────────────────────────────────────────
# 3. Add position:relative to the .fwm-tree container + SVG overlay
# ──────────────────────────────────────────────────
html = html.replace(
    '<!-- The Tree Map (HTML-based) -->\n        <div class="fwm-tree">',
    '<!-- The Tree Map (dynamic connectors) -->\n        <div class="fwm-tree" id="fwm-tree-container" style="position:relative;">\n          <!-- Dynamic SVG overlay for connector lines -->\n          <svg id="fwm-lines" style="position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;overflow:visible;"></svg>'
)
print("  Added position:relative to tree container + SVG overlay")

# ──────────────────────────────────────────────────
# 4. Add z-index:1 + position:relative to pill CSS
# ──────────────────────────────────────────────────
html = html.replace(
    """.fwm-pill { 
            display:inline-flex; align-items:center; justify-content:center;
            padding:8px 20px; border-radius:50px; font-size:13px; font-weight:600;
            cursor:pointer; border:2px solid; transition: all 0.2s; position:relative;""",
    """.fwm-pill { 
            display:inline-flex; align-items:center; justify-content:center;
            padding:8px 20px; border-radius:50px; font-size:13px; font-weight:600;
            cursor:pointer; border:2px solid; transition: all 0.2s; position:relative;
            z-index:1;"""
)
print("  Added z-index:1 to .fwm-pill CSS")

# ──────────────────────────────────────────────────
# 5. Add row gap/margin CSS for better vertical spacing between rows 
#    (so lines have room)
# ──────────────────────────────────────────────────
html = html.replace(
    '.fwm-row { display:flex; justify-content:center; gap:16px; margin-bottom:8px; position:relative; }',
    '.fwm-row { display:flex; justify-content:center; gap:16px; margin-bottom:14px; position:relative; }'
)
html = html.replace(
    '.fwm-label { text-align:center; color:#888; font-size:11px; font-style:italic; margin:4px 0; }',
    '.fwm-label { text-align:center; color:#888; font-size:11px; font-style:italic; margin:6px 0; }'
)
print("  Increased row spacing for better connector visibility")

# ──────────────────────────────────────────────────
# 6. Inject dynamic line drawing JS after the FWM IIFE
# ──────────────────────────────────────────────────
LINE_JS = r"""
      // ═══════════════════════════════════════════════
      // FRAMEWORK MAP — DYNAMIC CONNECTOR LINES
      // ═══════════════════════════════════════════════
      (function(){
        var FWM_CONNS = [
          // Profitability splits
          {f:'fwm-n-profitability', t:'fwm-n-revenue'},
          {f:'fwm-n-profitability', t:'fwm-n-costs'},
          // Revenue decomposition
          {f:'fwm-n-revenue', t:'fwm-n-volume'},
          {f:'fwm-n-revenue', t:'fwm-n-price'},
          // Revenue → Competitive Response (dashed: protection)
          {f:'fwm-n-revenue', t:'fwm-n-comp-resp', d:1},
          // Costs decomposition
          {f:'fwm-n-costs', t:'fwm-n-fc'},
          {f:'fwm-n-costs', t:'fwm-n-vc'},
          // Costs → Investment (dashed: cross-cutting)
          {f:'fwm-n-costs', t:'fwm-n-investment', d:1},
          // Volume → Growth
          {f:'fwm-n-volume', t:'fwm-n-growth'},
          // Price → Pricing
          {f:'fwm-n-price', t:'fwm-n-pricing'},
          // FC / VC → Cost Reduction
          {f:'fwm-n-fc', t:'fwm-n-cost-red'},
          {f:'fwm-n-vc', t:'fwm-n-cost-red'},
          // Growth sub-frameworks
          {f:'fwm-n-growth', t:'fwm-n-market-entry'},
          {f:'fwm-n-growth', t:'fwm-n-new-product'},
          {f:'fwm-n-growth', t:'fwm-n-m-and-a'},
          // Cost Reduction → Process Optimization
          {f:'fwm-n-cost-red', t:'fwm-n-process-opt'},
          // Cross-cutting: Market Entry / New Product → Pricing (dashed)
          {f:'fwm-n-market-entry', t:'fwm-n-pricing', d:1},
          {f:'fwm-n-new-product', t:'fwm-n-pricing', d:1}
        ];

        function drawFwmLines(){
          var c = document.getElementById('fwm-tree-container');
          var svg = document.getElementById('fwm-lines');
          if(!c || !svg) return;
          // Check if fw-map section is visible
          var fwMap = document.getElementById('fw-map');
          if(fwMap && !fwMap.classList.contains('active')) return;
          
          svg.innerHTML = '';
          var cr = c.getBoundingClientRect();
          
          FWM_CONNS.forEach(function(conn){
            var fe = document.getElementById(conn.f);
            var te = document.getElementById(conn.t);
            if(!fe || !te) return;
            var fr = fe.getBoundingClientRect();
            var tr = te.getBoundingClientRect();
            // From bottom-center of parent pill to top-center of child pill
            var x1 = fr.left + fr.width/2 - cr.left;
            var y1 = fr.bottom - cr.top;
            var x2 = tr.left + tr.width/2 - cr.left;
            var y2 = tr.top - cr.top;
            
            // Use curved paths for cleaner look
            var midY = (y1 + y2) / 2;
            var path = document.createElementNS('http://www.w3.org/2000/svg','path');
            var d = 'M'+x1+','+y1+' C'+x1+','+midY+' '+x2+','+midY+' '+x2+','+y2;
            path.setAttribute('d', d);
            path.setAttribute('fill', 'none');
            path.setAttribute('stroke', conn.d ? '#ccc' : '#aaa');
            path.setAttribute('stroke-width', conn.d ? '1.5' : '2');
            if(conn.d) path.setAttribute('stroke-dasharray','6,4');
            svg.appendChild(path);
          });
        }

        // Monkey-patch showSection to draw lines when fw-map becomes visible
        var _origShow = window.showSection;
        window.showSection = function(id){
          _origShow(id);
          if(id === 'fw-map') setTimeout(drawFwmLines, 60);
        };
        window.addEventListener('resize', drawFwmLines);
        // Draw on initial load (with delay for layout)
        setTimeout(drawFwmLines, 400);
        // Also try after a longer delay in case section is visible at start
        setTimeout(drawFwmLines, 1000);
      })();
"""

# Insert after the FWM IIFE closing, before INDUSTRY TABLE comment
marker = """      // ═══════════════════════════════════════════════
      // INDUSTRY TABLE — 3RD COLUMN: EXPLANATIONS
      // ═══════════════════════════════════════════════"""

if marker in html:
    html = html.replace(marker, LINE_JS + "\n" + marker)
    print("  Injected dynamic line drawing JS")
else:
    print("  ERROR: Could not find INDUSTRY TABLE marker!")

# ──────────────────────────────────────────────────
# WRITE
# ──────────────────────────────────────────────────
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nDone! {original_len} → {len(html)} chars ({len(html)-original_len:+d})")
print("Connector lines now dynamically drawn between actual pill positions using cubic bezier curves.")
