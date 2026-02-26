#!/usr/bin/env python3
"""Generate the replacement HTML for the Frameworks section based on CaseCoach PDFs.
All content is EN/PT bilingual. CaseCoach Top 10 frameworks + Academic + Logical."""

# ═══════════════════════════════════════════════════════════════
# TOP 10 CASE FRAMEWORKS (from CaseCoach PDF)
# ═══════════════════════════════════════════════════════════════

frameworks_html = '''      <div class="section" id="frameworks">
        <div class="section-title">📐 Frameworks</div>
        <div class="section-subtitle">
          Top 10 CaseCoach Frameworks + Academic + Logical — EN/PT Bilingual
        </div>

        <!-- AIM TEST -->
        <div class="card card-accent" style="margin-bottom: 24px">
          <h3>🎯 The AIM Test / O Teste AIM</h3>
          <p style="margin-bottom: 12px">Every structure must pass all 3 / Toda a estrutura deve passar nos 3:</p>
          <table>
            <thead>
              <tr><th></th><th>English</th><th>Português</th></tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>A</strong></td>
                <td><strong>Answer-focused</strong> — Focus on the right question; provide a prioritized approach to solving it</td>
                <td><strong>Focado na resposta</strong> — Foca na pergunta certa; abordagem priorizada para a resolver</td>
              </tr>
              <tr>
                <td><strong>I</strong></td>
                <td><strong>Insightful</strong> — Tailor structure to the client's specific situation</td>
                <td><strong>Perspicaz</strong> — Adaptar a estrutura à situação específica do cliente</td>
              </tr>
              <tr>
                <td><strong>M</strong></td>
                <td><strong>MECE</strong> — Break down into an exhaustive set of independent drivers</td>
                <td><strong>MECE</strong> — Dividir num conjunto exaustivo de fatores independentes</td>
              </tr>
            </tbody>
          </table>
          <div class="card card-danger" style="margin-top: 12px">
            <strong>TIP:</strong> Only ask questions that help you structure. Don't restate the whole brief. / Só faz perguntas que ajudem a estruturar. Não repitas todo o briefing.
          </div>
        </div>

        <!-- HOW TO BUILD A STRUCTURE -->
        <div class="collapsible" onclick="toggleCollapsible(this)">
          🔨 How to Build a Structure / Como Construir uma Estrutura
        </div>
        <div class="collapsible-content">
          <table>
            <thead><tr><th>Step</th><th>English</th><th>Português</th></tr></thead>
            <tbody>
              <tr>
                <td><strong>1</strong></td>
                <td>Break down into first-level drivers</td>
                <td>Dividir em fatores de primeiro nível</td>
              </tr>
              <tr>
                <td><strong>2</strong></td>
                <td>Order the 1st level drivers by priority</td>
                <td>Ordenar por prioridade</td>
              </tr>
              <tr>
                <td><strong>3</strong></td>
                <td>Add depth and insights</td>
                <td>Adicionar profundidade e insights</td>
              </tr>
            </tbody>
          </table>
          <h4 style="margin-top: 16px">Two approaches / Duas abordagens:</h4>
          <table>
            <thead><tr><th>Top-Down</th><th>Bottom-Up</th></tr></thead>
            <tbody>
              <tr>
                <td>Break down the problem into components / Decompor o problema em componentes<br>Leverage the 20+ frameworks / Usar os 20+ frameworks</td>
                <td>Generate ideas that could solve the question / Gerar ideias que possam resolver a questão<br>Group these ideas into factors / Agrupar ideias em fatores</td>
              </tr>
              <tr>
                <td>Requires the right logical approach / Requer abordagem lógica</td>
                <td>Requires the right insights / Requer os insights certos</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- HOW TO COMMUNICATE -->
        <div class="collapsible" onclick="toggleCollapsible(this)">
          🗣️ How to Communicate Your Structure / Como Comunicar a Estrutura
        </div>
        <div class="collapsible-content">
          <div class="card card-accent">
            <h4>Step 1: List all drivers upfront / Listar todos os fatores à partida</h4>
            <blockquote>"There are three areas I'd consider. First... Second... Third..."<br>
            "Há três áreas que eu consideraria. Primeiro... Segundo... Terceiro..."</blockquote>
          </div>
          <div class="card card-accent" style="margin-top: 12px">
            <h4>Step 2: Signpost before detail / Sinalizar antes do detalhe</h4>
            <blockquote>"If I go to the first driver — [name] — I think the most important question is..."<br>
            "Se for ao primeiro fator — [nome] — a questão mais importante é..."</blockquote>
          </div>
        </div>

        <h2>🏆 Top 10 Case Frameworks (CaseCoach)</h2>

        <!-- 1. PROFITABILITY -->
        <div class="collapsible" onclick="toggleCollapsible(this)">
          💰 1. How to Improve Profits? / Como Melhorar Lucros?
        </div>
        <div class="collapsible-content">
          <ul class="tree-list">
            <li><strong>How to improve profits? / Como melhorar lucros?</strong>
              <ul>
                <li><span class="tree-branch">Revenue / Receitas</span>
                  <ul>
                    <li>Volume / Volume</li>
                    <li>Price / Preço</li>
                  </ul>
                </li>
                <li><span class="tree-branch">Costs / Custos</span>
                  <ul>
                    <li>Fixed costs / Custos fixos</li>
                    <li>Variable costs / Custos variáveis</li>
                  </ul>
                </li>
              </ul>
            </li>
          </ul>
          <blockquote>"To analyze profitability, I'd break it into revenue and costs. On revenue, I'd look at price and volume. On costs, I'd separate fixed and variable."<br>
          "Para analisar a rentabilidade, vou dividir em receitas e custos. Nas receitas, olho para preço e volume. Nos custos, separo fixos e variáveis."</blockquote>
        </div>

        <!-- 2. GROWTH -->
        <div class="collapsible" onclick="toggleCollapsible(this)">
          📈 2. How to Grow a Business? / Como Fazer Crescer um Negócio?
        </div>
        <div class="collapsible-content">
          <ul class="tree-list">
            <li><strong>How to grow a business? / Como crescer?</strong>
              <ul>
                <li><span class="tree-branch">Grow the core business / Crescer no core</span>
                  <ul>
                    <li>Grow across current segments / Crescer nos segmentos atuais
                      <ul>
                        <li>Better products / Melhores produtos</li>
                        <li>Improved marketing / Marketing melhorado</li>
                        <li>Competitive prices / Preços competitivos</li>
                      </ul>
                    </li>
                    <li>Invest in fastest-growing segments / Investir nos segmentos de maior crescimento</li>
                  </ul>
                </li>
                <li><span class="tree-branch">Grow outside of the core / Crescer fora do core</span>
                  <ul>
                    <li>Sell new products to existing clients / Vender novos produtos a clientes atuais</li>
                    <li>Use capabilities to get into new businesses / Usar capacidades para entrar em novos negócios</li>
                  </ul>
                </li>
              </ul>
            </li>
          </ul>
        </div>

        <!-- 3. CUT COSTS -->
        <div class="collapsible" onclick="toggleCollapsible(this)">
          📉 3. How to Cut Costs? / Como Reduzir Custos?
        </div>
        <div class="collapsible-content">
          <ul class="tree-list">
            <li><strong>How to cut costs? / Como reduzir custos?</strong>
              <ul>
                <li><span class="tree-branch">Reduce the need / Reduzir a necessidade</span>
                  <ul>
                    <li>Eliminate the need entirely / Eliminar totalmente a necessidade</li>
                    <li>Reduce the service level / Reduzir o nível de serviço</li>
                  </ul>
                </li>
                <li><span class="tree-branch">Meet the need with less resource / Cumprir com menos recursos</span>
                  <ul>
                    <li>Eliminate waste / Eliminar desperdício</li>
                    <li>Improve productivity / Melhorar produtividade</li>
                  </ul>
                </li>
                <li><span class="tree-branch">Reduce the cost of resources / Reduzir o custo dos recursos</span>
                  <ul>
                    <li>Find cheaper alternatives / Encontrar alternativas mais baratas</li>
                    <li>Renegotiate costs / Renegociar custos</li>
                  </ul>
                </li>
              </ul>
            </li>
          </ul>
          <p style="color: var(--text-muted)">Examples / Exemplos: Self-service portal / Portal self-service, Offshoring, Training / Formação</p>
        </div>

        <!-- 4. ENTER A NEW MARKET -->
        <div class="collapsible" onclick="toggleCollapsible(this)">
          🚀 4. Whether to Enter a New Market? / Devemos Entrar num Novo Mercado?
        </div>
        <div class="collapsible-content">
          <ul class="tree-list">
            <li><strong>Whether to enter? / Devemos entrar?</strong>
              <ul>
                <li><span class="tree-branch">Market opportunity / Oportunidade de mercado</span>
                  <ul>
                    <li>Market size / Dimensão do mercado</li>
                    <li>Market growth / Crescimento do mercado</li>
                  </ul>
                </li>
                <li><span class="tree-branch">Potential share / Quota potencial</span>
                  <ul>
                    <li>Customer needs / Necessidades dos clientes</li>
                    <li>Our offering / A nossa oferta</li>
                    <li>Competitors / Concorrentes</li>
                  </ul>
                </li>
                <li><span class="tree-branch">Potential profit / Lucro potencial</span>
                  <ul>
                    <li>Investment / Investimento</li>
                    <li>Running costs / Custos operacionais</li>
                    <li>Revenue / Receitas</li>
                  </ul>
                </li>
                <li><span class="tree-branch">Capabilities & risks / Capacidades e riscos</span></li>
              </ul>
            </li>
          </ul>
        </div>

        <!-- 5. LAUNCH NEW PRODUCT -->
        <div class="collapsible" onclick="toggleCollapsible(this)">
          🆕 5. How to Launch a New Product? / Como Lançar um Novo Produto?
        </div>
        <div class="collapsible-content">
          <ul class="tree-list">
            <li><strong>How to launch? / Como lançar?</strong>
              <ul>
                <li><span class="tree-branch">Choose target segments / Escolher segmentos-alvo</span>
                  <ul>
                    <li>Size & growth / Dimensão e crescimento</li>
                    <li>Competition / Concorrência</li>
                    <li>Customer needs / Necessidades dos clientes</li>
                  </ul>
                </li>
                <li><span class="tree-branch">Define marketing strategy / Definir estratégia de marketing</span>
                  <ul>
                    <li>Product / Produto</li>
                    <li>Price / Preço</li>
                    <li>Distribution / Distribuição</li>
                    <li>Promotion / Promoção</li>
                  </ul>
                </li>
                <li><span class="tree-branch">Implementation / Implementação</span>
                  <ul>
                    <li>Product design / Design do produto</li>
                    <li>Production / Produção</li>
                    <li>Marketing & sales / Marketing e vendas</li>
                    <li>Logistics / Logística</li>
                    <li>Aftercare / Pós-venda</li>
                  </ul>
                </li>
              </ul>
            </li>
          </ul>
        </div>

        <!-- 6. PRICING -->
        <div class="collapsible" onclick="toggleCollapsible(this)">
          🏷️ 6. How to Price a Product? / Como Definir o Preço?
        </div>
        <div class="collapsible-content">
          <ul class="tree-list">
            <li><strong>How to price? / Como precificar?</strong>
              <ul>
                <li><span class="tree-branch">Costs / Custos</span>
                  <ul>
                    <li>Variable costs / Custos variáveis</li>
                    <li>Fixed costs / Custos fixos</li>
                    <li>Investment costs / Custos de investimento</li>
                    <li>Plus enough markup to cover margin / Margem suficiente</li>
                  </ul>
                </li>
                <li><span class="tree-branch">Competitors or substitutes / Concorrentes ou substitutos</span>
                  <ul>
                    <li>Should we price above or below? / Devemos fixar acima ou abaixo?</li>
                  </ul>
                </li>
                <li><span class="tree-branch">Clients' willingness to pay / Disposição a pagar dos clientes</span></li>
              </ul>
            </li>
          </ul>
        </div>

        <!-- 7. INVESTMENT -->
        <div class="collapsible" onclick="toggleCollapsible(this)">
          💼 7. Whether to Make an Investment? / Devemos Investir?
        </div>
        <div class="collapsible-content">
          <ul class="tree-list">
            <li><strong>Whether to invest? / Devemos investir?</strong>
              <ul>
                <li><span class="tree-branch">Impact on revenue / Impacto nas receitas</span></li>
                <li><span class="tree-branch">Impact on costs / Impacto nos custos</span></li>
                <li><span class="tree-branch">Break even? / Ponto de equilíbrio?</span></li>
                <li><span class="tree-branch">Implementation / Implementação</span></li>
              </ul>
            </li>
          </ul>
        </div>

        <!-- 8. ACQUIRE A BUSINESS -->
        <div class="collapsible" onclick="toggleCollapsible(this)">
          🤝 8. Whether to Acquire a Business? / Devemos Adquirir?
        </div>
        <div class="collapsible-content">
          <ul class="tree-list">
            <li><strong>Whether to acquire? / Devemos adquirir?</strong>
              <ul>
                <li><span class="tree-branch">Standalone value / Valor autónomo</span>
                  <ul>
                    <li>Future revenue / Receitas futuras</li>
                    <li>Future cost / Custos futuros</li>
                    <li>Valuation multiples / Múltiplos de avaliação</li>
                  </ul>
                </li>
                <li><span class="tree-branch">Synergies / Sinergias</span>
                  <ul>
                    <li>Cost reduction / Redução de custos</li>
                    <li>Revenue growth / Crescimento de receitas</li>
                  </ul>
                </li>
                <li><span class="tree-branch">Capabilities & risks / Capacidades e riscos</span></li>
              </ul>
            </li>
          </ul>
        </div>

        <!-- 9. COMPETITIVE THREAT -->
        <div class="collapsible" onclick="toggleCollapsible(this)">
          ⚔️ 9. How to Respond to a Competitive Threat? / Como Responder a uma Ameaça Competitiva?
        </div>
        <div class="collapsible-content">
          <ul class="tree-list">
            <li><strong>How to respond? / Como responder?</strong>
              <ul>
                <li><span class="tree-branch">Potential impact on our business / Impacto potencial no nosso negócio</span>
                  <ul>
                    <li>Segment affected / Segmento afetado</li>
                    <li>Size / Dimensão</li>
                    <li>Profitability / Rentabilidade</li>
                    <li>Estimated loss / Perda estimada</li>
                  </ul>
                </li>
                <li><span class="tree-branch">Opportunity pursued by competitor / Oportunidade do concorrente</span></li>
                <li><span class="tree-branch">Possible responses / Respostas possíveis</span>
                  <ul>
                    <li>Do nothing / Não fazer nada</li>
                    <li>Mitigate (retain clients) / Mitigar (reter clientes)</li>
                    <li>Replicate (launch competing offer) / Replicar (lançar oferta concorrente)</li>
                    <li>Collaborate / Colaborar</li>
                    <li>Align (lower prices) / Alinhar (baixar preços)</li>
                  </ul>
                </li>
              </ul>
            </li>
          </ul>
        </div>

        <!-- 10. OPTIMIZE A PROCESS -->
        <div class="collapsible" onclick="toggleCollapsible(this)">
          ⚙️ 10. How to Optimize a Process? / Como Otimizar um Processo?
        </div>
        <div class="collapsible-content">
          <ul class="tree-list">
            <li><strong>How to optimize? / Como otimizar?</strong>
              <ul>
                <li><span class="tree-branch">Map out current process / Mapear o processo atual</span>
                  <ul>
                    <li>Capacity? / Capacidade?</li>
                    <li>Utilization? / Utilização?</li>
                    <li>Bottleneck? / Gargalo?</li>
                  </ul>
                </li>
                <li><span class="tree-branch">Look into each step / Analisar cada etapa</span>
                  <ul>
                    <li>Eliminate / Eliminar</li>
                    <li>Anticipate / Antecipar</li>
                  </ul>
                </li>
                <li><span class="tree-branch">Estimate gains / Estimar ganhos</span>
                  <ul>
                    <li>Reduce cost / Reduzir custo</li>
                    <li>Increase quality / Aumentar qualidade</li>
                    <li>Increase speed / Aumentar velocidade</li>
                  </ul>
                </li>
              </ul>
            </li>
          </ul>
        </div>

        <!-- SECOND-LEVEL DRIVERS -->
        <div class="collapsible" onclick="toggleCollapsible(this)">
          🔍 Second-Level Drivers to Think About / Fatores de Segundo Nível
        </div>
        <div class="collapsible-content">
          <table>
            <thead><tr><th>Category / Categoria</th><th>English</th><th>Português</th></tr></thead>
            <tbody>
              <tr><td><strong>Market / Mercado</strong></td><td>Geographies, Size & growth, Segments, Distribution channels, Customer segments</td><td>Geografias, Dimensão e crescimento, Segmentos, Canais de distribuição, Segmentos de clientes</td></tr>
              <tr><td><strong>Customers / Clientes</strong></td><td>Purchasing decision, Preferences, Substitutes</td><td>Decisão de compra, Preferências, Substitutos</td></tr>
              <tr><td><strong>Competition / Concorrência</strong></td><td>New entrants, Market shares, Profitability, Skills, Barriers to entry, Key success factors, Brand, Capital, Partners</td><td>Novos entrantes, Quotas de mercado, Rentabilidade, Competências, Barreiras à entrada, Fatores-chave de sucesso, Marca, Capital, Parceiros</td></tr>
              <tr><td><strong>Macro</strong></td><td>Regulation, Political issues, Economy, Unions, Technology, Execution</td><td>Regulação, Questões políticas, Economia, Sindicatos, Tecnologia, Execução</td></tr>
            </tbody>
          </table>
        </div>

        <h2>📚 Academic Frameworks / Frameworks Académicos</h2>

        <div class="collapsible" onclick="toggleCollapsible(this)">
          📊 Supply & Demand / Oferta e Procura
        </div>
        <div class="collapsible-content">
          <p>Price / Quantity equilibrium / Equilíbrio preço / quantidade</p>
          <p><strong>Helpful for / Útil para:</strong> Price changes / Alterações de preço, Profit forecasting / Previsão de lucro, Operations / Operações, Markets outside of business / Mercados fora do negócio</p>
        </div>

        <div class="collapsible" onclick="toggleCollapsible(this)">
          🔺 The Three Cs / Os Três Cs
        </div>
        <div class="collapsible-content">
          <ul class="tree-list">
            <li><strong>Three Cs</strong>
              <ul>
                <li><span class="tree-branch">Company / Empresa</span> (Supply / Oferta)</li>
                <li><span class="tree-branch">Competitors / Concorrentes</span> (Supply / Oferta)</li>
                <li><span class="tree-branch">Customers / Clientes</span> (Demand / Procura)</li>
              </ul>
            </li>
          </ul>
        </div>

        <div class="collapsible" onclick="toggleCollapsible(this)">
          ⭐ Porter's Five Forces / As 5 Forças de Porter
        </div>
        <div class="collapsible-content">
          <p><strong>Helpful for understanding industry attractiveness / Útil para entender a atratividade de uma indústria</strong></p>
          <ul class="tree-list">
            <li><strong>Five Forces / 5 Forças</strong>
              <ul>
                <li><span class="tree-branch">Competitors / Concorrentes</span></li>
                <li><span class="tree-branch">Customers / Clientes</span></li>
                <li><span class="tree-branch">Suppliers / Fornecedores</span></li>
                <li><span class="tree-branch">Substitutes / Substitutos</span></li>
                <li><span class="tree-branch">New Entrants / Novos Entrantes</span></li>
              </ul>
            </li>
          </ul>
        </div>

        <div class="collapsible" onclick="toggleCollapsible(this)">
          🎯 The Four Ps / Os Quatro Ps
        </div>
        <div class="collapsible-content">
          <table>
            <thead><tr><th>English</th><th>Português</th><th>Sub-elements / Sub-elementos</th></tr></thead>
            <tbody>
              <tr><td><strong>Product</strong></td><td><strong>Produto</strong></td><td>Features / Características, Design, Branding / Marca</td></tr>
              <tr><td><strong>Price</strong></td><td><strong>Preço</strong></td><td>Pricing strategies / Estratégias de preço, Competitiveness / Competitividade</td></tr>
              <tr><td><strong>Place</strong> (Distribution)</td><td><strong>Distribuição</strong></td><td>Distribution channels / Canais de distribuição, Partnerships / Parcerias</td></tr>
              <tr><td><strong>Promotion</strong></td><td><strong>Promoção</strong></td><td>Advertising / Publicidade, Communication / Comunicação, PR / Relações públicas</td></tr>
            </tbody>
          </table>
        </div>

        <h2>🧩 Logical Frameworks / Frameworks Lógicos</h2>

        <div class="collapsible" onclick="toggleCollapsible(this)">
          6 Types of Logical Structures / 6 Tipos de Estruturas Lógicas
        </div>
        <div class="collapsible-content">
          <table>
            <thead><tr><th>#</th><th>Type / Tipo</th><th>Best for / Melhor para</th><th>Example / Exemplo</th></tr></thead>
            <tbody>
              <tr><td>1</td><td><strong>Equations / Equações</strong></td><td>Quantitative questions / Questões quantitativas</td><td>Profit = Revenue − Costs / Lucro = Receitas − Custos</td></tr>
              <tr><td>2</td><td><strong>Key Questions / Questões-chave</strong></td><td>Qualitative decisions / Decisões qualitativas</td><td>Do they have track record? Is price competitive? / Têm histórico? O preço é competitivo?</td></tr>
              <tr><td>3</td><td><strong>Hypotheses / Hipóteses</strong></td><td>Qualitative decisions / Decisões qualitativas</td><td>"I should hire X if..." / "Devo contratar X se..."</td></tr>
              <tr><td>4</td><td><strong>Root Causes / Causas-raiz</strong></td><td>Issue investigations / Investigação de problemas</td><td>Why are deliveries delayed? / Porquê atrasos nas entregas?</td></tr>
              <tr><td>5</td><td><strong>Process Map / Mapa de Processo</strong></td><td>Operations optimization / Otimização de operações</td><td>Attraction → Screening → Selection → Offer / Atração → Triagem → Seleção → Oferta</td></tr>
              <tr><td>6</td><td><strong>From-To</strong></td><td>Reaching a future state / Atingir um estado futuro</td><td>Define objective → Establish current state → Measure gap / Definir objetivo → Estado atual → Medir o gap</td></tr>
            </tbody>
          </table>
        </div>

        <!-- SELECTION GUIDE -->
        <h2>🔑 Quick Selection Guide / Guia Rápido de Seleção</h2>
        <div class="card">
          <table>
            <thead>
              <tr>
                <th>If the prompt mentions... / Se o prompt menciona...</th>
                <th>Framework</th>
              </tr>
            </thead>
            <tbody>
              <tr><td>Profits declining / Lucros a cair</td><td>#1 Profitability / Rentabilidade</td></tr>
              <tr><td>Grow, increase revenue / Crescer, aumentar receitas</td><td>#2 Growth / Crescimento</td></tr>
              <tr><td>Reduce costs, efficiency / Reduzir custos, eficiência</td><td>#3 Cost Cutting / Redução de Custos</td></tr>
              <tr><td>Enter a new market / Entrar num novo mercado</td><td>#4 Market Entry / Entrada no Mercado</td></tr>
              <tr><td>Launch a new product / Lançar novo produto</td><td>#5 Product Launch / Lançamento</td></tr>
              <tr><td>Set / change price / Definir preço</td><td>#6 Pricing / Preço</td></tr>
              <tr><td>Should we invest? / Devemos investir?</td><td>#7 Investment / Investimento</td></tr>
              <tr><td>Buy / merge with company / Comprar / fundir</td><td>#8 M&A / Aquisição</td></tr>
              <tr><td>Competitor threat / Ameaça competitiva</td><td>#9 Competitive Response / Resposta Competitiva</td></tr>
              <tr><td>Improve process, operations / Melhorar processo</td><td>#10 Process Optimization / Otimização</td></tr>
              <tr><td>How big is the market? / Qual o tamanho do mercado?</td><td>Market Sizing (see Math tab / ver tab Math)</td></tr>
            </tbody>
          </table>
        </div>

        <div class="card card-danger">
          <strong>⚠️ NEVER name the framework!</strong> / <strong>NUNCA digas o nome do framework!</strong><br>
          ❌ "I'll use the profitability framework." / "Vou usar o framework de profitability."<br>
          ✅ "To analyze this, I'd look at two main dimensions: revenue and costs." / "Para analisar isto, proponho olhar para duas dimensões: receitas e custos."
        </div>
      </div>'''

print(f"Frameworks section: {len(frameworks_html)} chars, {frameworks_html.count(chr(10))} lines")

# Write to a temp file for easier insertion
import os
output_dir = os.path.join(os.path.dirname(__file__), "..", "0_ACTIVE_NOW", "BCG_Interview_Prep", "sections")
os.makedirs(output_dir, exist_ok=True)

with open(os.path.join(output_dir, "frameworks_new.html"), "w", encoding="utf-8") as f:
    f.write(frameworks_html)

print("Written to sections/frameworks_new.html")
