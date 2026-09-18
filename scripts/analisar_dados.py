import pandas as pd 
import plotly.express as px

df = pd.read_csv(
    "dados/faturamento_historico.csv",
    parse_dates=["data"]
)

print(df.head())
print("\nTipos das colunas:")
print(df.dtypes)

faturamento_total = df["faturamento"].sum()

media_diaria = df["faturamento"].mean()

maior_faturamento = df["faturamento"].max()

dias_sem_faturamento = (df["faturamento"] == 0).sum()

print("\n--- INDICADORES ---")

print("Faturamento total:", faturamento_total)
print("Média diária:", media_diaria)
print("Maior faturamento diário:", maior_faturamento)
print("Dias sem faturamento:", dias_sem_faturamento)

indice_maior = df["faturamento"].idxmax()

registro_maior = df.loc[indice_maior]

print("\n--- RECORDE DE FATURAMENTO ---")
print(registro_maior)

faturamento_por_ano = df.groupby("ano")["faturamento"].sum()

print("\n--- FATURAMENTO POR ANO ---")
print(faturamento_por_ano)

crescimento_anual = faturamento_por_ano.pct_change() * 100

print("\n--- CRESCIMENTO ANUAL (%) ---")
print(crescimento_anual)

faturamento_mensal = (
    df.groupby(["ano", "mes"])["faturamento"]
    .sum()
    .reset_index()
)

print("\n--- FATURAMENTO MENSAL ---")
print(faturamento_mensal)

anos_completos = df[df["ano"] <= 2025]

media_por_mes = (
    anos_completos.groupby("mes")["faturamento"]
    .sum()
    .groupby("mes")
    .sum()
)

mensal_anos_completos = faturamento_mensal[
    faturamento_mensal["ano"] <= 2025
]

media_por_mes = (
    mensal_anos_completos
    .groupby("mes")["faturamento"]
    .mean()
)

print("\n--- MÉDIA DE FATURAMENTO POR MÊS ---")
print(media_por_mes)

mes_maior_media = media_por_mes.idxmax()
valor_maior_media = media_por_mes.max()

print("\nMês com maior média:")
print(mes_maior_media)

print("\nMaior média mensal:")
print(valor_maior_media)

nomes_meses = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembero",
    12: "Dezembro"
}

print("\nMês com maior média:")
print(nomes_meses[mes_maior_media])

periodo_2025 = df[
    (df["ano"] == 2025) &
    (df["mes"] <= 7)
]

periodo_2026 = df[
    (df["ano"] == 2026) &
    (df["mes"] <= 7)
]

total_2025_jan_jul = periodo_2025["faturamento"].sum()
total_2026_jan_jul = periodo_2026["faturamento"].sum()

print("\n--- COMPARAÇÃO JAN-JUL ---")

print("2025:", total_2025_jan_jul)
print("2026:", total_2026_jan_jul)

crescimento = (
    (total_2026_jan_jul - total_2025_jan_jul)
    / total_2025_jan_jul
) * 100

print("\nCrescimento de Jan-Jul 2025 para Jan-Jul 2026:")
print(crescimento)

mensal_2025 = faturamento_mensal[
    (faturamento_mensal["ano"] == 2025) &
    (faturamento_mensal["mes"] <= 7)
]

mensal_2026 = faturamento_mensal[
    (faturamento_mensal["ano"] == 2026) &
    (faturamento_mensal["mes"] <= 7)
]

print("\n--- MENSAL 2025 ---")
print(mensal_2025)

print("\n--- MENSAL 2026 ---")
print(mensal_2026)

comparacao = pd.merge(
    mensal_2025,
    mensal_2026,
    on="mes",
    suffixes=("_2025", "_2026")
)

print("\n--- COMPARAÇÃO 2025 x 2026 ---")
print(comparacao)

comparacao["crescimento_percentual"] = (
    (comparacao["faturamento_2026"] - comparacao["faturamento_2025"])
    / comparacao["faturamento_2025"]
) * 100

print("\n--- CRESCIMENTO POR MÊS ---")

print(
    comparacao[
        [
            "mes",
            "faturamento_2025",
            "faturamento_2026",
            "crescimento_percentual"
        ]
    ]
)

comparacao["nome_mes"] = comparacao["mes"].map(nomes_meses)

fig = px.bar(
    comparacao,
    x="nome_mes",
    y=["faturamento_2025", "faturamento_2026"],
    barmode="group",
    title="Comparação de Faturamento Mensal - 2025 x 2026",

    labels={
        "nome_mes": "Mês",
        "value": "Faturamento (R$)",
        "variable": "Ano"
    },
    
    category_orders={
        "nome_mes": [
            "Janeiro",
            "Fevereiro",
            "Março",
            "Abril",
            "Maio",
            "Junho",
            "Julho"
        ]
    }
)

fig.update_layout(
    yaxis_tickprefix="R$ ",
    legend_title_text="Ano"
)

fig.for_each_trace(
    lambda trace: trace.update(
        name=trace.name.replace("faturamento_", "")
    )
)

fig.show()