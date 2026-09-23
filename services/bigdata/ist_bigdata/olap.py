"""Análises OLAP em Spark SQL sobre a tabela `fato_casos` (somente ISTs)."""

import matplotlib.pyplot as plt
import seaborn as sns

from ist_bigdata import config
from ist_bigdata.graficos import salvar_figura

_FILTRO_ISTS = ", ".join(f"'{d}'" for d in config.ISTS)
_AZUL = sns.color_palette("Blues", n_colors=6)[4]


def _consultar(spark, sql):
    return spark.sql(sql.format(ists=_FILTRO_ISTS)).toPandas()


def _formatar_eixos(titulo, rotulo_x, rotulo_y):
    plt.title(titulo)
    plt.xlabel(rotulo_x)
    plt.ylabel(rotulo_y)
    plt.xticks(rotation=45)
    plt.tight_layout()


def casos_por_localidade(spark):
    resultado = _consultar(spark, """
        SELECT localidade, COUNT(*) AS total_casos
        FROM fato_casos
        WHERE doenca IN ({ists})
        GROUP BY localidade
        ORDER BY total_casos DESC
    """)
    plt.figure(figsize=(18, 9))
    sns.barplot(data=resultado, x="localidade", y="total_casos", color=_AZUL)
    _formatar_eixos("Casos por Localidade (Somente ISTs)", "Localidade", "Número de Casos")
    salvar_figura("casos_por_localidade.png")


def media_idade_por_doenca(spark):
    resultado = _consultar(spark, """
        SELECT doenca, ROUND(AVG(idade), 2) AS media_idade
        FROM fato_casos
        WHERE doenca IN ({ists})
        GROUP BY doenca
        ORDER BY media_idade DESC
    """)
    plt.figure(figsize=(10, 6))
    sns.barplot(data=resultado, x="doenca", y="media_idade", palette="Blues")
    _formatar_eixos("Média de Idade por Tipo de IST", "Doença", "Média de Idade")
    salvar_figura("media_idade_por_doenca.png")


def media_renda_por_escolaridade_e_doenca(spark):
    resultado = _consultar(spark, """
        SELECT nivel_educacional, doenca, ROUND(AVG(renda_media), 2) AS media_renda
        FROM fato_casos
        WHERE doenca IN ({ists})
        GROUP BY nivel_educacional, doenca
        ORDER BY media_renda DESC
    """)
    plt.figure(figsize=(15, 6))
    sns.barplot(data=resultado, x="nivel_educacional", y="media_renda", hue="doenca", palette="Blues")
    _formatar_eixos("Média de Renda por Escolaridade e Doença (Somente ISTs)", "Nível Educacional", "Média de Renda")
    salvar_figura("media_renda_por_escolaridade_e_doenca.png")


def casos_por_ano(spark):
    resultado = _consultar(spark, """
        SELECT YEAR(data_teste) AS ano_teste, COUNT(*) AS total_casos
        FROM fato_casos
        WHERE doenca IN ({ists})
        GROUP BY ano_teste
        ORDER BY ano_teste
    """)
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=resultado, x="ano_teste", y="total_casos", marker="o", color=_AZUL)
    _formatar_eixos("Número de Casos por Ano (Somente ISTs)", "Ano", "Total de Casos")
    salvar_figura("casos_por_ano_olap.png")


ANALISES = {
    "Casos por Localidade": casos_por_localidade,
    "Média de Idade por Doença": media_idade_por_doenca,
    "Média de Renda por Escolaridade e Doença": media_renda_por_escolaridade_e_doenca,
    "Casos por Ano": casos_por_ano,
}


def executar_analise(spark, escolha):
    ANALISES[escolha](spark)


def executar_todas(spark):
    for analise in ANALISES.values():
        analise(spark)
