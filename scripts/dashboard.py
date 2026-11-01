from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


PASTA_PROJETO = Path(__file__).resolve().parent.parent
CAMINHO_CSV = PASTA_PROJETO / "dados" / "faturamento_historico.csv"
CAMINHO_CSS = PASTA_PROJETO / "css" / "style.css"


def formatar_real(valor):
    valor_formatado = f"{valor:,.2f}"
    valor_formatado = valor_formatado.replace(",", "X")
    valor_formatado = valor_formatado.replace(".", ",")
    valor_formatado = valor_formatado.replace("X", ".")
    return f"R$ {valor_formatado}"


st.set_page_config(
    page_title="Dashboard - Mundo da Moda",
    layout="wide",
    initial_sidebar_state="collapsed",
)


if CAMINHO_CSS.exists():
    css = CAMINHO_CSS.read_text(encoding="utf-8")
    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True,
    )


df = pd.read_csv(
    CAMINHO_CSV,
    parse_dates=["data"],
)

st.markdown(
    """
    <div class="hero-moda">
        <div class="rua-moda" aria-hidden="true">
            <div class="sol"></div>
            <div class="nuvem nuvem-esquerda"></div>
            <div class="nuvem nuvem-direita"></div>
            <div class="predio predio-esquerdo">
                <span></span><span></span>
                <div class="porta-predio"></div>
            </div>
            <div class="predio predio-alto-esquerdo">
                <span></span><span></span><span></span>
                <span></span><span></span><span></span>
                <div class="porta-predio"></div>
            </div>
            <div class="predio predio-alto-direito">
                <span></span><span></span><span></span>
                <span></span><span></span><span></span>
                <div class="porta-predio"></div>
            </div>
            <div class="predio predio-direito">
                <span></span><span></span>
                <div class="porta-predio"></div>
            </div>
            <div class="poste poste-esquerdo">
                <span class="lampada"></span>
            </div>
            <div class="poste poste-direito">
                <span class="lampada"></span>
            </div>
            <div class="hidrante hidrante-esquerdo"><span></span></div>
            <div class="hidrante hidrante-direito"><span></span></div>
            <div class="loja-desenho">
                <div class="placa-loja">Mundo da Moda</div>
                <div class="toldo-loja"></div>
                <div class="vitrine vitrine-esquerda">👗</div>
                <div class="porta-loja"></div>
                <div class="vitrine vitrine-direita">🛍️</div>
            </div>
            <div class="carro carro-azul"><span></span><span></span></div>
            <div class="carro carro-coral"><span></span><span></span></div>
            <div class="rua-asfalto"></div>
        </div>
        <p class="hero-etiqueta">PAINEL DE VENDAS</p>
        <h1>Dashboard de Faturamento</h1>
        <p class="hero-descricao">
            Acompanhe o desempenho da loja e explore os resultados por ano e mês.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

anos_disponiveis = sorted(df["ano"].unique())

ano_atual = pd.Timestamp.now().year
ano_padrao = (
    ano_atual
    if ano_atual in anos_disponiveis
    else max(anos_disponiveis)
)

if "ano_grafico" not in st.session_state:
    st.session_state["ano_grafico"] = ano_padrao

st.markdown(
    '<div class="titulo-escolha-ano">'
    'Escolha qual ano você gostaria de analisar'
    '</div>',
    unsafe_allow_html=True,
)

col_vazia_esquerda, col_seletor_ano, col_vazia_direita = st.columns(
    [1, 2, 1]
)

with col_seletor_ano:
    ano_grafico = st.selectbox(
        "Ano",
        anos_disponiveis,
        key="ano_grafico",
        label_visibility="collapsed",
    )


nomes_meses_grafico = {
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
    12: "Dezembro",
}

col_grafico, col_controles = st.columns([4, 1], gap="large")
def configurar_grafico(fig, altura=380):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#1B2432",
        plot_bgcolor="#1B2432",
        font_color="#F9FAFB",
        yaxis_tickprefix="R$ ",
        yaxis_tickformat=",.0f",
        height=altura,
        margin=dict(l=35, r=20, t=25, b=45),
    )
    return fig


# Linha 1: faturamento mensal do ano escolhido e comparação entre anos.
col_anual, col_comparacao = st.columns(2, gap="large")

with col_anual:
    st.markdown(
        f'<h2 class="titulo-grafico">Faturamento de {ano_grafico}</h2>',
        unsafe_allow_html=True,
    )

    tipo_grafico = st.selectbox(
        "Estilo do gráfico:",
        ["Linha", "Barras", "Área"],
        key="tipo_grafico",
    )

    df_ano_grafico = df[df["ano"] == ano_grafico]

    dados_mensais_grafico = (
        df_ano_grafico
        .groupby("mes", as_index=False)["faturamento"]
        .sum()
    )

    dados_mensais_grafico["nome_mes"] = (
        dados_mensais_grafico["mes"].map(nomes_meses_grafico)
    )

    opcoes_grafico = {
        "data_frame": dados_mensais_grafico,
        "x": "nome_mes",
        "y": "faturamento",
        "category_orders": {
            "nome_mes": list(nomes_meses_grafico.values()),
        },
        "labels": {
            "nome_mes": "Mês",
            "faturamento": "Faturamento (R$)",
        },
    }

    if tipo_grafico == "Linha":
        fig_ano = px.line(**opcoes_grafico, markers=True)
        fig_ano.update_traces(
            line_color="#B84DFF",
            line_width=4,
            marker_size=8,
        )
    elif tipo_grafico == "Barras":
        fig_ano = px.bar(
            **opcoes_grafico,
            color_discrete_sequence=["#F08CA7"],
        )
    else:
        fig_ano = px.area(
            **opcoes_grafico,
            color_discrete_sequence=["#F08CA7"],
        )
        fig_ano.update_traces(
            line_color="#F08CA7",
            fillcolor="rgba(184, 77, 255, 0.25)",
        )

    configurar_grafico(fig_ano)
    fig_ano.update_xaxes(tickangle=-35)

    st.plotly_chart(fig_ano, use_container_width=True)

    texto_grafico = "Cada ponto ou barra mostra o faturamento total de um mês."
    if ano_grafico == 2026:
        texto_grafico += " Os dados de 2026 são parciais, até 01/08/2026."

    st.caption(texto_grafico)


with col_comparacao:
    st.subheader("Comparação mensal do faturamento")

    if "ano_comparacao_1" not in st.session_state:
        st.session_state["ano_comparacao_1"] = anos_disponiveis[-2]

    if "ano_comparacao_2" not in st.session_state:
        st.session_state["ano_comparacao_2"] = anos_disponiveis[-1]

    ano_comparacao_1 = st.selectbox(
        "Primeiro ano:",
        anos_disponiveis,
        key="ano_comparacao_1",
    )

    opcoes_segundo_ano = [
        ano for ano in anos_disponiveis
        if ano != ano_comparacao_1
    ]

    if st.session_state["ano_comparacao_2"] not in opcoes_segundo_ano:
        st.session_state["ano_comparacao_2"] = opcoes_segundo_ano[-1]

    ano_comparacao_2 = st.selectbox(
        "Segundo ano:",
        opcoes_segundo_ano,
        key="ano_comparacao_2",
    )

    anos_escolhidos = [ano_comparacao_1, ano_comparacao_2]
    ultimo_mes = 7 if 2026 in anos_escolhidos else 12

    df_comparacao = df[
        df["ano"].isin(anos_escolhidos)
        & df["mes"].between(1, ultimo_mes)
    ]

    dados_comparacao = (
        df_comparacao
        .groupby(["mes", "ano"], as_index=False)["faturamento"]
        .sum()
    )

    dados_comparacao["nome_mes"] = (
        dados_comparacao["mes"].map(nomes_meses_grafico)
    )
    dados_comparacao["ano"] = dados_comparacao["ano"].astype(str)

    anos_como_texto = [
        str(ano_comparacao_1),
        str(ano_comparacao_2),
    ]

    fig_comparacao = px.bar(
        dados_comparacao,
        x="nome_mes",
        y="faturamento",
        color="ano",
        barmode="group",
        category_orders={
            "nome_mes": list(nomes_meses_grafico.values()),
            "ano": anos_como_texto,
        },
        color_discrete_map={
            anos_como_texto[0]: "#63D9E8",
            anos_como_texto[1]: "#F08CA7",
        },
        labels={
            "nome_mes": "Mês",
            "faturamento": "Faturamento (R$)",
            "ano": "Ano",
        },
    )

    configurar_grafico(fig_comparacao)
    fig_comparacao.update_xaxes(tickangle=-35)

    st.plotly_chart(fig_comparacao, use_container_width=True)

    periodo_comparado = (
        "janeiro a julho"
        if ultimo_mes == 7
        else "janeiro a dezembro"
    )
    st.caption(
        f"Compara o faturamento de {periodo_comparado} "
        "nos dois anos escolhidos."
    )


# Linha 2: faturamento diário do mês escolhido e média diária por mês.
col_diario, col_media_mensal = st.columns(2, gap="large")

meses_do_ano = sorted(
    df.loc[df["ano"] == ano_grafico, "mes"].unique()
)

opcoes_meses_diario = [
    nomes_meses_grafico[mes] for mes in meses_do_ano
]

dias_por_mes = (
    df[df["ano"] == ano_grafico]
    .groupby("mes")["data"]
    .count()
)

meses_com_varios_dias = [
    mes for mes in meses_do_ano
    if dias_por_mes[mes] > 1
]

mes_padrao = (
    max(meses_com_varios_dias)
    if meses_com_varios_dias
    else max(meses_do_ano)
)

with col_diario:
    st.subheader(f"Faturamento diário de {ano_grafico}")

    mes_selecionado_diario = st.selectbox(
        "Mês:",
        opcoes_meses_diario,
        index=opcoes_meses_diario.index(
            nomes_meses_grafico[mes_padrao]
        ),
        key=f"mes_diario_{ano_grafico}",
    )

    numero_mes_selecionado = next(
        mes
        for mes, nome in nomes_meses_grafico.items()
        if nome == mes_selecionado_diario
    )

    df_diario = df[
        (df["ano"] == ano_grafico)
        & (df["mes"] == numero_mes_selecionado)
    ].sort_values("data")

    fig_diario = px.line(
        df_diario,
        x="data",
        y="faturamento",
        markers=True,
        labels={
            "data": "Dia",
            "faturamento": "Faturamento (R$)",
        },
    )

    fig_diario.update_traces(
        line_color="#63D9E8",
        line_width=3,
        marker_size=5,
    )
    configurar_grafico(fig_diario, altura=400)
    fig_diario.update_xaxes(
        tickmode="linear",
        tick0=f"{ano_grafico}-{numero_mes_selecionado:02d}-01",
        dtick=86400000,
        tickformat="%d",
        tickangle=-45,
        automargin=True,
    )

    st.plotly_chart(fig_diario, use_container_width=True)
    st.caption(
        "Cada ponto mostra o faturamento de um dia do mês selecionado."
    )


with col_media_mensal:
    st.subheader(f"Faturamento diário médio por mês — {ano_grafico}")

    df_ano = df[df["ano"] == ano_grafico].copy()

    media_diaria_por_mes = (
        df_ano
        .groupby("mes", as_index=False)["faturamento"]
        .mean()
        .rename(columns={"faturamento": "media_diaria"})
    )

    media_diaria_por_mes["nome_mes"] = (
        media_diaria_por_mes["mes"].map(nomes_meses_grafico)
    )

    fig_media_mensal = px.bar(
        media_diaria_por_mes,
        x="nome_mes",
        y="media_diaria",
        category_orders={
            "nome_mes": list(nomes_meses_grafico.values()),
        },
        labels={
            "nome_mes": "Mês",
            "media_diaria": "Faturamento diário médio (R$)",
        },
        color_discrete_sequence=["#9A59FF"],
    )

    configurar_grafico(fig_media_mensal)
    fig_media_mensal.update_xaxes(tickangle=-35)

    st.plotly_chart(fig_media_mensal, use_container_width=True)

    if ano_grafico == 2026:
        st.caption(
            "Agosto de 2026 está parcial; a média considera os dias "
            "registrados até 01/08/2026."
        )
    else:
        st.caption("Cada barra mostra a média diária de faturamento do mês.")


# Linha 3: padrão por dia da semana e maiores faturamentos diários.
col_dia_semana, col_maiores_dias = st.columns(2, gap="large")

df_ano = df[df["ano"] == ano_grafico].copy()

nomes_dias = {
    0: "Segunda-feira",
    1: "Terça-feira",
    2: "Quarta-feira",
    3: "Quinta-feira",
    4: "Sexta-feira",
    5: "Sábado",
    6: "Domingo",
}

ordem_dias = list(nomes_dias.values())
df_ano["nome_dia_semana"] = (
    df_ano["data"].dt.dayofweek.map(nomes_dias)
)

media_por_dia_semana = (
    df_ano
    .groupby("nome_dia_semana", as_index=False)["faturamento"]
    .mean()
)

with col_dia_semana:
    st.subheader(f"Faturamento médio por dia da semana — {ano_grafico}")

    fig_dia_semana = px.bar(
        media_por_dia_semana,
        x="nome_dia_semana",
        y="faturamento",
        category_orders={"nome_dia_semana": ordem_dias},
        labels={
            "nome_dia_semana": "Dia da semana",
            "faturamento": "Faturamento médio (R$)",
        },
        color_discrete_sequence=["#F08CA7"],
    )

    configurar_grafico(fig_dia_semana)
    fig_dia_semana.update_xaxes(tickangle=-35)

    st.plotly_chart(fig_dia_semana, use_container_width=True)
    st.caption("A média inclui os dias registrados com faturamento zero.")


with col_maiores_dias:
    st.subheader(f"10 dias de maior faturamento — {ano_grafico}")

    dez_melhores_dias = (
        df_ano
        .nlargest(10, "faturamento")
        .copy()
    )
    dez_melhores_dias["data_texto"] = (
        dez_melhores_dias["data"].dt.strftime("%d/%m/%Y")
    )
    dez_melhores_dias = dez_melhores_dias.sort_values("faturamento")

    fig_melhores_dias = px.bar(
        dez_melhores_dias,
        x="faturamento",
        y="data_texto",
        orientation="h",
        labels={
            "data_texto": "Data",
            "faturamento": "Faturamento (R$)",
        },
        color_discrete_sequence=["#D89BFF"],
    )

    configurar_grafico(fig_melhores_dias)
    fig_melhores_dias.update_layout(yaxis_title="Data")

    st.plotly_chart(fig_melhores_dias, use_container_width=True)
    st.caption("Mostra as dez datas com maior faturamento no ano selecionado.")


# Linha 4: acumulado ocupa toda a largura.
st.subheader("Faturamento acumulado: comparar dois anos")

if "ano_acumulado_1" not in st.session_state:
    st.session_state["ano_acumulado_1"] = anos_disponiveis[-2]

if "ano_acumulado_2" not in st.session_state:
    st.session_state["ano_acumulado_2"] = anos_disponiveis[-1]

col_acumulado_1, col_acumulado_2 = st.columns(2)

with col_acumulado_1:
    ano_acumulado_1 = st.selectbox(
        "Primeiro ano:",
        anos_disponiveis,
        key="ano_acumulado_1",
    )

opcoes_ano_acumulado_2 = [
    ano for ano in anos_disponiveis
    if ano != ano_acumulado_1
]

if st.session_state["ano_acumulado_2"] not in opcoes_ano_acumulado_2:
    st.session_state["ano_acumulado_2"] = opcoes_ano_acumulado_2[-1]

with col_acumulado_2:
    ano_acumulado_2 = st.selectbox(
        "Segundo ano:",
        opcoes_ano_acumulado_2,
        key="ano_acumulado_2",
    )

anos_acumulados = [ano_acumulado_1, ano_acumulado_2]
ultimo_mes_acumulado = 7 if 2026 in anos_acumulados else 12

df_acumulado = df[
    df["ano"].isin(anos_acumulados)
    & df["mes"].between(1, ultimo_mes_acumulado)
].copy()

df_acumulado["data_referencia"] = pd.to_datetime(
    {
        "year": 2000,
        "month": df_acumulado["mes"],
        "day": df_acumulado["dia"],
    },
    errors="coerce",
)

df_acumulado = (
    df_acumulado
    .dropna(subset=["data_referencia"])
    .sort_values(["ano", "data_referencia"])
)

df_acumulado["faturamento_acumulado"] = (
    df_acumulado
    .groupby("ano")["faturamento"]
    .cumsum()
)
df_acumulado["ano_texto"] = df_acumulado["ano"].astype(str)

fig_acumulado = px.line(
    df_acumulado,
    x="data_referencia",
    y="faturamento_acumulado",
    color="ano_texto",
    labels={
        "data_referencia": "Data do ano",
        "faturamento_acumulado": "Faturamento acumulado (R$)",
        "ano_texto": "Ano",
    },
    color_discrete_map={
        str(ano_acumulado_1): "#63D9E8",
        str(ano_acumulado_2): "#F08CA7",
    },
)

fig_acumulado.update_traces(line_width=3)
fig_acumulado.update_layout(
    hovermode="x unified",
    legend_title_text="Ano",
)

configurar_grafico(fig_acumulado, altura=440)

st.plotly_chart(fig_acumulado, use_container_width=True)

if ultimo_mes_acumulado == 7:
    st.caption(
        "Compara o faturamento acumulado de janeiro a julho, "
        "usando meses completos para incluir 2026."
    )
else:
    st.caption(
        "Compara o faturamento acumulado de janeiro a dezembro."
    )
st.image(
    PASTA_PROJETO / "imagens" / "Gengar.png",
    width=64,
)