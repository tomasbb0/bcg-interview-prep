      // FRAMEWORK MAP — INLINE TREE DATA FOR GRAY BOX
      window.FWM_INLINE_TREE = {
        profitability: {
          label: "How to improve profits? / Como melhorar lucros?",
          subs: [
            { label: "Revenue / Receitas", hint: "Revenue = Volume × Price — how many units sold and at what price?",
              subs: [
                { label: "Volume / Volume", hint: "# of customers, frequency per customer, units per transaction, channel mix" },
                { label: "Price / Preço", hint: "list price, discounts, promotions, price per unit, FX effects, price mix" }
              ] },
            { label: "Costs / Custos", hint: "Cost = Fixed + Variable — what doesn't change vs what scales with output?",
              subs: [
                { label: "Fixed costs / Custos fixos", hint: "rent, salaries, insurance, depreciation, IT, licenses, interest, admin overhead" },
                { label: "Variable costs / Custos variáveis", hint: "raw materials, packaging, shipping, commissions, payment fees, energy per unit" }
              ] }
          ] },
        revenue: {
          label: "Revenue / Receitas",
          hint: "Revenue = Volume × Price — how many units sold and at what price?",
          subs: [
            { label: "Volume / Volume", hint: "# of customers, frequency per customer, units per transaction, channel mix" },
            { label: "Price / Preço", hint: "list price, discounts, promotions, price per unit, FX effects, price mix" }
          ] },
        costs: {
          label: "Costs / Custos",
          hint: "Cost = Fixed + Variable — what doesn't change vs what scales with output?",
          subs: [
            { label: "Fixed costs / Custos fixos", hint: "rent, salaries, insurance, depreciation, IT, licenses, interest, admin overhead" },
            { label: "Variable costs / Custos variáveis", hint: "raw materials, packaging, shipping, commissions, payment fees, energy per unit" }
          ] },
        volume: { label: "Volume / Volume", hint: "# of customers, frequency per customer, units per transaction, channel mix", subs: [] },
        price: { label: "Price / Preço", hint: "list price, discounts, promotions, price per unit, FX effects, price mix", subs: [] },
        "fixed-costs": { label: "Fixed costs / Custos fixos", hint: "rent, salaries, insurance, depreciation, IT, licenses, interest, admin overhead", subs: [] },
        "variable-costs": { label: "Variable costs / Custos variáveis", hint: "raw materials, packaging, shipping, commissions, payment fees, energy per unit", subs: [] },
        growth: {
          label: "How to grow a business? / Como crescer?",
          subs: [
            { label: "Grow the core business / Crescer no core",
              hint: "Expand what you already do — sell more to existing customers in existing markets",
              subs: [
                { label: "Grow across current segments / Crescer nos segmentos atuais",
                  hint: "improve product, enhance marketing, adjust pricing, increase retention, boost conversion",
                  subs: [
                    { label: "Better products / Melhores produtos", hint: "R&D, new features, higher quality, better UX, faster delivery, innovation pipeline" },
                    { label: "Improved marketing / Marketing melhorado", hint: "brand awareness, digital channels, content strategy, referral programs, CRM optimization" },
                    { label: "Competitive prices / Preços competitivos", hint: "benchmarking, volume discounts, loyalty rewards, freemium tiers, flexible payment plans" }
                  ] },
                { label: "Invest in fastest-growing segments / Investir nos de maior crescimento", hint: "identify fastest-growing segments, reallocate resources and investment toward them" }
              ] },
            { label: "Grow outside of the core / Crescer fora do core",
              hint: "Go beyond current scope — new products, new customer types, new business models",
              subs: [
                { label: "Sell new products to existing clients / Vender novos produtos a clientes atuais", hint: "cross-sell, upsell, bundle, add complementary products or services" },
                { label: "Use capabilities for new businesses / Usar capacidades para novos negócios", hint: "leverage capabilities into adjacent markets, partnerships, licensing, JVs" }
              ] }
          ] },
        "cost-reduction": {
          label: "How to cut costs? / Como reduzir custos?",
          subs: [
            { label: "Reduce the need / Reduzir a necessidade",
              hint: "Can we stop doing this entirely or reduce how much is needed?",
              subs: [
                { label: "Eliminate the need entirely / Eliminar totalmente", hint: "remove unnecessary steps, sunset low-value activities, automate fully, outsource entirely" },
                { label: "Reduce the service level / Reduzir o nível de serviço", hint: "offer lower-cost tiers, reduce frequency, shift to self-service, simplify specifications" }
              ] },
            { label: "Meet the need with less resource / Cumprir com menos recursos",
              hint: "Can we do the same thing using fewer resources?",
              subs: [
                { label: "Eliminate waste / Eliminar desperdício", hint: "reduce rework, minimize idle time, cut scrap/defects, lean processes, remove duplication" },
                { label: "Improve productivity / Melhorar produtividade", hint: "upskill staff, invest in tools/technology, optimize workflows, increase throughput per FTE" }
              ] },
            { label: "Reduce the cost of resources / Reduzir o custo dos recursos",
              hint: "Can we get the same resources for less money?",
              subs: [
                { label: "Find cheaper alternatives / Encontrar alternativas mais baratas", hint: "alternative suppliers, substitute materials, offshore/nearshore, open-source solutions" },
                { label: "Renegotiate costs / Renegociar custos", hint: "volume discounts, longer-term contracts, competitive bidding, renegotiate payment terms" }
              ] }
          ] },
        pricing: {
          label: "How to price a product? / Como definir o preço?",
          subs: [
            { label: "Costs / Custos", hint: "Floor: minimum price to cover all costs and earn a margin",
              subs: [
                { label: "Variable costs / Custos variáveis", hint: "unit COGS, raw materials, packaging, shipping, commissions, transaction fees" },
                { label: "Fixed costs / Custos fixos", hint: "rent, salaries, insurance, depreciation, overhead — allocated per unit" },
                { label: "Investment costs / Custos de investimento", hint: "R&D, tooling, setup, marketing launch spend — amortized over expected volume" },
                { label: "Plus enough markup / Margem suficiente", hint: "target gross margin %, contribution margin, breakeven volume analysis" }
              ] },
            { label: "Competitors or substitutes / Concorrentes ou substitutos",
              hint: "Benchmark: how are alternatives and substitutes priced?",
              subs: [
                { label: "Price above or below? / Fixar acima ou abaixo?", hint: "premium vs discount positioning, feature comparison, brand perception, segment" }
              ] },
            { label: "Clients' willingness to pay / Disposição a pagar", hint: "Ceiling: maximum the customer will pay for the value delivered", subs: [] }
          ] },
        "competitive-response": {
          label: "How to respond to a competitive threat? / Como responder a uma ameaça?",
          subs: [
            { label: "Potential impact / Impacto potencial", hint: "How much of our business is actually at risk?",
              subs: [
                { label: "Segment affected / Segmento afetado", hint: "which customer groups, geographies, or product lines are most exposed" },
                { label: "Size / Dimensão", hint: "revenue at risk in affected segment, % of total business" },
                { label: "Profitability / Rentabilidade", hint: "margin on the affected segment — high-margin segments hurt most" },
                { label: "Estimated loss / Perda estimada", hint: "expected % of customers/revenue lost, over what timeframe" }
              ] },
            { label: "Opportunity pursued by competitor / Oportunidade do concorrente", hint: "What exactly is the competitor doing — and what's their advantage?", subs: [] },
            { label: "Possible responses / Respostas possíveis", hint: "What are our realistic response options — and which is smartest?",
              subs: [
                { label: "Do nothing / Não fazer nada", hint: "absorb the impact, focus resources elsewhere, let competitor overextend" },
                { label: "Mitigate / Mitigar", hint: "loyalty programs, better service, contract extensions, relationship management" },
                { label: "Replicate / Replicar", hint: "match competitor's product, launch own version, fast-follow strategy" },
                { label: "Collaborate / Colaborar", hint: "partnership, joint venture, licensing, referral arrangement" },
                { label: "Align / Alinhar (baixar preços)", hint: "price match, selective discounts, value bundles, promotional offers" }
              ] }
          ] },
        investment: {
          label: "Whether to make an investment? / Devemos investir?",
          subs: [
            { label: "Revenue impact / Impacto nas receitas", hint: "additional volume × price from the investment" },
            { label: "Cost impact / Impacto nos custos", hint: "savings generated minus new costs incurred" },
            { label: "Break even / Ponto de equilíbrio", hint: "investment ÷ annual net benefit → years, plus NPV and IRR" },
            { label: "Implementation / Implementação", hint: "capabilities needed, timeline, change management, risk factors" }
          ] },
        "market-entry": {
          label: "Whether to enter a new market? / Devemos entrar num novo mercado?",
          subs: [
            { label: "Market opportunity / Oportunidade de mercado", hint: "Is the market big enough and growing?",
              subs: [
                { label: "Market size / Dimensão do mercado", hint: "TAM/SAM/SOM, units × price, current size, historical growth rate" },
                { label: "Market growth / Crescimento do mercado", hint: "growth rate %, demand drivers, secular trends, regulatory tailwinds/headwinds" }
              ] },
            { label: "Potential share / Quota potencial", hint: "Can we realistically win customers against existing players?",
              subs: [
                { label: "Customer needs / Necessidades dos clientes", hint: "unmet needs, pain points, willingness to switch, decision criteria" },
                { label: "Our offering / A nossa oferta", hint: "differentiation, value proposition vs incumbents, product-market fit" },
                { label: "Competitors / Concorrentes", hint: "# of players, market shares, strengths/weaknesses, barriers to entry" }
              ] },
            { label: "Potential profit / Lucro potencial", hint: "Will the economics work — can we make money here?",
              subs: [
                { label: "Investment / Investimento", hint: "capex required, working capital, setup costs, time to build, go-to-market spend" },
                { label: "Running costs / Custos operacionais", hint: "opex, cost to serve, supply chain, distribution, support, compliance" },
                { label: "Revenue / Receitas", hint: "pricing model, revenue per customer, expected volume, ramp-up timeline, breakeven" }
              ] },
            { label: "Capabilities & risks / Capacidades e riscos", hint: "Do we have the skills and can we manage the risks?", subs: [] }
          ] },
        "new-product": {
          label: "How to launch a new product? / Como lançar um novo produto?",
          subs: [
            { label: "Choose target segments / Escolher segmentos-alvo", hint: "Which customer groups to target, and why those?",
              subs: [
                { label: "Size & growth / Dimensão e crescimento", hint: "segment size, growth rate, addressable market, willingness to pay" },
                { label: "Competition / Concorrência", hint: "existing solutions, competitive intensity, market gaps, substitutes" },
                { label: "Customer needs / Necessidades dos clientes", hint: "pain points, jobs-to-be-done, desired features, buying criteria" }
              ] },
            { label: "Define marketing strategy / Definir estratégia 4P", hint: "What should the 4P marketing mix look like?",
              subs: [
                { label: "Product / Produto", hint: "features, design, quality, MVP scope, differentiation from alternatives" },
                { label: "Price / Preço", hint: "cost-plus, value-based, competitive, tiered, freemium, subscription" },
                { label: "Distribution / Distribuição", hint: "online vs offline, direct vs partners, channel strategy, logistics" },
                { label: "Promotion / Promoção", hint: "go-to-market plan, advertising, content marketing, PR, sales force" }
              ] },
            { label: "Implementation / Implementação", hint: "What's needed to build, execute, and deliver?",
              subs: [
                { label: "Product design / Design do produto", hint: "R&D, prototyping, user testing, iteration cycles, regulatory approvals" },
                { label: "Production / Produção", hint: "manufacturing or development, sourcing, capacity planning, quality control" },
                { label: "Marketing & sales / Marketing e vendas", hint: "launch campaign, sales enablement, channel activation, demos and trials" },
                { label: "Logistics / Logística", hint: "warehousing, fulfillment, delivery, inventory management, returns handling" },
                { label: "Aftercare / Pós-venda", hint: "customer support, warranties, maintenance, upgrades, community, feedback" }
              ] }
          ] },
        "m-and-a": {
          label: "Whether to acquire a business? / Devemos adquirir?",
          subs: [
            { label: "Standalone value / Valor autónomo", hint: "What is the target worth on its own? (DCF, multiples, asset value)",
              subs: [
                { label: "Future revenue / Receitas futuras", hint: "revenue trend, growth rate, customer base, market position, contract pipeline" },
                { label: "Future cost / Custos futuros", hint: "cost structure, margin trajectory, expected efficiencies, risks to cost base" },
                { label: "Valuation multiples / Múltiplos", hint: "EV/EBITDA, P/E, revenue multiples, comparable deals, premium over market price" }
              ] },
            { label: "Synergies / Sinergias", hint: "What extra value does combining create? (cost + revenue synergies)",
              subs: [
                { label: "Cost reduction / Redução de custos", hint: "eliminate duplicates (HQ, IT, back-office), procurement savings, shared services" },
                { label: "Revenue growth / Crescimento de receitas", hint: "cross-sell to combined base, enter new markets, bundled offerings, pricing power" }
              ] },
            { label: "Capabilities & risks / Capacidades e riscos", hint: "Can we actually make it work? (integration, culture, regulatory risk)", subs: [] }
          ] },
        "process-optimization": {
          label: "How to optimize a process? / Como otimizar um processo?",
          subs: [
            { label: "Map out current process / Mapear o processo atual", hint: "What does the process look like today — where's the constraint?",
              subs: [
                { label: "Capacity? / Capacidade?", hint: "max throughput (units/day, cases/hour), theoretical vs practical capacity" },
                { label: "Utilization? / Utilização?", hint: "actual vs capacity, idle time, peak vs off-peak variation, resource allocation" },
                { label: "Bottleneck? / Gargalo?", hint: "slowest step, longest queue, highest wait time, constraining resource, SPOF" }
              ] },
            { label: "Look into each step / Analisar cada etapa", hint: "For each step: can we cut it, speed it up, or redesign it?",
              subs: [
                { label: "Eliminate / Eliminar", hint: "remove non-value-adding steps, cut handoffs, delete redundant approvals, automate" },
                { label: "Anticipate / Antecipar", hint: "pre-process, batch, schedule ahead, predictive triggers, parallel processing" }
              ] },
            { label: "Estimate gains / Estimar ganhos", hint: "What's the potential upside — in cost, quality, or speed?",
              subs: [
                { label: "Reduce cost / Reduzir custo", hint: "cost per unit processed, labor savings, material savings, overhead reduction" },
                { label: "Increase quality / Aumentar qualidade", hint: "error rate, defect rate, rework rate, customer satisfaction, accuracy %" },
                { label: "Increase speed / Aumentar velocidade", hint: "cycle time, lead time, throughput time, response time, time-to-delivery" }
              ] }
          ] }
      };

      window.fwmRenderInlineTree = function (node, depth) {
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
      };

