#!/usr/bin/env python3
"""Rewrite FWM_DATA insight texts to be more contextual:
- WHEN to use the framework
- What using it IMPLIES (parent chain context)
- What sub-frameworks to apply next
"""

FILE = '/Users/tomasbatalha/Projects/Planning and Advisory/Tomas_Batalha_Future_Plan/0_ACTIVE_NOW/BCG_Interview_Prep/index.html'

with open(FILE, 'r', encoding='utf-8') as f:
    html = f.read()

# Map of data-fwm key → new insight text
NEW_INSIGHTS = {
    'profitability': (
        'The ROOT framework — every case ultimately connects here. '
        'USE WHEN: the prompt says "profits declining", "margins shrinking", or any broad "improve performance". '
        'IMPLIES: you\'re at the very top of the tree; no parent framework above. '
        'NEXT: Decompose into Revenue vs. Costs. If revenue is the problem → Growth, Pricing, or Competitive Response. '
        'If costs → Cost Reduction or Investment. This is always your starting anchor.'
    ),
    'revenue': (
        'The revenue branch of Profitability. '
        'USE WHEN: you\'ve isolated that the problem sits on the top line — sales are down or not growing enough. '
        'IMPLIES: you\'re studying Profitability and have ruled out (or parked) the cost side. '
        'NEXT: Ask "Is it a Volume problem or a Price problem?" — then dive into Growth (volume) or Pricing (price). '
        'If it\'s an external threat eating revenue, consider Competitive Response.'
    ),
    'costs': (
        'The cost branch of Profitability. '
        'USE WHEN: revenue looks healthy but margins are shrinking — the problem is on the expense side. '
        'IMPLIES: you\'re studying Profitability and have identified costs as the lever. '
        'NEXT: Decompose into Fixed Costs vs. Variable Costs. '
        'Then apply Cost Reduction to cut them, Investment to evaluate spending, or Process Optimization for operational efficiency.'
    ),
    'volume': (
        'The volume lever under Revenue. '
        'USE WHEN: revenue is declining because fewer units are being sold, fewer customers are buying, or purchase frequency dropped. '
        'IMPLIES: you\'re studying Revenue → Profitability. You\'ve already identified it\'s not a pricing issue. '
        'NEXT: Apply the Growth framework — "How do we sell more?" leads to growing the core, Market Entry, New Product, or M&A.'
    ),
    'price': (
        'The price lever under Revenue. '
        'USE WHEN: volume is fine but revenue per unit is too low — discounts are too aggressive, pricing power is weak, or the pricing model is wrong. '
        'IMPLIES: you\'re studying Revenue → Profitability. You\'ve identified that the issue is price, not volume. '
        'NEXT: Apply the Pricing framework — analyze costs (floor), competitors (benchmark), and willingness to pay (ceiling). '
        'Pricing also gets triggered from New Product or Market Entry when setting prices for new offerings.'
    ),
    'fixed-costs': (
        'Fixed costs — expenses that don\'t change with output: rent, salaries, insurance, depreciation, IT, licenses. '
        'USE WHEN: the cost problem is structural — high overhead regardless of how much you produce. '
        'IMPLIES: you\'re studying Costs → Profitability. You\'ve split costs into fixed vs. variable. '
        'NEXT: Apply Cost Reduction to these costs — can we eliminate the need, do more with less, or find cheaper resources? '
        'Investment framework also connects here (e.g., "Should we invest in automation to reduce fixed labor costs?").'
    ),
    'variable-costs': (
        'Variable costs — expenses that scale with output: raw materials, packaging, shipping, commissions, energy per unit. '
        'USE WHEN: per-unit costs are too high, eating into margins as volume grows. '
        'IMPLIES: you\'re studying Costs → Profitability. You\'ve identified the variable component as the issue. '
        'NEXT: Apply Cost Reduction and specifically Process Optimization — optimize the process to reduce cost per unit. '
        'Common levers: renegotiate supplier contracts, reduce waste, improve production efficiency.'
    ),
    'growth': (
        'The Growth framework — "How to grow the business?" '
        'USE WHEN: the prompt asks about increasing revenue, expanding the business, or scaling up. You\'ve identified a volume gap. '
        'IMPLIES: you\'re studying Volume → Revenue → Profitability. The fact that you\'re here means you believe the company needs to sell MORE. '
        'NEXT: Branch into three paths — Market Entry ("enter a new geography/segment?"), '
        'New Product ("launch something new?"), or M&A ("acquire growth inorganically?"). '
        'Each of these is a deeper zoom-in on a specific growth mechanism.'
    ),
    'pricing': (
        'The Pricing framework — "How to price a product/service?" '
        'USE WHEN: the prompt asks about pricing strategy, price optimization, or when you\'re launching something new and need to set a price. '
        'IMPLIES: you\'re studying Price → Revenue → Profitability. The core question is "what price maximizes profit?" '
        'This is a CROSS-CUTTING framework — it can be triggered from Market Entry (pricing for a new market), '
        'New Product (pricing a new launch), or directly from the Price lever. '
        'STRUCTURE: Costs (floor) → Competitors (benchmark) → Willingness to Pay (ceiling).'
    ),
    'competitive-response': (
        'The Competitive Response framework — "How to respond to a competitive threat?" '
        'USE WHEN: a competitor has entered the market, launched a disruptive product, or is stealing market share. Revenue is under external threat. '
        'IMPLIES: you\'re DEFENDING Revenue → Profitability. Unlike Growth (which is proactive), this is reactive — something is attacking your top line. '
        'NEXT: Assess the impact, understand the competitor\'s play, then choose a response: '
        'do nothing, mitigate (retain clients), replicate (copy their offer), collaborate, or align (lower prices). '
        'May trigger Pricing (if you need to adjust prices) or Growth (if you need to outgrow the threat).'
    ),
    'cost-reduction': (
        'The Cost Reduction framework — "How to cut costs?" '
        'USE WHEN: the prompt asks about reducing expenses, improving margins on the cost side, or making operations leaner. '
        'IMPLIES: you\'re studying Costs → Profitability. You\'ve identified that the business spends too much (fixed, variable, or both). '
        'NEXT: For operational and process-specific cost issues, zoom into Process Optimization. '
        'STRUCTURE: (1) Reduce the need entirely, (2) Meet the need with fewer resources, (3) Reduce the cost of resources. '
        'Each of these can apply to both fixed and variable costs.'
    ),
    'investment': (
        'The Investment framework — "Should we make this investment?" '
        'USE WHEN: the prompt asks about buying equipment, building a factory, entering a new business, or any major CAPEX decision. '
        'IMPLIES: this is CROSS-CUTTING — it can sit on both sides of the Profitability tree. '
        'Invest to GROW (Revenue side: new market, new product) or invest to SAVE (Cost side: automation, process improvement). '
        'STRUCTURE: Impact on revenue + Impact on costs → Break-even analysis → Implementation feasibility. '
        'Often follows Growth or Cost Reduction as the "financial validation" step.'
    ),
    'market-entry': (
        'The Market Entry framework — "Should we enter a new market?" '
        'USE WHEN: the prompt asks about expanding to a new geography, entering a new customer segment, or launching in a new country. '
        'IMPLIES: you\'re studying Growth → Volume → Revenue → Profitability. The full chain means: '
        'someone decided profits need to improve → via revenue → via selling more → via entering a new market. '
        'NEXT: May trigger Pricing (what price for this new market?) and Investment (what does entry cost?). '
        'STRUCTURE: Market opportunity (size, growth) → Potential share (customers, competitors) → Potential profit → Capabilities & risks.'
    ),
    'new-product': (
        'The New Product framework — "Should we launch a new product?" '
        'USE WHEN: the prompt asks about product launches, new product lines, product diversification, or R&D decisions. '
        'IMPLIES: you\'re studying Growth → Volume → Revenue → Profitability. The chain tells you: '
        'we need more profit → via more revenue → via more volume → via a NEW offering customers can buy. '
        'NEXT: Almost always triggers Pricing ("what do we charge?") and Investment ("what does development cost?"). '
        'STRUCTURE: Choose target segments → Define 4P strategy (Product, Price, Distribution, Promotion) → Implementation plan.'
    ),
    'm-and-a': (
        'The M&A framework — "Should we acquire this company?" '
        'USE WHEN: the prompt asks about mergers, acquisitions, or any "should we buy this business?" question. '
        'IMPLIES: you\'re studying Growth → Volume → Revenue → Profitability — but through the INORGANIC path. '
        'Instead of building growth organically (Market Entry, New Product), you\'re buying it. '
        'NEXT: Connects to Investment (valuation, break-even) and Cost Reduction (synergies on the cost side). '
        'STRUCTURE: Standalone value (future revenue, costs, multiples) → Synergies (cost + revenue) → Capabilities & risks.'
    ),
    'process-optimization': (
        'The Process Optimization framework — "How to optimize this process?" '
        'USE WHEN: the prompt asks about improving operations, fixing a bottleneck, reducing waste, or increasing throughput. '
        'IMPLIES: you\'re studying Cost Reduction → Costs → Profitability. You\'ve already identified WHAT costs to cut; '
        'now you\'re zooming into the operational HOW — mapping the process, finding inefficiencies, and fixing them. '
        'This is the deepest "zoom-in" on the cost side of the map. '
        'STRUCTURE: Map current process (capacity, utilization, bottleneck) → Analyze each step (eliminate, anticipate) → Estimate gains (cost, quality, speed).'
    ),
}

count = 0
for key, new_insight in NEW_INSIGHTS.items():
    # Find: insight: "OLD TEXT",
    # in the FWM_DATA object
    import re
    # Match insight property for this key's block
    # Pattern: after the key's label/chain, find insight: "..."
    # Use a non-greedy match for the insight string
    pattern = rf'(          {re.escape(key)}:\s*\{{[^}}]*?insight:\s*")([^"]*?)(")'
    # Actually this won't work because the key might have quotes and the block spans multiple lines
    # Let me use a simpler approach: find the exact old insight text and replace it
    pass

# Simpler approach: find each insight string by searching for the key pattern in FWM_DATA
# The format is:   key: {  label: "...", chain: [...], insight: "OLD TEXT", tree: ...
# So I'll search for: insight: "OLD" within each block

for key, new_insight in NEW_INSIGHTS.items():
    # Find the block for this key in FWM_DATA
    # The insight line looks like: insight: "some text here",
    # We need to find it specifically within the right block
    
    # Strategy: find the key's block start, then find the insight within it
    if key == 'profitability':
        search_key = 'profitability:'
    elif key == 'fixed-costs':
        search_key = '"fixed-costs":'
    elif key == 'variable-costs':
        search_key = '"variable-costs":'
    elif key == 'competitive-response':
        search_key = '"competitive-response":'
    elif key == 'cost-reduction':
        search_key = '"cost-reduction":'
    elif key == 'market-entry':
        search_key = '"market-entry":'
    elif key == 'new-product':
        search_key = '"new-product":'
    elif key == 'm-and-a':
        search_key = '"m-and-a":'
    elif key == 'process-optimization':
        search_key = '"process-optimization":'
    else:
        search_key = key + ':'
    
    # Find the block start (within FWM_DATA)
    fwm_start = html.index('var FWM_DATA = {')
    block_start = html.index(search_key, fwm_start)
    
    # Find the insight property within this block (before the next top-level key)
    insight_start = html.index('insight:', block_start)
    # Find the opening quote
    quote_start = html.index('"', insight_start)
    # Find the closing quote (handle escaped quotes)
    pos = quote_start + 1
    while pos < len(html):
        if html[pos] == '\\':
            pos += 2  # skip escaped char
            continue
        if html[pos] == '"':
            break
        pos += 1
    quote_end = pos
    
    old_insight = html[quote_start+1:quote_end]
    
    # Escape the new insight for JS string
    escaped_new = new_insight.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")
    
    html = html[:quote_start+1] + escaped_new + html[quote_end:]
    count += 1
    print(f"  ✅ {key}: replaced {len(old_insight)} chars → {len(escaped_new)} chars")

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nDone! Updated {count} insight texts.")
print(f"File size: {len(html)} chars")
