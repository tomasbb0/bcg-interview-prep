#!/usr/bin/env python3
"""Inject academic & logical framework pills into the Framework Map."""

import pathlib, sys

ROOT = pathlib.Path(__file__).parent
HTML = ROOT / "index.html"

src = HTML.read_text(encoding="utf-8")

# Guard
if "fwm-n-supply-demand" in src:
    print("Academic pills already present — skipping")
    sys.exit(0)

# ── Step 1: Add new pill rows after Row 4 (before the closing </div> of the map) ──

# The map ends with </div> right after the Row 4 block
# Find the marker after the last row
MARKER_END_MAP = """        </div>

        <!-- Expandable framework panel (shows on click) -->"""

NEW_ROWS = """
          <!-- DIVIDER: Academic Frameworks -->
          <div style="width:100%;text-align:center;margin:18px 0 6px;padding-top:10px;border-top:2px dashed #bbb;">
            <span style="font-size:0.85em;font-weight:700;color:#666;letter-spacing:1px;">📚 ACADEMIC FRAMEWORKS / FRAMEWORKS ACADÉMICOS</span>
          </div>

          <!-- ROW 5: Supply & Demand / Three Cs / Porter's Five Forces / Four Ps -->
          <div class="fwm-row" style="gap:14px">
            <div class="fwm-pill" id="fwm-n-supply-demand" data-en="📊 Supply &amp; Demand" data-pt="📊 Oferta e Procura" data-fwm="supply-demand" style="background:#e3f2fd;color:#1565c0;border-color:#1565c0;font-size:12px;">📊 Supply &amp; Demand</div>
            <div class="fwm-pill" id="fwm-n-three-cs" data-en="🔺 Three Cs" data-pt="🔺 Três Cs" data-fwm="three-cs" style="background:#fce4ec;color:#c62828;border-color:#c62828;font-size:12px;">🔺 Three Cs</div>
            <div class="fwm-pill" id="fwm-n-porters-five" data-en="⭐ Porter's 5 Forces" data-pt="⭐ 5 Forças de Porter" data-fwm="porters-five" style="background:#fff8e1;color:#f57f17;border-color:#f57f17;font-size:12px;">⭐ Porter's 5 Forces</div>
            <div class="fwm-pill" id="fwm-n-four-ps" data-en="🎯 Four Ps" data-pt="🎯 Quatro Ps" data-fwm="four-ps" style="background:#f3e5f5;color:#7b1fa2;border-color:#7b1fa2;font-size:12px;">🎯 Four Ps</div>
          </div>

          <!-- DIVIDER: Logical Structures -->
          <div style="width:100%;text-align:center;margin:18px 0 6px;padding-top:10px;border-top:2px dashed #bbb;">
            <span style="font-size:0.85em;font-weight:700;color:#666;letter-spacing:1px;">🧩 LOGICAL STRUCTURES / ESTRUTURAS LÓGICAS</span>
          </div>

          <!-- ROW 6: 6 Logical Structures -->
          <div class="fwm-row fwm-row-wide" style="gap:12px">
            <div class="fwm-pill" id="fwm-n-equations" data-en="🔢 Equations" data-pt="🔢 Equações" data-fwm="equations" style="background:#e8eaf6;color:#283593;border-color:#283593;font-size:11px;">🔢 Equations</div>
            <div class="fwm-pill" id="fwm-n-key-questions" data-en="❓ Key Questions" data-pt="❓ Questões-chave" data-fwm="key-questions" style="background:#e0f2f1;color:#00695c;border-color:#00695c;font-size:11px;">❓ Key Questions</div>
            <div class="fwm-pill" id="fwm-n-hypotheses" data-en="🧪 Hypotheses" data-pt="🧪 Hipóteses" data-fwm="hypotheses" style="background:#fff3e0;color:#e65100;border-color:#e65100;font-size:11px;">🧪 Hypotheses</div>
            <div class="fwm-pill" id="fwm-n-root-causes" data-en="🔍 Root Causes" data-pt="🔍 Causas-raiz" data-fwm="root-causes" style="background:#fce4ec;color:#ad1457;border-color:#ad1457;font-size:11px;">🔍 Root Causes</div>
            <div class="fwm-pill" id="fwm-n-process-map" data-en="🗺️ Process Map" data-pt="🗺️ Mapa de Processo" data-fwm="process-map" style="background:#efebe9;color:#4e342e;border-color:#4e342e;font-size:11px;">🗺️ Process Map</div>
            <div class="fwm-pill" id="fwm-n-from-to" data-en="➡️ From-To" data-pt="➡️ De-Para" data-fwm="from-to" style="background:#e8f5e9;color:#2e7d32;border-color:#2e7d32;font-size:11px;">➡️ From-To</div>
          </div>
"""

if MARKER_END_MAP not in src:
    sys.exit("ERROR: cannot find end-of-map marker")

src = src.replace(MARKER_END_MAP, NEW_ROWS + "\n" + MARKER_END_MAP, 1)
print("Injected academic + logical pill rows")

# ── Step 2: Add FWM_DATA entries for new pills ──

MARKER_FWM_DATA_END = """        var currentFwmNode = null;"""

NEW_FWM_DATA = """
        // Academic & Logical framework data
        FWM_DATA["supply-demand"] = {
          label: "📊 Supply & Demand",
          chain: ["Supply & Demand"],
          insight: "Classic economics framework. USE WHEN: the case involves price changes, market equilibria, commodity markets, or operations capacity vs. demand. Think about shifts in supply curve (cost changes, new entrants, regulation) and demand curve (income, preferences, substitutes). Key: find equilibrium price/quantity, then analyze what shifts the curves.",
          tree: null
        };
        FWM_DATA["three-cs"] = {
          label: "🔺 Three Cs",
          chain: ["Three Cs"],
          insight: "Company–Competitors–Customers. USE WHEN: you need a quick external/internal scan to understand competitive positioning. Company = our strengths, capabilities, costs. Competitors = who else plays, their share, strategy, advantages. Customers = needs, segments, willingness to pay, switching costs. Pairs well with Market Entry and Competitive Response.",
          tree: { root: "Three Cs", branches: [
            { name: "Company / Empresa", children: ["Capabilities / Capacidades", "Cost structure / Estrutura de custos", "Brand & reputation / Marca e reputação"] },
            { name: "Competitors / Concorrentes", children: ["Market share / Quota de mercado", "Strategy / Estratégia", "Strengths & weaknesses / Forças e fraquezas"] },
            { name: "Customers / Clientes", children: ["Needs & pain points / Necessidades", "Segments / Segmentos", "Willingness to pay / Disposição a pagar"] }
          ] }
        };
        FWM_DATA["porters-five"] = {
          label: "⭐ Porter's Five Forces",
          chain: ["Porter's Five Forces"],
          insight: "Industry attractiveness analysis. USE WHEN: evaluating whether to enter a market, assessing industry profitability, or understanding competitive dynamics. Five forces: (1) Rivalry among existing competitors, (2) Bargaining power of buyers, (3) Bargaining power of suppliers, (4) Threat of substitutes, (5) Threat of new entrants. High forces = lower industry profitability.",
          tree: { root: "Five Forces / 5 Forças", branches: [
            { name: "Rivalry / Rivalidade", children: ["# of competitors", "Industry growth rate", "Product differentiation", "Switching costs", "Exit barriers"] },
            { name: "Buyer Power / Poder dos Compradores", children: ["Concentration", "Switching costs", "Price sensitivity", "Backward integration threat"] },
            { name: "Supplier Power / Poder dos Fornecedores", children: ["Concentration", "Uniqueness of input", "Switching costs", "Forward integration threat"] },
            { name: "Substitutes / Substitutos", children: ["Availability", "Price-performance", "Switching costs"] },
            { name: "New Entrants / Novos Entrantes", children: ["Capital requirements", "Economies of scale", "Brand loyalty", "Regulatory barriers", "Access to distribution"] }
          ] }
        };
        FWM_DATA["four-ps"] = {
          label: "🎯 Four Ps",
          chain: ["Four Ps (Marketing Mix)"],
          insight: "Marketing mix framework. USE WHEN: launching a new product, defining go-to-market strategy, or analyzing why a product is underperforming. Product = features, quality, design. Price = pricing strategy, discounts, value perception. Place = distribution channels, coverage, logistics. Promotion = advertising, sales force, PR, digital marketing. Overlaps with New Product framework.",
          tree: { root: "Four Ps / Quatro Ps", branches: [
            { name: "Product / Produto", children: ["Features / Características", "Quality / Qualidade", "Design / Design", "Branding / Marca"] },
            { name: "Price / Preço", children: ["Pricing strategy / Estratégia de preço", "Discounts / Descontos", "Value perception / Perceção de valor"] },
            { name: "Place / Distribuição", children: ["Channels / Canais", "Coverage / Cobertura", "Logistics / Logística", "Online vs Offline"] },
            { name: "Promotion / Promoção", children: ["Advertising / Publicidade", "Sales force / Força de vendas", "PR / Relações públicas", "Digital marketing / Marketing digital"] }
          ] }
        };
        FWM_DATA["equations"] = {
          label: "🔢 Equations",
          chain: ["Logical Structure: Equations"],
          insight: "Structure type for QUANTITATIVE questions. USE WHEN: the answer requires a number — profit, breakeven, market size, ROI. Start by writing the equation (e.g., Profit = Revenue − Costs, Revenue = Volume × Price). Then decompose each variable. This is the most common logical structure in case interviews. Always try to express the problem as an equation first.",
          tree: null
        };
        FWM_DATA["key-questions"] = {
          label: "❓ Key Questions",
          chain: ["Logical Structure: Key Questions"],
          insight: "Structure type for QUALITATIVE decisions. USE WHEN: there is no single formula and you need to evaluate multiple criteria. List 3-5 key questions that, if answered, would resolve the decision. Example: Should we acquire company X? → (1) Is the standalone value attractive? (2) Are there meaningful synergies? (3) Can we integrate successfully? (4) What are the risks?",
          tree: null
        };
        FWM_DATA["hypotheses"] = {
          label: "🧪 Hypotheses",
          chain: ["Logical Structure: Hypotheses"],
          insight: "Structure type for QUALITATIVE decisions with a testable thesis. USE WHEN: you have a directional belief and need to prove/disprove it. State your hypothesis, then list the conditions that must be TRUE for the hypothesis to hold. Example: 'We should enter market X IF (1) market size > $500M, (2) we can achieve 10%+ share in 3 years, (3) expected margins > 15%.'",
          tree: null
        };
        FWM_DATA["root-causes"] = {
          label: "🔍 Root Causes",
          chain: ["Logical Structure: Root Causes"],
          insight: "Structure type for ISSUE INVESTIGATIONS. USE WHEN: something went wrong and you need to find out why. Think 'fishbone diagram' or '5 Whys'. List all possible root causes, then systematically test each. Group causes into categories (people, process, technology, external). Always ask: is this the root cause, or a symptom of something deeper?",
          tree: null
        };
        FWM_DATA["process-map"] = {
          label: "🗺️ Process Map",
          chain: ["Logical Structure: Process Map"],
          insight: "Structure type for OPERATIONS optimization. USE WHEN: the case involves a sequence of steps, a value chain, or a workflow. Map out the process end-to-end, then identify bottlenecks, waste, and improvement opportunities at each step. Example: Attraction → Screening → Selection → Offer → Onboarding. Works perfectly with the Process Optimization framework (#10).",
          tree: null
        };
        FWM_DATA["from-to"] = {
          label: "➡️ From-To",
          chain: ["Logical Structure: From-To"],
          insight: "Structure type for REACHING A FUTURE STATE. USE WHEN: the case is about transformation, change management, or strategic planning. Define: (1) Where are we now? (current state), (2) Where do we want to be? (target state), (3) What is the gap? (4) What initiatives close the gap? Example: digital transformation, turnaround, org restructuring.",
          tree: null
        };

"""

if MARKER_FWM_DATA_END not in src:
    sys.exit("ERROR: cannot find currentFwmNode marker")

src = src.replace(MARKER_FWM_DATA_END, NEW_FWM_DATA + MARKER_FWM_DATA_END, 1)
print("Injected FWM_DATA entries for academic/logical frameworks")

# ── Step 3: Add FWM_INLINE_TREE entries for new pills ──

MARKER_INLINE_END = "      window.fwmRenderInlineTree = function"

NEW_INLINE = """        "supply-demand": {
          label: "Supply & Demand / Oferta e Procura",
          hint: "Where is the equilibrium? What shifts the curves?",
          subs: [
            { label: "Supply-side / Lado da oferta", hint: "production costs, number of producers, technology, regulation, input prices",
              subs: [
                { label: "Cost changes / Alterações de custo", hint: "raw material prices, labor costs, energy, logistics, tariffs" },
                { label: "Capacity / Capacidade", hint: "new entrants, factory expansion, exits, supply chain disruptions" }
              ] },
            { label: "Demand-side / Lado da procura", hint: "income levels, consumer preferences, substitutes, demographics, seasonality",
              subs: [
                { label: "Willingness to pay / Disposição a pagar", hint: "brand value, perceived quality, urgency, alternatives" },
                { label: "Market size / Dimensão do mercado", hint: "population, income, adoption rate, frequency of purchase" }
              ] },
            { label: "Equilibrium / Equilíbrio", hint: "where supply = demand, price clearing point, surplus/shortage" }
          ] },
        "three-cs": {
          label: "Three Cs / Três Cs",
          hint: "Company, Competitors, Customers — a quick competitive scan",
          subs: [
            { label: "Company / Empresa", hint: "strengths, capabilities, cost structure, brand, resources, strategy" },
            { label: "Competitors / Concorrentes", hint: "market share, strategies, strengths vs weaknesses, likely responses" },
            { label: "Customers / Clientes", hint: "needs, segments, willingness to pay, switching costs, decision criteria" }
          ] },
        "porters-five": {
          label: "Porter's Five Forces / 5 Forças de Porter",
          hint: "How attractive is this industry? Higher forces = lower profitability",
          subs: [
            { label: "Rivalry / Rivalidade", hint: "# competitors, growth rate, differentiation, switching costs, exit barriers" },
            { label: "Buyer power / Poder dos compradores", hint: "concentration, switching costs, price sensitivity, backward integration" },
            { label: "Supplier power / Poder dos fornecedores", hint: "concentration, uniqueness, switching costs, forward integration" },
            { label: "Substitutes / Substitutos", hint: "availability, price-performance, switching costs" },
            { label: "New entrants / Novos entrantes", hint: "capital requirements, economies of scale, brand loyalty, regulation, distribution" }
          ] },
        "four-ps": {
          label: "Four Ps / Quatro Ps (Marketing Mix)",
          hint: "Product, Price, Place, Promotion — the marketing strategy toolkit",
          subs: [
            { label: "Product / Produto", hint: "features, quality, design, branding, packaging, lifecycle, differentiation" },
            { label: "Price / Preço", hint: "cost-plus, value-based, competitive, tiered, freemium, discounts" },
            { label: "Place / Distribuição", hint: "channels (online/offline), coverage, logistics, partnerships, DTC vs wholesale" },
            { label: "Promotion / Promoção", hint: "advertising, sales force, PR, digital marketing, content, referrals, events" }
          ] },
        "equations": {
          label: "Equations / Equações",
          hint: "Express the problem as a formula, then decompose each variable",
          subs: [
            { label: "Profit = Revenue − Costs", hint: "the fundamental equation — always start here for profitability cases" },
            { label: "Revenue = Volume × Price", hint: "decompose volume (customers × frequency × units) and price (list − discounts)" },
            { label: "Breakeven = Fixed Costs ÷ (Price − Variable Cost)", hint: "units needed to cover all fixed costs" },
            { label: "Market Size = Population × Adoption × Frequency × Price", hint: "bottom-up sizing approach" },
            { label: "ROI = Net Benefit ÷ Investment", hint: "or NPV, IRR for time-value analysis" }
          ] },
        "key-questions": {
          label: "Key Questions / Questões-chave",
          hint: "List 3-5 questions that, if answered, resolve the decision",
          subs: [
            { label: "What is the objective?", hint: "clarify what success looks like — revenue, profit, market share, strategic positioning" },
            { label: "What are the options?", hint: "enumerate the realistic alternatives (do nothing is always an option)" },
            { label: "What criteria matter?", hint: "financial return, strategic fit, risk, feasibility, timeline, stakeholder impact" },
            { label: "What evidence decides?", hint: "for each criterion, what data or analysis would tip the decision" }
          ] },
        "hypotheses": {
          label: "Hypotheses / Hipóteses",
          hint: "State a directional belief, then list conditions that must hold",
          subs: [
            { label: "Formulate hypothesis", hint: "'We should do X IF conditions A, B, C are true'" },
            { label: "List conditions / Listar condições", hint: "each condition is testable — market size, capabilities, margins, risk level" },
            { label: "Test each condition", hint: "gather data/analysis to confirm or refute each condition" },
            { label: "Conclude", hint: "if all conditions hold → proceed; if any fails → reject or modify hypothesis" }
          ] },
        "root-causes": {
          label: "Root Causes / Causas-raiz",
          hint: "Something went wrong — find out why (fishbone / 5 Whys)",
          subs: [
            { label: "People / Pessoas", hint: "skills gaps, understaffing, training, motivation, leadership, turnover" },
            { label: "Process / Processo", hint: "bottlenecks, missing steps, handoff errors, outdated procedures, lack of automation" },
            { label: "Technology / Tecnologia", hint: "system failures, outdated tools, integration issues, data quality" },
            { label: "External / Externo", hint: "regulation changes, market shifts, supplier issues, competitive actions, macro events" }
          ] },
        "process-map": {
          label: "Process Map / Mapa de Processo",
          hint: "Map the end-to-end process, find bottlenecks and waste at each step",
          subs: [
            { label: "Step 1: Map current state", hint: "draw the full process chain from input to output, including all handoffs" },
            { label: "Step 2: Identify bottleneck", hint: "which step has the longest wait, lowest throughput, or highest error rate?" },
            { label: "Step 3: Analyze each step", hint: "value-add vs non-value-add, can it be eliminated, automated, or parallelized?" },
            { label: "Step 4: Redesign", hint: "propose improved process, estimate time/cost savings, implementation plan" }
          ] },
        "from-to": {
          label: "From-To / De-Para",
          hint: "Define current state, target state, gap, and initiatives to close it",
          subs: [
            { label: "Current state / Estado atual", hint: "where are we now? metrics, capabilities, performance, market position" },
            { label: "Target state / Estado-alvo", hint: "where do we want to be? vision, KPIs, benchmarks, timeline" },
            { label: "Gap analysis / Análise do gap", hint: "what's the delta? in revenue, capability, market share, technology, talent" },
            { label: "Initiatives / Iniciativas", hint: "what actions close the gap? prioritize by impact vs feasibility, create roadmap" }
          ] },
"""

if MARKER_INLINE_END not in src:
    sys.exit("ERROR: cannot find fwmRenderInlineTree marker")

src = src.replace(MARKER_INLINE_END, NEW_INLINE + "\n" + MARKER_INLINE_END, 1)
print("Injected FWM_INLINE_TREE entries for academic/logical frameworks")

# ── Step 4: Add PT translations for new pills to FWM_PT ──

MARKER_PT_END = """      window.fwmSetLang = function"""

NEW_PT = """        // Academic & Logical framework translations
        window.FWM_PT["supply-demand"] = "📊 Oferta e Procura";
        window.FWM_PT["three-cs"] = "🔺 Três Cs";
        window.FWM_PT["porters-five"] = "⭐ 5 Forças de Porter";
        window.FWM_PT["four-ps"] = "🎯 Quatro Ps";
        window.FWM_PT["equations"] = "🔢 Equações";
        window.FWM_PT["key-questions"] = "❓ Questões-chave";
        window.FWM_PT["hypotheses"] = "🧪 Hipóteses";
        window.FWM_PT["root-causes"] = "🔍 Causas-raiz";
        window.FWM_PT["process-map"] = "🗺️ Mapa de Processo";
        window.FWM_PT["from-to"] = "➡️ De-Para";

"""

if MARKER_PT_END not in src:
    print("WARNING: Could not find FWM_PT marker — PT translations not injected")
else:
    src = src.replace(MARKER_PT_END, NEW_PT + MARKER_PT_END, 1)
    print("Injected PT translations for academic/logical pills")

HTML.write_text(src, encoding="utf-8")
print(f"Done — wrote {len(src):,} chars to {HTML.name}")
