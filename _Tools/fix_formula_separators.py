#!/usr/bin/env python3
"""Fix formula sections to use separate lines for EN/PT instead of / separator."""

with open('0_ACTIVE_NOW/BCG_Interview_Prep/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Breakeven formula
content = content.replace(
    '''            BE (units) = Fixed Costs ÷ (Price − Variable Cost per Unit)<br />
            BE (unidades) = Custos Fixos ÷ (Preço − Custo Variável por
            Unidade)<br /><br />
            Contribution Margin / Margem de Contribuição = Price − Variable Cost
            / Preço − CV''',
    '''            <strong>🇬🇧</strong> BE (units) = Fixed Costs ÷ (Price − Variable Cost per Unit)<br />
            <strong>🇵🇹</strong> BE (unidades) = Custos Fixos ÷ (Preço − Custo Variável por Unidade)<br /><br />
            <strong>🇬🇧</strong> Contribution Margin = Price − Variable Cost<br />
            <strong>🇵🇹</strong> Margem de Contribuição = Preço − Custo Variável'''
)
print("1. Breakeven done")

# 2. Payback formula
content = content.replace(
    '''            Payback = Initial Investment ÷ Annual Cash Flow / Investimento
            Inicial ÷ Fluxo de Caixa Anual''',
    '''            <strong>🇬🇧</strong> Payback = Initial Investment ÷ Annual Cash Flow<br />
            <strong>🇵🇹</strong> Payback = Investimento Inicial ÷ Fluxo de Caixa Anual'''
)
print("2. Payback done")

# 3. ROI formula
content = content.replace(
    '''            ROI = (Gain − Investment) ÷ Investment × 100% / (Ganho −
            Investimento) ÷ Investimento × 100%''',
    '''            <strong>🇬🇧</strong> ROI = (Gain − Investment) ÷ Investment × 100%<br />
            <strong>🇵🇹</strong> ROI = (Ganho − Investimento) ÷ Investimento × 100%'''
)
print("3. ROI done")

# 4. Margins formulas
content = content.replace(
    '''            Gross Margin / Margem Bruta = (Revenue − COGS) ÷ Revenue<br />
            Operating Margin / Margem Operacional = EBIT ÷ Revenue / Receita<br />
            Net Margin / Margem Líquida = Net Profit ÷ Revenue / Lucro Líquido ÷
            Receita<br />
            Contribution Margin / Margem de Contribuição = (Price − VC) ÷ Price
            / (Preço − CV) ÷ Preço''',
    '''            <strong>🇬🇧</strong> Gross Margin = (Revenue − COGS) ÷ Revenue<br />
            <strong>🇵🇹</strong> Margem Bruta = (Receita − COGS) ÷ Receita<br /><br />
            <strong>🇬🇧</strong> Operating Margin = EBIT ÷ Revenue<br />
            <strong>🇵🇹</strong> Margem Operacional = EBIT ÷ Receita<br /><br />
            <strong>🇬🇧</strong> Net Margin = Net Profit ÷ Revenue<br />
            <strong>🇵🇹</strong> Margem Líquida = Lucro Líquido ÷ Receita<br /><br />
            <strong>🇬🇧</strong> Contribution Margin = (Price − VC) ÷ Price<br />
            <strong>🇵🇹</strong> Margem de Contribuição = (Preço − CV) ÷ Preço'''
)
print("4. Margins done")

# 5. Growth/CAGR
content = content.replace(
    '''            Growth / Crescimento = (Final − Initial) ÷ Initial × 100%<br />CAGR
            = (Final ÷ Initial)^(1/n) − 1''',
    '''            <strong>🇬🇧</strong> Growth = (Final − Initial) ÷ Initial × 100%<br />
            <strong>🇵🇹</strong> Crescimento = (Final − Inicial) ÷ Inicial × 100%<br /><br />
            CAGR = (Final ÷ Initial)^(1/n) − 1'''
)
print("5. Growth done")

# 6. NPV/CLV/CAC block
content = content.replace(
    '''            NPV / VAL = Σ [CF_t ÷ (1 + r)^t] − Initial Investment / Investimento
            Inicial<br /><br />
            CLV = Avg Revenue × Margin × Retention Time / Receita Média × Margem
            × Tempo Retenção<br />
            CAC = Total Marketing+Sales Cost ÷ # New Customers / Custo Total
            Marketing+Vendas ÷ # Novos Clientes<br />
            Healthy ratio / Rácio saudável: CLV/CAC > 3<br /><br />
            Market Share / Quota de Mercado = Company Sales ÷ Market Sales /
            Vendas Empresa ÷ Vendas Mercado<br /><br />
            Elasticity / Elasticidade = % Change Quantity ÷ % Change Price / %
            Variação Quantidade ÷ % Variação Preço<br />
            |E| > 1: Elastic / Elástico (price-sensitive) &nbsp; |E| < 1:
            Inelastic / Inelástico''',
    '''            <strong>🇬🇧</strong> NPV = Σ [CF_t ÷ (1 + r)^t] − Initial Investment<br />
            <strong>🇵🇹</strong> VAL = Σ [CF_t ÷ (1 + r)^t] − Investimento Inicial<br /><br />
            <strong>🇬🇧</strong> CLV = Avg Revenue × Margin × Retention Time<br />
            <strong>🇵🇹</strong> CLV = Receita Média × Margem × Tempo de Retenção<br /><br />
            <strong>🇬🇧</strong> CAC = Total Marketing+Sales Cost ÷ # New Customers<br />
            <strong>🇵🇹</strong> CAC = Custo Total Marketing+Vendas ÷ # Novos Clientes<br />
            Healthy ratio: CLV÷CAC > 3<br /><br />
            <strong>🇬🇧</strong> Market Share = Company Sales ÷ Market Sales<br />
            <strong>🇵🇹</strong> Quota de Mercado = Vendas Empresa ÷ Vendas Mercado<br /><br />
            <strong>🇬🇧</strong> Elasticity = % Change Quantity ÷ % Change Price<br />
            <strong>🇵🇹</strong> Elasticidade = % Variação Quantidade ÷ % Variação Preço<br />
            |E| > 1: Elastic (price-sensitive) &nbsp; |E| < 1: Inelastic'''
)
print("6. NPV/CLV/CAC done")

# 7. Also fix the example lines that use / for EN/PT
content = content.replace(
    'FC=€100K, Price/Preço=€50,\n            VC/CV=€30',
    'FC=€100K, Price=€50, VC=€30'
)
print("7. Example fix done")

with open('0_ACTIVE_NOW/BCG_Interview_Prep/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\nAll formula EN/PT separators fixed!")
