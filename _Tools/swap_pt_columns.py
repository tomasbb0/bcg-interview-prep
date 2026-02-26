#!/usr/bin/env python3
"""Swap EN/PT column order in Portuguese terms section to have English first (left), Portuguese second (right)."""
import os

BASE = os.path.join(os.path.dirname(__file__), "..", "0_ACTIVE_NOW", "BCG_Interview_Prep")
HTML_PATH = os.path.join(BASE, "index.html")

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Swap table headers in the Portuguese section
# Table 1: Business Terms
html = html.replace(
    '''<th>Português</th>
                <th>English</th>
                <th>Notas</th>''',
    '''<th>English</th>
                <th>Português</th>
                <th>Notas</th>'''
)

# Table 2: Financial Terms (same header pattern)
# Already caught by the first replace since they're identical

# Table 3: Analysis Terms (only 2 columns)
html = html.replace(
    '''<th>Português</th>
                <th>English</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Dimensionamento de mercado</td>
                <td>Market sizing</td>''',
    '''<th>English</th>
                <th>Português</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Market sizing</td>
                <td>Dimensionamento de mercado</td>'''
)

# Now swap the individual rows in Business Terms table
swaps_business = [
    ("Empresa / Companhia", "Company"),
    ("Quota de mercado", "Market share"),
    ("Cadeia de valor", "Value chain"),
    ("Vantagem competitiva", "Competitive advantage"),
    ("Proposta de valor", "Value proposition"),
    ("Concorrente", "Competitor"),
    ("Fornecedor", "Supplier"),
    ("Retalho", "Retail"),
    ("Grossista", "Wholesale"),
    ("Canal de distribuição", "Distribution channel"),
    ("Modelo de negócio", "Business model"),
]

for pt, en in swaps_business:
    old = f"<td>{pt}</td>\n                <td>{en}</td>"
    new = f"<td>{en}</td>\n                <td>{pt}</td>"
    html = html.replace(old, new)

# Financial Terms
swaps_financial = [
    ("Receitas / Faturação", "Revenue"),
    ("Lucro / Resultado", "Profit"),
    ("Prejuízo", "Loss"),
    ("Custos fixos / variáveis", "Fixed / Variable costs"),
    ("Margem bruta / operacional", "Gross / Operating margin"),
    ("Margem de contribuição", "Contribution margin"),
    ("Ponto de equilíbrio", "Breakeven"),
    ("Fluxo de caixa", "Cash flow"),
    ("Período de retorno", "Payback period"),
    ("Valor atual líquido (VAL)", "NPV"),
    ("Balanço", "Balance sheet"),
    ("Demonstração de resultados", "P&amp;L"),
    ("Ativo / Passivo", "Assets / Liabilities"),
    ("Capital próprio", "Equity"),
    ("Alavancagem", "Leverage"),
    ("CAPEX / OPEX", "Capital / Operating expenditure"),
]

for pt, en in swaps_financial:
    old = f"<td>{pt}</td>\n                <td>{en}</td>"
    new = f"<td>{en}</td>\n                <td>{pt}</td>"
    html = html.replace(old, new)

# Analysis Terms (2-column table)
swaps_analysis = [
    ("Taxa de crescimento / penetração / retenção / cancelamento", "Growth / Penetration / Retention / Churn rate"),
    ("Custo de aquisição de cliente", "CAC"),
    ("Valor do ciclo de vida do cliente", "CLV"),
    ("Economias de escala", "Economies of scale"),
    ("Sinergias", "Synergies"),
    ("Barreiras à entrada", "Barriers to entry"),
    ("Poder negocial", "Bargaining power"),
    ("Disrupção", "Disruption"),
    ("Sustentabilidade", "Sustainability"),
]

for pt, en in swaps_analysis:
    old = f"<td>{pt}</td>\n                <td>{en}</td>"
    new = f"<td>{en}</td>\n                <td>{pt}</td>"
    html = html.replace(old, new)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Done! Swapped EN/PT column order in Portuguese terms section.")
print(f"Total file: {html.count(chr(10))+1} lines")
