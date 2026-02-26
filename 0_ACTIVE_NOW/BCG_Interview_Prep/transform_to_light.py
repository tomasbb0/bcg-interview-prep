#!/usr/bin/env python3
"""Transform BCG Prep HTML from dark theme to Burnay Labs light theme."""

import re

INPUT = "index_dark_backup.html"
OUTPUT = "index.html"

NEW_CSS = r"""
      :root {
        --bcg-green: #00a651;
        --text: #1a1a1a;
        --text-muted: #888;
        --bg: #ffffff;
        --card-bg: #fafafa;
        --card-border: #e5e5e5;
        --highlight: #e8a500;
        --danger: #d32f2f;
        --success: #2e7d32;
        --info: #1976d2;
        --sidebar-width: 260px;
      }

      * { margin: 0; padding: 0; box-sizing: border-box; }

      body {
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background: var(--bg);
        color: var(--text);
        line-height: 1.7;
        display: flex;
        min-height: 100vh;
        font-size: 14px;
      }

      /* SIDEBAR */
      .sidebar {
        width: var(--sidebar-width);
        background: #fafafa;
        border-right: 1px solid #e5e5e5;
        position: fixed;
        top: 0; left: 0; bottom: 0;
        overflow-y: auto;
        z-index: 100;
        transition: transform 0.3s ease;
      }

      .sidebar-header {
        padding: 24px 20px;
        border-bottom: 1px solid #e5e5e5;
        background: #fff;
      }

      .sidebar-header h1 {
        font-size: 16px;
        color: #000;
        font-weight: 700;
        letter-spacing: 2px;
      }

      .sidebar-header p {
        font-size: 12px;
        color: var(--text-muted);
        margin-top: 4px;
      }

      .sidebar-header .countdown {
        margin-top: 12px;
        padding: 8px 12px;
        background: rgba(0,166,81,0.06);
        border: 1px solid rgba(0,166,81,0.2);
        border-radius: 8px;
        font-size: 12px;
        color: var(--bcg-green);
        font-weight: 600;
      }

      .sidebar nav {
        padding: 12px 0;
      }

      .sidebar nav a {
        display: flex;
        align-items: center;
        padding: 10px 20px;
        color: var(--text-muted);
        text-decoration: none;
        font-size: 13px;
        font-weight: 500;
        transition: all 0.15s;
        border-left: 3px solid transparent;
      }

      .sidebar nav a:hover {
        color: #000;
        background: #f5f5f5;
      }

      .sidebar nav a.active {
        color: #000;
        font-weight: 600;
        background: rgba(0,166,81,0.04);
        border-left-color: var(--bcg-green);
      }

      .sidebar nav .icon {
        margin-right: 10px;
        font-size: 16px;
      }

      .sidebar .divider {
        height: 1px;
        background: #e5e5e5;
        margin: 8px 20px;
      }

      /* MOBILE MENU */
      .menu-toggle {
        display: none;
        position: fixed;
        top: 16px; left: 16px;
        z-index: 200;
        background: #fff;
        border: 1px solid #e5e5e5;
        border-radius: 8px;
        width: 40px; height: 40px;
        font-size: 20px;
        cursor: pointer;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        color: #000;
      }

      /* MAIN */
      .main {
        margin-left: var(--sidebar-width);
        max-width: 900px;
        padding: 48px 56px;
        flex: 1;
      }

      .section { display: none; }
      .section.active { display: block; animation: fadeIn 0.3s ease; }

      @keyframes fadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
      }

      .section-title {
        font-size: 28px;
        font-weight: 700;
        color: #000;
        margin-bottom: 4px;
        letter-spacing: -0.3px;
      }

      .section-subtitle {
        font-size: 14px;
        color: var(--text-muted);
        margin-bottom: 32px;
      }

      /* CARDS */
      .card {
        background: #fafafa;
        border: 1px solid #e5e5e5;
        border-radius: 12px;
        padding: 20px 24px;
        margin: 16px 0;
      }

      .card-accent {
        border-left: 4px solid var(--bcg-green);
        background: rgba(0,166,81,0.03);
      }

      .card-warning {
        border-left: 4px solid var(--highlight);
        background: rgba(232,165,0,0.04);
      }

      .card-danger {
        border-left: 4px solid var(--danger);
        background: rgba(211,47,47,0.04);
      }

      .card-info {
        border-left: 4px solid var(--info);
        background: rgba(25,118,210,0.04);
      }

      h2 {
        font-size: 20px;
        color: #000;
        margin: 36px 0 16px 0;
        display: flex;
        align-items: center;
        gap: 10px;
        font-weight: 700;
      }

      h3 {
        font-size: 16px;
        color: #000;
        margin: 16px 0 10px 0;
        font-weight: 600;
      }

      h4 {
        font-size: 14px;
        color: var(--text);
        margin: 14px 0 6px 0;
        font-weight: 600;
      }

      /* TABLES */
      table {
        width: 100%;
        border-collapse: collapse;
        margin: 12px 0 20px 0;
        font-size: 13px;
      }

      th {
        background: #fafafa;
        color: #888;
        padding: 10px 14px;
        text-align: left;
        font-weight: 600;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border-bottom: 1px solid #e5e5e5;
      }

      td {
        padding: 10px 14px;
        border-bottom: 1px solid #f5f5f5;
        color: var(--text);
      }

      tr:hover td {
        background: rgba(0,166,81,0.02);
      }

      .time-col {
        color: var(--bcg-green);
        font-weight: 600;
        white-space: nowrap;
      }
      .activity-col { font-weight: 500; }

      /* FRAMEWORK TREES — proper CSS tree rendering */
      .tree {
        background: #fafafa;
        border: 1px solid #e5e5e5;
        border-radius: 10px;
        padding: 20px 24px;
        margin: 12px 0;
        font-family: 'SF Mono', 'Fira Code', 'Menlo', Consolas, monospace;
        font-size: 13px;
        line-height: 1.9;
        overflow-x: auto;
        white-space: pre;
        color: #555;
      }

      .tree .highlight {
        color: var(--bcg-green);
        font-weight: 600;
      }

      /* Pretty nested tree list */
      ul.tree-list {
        list-style: none;
        padding-left: 0;
        margin: 12px 0;
        font-size: 14px;
      }
      ul.tree-list ul {
        list-style: none;
        padding-left: 24px;
        position: relative;
      }
      ul.tree-list ul::before {
        content: '';
        position: absolute;
        left: 8px;
        top: 0;
        bottom: 12px;
        width: 1px;
        background: #d0d0d0;
      }
      ul.tree-list li {
        position: relative;
        padding: 3px 0 3px 0;
        font-size: 14px;
        color: var(--text);
      }
      ul.tree-list ul > li::before {
        content: '';
        position: absolute;
        left: -16px;
        top: 14px;
        width: 12px;
        height: 1px;
        background: #d0d0d0;
      }
      ul.tree-list > li > strong,
      ul.tree-list > li > .tree-root {
        color: #000;
        font-weight: 700;
        font-size: 14px;
      }
      ul.tree-list .tree-branch {
        color: var(--bcg-green);
        font-weight: 600;
      }

      /* FORMULAS */
      .formula {
        background: #f0faf4;
        border: 1px solid rgba(0,166,81,0.15);
        border-radius: 8px;
        padding: 14px 18px;
        margin: 12px 0;
        font-family: 'SF Mono', 'Fira Code', Consolas, monospace;
        font-size: 13px;
        color: #1a5c35;
      }

      /* COLLAPSIBLES */
      .collapsible {
        cursor: pointer;
        padding: 14px 18px;
        background: #fff;
        border: 1px solid #e5e5e5;
        border-radius: 8px;
        margin: 8px 0;
        font-size: 14px;
        font-weight: 600;
        color: #000;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: all 0.15s;
      }

      .collapsible:hover {
        background: #f8f8f8;
        border-color: #ccc;
      }

      .collapsible::after {
        content: '▸';
        font-size: 13px;
        color: var(--bcg-green);
        transition: transform 0.2s;
      }

      .collapsible.open::after {
        transform: rotate(90deg);
      }

      .collapsible-content {
        max-height: 0;
        overflow: hidden;
        transition: max-height 0.4s ease;
        padding: 0 18px;
      }

      .collapsible-content.open {
        max-height: 5000px;
        padding: 16px 18px;
        border: 1px solid #e5e5e5;
        border-top: none;
        border-radius: 0 0 8px 8px;
        background: #fafafa;
      }

      /* LISTS */
      ul, ol { padding-left: 24px; margin: 8px 0; }
      li { margin: 4px 0; font-size: 14px; }

      /* QUOTES */
      blockquote {
        border-left: 3px solid var(--bcg-green);
        padding: 12px 18px;
        margin: 12px 0;
        background: rgba(0,166,81,0.03);
        border-radius: 0 8px 8px 0;
        font-style: italic;
        color: var(--text);
      }

      /* BADGES */
      .badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
      }

      .badge-green { background: rgba(46,125,50,0.1); color: var(--success); }
      .badge-yellow { background: rgba(232,165,0,0.1); color: var(--highlight); }
      .badge-red { background: rgba(211,47,47,0.1); color: var(--danger); }
      .badge-blue { background: rgba(25,118,210,0.1); color: var(--info); }

      /* MATH DRILL BUTTONS */
      .drill-answer {
        display: none;
        margin-top: 8px;
        padding: 8px 14px;
        background: rgba(0,166,81,0.06);
        border-radius: 6px;
        font-weight: 600;
        color: var(--bcg-green);
      }

      .drill-btn {
        display: inline-block;
        padding: 4px 12px;
        background: #fff;
        border: 1px solid #e5e5e5;
        border-radius: 6px;
        color: var(--text);
        cursor: pointer;
        font-size: 12px;
        margin-top: 4px;
        transition: all 0.15s;
      }

      .drill-btn:hover {
        background: var(--bcg-green);
        color: #fff;
        border-color: var(--bcg-green);
      }

      /* STAR TEMPLATE */
      .star-box {
        background: #f9f9f9;
        border: 1px dashed #d5d5d5;
        border-radius: 8px;
        padding: 16px;
        margin: 12px 0;
      }

      .star-label {
        display: inline-block;
        width: 28px;
        height: 28px;
        background: var(--bcg-green);
        color: #fff;
        border-radius: 50%;
        text-align: center;
        line-height: 28px;
        font-size: 13px;
        font-weight: 700;
        margin-right: 10px;
      }

      /* CHECKLIST */
      .checklist { list-style: none; padding: 0; }
      .checklist li {
        padding: 8px 0;
        border-bottom: 1px solid #f0f0f0;
        display: flex;
        align-items: center;
        gap: 10px;
        cursor: pointer;
      }
      .checklist li::before {
        content: '☐';
        font-size: 18px;
        color: var(--bcg-green);
      }
      .checklist li.checked::before { content: '☑'; }
      .checklist li.checked { text-decoration: line-through; color: var(--text-muted); }

      /* DO / DON'T TABLE */
      .do-dont {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
        margin: 16px 0;
      }
      .do-col, .dont-col { padding: 16px; border-radius: 10px; }
      .do-col {
        background: rgba(46,125,50,0.04);
        border: 1px solid rgba(46,125,50,0.15);
      }
      .dont-col {
        background: rgba(211,47,47,0.04);
        border: 1px solid rgba(211,47,47,0.15);
      }
      .do-col h4 { color: var(--success); }
      .dont-col h4 { color: var(--danger); }

      /* PROGRESS BAR */
      .progress-bar {
        height: 4px;
        background: #e5e5e5;
        border-radius: 2px;
        margin: 8px 0 20px;
        overflow: hidden;
      }
      .progress-fill {
        height: 100%;
        background: var(--bcg-green);
        border-radius: 2px;
        transition: width 0.5s ease;
      }

      /* COMMANDMENT */
      .commandment {
        background: #fafafa;
        border: 1px solid #e5e5e5;
        border-radius: 12px;
        padding: 20px;
        margin: 12px 0;
      }
      .commandment-number {
        display: inline-block;
        width: 32px; height: 32px;
        background: #000;
        color: #fff;
        border-radius: 50%;
        text-align: center;
        line-height: 32px;
        font-weight: 700;
        margin-right: 10px;
      }
      .commandment h3 { display: inline; }
      .commandment blockquote { margin-top: 10px; }

      /* SCROLLBAR */
      ::-webkit-scrollbar { width: 6px; }
      ::-webkit-scrollbar-track { background: #fff; }
      ::-webkit-scrollbar-thumb { background: #ddd; border-radius: 3px; }
      ::-webkit-scrollbar-thumb:hover { background: #bbb; }

      /* RESPONSIVE */
      @media (max-width: 768px) {
        .sidebar { transform: translateX(-100%); }
        .sidebar.open { transform: translateX(0); }
        .menu-toggle { display: block; }
        .main { margin-left: 0; padding: 20px; padding-top: 72px; }
        .section-title { font-size: 22px; }
        .do-dont { grid-template-columns: 1fr; }
        table { font-size: 12px; }
        th, td { padding: 6px 8px; }
      }

      /* PRINT */
      @media print {
        .sidebar, .menu-toggle { display: none !important; }
        .main { margin-left: 0; max-width: 100%; }
        .section { display: block !important; page-break-before: always; }
        body { background: #fff; color: #000; }
        .card { border-color: #ddd; }
      }

      .back-to-top {
        position: fixed;
        bottom: 24px; right: 24px;
        width: 40px; height: 40px;
        background: #000;
        color: #fff;
        border: none;
        border-radius: 50%;
        font-size: 18px;
        cursor: pointer;
        box-shadow: 0 2px 12px rgba(0,0,0,0.12);
        z-index: 50;
        opacity: 0;
        transition: opacity 0.3s;
      }
      .back-to-top.visible { opacity: 1; }

      .day-tab {
        display: inline-block;
        padding: 8px 16px;
        margin: 4px;
        background: #fff;
        border: 1px solid #e5e5e5;
        border-radius: 8px;
        cursor: pointer;
        font-size: 13px;
        font-weight: 600;
        color: var(--text-muted);
        transition: all 0.15s;
      }
      .day-tab:hover, .day-tab.active {
        background: rgba(0,166,81,0.06);
        border-color: var(--bcg-green);
        color: var(--bcg-green);
      }
      .day-content { display: none; }
      .day-content.active { display: block; }

      .kbd {
        display: inline-block;
        padding: 2px 8px;
        background: #f5f5f5;
        border: 1px solid #e5e5e5;
        border-radius: 4px;
        font-family: monospace;
        font-size: 13px;
      }

      .term-grid {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 2px;
        font-size: 13px;
      }
      .term-grid .term-pt { color: var(--bcg-green); font-weight: 600; }
      .term-grid .term-en { color: var(--text-muted); }
      .term-grid .term-note { color: var(--info); font-style: italic; font-size: 12px; }

      @media (max-width: 768px) {
        .term-grid { grid-template-columns: 1fr 1fr; }
        .term-grid .term-note { display: none; }
      }
"""

def transform():
    with open(INPUT, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Replace the entire <style> block
    # Find from <style> to </style>
    style_pattern = r'(<style>).*?(</style>)'
    html = re.sub(style_pattern, r'\1' + NEW_CSS + r'    \2', html, count=1, flags=re.DOTALL)

    # 2. Fix sidebar header gradient to plain white
    html = html.replace(
        'background: linear-gradient(135deg, var(--bcg-dark), var(--bcg-accent));',
        'background: #fff;'
    )

    # 3. Fix countdown year from 2025 to 2026
    html = html.replace(
        'new Date("2025-02-28T15:30:00")',
        'new Date("2026-02-28T15:30:00")'
    )

    # 4. Fix inline color references to CSS variables that changed
    # Replace color: var(--text-muted) — already compatible 
    # Replace color: white → color: #000 in h3 inline styles
    # Fix the game day final card inline styles
    html = html.replace(
        'font-size: 20px; color: white; font-weight: 600',
        'font-size: 20px; color: #000; font-weight: 600'
    )
    html = html.replace(
        'font-size: 24px;\n              color: var(--highlight);\n              margin-top: 8px;\n              font-weight: 700;',
        'font-size: 24px;\n              color: var(--bcg-green);\n              margin-top: 8px;\n              font-weight: 700;'
    )

    # 5. Fix inline "border: 2px solid var(--bcg-green)" — keep, that's fine

    # 6. Fix the sidebar header style (no gradient)
    # Already handled by CSS replacement

    # 7. Convert framework tree divs to proper tree HTML
    # Framework tree: Profitability
    html = html.replace(
        '''<div class="tree">
            PROFITABILIDADE RECEITAS (Revenue) CUSTOS (Costs) ├── Preço
            (pricing) ├── Fixos (Fixed) │ ├── Estratégia de preço │ ├── Rendas,
            Salários, Depreciação │ ├── Mudanças recentes? │ ├── Mudaram
            recentemente? │ └── vs. concorrência? │ └── Benchmark vs. indústria?
            ├── Volume ├── Variáveis (Variable) │ ├── Nº clientes │ ├──
            Matérias-primas, Comissões │ ├── Frequência de compra │ ├── Mudaram
            recentemente? │ └── Ticket médio (avg revenue/tx) │ └── Benchmark
            vs. indústria? └── Mix de produtos └── Estrutura de custos └──
            Margens por produto/segmento └── Qual a % de fixos vs. variáveis?
          </div>''',
        '''<ul class="tree-list">
            <li><strong>PROFITABILIDADE</strong>
              <ul>
                <li><span class="tree-branch">RECEITAS (Revenue)</span>
                  <ul>
                    <li>Preço (pricing)
                      <ul>
                        <li>Estratégia de preço</li>
                        <li>Mudanças recentes?</li>
                        <li>vs. concorrência?</li>
                      </ul>
                    </li>
                    <li>Volume
                      <ul>
                        <li>Nº clientes</li>
                        <li>Frequência de compra</li>
                        <li>Ticket médio (avg revenue/tx)</li>
                      </ul>
                    </li>
                    <li>Mix de produtos
                      <ul>
                        <li>Margens por produto/segmento</li>
                      </ul>
                    </li>
                  </ul>
                </li>
                <li><span class="tree-branch">CUSTOS (Costs)</span>
                  <ul>
                    <li>Fixos (Fixed)
                      <ul>
                        <li>Rendas, Salários, Depreciação</li>
                        <li>Mudaram recentemente?</li>
                        <li>Benchmark vs. indústria?</li>
                      </ul>
                    </li>
                    <li>Variáveis (Variable)
                      <ul>
                        <li>Matérias-primas, Comissões</li>
                        <li>Mudaram recentemente?</li>
                        <li>Benchmark vs. indústria?</li>
                      </ul>
                    </li>
                    <li>Estrutura de custos
                      <ul>
                        <li>Qual a % de fixos vs. variáveis?</li>
                      </ul>
                    </li>
                  </ul>
                </li>
              </ul>
            </li>
          </ul>'''
    )

    # Framework tree: Market Entry
    html = html.replace(
        '''<div class="tree">
            ENTRADA NO MERCADO 1. MERCADO (Market) 2. EMPRESA (Company) 3.
            CONCORRÊNCIA 4. MODO DE ENTRADA ├── Tamanho & crescimento ├──
            Capacidades? ├── Quem? Quantos? ├── Orgânico (greenfield) ├──
            Segmentos? ├── Fit estratégico? ├── Quota de mercado? ├── Aquisição
            ├── Tendências? ├── Recursos necessários? ├── Diferenciação? ├──
            Joint Venture ├── Regulamentação? ├── Sinergias? ├── Barreiras à
            entrada └── Parceria / Licensing └── Barreiras à entrada? └── Gap
            no mercado? └── Reação esperada? └── Investimento & timeline?
          </div>''',
        '''<ul class="tree-list">
            <li><strong>ENTRADA NO MERCADO</strong>
              <ul>
                <li><span class="tree-branch">1. MERCADO (Market)</span>
                  <ul>
                    <li>Tamanho & crescimento</li>
                    <li>Segmentos?</li>
                    <li>Tendências?</li>
                    <li>Regulamentação?</li>
                    <li>Barreiras à entrada?</li>
                  </ul>
                </li>
                <li><span class="tree-branch">2. EMPRESA (Company)</span>
                  <ul>
                    <li>Capacidades?</li>
                    <li>Fit estratégico?</li>
                    <li>Recursos necessários?</li>
                    <li>Sinergias?</li>
                    <li>Gap no mercado?</li>
                  </ul>
                </li>
                <li><span class="tree-branch">3. CONCORRÊNCIA</span>
                  <ul>
                    <li>Quem? Quantos?</li>
                    <li>Quota de mercado?</li>
                    <li>Diferenciação?</li>
                    <li>Barreiras à entrada</li>
                    <li>Reação esperada?</li>
                  </ul>
                </li>
                <li><span class="tree-branch">4. MODO DE ENTRADA</span>
                  <ul>
                    <li>Orgânico (greenfield)</li>
                    <li>Aquisição</li>
                    <li>Joint Venture</li>
                    <li>Parceria / Licensing</li>
                    <li>Investimento & timeline?</li>
                  </ul>
                </li>
              </ul>
            </li>
          </ul>'''
    )

    # Framework tree: Pricing
    html = html.replace(
        '''<div class="tree">
            PRICING 1. CUSTO (Cost-based) 2. VALOR (Value-based) 3. CONCORRÊNCIA
            (Competition) ├── Custo total + margem ├── WTP do cliente ├──
            Preços dos concorrentes ├── Custo fixo + variável ├── Valor
            percebido ├── Posicionamento ├── Margem desejada ├── Diferenciação?
            ├── Premium vs. discount └── Preço mínimo viável └── Segmentação de
            preço └── Elasticidade-preço └── Bundling / Tiering
          </div>''',
        '''<ul class="tree-list">
            <li><strong>PRICING</strong>
              <ul>
                <li><span class="tree-branch">1. CUSTO (Cost-based)</span>
                  <ul>
                    <li>Custo total + margem</li>
                    <li>Custo fixo + variável</li>
                    <li>Margem desejada</li>
                    <li>Preço mínimo viável</li>
                  </ul>
                </li>
                <li><span class="tree-branch">2. VALOR (Value-based)</span>
                  <ul>
                    <li>WTP do cliente</li>
                    <li>Valor percebido</li>
                    <li>Diferenciação?</li>
                    <li>Segmentação de preço</li>
                  </ul>
                </li>
                <li><span class="tree-branch">3. CONCORRÊNCIA (Competition)</span>
                  <ul>
                    <li>Preços dos concorrentes</li>
                    <li>Posicionamento</li>
                    <li>Premium vs. discount</li>
                    <li>Elasticidade-preço</li>
                    <li>Bundling / Tiering</li>
                  </ul>
                </li>
              </ul>
            </li>
          </ul>'''
    )

    # Framework tree: M&A
    html = html.replace(
        '''<div class="tree">
            M&A / AQUISIÇÃO 1. RACIONAL 2. ALVO 3. SINERGIAS 4. RISCOS ├──
            Porquê comprar? ├── Fit estratégico? ├── Receitas (cross-sell) ├──
            Integração ├── Crescimento, capacidades? ├── Valorização justa? ├──
            Custos (economias escala) ├── Cultural ├── Alternativa a orgânico?
            ├── Saúde financeira? ├── Capabilidades (tech, talento) ├──
            Regulamentação └── Buy vs. build vs. partner └── Cultura da
            empresa? └── Timeline de captura └── Canibalização
          </div>''',
        '''<ul class="tree-list">
            <li><strong>M&A / AQUISIÇÃO</strong>
              <ul>
                <li><span class="tree-branch">1. RACIONAL</span>
                  <ul>
                    <li>Porquê comprar?</li>
                    <li>Crescimento, capacidades?</li>
                    <li>Alternativa a orgânico?</li>
                    <li>Buy vs. build vs. partner</li>
                  </ul>
                </li>
                <li><span class="tree-branch">2. ALVO</span>
                  <ul>
                    <li>Fit estratégico?</li>
                    <li>Valorização justa?</li>
                    <li>Saúde financeira?</li>
                    <li>Cultura da empresa?</li>
                  </ul>
                </li>
                <li><span class="tree-branch">3. SINERGIAS</span>
                  <ul>
                    <li>Receitas (cross-sell)</li>
                    <li>Custos (economias escala)</li>
                    <li>Capabilidades (tech, talento)</li>
                    <li>Timeline de captura</li>
                  </ul>
                </li>
                <li><span class="tree-branch">4. RISCOS</span>
                  <ul>
                    <li>Integração</li>
                    <li>Cultural</li>
                    <li>Regulamentação</li>
                    <li>Canibalização</li>
                  </ul>
                </li>
              </ul>
            </li>
          </ul>'''
    )

    # Framework tree: Growth
    html = html.replace(
        '''<div class="tree">
            CRESCIMENTO ORGÂNICO INORGÂNICO ├── Clientes existentes ├──
            Aquisições │ ├── Upsell / Cross-sell │ ├── Comprar concorrente │
            ├── Aumentar frequência │ ├── Comprar capacidades │ └── Reduzir
            churn │ └── Consolidação ├── Novos clientes ├── Parcerias │ ├──
            Novos segmentos │ ├── Joint ventures │ ├── Expansão geográfica │
            ├── Licensing │ └── Canais novos │ └── Distribuição └── Novos
            produtos/serviços └── Diversificação ├── Inovação ├── Adjacências
            └── Extensão de linha └── Novos mercados
          </div>''',
        '''<ul class="tree-list">
            <li><strong>CRESCIMENTO</strong>
              <ul>
                <li><span class="tree-branch">ORGÂNICO</span>
                  <ul>
                    <li>Clientes existentes
                      <ul>
                        <li>Upsell / Cross-sell</li>
                        <li>Aumentar frequência</li>
                        <li>Reduzir churn</li>
                      </ul>
                    </li>
                    <li>Novos clientes
                      <ul>
                        <li>Novos segmentos</li>
                        <li>Expansão geográfica</li>
                        <li>Canais novos</li>
                      </ul>
                    </li>
                    <li>Novos produtos/serviços
                      <ul>
                        <li>Inovação</li>
                        <li>Extensão de linha</li>
                      </ul>
                    </li>
                  </ul>
                </li>
                <li><span class="tree-branch">INORGÂNICO</span>
                  <ul>
                    <li>Aquisições
                      <ul>
                        <li>Comprar concorrente</li>
                        <li>Comprar capacidades</li>
                        <li>Consolidação</li>
                      </ul>
                    </li>
                    <li>Parcerias
                      <ul>
                        <li>Joint ventures</li>
                        <li>Licensing</li>
                        <li>Distribuição</li>
                      </ul>
                    </li>
                    <li>Diversificação
                      <ul>
                        <li>Adjacências</li>
                        <li>Novos mercados</li>
                      </ul>
                    </li>
                  </ul>
                </li>
              </ul>
            </li>
          </ul>'''
    )

    # Framework tree: Cost Reduction
    html = html.replace(
        '''<div class="tree">
            REDUÇÃO DE CUSTOS CUSTOS FIXOS CUSTOS VARIÁVEIS EFICIÊNCIA ├──
            Renegociar contratos ├── Matérias-primas ├── Automação ├──
            Consolidar instalações ├── Fornecedores alternativos? ├── Lean
            operations ├── Outsourcing ├── Renegociar preços ├── Eliminar
            desperdício ├── Redução de headcount ├── Qualidade (menos defeitos)
            ├── Standardização └── Renegociar rendas └── Logística otimizar └──
            Economies of scale └── Shared services
          </div>''',
        '''<ul class="tree-list">
            <li><strong>REDUÇÃO DE CUSTOS</strong>
              <ul>
                <li><span class="tree-branch">CUSTOS FIXOS</span>
                  <ul>
                    <li>Renegociar contratos</li>
                    <li>Consolidar instalações</li>
                    <li>Outsourcing</li>
                    <li>Redução de headcount</li>
                    <li>Renegociar rendas</li>
                  </ul>
                </li>
                <li><span class="tree-branch">CUSTOS VARIÁVEIS</span>
                  <ul>
                    <li>Matérias-primas</li>
                    <li>Fornecedores alternativos?</li>
                    <li>Renegociar preços</li>
                    <li>Qualidade (menos defeitos)</li>
                    <li>Logística otimizar</li>
                  </ul>
                </li>
                <li><span class="tree-branch">EFICIÊNCIA</span>
                  <ul>
                    <li>Automação</li>
                    <li>Lean operations</li>
                    <li>Eliminar desperdício</li>
                    <li>Standardização</li>
                    <li>Economies of scale</li>
                    <li>Shared services</li>
                  </ul>
                </li>
              </ul>
            </li>
          </ul>'''
    )

    # Framework tree: Market Sizing
    html = html.replace(
        '''<div class="tree">
            MARKET SIZING TOP-DOWN BOTTOM-UP ├── Mercado total (TAM) ├──
            Nº unidades / clientes ├── Filtrar por segmento ├── × Frequência de
            uso ├── × % relevante ├── × Preço unitário └── = Mercado
            endereçável (SAM) └── = Tamanho estimado │ └── Ajustar por
            penetração realista │ └── = Mercado atingível (SOM)
          </div>''',
        '''<ul class="tree-list">
            <li><strong>MARKET SIZING</strong>
              <ul>
                <li><span class="tree-branch">TOP-DOWN</span>
                  <ul>
                    <li>Mercado total (TAM)</li>
                    <li>Filtrar por segmento</li>
                    <li>× % relevante</li>
                    <li>= Mercado endereçável (SAM)</li>
                    <li>Ajustar por penetração realista</li>
                    <li>= Mercado atingível (SOM)</li>
                  </ul>
                </li>
                <li><span class="tree-branch">BOTTOM-UP</span>
                  <ul>
                    <li>Nº unidades / clientes</li>
                    <li>× Frequência de uso</li>
                    <li>× Preço unitário</li>
                    <li>= Tamanho estimado</li>
                  </ul>
                </li>
              </ul>
            </li>
          </ul>'''
    )

    # Creativity section trees
    html = html.replace(
        '''<div class="tree">
            QUEM (stakeholders) O QUÊ (o que mudar) ├── Clientes atuais ├──
            Produto/Serviço ├── Novos clientes ├── Preço ├── Parceiros/Canais
            ├── Experiência └── Equipa interna └── Canal/Distribuição COMO
            (mecanismos) ├── Tecnologia/Digital ├── Marketing/Comunicação ├──
            Operacional └── Parcerias
          </div>''',
        '''<ul class="tree-list">
            <li><strong>QUEM</strong> (stakeholders)
              <ul>
                <li>Clientes atuais</li>
                <li>Novos clientes</li>
                <li>Parceiros/Canais</li>
                <li>Equipa interna</li>
              </ul>
            </li>
            <li><strong>O QUÊ</strong> (o que mudar)
              <ul>
                <li>Produto/Serviço</li>
                <li>Preço</li>
                <li>Experiência</li>
                <li>Canal/Distribuição</li>
              </ul>
            </li>
            <li><strong>COMO</strong> (mecanismos)
              <ul>
                <li>Tecnologia/Digital</li>
                <li>Marketing/Comunicação</li>
                <li>Operacional</li>
                <li>Parcerias</li>
              </ul>
            </li>
          </ul>'''
    )

    html = html.replace(
        '''<div class="tree">
            INTERNO (controlamos) EXTERNO (influenciamos) ├── Produto/Serviço
            ├── Clientes ├── Processos ├── Mercado/Concorrência ├──
            Pessoas/Equipa ├── Regulamentação └── Tecnologia └── Parcerias
          </div>''',
        '''<ul class="tree-list">
            <li><strong>INTERNO</strong> (controlamos)
              <ul>
                <li>Produto/Serviço</li>
                <li>Processos</li>
                <li>Pessoas/Equipa</li>
                <li>Tecnologia</li>
              </ul>
            </li>
            <li><strong>EXTERNO</strong> (influenciamos)
              <ul>
                <li>Clientes</li>
                <li>Mercado/Concorrência</li>
                <li>Regulamentação</li>
                <li>Parcerias</li>
              </ul>
            </li>
          </ul>'''
    )

    html = html.replace(
        '''<div class="tree">
            CURTO (0-3 meses): Quick wins, low-hanging fruit, otimizações
            rápidas MÉDIO (3-12 meses): Novos processos, canais, mudanças
            operacionais LONGO (1-3+ anos): Novos produtos/mercados,
            transformação digital, M&A
          </div>''',
        '''<ul class="tree-list">
            <li><strong>CURTO</strong> (0-3 meses)
              <ul>
                <li>Quick wins, low-hanging fruit</li>
                <li>Otimizações rápidas</li>
              </ul>
            </li>
            <li><strong>MÉDIO</strong> (3-12 meses)
              <ul>
                <li>Novos processos, canais</li>
                <li>Mudanças operacionais</li>
              </ul>
            </li>
            <li><strong>LONGO</strong> (1-3+ anos)
              <ul>
                <li>Novos produtos/mercados</li>
                <li>Transformação digital, M&A</li>
              </ul>
            </li>
          </ul>'''
    )

    # BCG Patterns section tree
    html = html.replace(
        '''<div class="tree">
            ENTREVISTA 1 (45 min) ENTREVISTA 2 (45 min) ├── Fit/PEI: 10-15 min
            ├── Fit/PEI: 10-15 min │ └── 1-2 perguntas │ └── 1-2 perguntas
            (diferentes) └── Caso: 25-30 min └── Caso: 25-30 min └── Caso
            completo └── Tipo diferente
          </div>''',
        '''<ul class="tree-list">
            <li><strong>ENTREVISTA 1</strong> (45 min)
              <ul>
                <li>Fit/PEI: 10-15 min
                  <ul><li>1-2 perguntas</li></ul>
                </li>
                <li>Caso: 25-30 min
                  <ul><li>Caso completo</li></ul>
                </li>
              </ul>
            </li>
            <li><strong>ENTREVISTA 2</strong> (45 min)
              <ul>
                <li>Fit/PEI: 10-15 min
                  <ul><li>1-2 perguntas (diferentes)</li></ul>
                </li>
                <li>Caso: 25-30 min
                  <ul><li>Tipo diferente</li></ul>
                </li>
              </ul>
            </li>
          </ul>'''
    )

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ Transformed {INPUT} → {OUTPUT}")
    print(f"   File size: {len(html):,} chars")

if __name__ == '__main__':
    transform()
