import pandas as pd
import pdfplumber


def converter_valor(valor):
    valor = valor.replace(".", "")
    valor = valor.replace(",", ".")
    return float(valor)


def processar_pdf(caminho_pdf, ano):
    registros = []

    with pdfplumber.open(caminho_pdf) as pdf:
        pagina = pdf.pages[0]
        texto = pagina.extract_text()

    linhas = texto.split("\n")

    for linha in linhas:
        partes = linha.split()

        if len(partes) == 13 and partes[0].isdigit():

            dia = int(partes[0])

            for mes in range(1, 13):
                valor = converter_valor(partes[mes])

                registros.append({
                    "ano": ano,
                    "mes": mes,
                    "dia": dia,
                    "faturamento": valor
                })

    df = pd.DataFrame(registros)

    df["data"] = pd.to_datetime(
        dict(
            year=df["ano"],
            month=df["mes"],
            day=df["dia"]
        ),
        errors="coerce"
    )

    df = df.dropna(subset=["data"])
    df = df.sort_values("data")
    df = df.reset_index(drop=True)

    return df

df_2023 = processar_pdf("dados/faturamento_2023.pdf", 2023)
df_2024 = processar_pdf("dados/faturamento_2024.pdf", 2024)
df_2025 = processar_pdf("dados/faturamento_2025.pdf", 2025)
df_2026 = processar_pdf("dados/faturamento_2026.pdf", 2026)

df_2026 = df_2026[df_2026["data"] <= "2026-08-01"]

df_2026 = df_2026.reset_index(drop=True)

df_completo = pd.concat(
    [df_2023, df_2024, df_2025, df_2026],
    ignore_index=True
)

print("\nBase completa:")
print(df_completo)

print("\nQuantidade total de registros:")
print(len(df_completo))
print("\nRegistros por ano:")
print(df_completo.groupby("ano").size())

total_por_ano = df_completo.groupby("ano")["faturamento"].sum()

print("\nFaturamento por ano:")
print(total_por_ano)

df_completo.to_csv(
    "dados/faturamento_historico.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nBase histórica criada com sucesso!")