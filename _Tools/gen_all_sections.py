#!/usr/bin/env python3
"""
Generate all replacement sections for the BCG prep HTML.
All content EN/PT bilingual. Incorporates CaseCoach PDF data.
"""
import os

BASE = os.path.join(os.path.dirname(__file__), "..", "0_ACTIVE_NOW", "BCG_Interview_Prep")
SECTIONS_DIR = os.path.join(BASE, "sections")
os.makedirs(SECTIONS_DIR, exist_ok=True)

# ═══════════════════════════════════════════════════════════════
# 1. CASE EXAMPLES (from Case-structuring-in-action.pdf)
# Insert AFTER frameworks, BEFORE math
# ═══════════════════════════════════════════════════════════════
case_examples = '''
        <!-- CASE STRUCTURING IN ACTION -->
        <h2>📋 Case Structuring in Action / Estruturação na Prática</h2>
        <p style="color: var(--text-muted); margin-bottom: 16px">7 example structures from CaseCoach / 7 estruturas exemplo do CaseCoach</p>

        <div class="collapsible" onclick="toggleCollapsible(this)">
          🍫 Simple Snack Bar — Pricing / Precificação
        </div>
        <div class="collapsible-content">
          <p><strong>Q:</strong> Friend created allergen-free snack bar. Help determine the right price. / Amigo criou barra sem alergénios. Ajudar a definir o preço.</p>
          <ol>
            <li><strong>Target segments / Segmentos-alvo</strong>
              <ul>
                <li>a. Corporate clients (airlines, schools) liable for reactions / Clientes corporativos responsáveis por reações</li>
                <li>b. Parents buying for children / Pais a comprar para crianças</li>
                <li>c. Adults buying for themselves / Adultos a comprar para si</li>
              </ul>
            </li>
            <li><strong>Price of competitors / Preço dos concorrentes</strong> (direct + indirect e.g. fresh fruit)</li>
            <li><strong>Perceived value vs alternatives / Valor percebido vs alternativas</strong> + potential markup</li>
            <li><strong>Costs / Custos</strong></li>
          </ol>
          <div class="card card-accent"><strong>Why?</strong> Based on 3 pricing factors (competitors, willingness to pay, costs). Starts with target clients since undecided. / Baseado nos 3 fatores de pricing. Começa por target porque não está definido.</div>
        </div>

        <div class="collapsible" onclick="toggleCollapsible(this)">
          🌊 Splash Park — Profitability / Rentabilidade
        </div>
        <div class="collapsible-content">
          <p><strong>Q:</strong> Water park in Majorca wants to increase profitability. / Parque aquático em Maiorca quer aumentar rentabilidade.</p>
          <ol>
            <li><strong>Increase revenue / Aumentar receitas</strong>
              <ul>
                <li>a. Increase # clients / Aumentar nº clientes: capacity (hours, new rides) + demand (promotions, channels)</li>
                <li>b. Increase spend per client / Aumentar gasto por cliente: prices, add-ons (VIP, restaurants)</li>
              </ul>
            </li>
            <li><strong>Decrease costs / Reduzir custos</strong>
              <ul>
                <li>a. Decrease service level / Reduzir nível de serviço</li>
                <li>b. Do same with less / Fazer igual com menos (identify waste / identificar desperdício)</li>
                <li>c. Reduce input costs / Reduzir custos de input</li>
              </ul>
            </li>
          </ol>
          <div class="card card-accent"><strong>Why?</strong> Standard profitability but 3rd-level drivers tailored to water park. Volume is supply/demand issue. / Profitability standard mas drivers adaptados ao parque aquático.</div>
        </div>

        <div class="collapsible" onclick="toggleCollapsible(this)">
          ☀️ Sunshine Vacations — Turnaround
        </div>
        <div class="collapsible-content">
          <p><strong>Q:</strong> Package holiday provider lost 10% bookings. CEO wants turnaround. / Operador turístico perdeu 10% reservas. CEO quer recuperação.</p>
          <ol>
            <li><strong>Focus on most profitable offers / Focar nas ofertas mais rentáveis</strong> — reduce least-, increase most-profitable</li>
            <li><strong>Increase profitability across all / Aumentar rentabilidade geral</strong> — demand, pricing, costs</li>
            <li><strong>Invest in growth opportunities / Investir em oportunidades de crescimento</strong> — UK packages? Lower cost destinations? Cruises? Specialized holidays?</li>
          </ol>
          <div class="card card-accent"><strong>Why?</strong> Product mix drives overall profitability. Start with portfolio before individual P&L. / O mix de produtos determina a rentabilidade. Começar pelo portfólio antes do P&L individual.</div>
        </div>

        <div class="collapsible" onclick="toggleCollapsible(this)">
          🏙️ Bristol Valley — Government / Governo
        </div>
        <div class="collapsible-content">
          <p><strong>Q:</strong> Bristol wants to become Silicon Valley of UK. What does the council need to do? / Bristol quer ser o Silicon Valley do UK.</p>
          <ol>
            <li><strong>Identify target technologies / Identificar tecnologias-alvo</strong> — trends, university strengths, employer strengths</li>
            <li><strong>Strengthen the ecosystem / Fortalecer o ecossistema</strong>
              <ul>
                <li>Universities / Universidades — research funding, students / financiamento investigação</li>
                <li>Employers / Empregadores — R&D centers / centros I&D</li>
                <li>Funding / Financiamento — venture funds, investor networks / fundos venture, redes de investidores</li>
                <li>Entrepreneurs / Empreendedores — incubation, training, workspace / incubação, formação, espaço</li>
              </ul>
            </li>
            <li><strong>Improve location attractiveness / Melhorar atratividade do local</strong> — transport, accommodation / transportes, alojamento</li>
          </ol>
        </div>

        <div class="collapsible" onclick="toggleCollapsible(this)">
          🏛️ Social Return Capital — Market Analysis / Análise de Mercado
        </div>
        <div class="collapsible-content">
          <p><strong>Q:</strong> Why hasn't social investment fund received more investment? / Por que não recebeu mais investimento?</p>
          <ol>
            <li><strong>Lack of supply / Falta de oferta</strong> — limited need from social enterprises, not enough enterprises, lack of asset managers</li>
            <li><strong>Lack of demand / Falta de procura</strong> — investors don't know/care, insufficient returns, unfavorable tax</li>
            <li><strong>Lack of intermediation / Falta de intermediação</strong> — intermediaries don't distribute/know/promote</li>
          </ol>
          <div class="card card-accent"><strong>Why?</strong> Root cause analysis using supply/demand + intermediation. / Análise causa-raiz usando oferta/procura + intermediação.</div>
        </div>

        <div class="collapsible" onclick="toggleCollapsible(this)">
          🏦 Milna Bank — Process / Processo
        </div>
        <div class="collapsible-content">
          <p><strong>Q:</strong> Mortgage applications up but completions down. Why? / Candidaturas hipoteca subiram mas completadas desceram.</p>
          <ol>
            <li><strong>Quality of applications / Qualidade das candidaturas</strong> — credit-worthiness declining, wages vs property prices</li>
            <li><strong>Our process / O nosso processo</strong> — burdensome → abandoned, slow offers</li>
            <li><strong>Our approval rules / As nossas regras de aprovação</strong></li>
            <li><strong>Competitiveness of offers / Competitividade das ofertas</strong> — rates, features, brand</li>
          </ol>
          <div class="card card-accent"><strong>Why?</strong> Root cause analysis following application steps. / Análise causa-raiz seguindo as etapas da candidatura.</div>
        </div>'''

with open(os.path.join(SECTIONS_DIR, "case_examples.html"), "w", encoding="utf-8") as f:
    f.write(case_examples)
print(f"Case examples: {case_examples.count(chr(10))} lines")


# ═══════════════════════════════════════════════════════════════
# 2. MATH SECTION (updated with Estimations PDF + EN/PT)
# ═══════════════════════════════════════════════════════════════
math_section = '''      <div class="section" id="math">
        <div class="section-title">🔢 Math & Estimations / Matemática e Estimativas</div>
        <div class="section-subtitle">
          Formulas, mental math, market sizing — EN/PT Bilingual
        </div>

        <h2>📏 Market Sizing & Estimations / Dimensionamento de Mercado</h2>

        <div class="collapsible" onclick="toggleCollapsible(this)">
          Top-Down vs Bottom-Up (CaseCoach)
        </div>
        <div class="collapsible-content">
          <table>
            <thead><tr><th></th><th>Top-Down</th><th>Bottom-Up</th></tr></thead>
            <tbody>
              <tr>
                <td><strong>Approach / Abordagem</strong></td>
                <td>Break down a large number (market, population) / Decompor um número grande (mercado, população)</td>
                <td>Extrapolate a small number (observation, locality) / Extrapolar um número pequeno (observação, local)</td>
              </tr>
              <tr>
                <td><strong>Pros / Vantagens</strong></td>
                <td>Gets to right order of magnitude / Ordem de grandeza correta</td>
                <td>Very tangible / Muito tangível. Great for sanity checks / Ótimo para verificação</td>
              </tr>
              <tr>
                <td><strong>Cons / Desvantagens</strong></td>
                <td>Intangible / Intangível</td>
                <td>Small mistakes are magnified / Pequenos erros são amplificados</td>
              </tr>
            </tbody>
          </table>
          <div class="card card-accent"><strong>Bottom-up is the preferred approach / Bottom-up é a abordagem preferida</strong></div>
        </div>

        <div class="collapsible" onclick="toggleCollapsible(this)">
          🔄 The Replacement Method / Método de Substituição
        </div>
        <div class="collapsible-content">
          <p>For products that are replaced periodically / Para produtos substituídos periodicamente:</p>
          <div class="formula">
            Sales = Stock ÷ Lifetime + Growth / Vendas = Stock ÷ Vida útil + Crescimento
          </div>
          <p><strong>Example / Exemplo:</strong> Cars sold in US / Carros vendidos nos EUA</p>
          <ul class="tree-list">
            <li><strong># Cars sold / # Carros vendidos</strong>
              <ul>
                <li><span class="tree-branch">To maintain current stock / Para manter stock atual</span>
                  <ul>
                    <li># Cars in US / # Carros nos EUA</li>
                    <li>Lifetime of a car / Vida útil do carro</li>
                  </ul>
                </li>
                <li><span class="tree-branch">To increase stock / Para aumentar stock</span></li>
              </ul>
            </li>
          </ul>
        </div>

        <div class="collapsible" onclick="toggleCollapsible(this)">
          📊 Segmentation Technique / Técnica de Segmentação
        </div>
        <div class="collapsible-content">
          <p><strong>Example / Exemplo:</strong> Number of cars per household / Número de carros por família</p>
          <table>
            <thead><tr><th># Cars / Carros</th><th>0</th><th>1</th><th>2</th><th>3</th><th>Total / Média</th></tr></thead>
            <tbody>
              <tr><td><strong>% of households / % famílias</strong></td><td>10%</td><td>50%</td><td>30%</td><td>10%</td><td>100%</td></tr>
              <tr><td><strong>Weighted / Ponderado</strong></td><td>0.0</td><td>0.5</td><td>0.6</td><td>0.3</td><td><strong>1.4</strong></td></tr>
            </tbody>
          </table>
        </div>

        <div class="collapsible" onclick="toggleCollapsible(this)">
          🌍 Key Numbers to Know / Números-Chave a Saber
        </div>
        <div class="collapsible-content">
          <h4>World & Major Countries / Mundo e Países Principais</h4>
          <table>
            <thead><tr><th>Country / País</th><th>Population / População</th></tr></thead>
            <tbody>
              <tr><td>World / Mundo</td><td>~8 billion / mil milhões</td></tr>
              <tr><td>US / EUA</td><td>330M (~300M)</td></tr>
              <tr><td>China</td><td>1.4B (~1.5B)</td></tr>
              <tr><td>India / Índia</td><td>1.4B (~1.5B)</td></tr>
              <tr><td>Germany / Alemanha</td><td>83M (~80M)</td></tr>
              <tr><td>UK / Reino Unido</td><td>67M (~70M)</td></tr>
              <tr><td>Portugal</td><td>~10.3M</td></tr>
            </tbody>
          </table>
          <h4>US Demographics & Economics / Demografia e Economia EUA</h4>
          <table>
            <tbody>
              <tr><td>Life expectancy / Esperança de vida</td><td>~80 years / anos</td></tr>
              <tr><td>People per household / Pessoas por família</td><td>2.5</td></tr>
              <tr><td>GDP per capita / PIB per capita</td><td>$70,000</td></tr>
              <tr><td>Median individual income / Rendimento mediano individual</td><td>$50,000</td></tr>
              <tr><td>Median household income / Rendimento mediano familiar</td><td>$75,000</td></tr>
              <tr><td>Work hours per year / Horas trabalho por ano</td><td>~2,000</td></tr>
            </tbody>
          </table>
          <h4>Portugal Reference Numbers / Números de Referência Portugal</h4>
          <table>
            <tbody>
              <tr><td>Population / População</td><td>~10.3M</td></tr>
              <tr><td>GDP / PIB</td><td>~€260B / mil milhões</td></tr>
              <tr><td>GDP per capita / PIB per capita</td><td>~€25,000</td></tr>
              <tr><td>Average salary / Salário médio</td><td>~€1,400 gross / bruto</td></tr>
              <tr><td>Households / Famílias</td><td>~4M</td></tr>
              <tr><td>Lisbon metro / Lisboa metro</td><td>~3M</td></tr>
              <tr><td>Porto metro</td><td>~1.7M</td></tr>
              <tr><td>Tourists per year / Turistas por ano</td><td>~25-30M</td></tr>
            </tbody>
          </table>
        </div>

        <h2>📐 Core Formulas / Fórmulas Essenciais</h2>

        <div class="collapsible" onclick="toggleCollapsible(this)">
          1. Breakeven / Ponto de Equilíbrio
        </div>
        <div class="collapsible-content">
          <div class="formula">
            BE (units) = Fixed Costs ÷ (Price − Variable Cost per Unit)<br>
            BE (unidades) = Custos Fixos ÷ (Preço − Custo Variável por Unidade)<br><br>
            Contribution Margin / Margem de Contribuição = Price − Variable Cost / Preço − CV
          </div>
          <div class="card card-accent">
            <strong>Example / Exemplo:</strong> FC=€100K, Price/Preço=€50, VC/CV=€30 → BE = 100,000÷20 = <strong>5,000 units / unidades</strong>
          </div>
        </div>

        <div class="collapsible" onclick="toggleCollapsible(this)">
          2. Payback Period / Período de Retorno
        </div>
        <div class="collapsible-content">
          <div class="formula">Payback = Initial Investment ÷ Annual Cash Flow / Investimento Inicial ÷ Fluxo de Caixa Anual</div>
          <div class="card card-accent"><strong>Example:</strong> Investment=€500K, Annual CF=€125K → <strong>4 years / anos</strong></div>
        </div>

        <div class="collapsible" onclick="toggleCollapsible(this)">
          3. ROI (Return on Investment)
        </div>
        <div class="collapsible-content">
          <div class="formula">ROI = (Gain − Investment) ÷ Investment × 100% / (Ganho − Investimento) ÷ Investimento × 100%</div>
          <div class="card card-accent"><strong>Example:</strong> Invested €200K, gained €280K → ROI = (280−200)÷200 = <strong>40%</strong></div>
        </div>

        <div class="collapsible" onclick="toggleCollapsible(this)">
          4. Margins / Margens
        </div>
        <div class="collapsible-content">
          <div class="formula">
            Gross Margin / Margem Bruta = (Revenue − COGS) ÷ Revenue<br>
            Operating Margin / Margem Operacional = EBIT ÷ Revenue / Receita<br>
            Net Margin / Margem Líquida = Net Profit ÷ Revenue / Lucro Líquido ÷ Receita<br>
            Contribution Margin / Margem de Contribuição = (Price − VC) ÷ Price / (Preço − CV) ÷ Preço
          </div>
          <table>
            <thead><tr><th>Ratio / Rácio</th><th>Benchmark</th></tr></thead>
            <tbody>
              <tr><td>Gross Margin / Margem Bruta</td><td>Retail 30-40%, Tech 60-80%, Services 40-60%</td></tr>
              <tr><td>EBITDA Margin</td><td>15-25% (good / bom)</td></tr>
              <tr><td>Net Margin / Margem Líquida</td><td>10-20% (good / bom)</td></tr>
            </tbody>
          </table>
        </div>

        <div class="collapsible" onclick="toggleCollapsible(this)">
          5. Growth & CAGR / Crescimento e CAGR
        </div>
        <div class="collapsible-content">
          <div class="formula">Growth / Crescimento = (Final − Initial) ÷ Initial × 100%<br>CAGR = (Final ÷ Initial)^(1/n) − 1</div>
          <h4>Rule of 72 / Regra dos 72:</h4>
          <p>72 ÷ growth rate = years to double / anos para duplicar</p>
          <table>
            <tbody>
              <tr><td>7% growth / crescimento</td><td>→ doubles in ~10 years / duplica em ~10 anos</td></tr>
              <tr><td>10%</td><td>→ ~7 years / anos</td></tr>
              <tr><td>15%</td><td>→ ~5 years / anos</td></tr>
            </tbody>
          </table>
        </div>

        <div class="collapsible" onclick="toggleCollapsible(this)">
          6. NPV / VAL + CLV/CAC + Market Share / Quota de Mercado
        </div>
        <div class="collapsible-content">
          <div class="formula">
            NPV / VAL = Σ [CF_t ÷ (1 + r)^t] − Initial Investment / Investimento Inicial<br><br>
            CLV = Avg Revenue × Margin × Retention Time / Receita Média × Margem × Tempo Retenção<br>
            CAC = Total Marketing+Sales Cost ÷ # New Customers / Custo Total Marketing+Vendas ÷ # Novos Clientes<br>
            Healthy ratio / Rácio saudável: CLV/CAC > 3<br><br>
            Market Share / Quota de Mercado = Company Sales ÷ Market Sales / Vendas Empresa ÷ Vendas Mercado<br><br>
            Elasticity / Elasticidade = % Change Quantity ÷ % Change Price / % Variação Quantidade ÷ % Variação Preço<br>
            |E| > 1: Elastic / Elástico (price-sensitive) &nbsp; |E| < 1: Inelastic / Inelástico
          </div>
        </div>

        <h2>🧮 Mental Math Shortcuts / Atalhos de Cálculo Mental</h2>
        <div class="card">
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px">
            <div>
              <h4>Percentages / Percentagens</h4>
              <div class="formula" style="font-size: 13px">
                10% = ÷10 &nbsp; 5% = ÷20 &nbsp; 1% = ÷100<br>
                15% = 10%+5% &nbsp; 20% = ÷5 &nbsp; 25% = ÷4<br>
                33% = ÷3 &nbsp; 50% = ÷2 &nbsp; 75% = X − 25%
              </div>
            </div>
            <div>
              <h4>Multiplication / Multiplicação</h4>
              <div class="formula" style="font-size: 13px">
                ×5 = ×10 ÷ 2 &nbsp; ×15 = ×10 + ×5<br>
                ×25 = ×100 ÷ 4 &nbsp; ×50 = ×100 ÷ 2<br>
                ×1.1 = ×1 + 10%
              </div>
            </div>
          </div>
          <h4>Strategic Rounding / Arredondamento Estratégico</h4>
          <p>RULE: Always round to simplify. Adjust after if needed. / REGRA: Arredondar SEMPRE. Ajustar depois.</p>
          <p><span class="kbd">397 → 400</span> &nbsp; <span class="kbd">1,243 → 1,250</span> &nbsp; <span class="kbd">€4.7M → €5M</span></p>
        </div>

        <h2>💡 Math Tips During the Case / Dicas de Math no Caso</h2>
        <div class="card card-accent">
          <ol>
            <li><strong>Round first, adjust after / Arredondar primeiro, ajustar depois:</strong> "I'll round to simplify... 397 ≈ 400" / "Vou arredondar... 397 ≈ 400"</li>
            <li><strong>Think aloud / Falar em voz alta:</strong> "5M ÷ 200K units gives us €25 per unit" / "5M ÷ 200K unidades dá-nos €25"</li>
            <li><strong>Sanity check:</strong> "€25/unit for a premium product seems reasonable" / "€25/unidade para premium parece razoável"</li>
            <li><strong>State implications / Dizer implicações:</strong> After every calculation / Após cada cálculo</li>
          </ol>
        </div>
      </div>'''

with open(os.path.join(SECTIONS_DIR, "math_new.html"), "w", encoding="utf-8") as f:
    f.write(math_section)
print(f"Math section: {math_section.count(chr(10))} lines")


# ═══════════════════════════════════════════════════════════════
# 3. DRILLS SECTION (add CaseCoach drill types + keep existing)
# ═══════════════════════════════════════════════════════════════
drills_header = '''      <div class="section" id="drills">
        <div class="section-title">🧮 Drills</div>
        <div class="section-subtitle">
          CaseCoach 6 Drill Categories + Math Exercises — EN/PT
        </div>

        <div class="card card-accent" style="margin-bottom: 24px">
          <h3>⚡ CaseCoach Drill Categories / Categorias de Drills CaseCoach</h3>
          <p>Practice these daily on the platform / Praticar diariamente na plataforma:</p>
          <table>
            <thead><tr><th>#</th><th>Category / Categoria</th><th>Description / Descrição</th><th>Target / Objetivo</th></tr></thead>
            <tbody>
              <tr><td>1</td><td><strong>Structures / Estruturas</strong></td><td>Build MECE structures for case prompts / Construir estruturas MECE</td><td>5-10 per session / por sessão</td></tr>
              <tr><td>2</td><td><strong>Calculations / Cálculos</strong></td><td>Mental math speed drills / Cálculo mental rápido</td><td>15-30 sec each / seg cada</td></tr>
              <tr><td>3</td><td><strong>Case Math</strong></td><td>Full case math problems / Problemas de math de caso completos</td><td>2-3 min each / min cada</td></tr>
              <tr><td>4</td><td><strong>Market Sizing</strong></td><td>Bottom-up and top-down estimations / Estimativas bottom-up e top-down</td><td>5 min each / min cada</td></tr>
              <tr><td>5</td><td><strong>Charts / Gráficos</strong></td><td>Interpret exhibits and extract insights / Interpretar exhibits e extrair insights</td><td>2-3 min each / min cada</td></tr>
              <tr><td>6</td><td><strong>Creativity / Criatividade</strong></td><td>Brainstorm ideas in structured buckets / Brainstorming em categorias estruturadas</td><td>2 min each / min cada</td></tr>
            </tbody>
          </table>
        </div>

        <h2>📊 Chart Types / Tipos de Gráfico (from CaseCoach)</h2>
        <div class="collapsible" onclick="toggleCollapsible(this)">
          How to Identify Insights / Como Identificar Insights
        </div>
        <div class="collapsible-content">
          <table>
            <thead><tr><th>Objective / Objetivo</th><th>Chart Types / Tipos de Gráfico</th><th>Characteristics / Características</th></tr></thead>
            <tbody>
              <tr><td><strong>Comparison / Comparação</strong></td><td>Bar charts, Harvey balls</td><td>Several data series against same axis / Várias séries no mesmo eixo</td></tr>
              <tr><td><strong>Composition / Composição</strong></td><td>Pie chart, Waterfall, Mekko, Area chart, Stacked bar</td><td>A total broken into components / Total decomposto em componentes</td></tr>
              <tr><td><strong>Distribution / Distribuição</strong></td><td>Bar chart, Line chart</td><td>How many times an event occurs / Frequência de ocorrências</td></tr>
              <tr><td><strong>Trend / Tendência</strong></td><td>Line chart, Dual axis</td><td>Time as an axis / Tempo como eixo</td></tr>
              <tr><td><strong>Relationship / Relação</strong></td><td>Scatter plot, Bubble chart</td><td>At least 3 dimensions / Pelo menos 3 dimensões</td></tr>
            </tbody>
          </table>
        </div>

        <h2>🔢 Math Exercises / Exercícios de Math</h2>'''

with open(os.path.join(SECTIONS_DIR, "drills_header.html"), "w", encoding="utf-8") as f:
    f.write(drills_header)
print(f"Drills header: {drills_header.count(chr(10))} lines")


# ═══════════════════════════════════════════════════════════════
# 4. BCG PATTERNS — Updated scoring rubric from scorecards
# ═══════════════════════════════════════════════════════════════
scoring_rubric = '''
        <h2>📋 CaseCoach Scoring Rubric / Rubrica de Avaliação (1-3-5)</h2>
        <div class="card">
          <table>
            <thead><tr><th>Dimension / Dimensão</th><th>1 (Below / Abaixo)</th><th>3 (Meets Standard / Cumpre)</th><th>5 (Stands Out / Destaca-se)</th></tr></thead>
            <tbody>
              <tr>
                <td><strong>Structuring / Estruturação</strong></td>
                <td>Did not offer clear structure / Não apresentou estrutura clara</td>
                <td>Clarified ambiguity; MECE set of independent drivers / Clarificou ambiguidades; fatores MECE independentes</td>
                <td>Prioritized steps; shared helpful insights / Passos priorizados; partilhou insights úteis</td>
              </tr>
              <tr>
                <td><strong>Math</strong></td>
                <td>Made mistakes, needed help / Erros, precisou de ajuda</td>
                <td>Calculated correctly and confidently; stated implications / Calculou corretamente e com confiança; declarou implicações</td>
                <td>Clear efficient approach; calculated particularly quickly / Abordagem clara e eficiente; calculou muito rapidamente</td>
              </tr>
              <tr>
                <td><strong>Judgement & Insights / Julgamento e Insights</strong></td>
                <td>Missed key insights / Perdeu insights-chave</td>
                <td>Connected findings to develop sound recommendations / Ligou achados para recomendações sólidas</td>
                <td>Processed info quickly; shared deep insights and far-reaching implications / Processou info rapidamente; insights profundos</td>
              </tr>
              <tr>
                <td><strong>Creativity / Criatividade</strong></td>
                <td>Struggled to generate ideas / Dificuldade em gerar ideias</td>
                <td>Shared numerous, varied and sound ideas / Partilhou ideias numerosas, variadas e sólidas</td>
                <td>Exceptional creativity in structured way / Criatividade excecional de forma estruturada</td>
              </tr>
              <tr>
                <td><strong>Synthesis / Síntese</strong></td>
                <td>No clear recommendation / Sem recomendação clara</td>
                <td>Supported recommendation with key points + next steps / Recomendação apoiada em pontos-chave + próximos passos</td>
                <td>Particularly convincing / Particularmente convincente</td>
              </tr>
              <tr>
                <td><strong>Case Leadership / Liderança de Caso</strong></td>
                <td>Appeared passive or lost / Pareceu passivo ou perdido</td>
                <td>Built on findings; stayed focused; made reasonable assumptions / Construiu sobre achados; focado; pressupostos razoáveis</td>
                <td>Progressed quickly; asked probing questions; adapted approach / Avançou rapidamente; perguntas incisivas; adaptou abordagem</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h2>🤝 Fit Scorecard / Rubrica Fit (1-3-5)</h2>
        <div class="card">
          <table>
            <thead><tr><th>Dimension / Dimensão</th><th>1</th><th>3</th><th>5</th></tr></thead>
            <tbody>
              <tr>
                <td><strong>Rapport-building</strong></td>
                <td>Failed to set stage / Não iniciou bem</td>
                <td>Maintained fluid back-and-forth / Conversa fluida</td>
                <td>Made personal connection; authentic; revealed unique traits / Conexão pessoal; autêntico</td>
              </tr>
              <tr>
                <td><strong>Performance Track Record / Histórico</strong></td>
                <td>Did not demonstrate top performance / Não demonstrou performance</td>
                <td>Provided evidence of top performance / Provou alta performance</td>
                <td>Presented demanding environment; not boastful / Ambiente exigente; sem se gabar</td>
              </tr>
              <tr>
                <td><strong>Transferable Abilities / Capacidades Transferíveis</strong></td>
                <td>Did not demonstrate target abilities / Não demonstrou capacidades</td>
                <td>Showed ambition, initiative, persistence, adaptability, leadership, teamwork, persuasion / Mostrou ambição, iniciativa, persistência, adaptabilidade, liderança, trabalho em equipa, persuasão</td>
                <td>Impressive achievements; detailed own actions and thought process / Feitos impressionantes; detalhou ações e raciocínio</td>
              </tr>
              <tr>
                <td><strong>Motivation / Motivação</strong></td>
                <td>No good reason for pursuing this / Sem boa razão</td>
                <td>Convincing rationale for consulting + this firm / Racional convincente para consultoria + esta firma</td>
                <td>Explained in personal terms; evidence of self-development / Explicou pessoalmente; prova de autodesenvolvimento</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h2>✨ General Impression / Impressão Geral (both scorecards / ambas as rubricas)</h2>
        <div class="card">
          <table>
            <thead><tr><th>Dimension / Dimensão</th><th>1</th><th>3</th><th>5</th></tr></thead>
            <tbody>
              <tr>
                <td><strong>Presence / Presença</strong></td>
                <td>Was not professional / Não foi profissional</td>
                <td>Professional, engaging, energetic and confident / Profissional, envolvente, energético e confiante</td>
                <td>Built genuine rapport; positive personality; expert-like credibility / Rapport genuíno; personalidade positiva; credibilidade de especialista</td>
              </tr>
              <tr>
                <td><strong>Communication / Comunicação</strong></td>
                <td>Unclear and scattered / Pouco claro e disperso</td>
                <td>Listened well; spoke precisely and concisely / Ouviu bem; falou precisa e concisamente</td>
                <td>Particularly organized; main idea before details; communicated visually / Muito organizado; ideia principal primeiro; comunicou visualmente</td>
              </tr>
            </tbody>
          </table>
        </div>'''

with open(os.path.join(SECTIONS_DIR, "scoring_rubric.html"), "w", encoding="utf-8") as f:
    f.write(scoring_rubric)
print(f"Scoring rubric: {scoring_rubric.count(chr(10))} lines")


# ═══════════════════════════════════════════════════════════════
# 5. PORTUGUESE TERMS — Updated header to EN/PT
# Already has good bilingual structure, just update subtitle
# ═══════════════════════════════════════════════════════════════

print("\nAll section files generated in:", SECTIONS_DIR)
print("Ready for insertion into index.html")
