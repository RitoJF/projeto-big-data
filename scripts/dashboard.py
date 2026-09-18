import streamlit as st
import pandas as pd
import plotly.express as px

def formatar_real(valor):
    valor_formatado = f"{valor:,.2f}"

    valor_formatado = valor_formatado.replace(",", "X")
    valor_formatado = valor_formatado.replace(".", ",")
    valor_formatado = valor_formatado.replace("X", ".")

    return f"R$ {valor_formatado}"


st.set_page_config(
    page_title="Dashboard - Mundo da Moda",
    layout="wide"
)

df = pd.read_csv(
    "dados/faturamento_historico.csv",
    parse_dates=["data"]
)


st.title("Dashboard de Faturamento")
st.write("Mundo da Moda")

st.sidebar.header("Filtros")


anos_disponiveis = sorted(df["ano"].unique())

ano_selecionado = st.sidebar.selectbox(
    "Selecione o ano:",
    anos_disponiveis
)

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
    11: "Novembro",
    12: "Dezembro"
}


meses_disponiveis = sorted(
    df[df["ano"] == ano_selecionado]["mes"].unique()
)

opcoes_meses = ["Todos"] + [
    nomes_meses[mes] for mes in meses_disponiveis
]

mes_selecionado = st.sidebar.selectbox(
    "Selecione o mês:",
    opcoes_meses
)

df_filtrado = df[
    df["ano"] == ano_selecionado
]

if mes_selecionado != "Todos":
    numero_mes = [
        numero
        for numero, nome in nomes_meses.items()
        if nome == mes_selecionado
    ][0]

    df_filtrado = df_filtrado[
        df_filtrado["mes"] == numero_mes
    ]


st.subheader(f"Análise do ano de {ano_selecionado}")

if ano_selecionado == 2026:
    st.warning(
        "Atenção: os dados de 2026 são parciais e correspondem "
        "ao período de 01/01/2026 a 01/08/2026."
    )


faturamento_total = df_filtrado["faturamento"].sum()
media_diaria = df_filtrado["faturamento"].mean()
maior_faturamento = df_filtrado["faturamento"].max()

dias_analisados = len(df_filtrado)

dias_sem_faturamento = (
    df_filtrado["faturamento"] == 0
).sum()


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Faturamento Total",
        formatar_real(faturamento_total)
    )

with col2:
    st.metric(
        "Média Diária",
        formatar_real(media_diaria)
    )

with col3:
    st.metric(
        "Maior Faturamento Diário",
        formatar_real(maior_faturamento)
    )

col4, col5 = st.columns(2)

with col4:
    st.metric(
        "Dias Analisados",
        dias_analisados
    )
with col5:
    st.metric(
        "Dias sem Faturamento",
        dias_sem_faturamento
    )

faturamento_mensal = (
    df_filtrado
    .groupby("mes")["faturamento"]
    .sum()
    .reset_index()
)

faturamento_mensal["nome_mes"] = (
    faturamento_mensal["mes"].map(nomes_meses)
)

fig_mensal = px.bar(
    faturamento_mensal,
    x="nome_mes",
    y="faturamento",
    title=f"Faturamento Mensal - {ano_selecionado}",
    labels={
        "nome_mes": "Mês",
        "faturamento": "Faturamento (R$)"
    },
    category_orders={
        "nome_mes": list(nomes_meses.values())
    }
)

st.plotly_chart(
    fig_mensal,
    use_container_width=True
)


fig_diario = px.line(
    df_filtrado,
    x="data",
    y="faturamento",
    title=f"Evolução Diária do Faturamento - {ano_selecionado}",
    labels={
        "data": "Data",
        "faturamento": "Faturamento (R$)"
    }
)

st.plotly_chart(
    fig_diario,
    use_container_width=True
)


valores_ausentes = df_filtrado.isnull().sum()
total_ausentes = valores_ausentes.sum()

registros_duplicados = df_filtrado.duplicated().sum()

datas_duplicadas = df_filtrado["data"].duplicated().sum()

data_inicial = df_filtrado["data"].min()
data_final = df_filtrado["data"].max()

datas_esperadas = pd.date_range(
    start=data_inicial,
    end=data_final,
    freq="D"
)

datas_faltantes = datas_esperadas.difference(
    df_filtrado["data"]
)

quantidade_datas_faltantes = len(datas_faltantes)

valores_negativos = (
    df_filtrado["faturamento"] < 0
).sum()

total_validacao = df_filtrado["faturamento"].sum()

totais_oficiais = {
    2023: 248292.47,
    2024: 297650.95,
    2025: 554876.47,
    2026: 788155.78
}

with st.expander("Verificação da Qualidade dos Dados"):

    st.write("### Resumo")

    st.write(f"Valores ausentes: {total_ausentes}")
    st.write(f"Registros duplicados: {registros_duplicados}")
    st.write(f"Datas duplicadas: {datas_duplicadas}")
    st.write(f"Datas faltantes: {quantidade_datas_faltantes}")
    st.write(f"Valores negativos de faturamento: {valores_negativos}")
    st.write(
        f"Faturamento do período: {formatar_real(total_validacao)}"
    )

    st.write("### Valores ausentes por coluna")
    st.dataframe(valores_ausentes)

    if mes_selecionado == "Todos":

        total_oficial = totais_oficiais[ano_selecionado]

        diferenca = abs(
            total_validacao - total_oficial
        )

        if diferenca < 0.01:
            st.success(
                "Total conferido com o relatório original."
            )
        else:
            st.error(
                "O total calculado não corresponde ao relatório original."
            )