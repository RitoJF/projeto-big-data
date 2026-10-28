# Projeto Big Data – Mundo da Moda

Projeto de extensão da disciplina **Tópicos de Big Data com Python** (Análise e Desenvolvimento de Sistemas – Centro Universitário Estácio de Campo Grande/MS, 2026.2).

O projeto transforma os relatórios anuais de faturamento da loja **Mundo da Moda** (Aero Rancho, Campo Grande/MS), emitidos em PDF pelo sistema de gestão da empresa, em uma base histórica analisável e em um dashboard interativo.

## Fluxo de dados

```
Relatórios PDF (2023–2026) → extração (pdfplumber) → tratamento (Pandas)
→ base histórica em CSV → análise (Pandas + Plotly) → dashboard (Streamlit + Plotly)
```

Não há banco de dados: a base consolidada tem pouco mais de 1.300 linhas e fica em `dados/faturamento_historico.csv`.

## Estrutura

```
projeto-big-data/
├── dados/
│   ├── faturamento_2023.pdf ... faturamento_2026.pdf   # relatórios originais da empresa
│   └── faturamento_historico.csv                       # base consolidada (gerada pelo processamento)
└── scripts/
    ├── processamento_dados.py   # PDF → CSV
    ├── analisar_dados.py        # indicadores no terminal + gráfico 2025 × 2026
    └── dashboard.py             # dashboard Streamlit
```

## Dados de origem

Cada PDF tem uma página com uma matriz de **dias (01 a 31) × meses (janeiro a dezembro)**, com valores no padrão brasileiro (`1.234,56`) e os totais de cada mês no rodapé. Os dias que não existem no calendário (30/02, 31/04 etc.) aparecem como `0,00` e são descartados no processamento.

> O cabeçalho dos PDFs mostra "MUNDO DAS BOLSAS", nome que vem do sistema de gestão. O nome correto da empresa é **Mundo da Moda**.

O relatório de 2026 é **parcial**: cobre de 01/01 a 01/08/2026.

## Como executar (Ubuntu)

Requer Python 3. Rode todos os comandos **a partir da raiz do repositório**, porque os scripts usam caminhos relativos (`dados/...`).

### Primeira vez

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pandas pdfplumber plotly streamlit
```

Versões testadas: pandas 3.1.0, pdfplumber 0.11.10, plotly 7.1.0 e streamlit 1.66.1.

### Dashboard

```bash
source .venv/bin/activate        # em todo terminal novo
streamlit run scripts/dashboard.py
```

O dashboard abre em `http://localhost:8501`. Para encerrar, use **Ctrl+C**.

> Na primeira execução, o Streamlit pede um e-mail no terminal. O e-mail é opcional: aperte **Enter** para continuar.

### Outros scripts

```bash
python scripts/processamento_dados.py   # regenera dados/faturamento_historico.csv a partir dos PDFs
python scripts/analisar_dados.py        # imprime os indicadores e abre o gráfico 2025 × 2026
```

O CSV já está no repositório, então o processamento só precisa ser rodado de novo se os PDFs mudarem.

## O que o dashboard mostra

- Filtros por ano e por mês.
- Indicadores: faturamento total, média diária, maior faturamento diário, dias analisados e dias sem faturamento.
- Gráfico de faturamento mensal e gráfico da evolução diária.
- **Verificação da qualidade dos dados:** valores ausentes, registros duplicados, datas duplicadas ou faltantes, valores negativos e a conferência do total do ano com o "TOTAL GERAL" do relatório original.

## Limitações conhecidas

- Os arquivos, os anos e a data de corte de 2026 estão fixos em `processamento_dados.py`. Para incluir um ano novo é preciso editar o script e o dicionário `totais_oficiais` em `dashboard.py`.
- O processamento lê só a primeira página de cada PDF, o que funciona porque cada relatório tem uma página.

## Equipe

- Breno Soares Dourado
- Matteus Anderson Lopez Kill
- Rito Flora da Silva Júnior

Professor: Caique Evangelista Fernandes Lopes.
