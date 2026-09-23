"""Agregações no paradigma Hadoop MapReduce, implementadas com RDDs do Spark."""

import matplotlib.pyplot as plt
import seaborn as sns
from pyspark.sql.functions import col

from ist_bigdata import config
from ist_bigdata.graficos import salvar_figura


def faixa_etaria(idade):
    if idade < 18:
        return "0-17"
    elif idade < 25:
        return "18-24"
    elif idade < 35:
        return "25-34"
    elif idade < 45:
        return "35-44"
    elif idade < 60:
        return "45-59"
    else:
        return "60+"


def media_renda_por_ist(df):
    """Map: (doenca, (renda, 1)) -> Reduce: soma renda e contagem -> MapValues: média."""
    ist_rdd = df.filter(col("doenca").isin(config.ISTS)).rdd

    media_renda = (
        ist_rdd.map(lambda row: (row.doenca, (row.renda_media, 1)))
               .reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1]))
               .mapValues(lambda v: round(v[0] / v[1], 2))
               .toDF(["Doenca", "Media_Renda"])
    )
    media_renda.show()

    plt.figure(figsize=(10, 6))
    sns.barplot(data=media_renda.toPandas(), x="Doenca", y="Media_Renda", palette="Blues")
    plt.title("Média de Renda por Tipo de IST - Análise Hadoop (MapReduce)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    salvar_figura("media_renda_mapreduce.png")
    return media_renda


def distribuicao_faixa_etaria(df):
    """Map: (faixa_etaria, 1) -> Reduce: soma das ocorrências por faixa."""
    resultado = (
        df.rdd.map(lambda row: (faixa_etaria(row.idade), 1))
              .reduceByKey(lambda a, b: a + b)
              .toDF(["Faixa_Etaria", "Total_de_Casos"])
    )
    resultado.show()

    plt.figure(figsize=(8, 6))
    sns.barplot(data=resultado.toPandas(), x="Faixa_Etaria", y="Total_de_Casos", palette="Blues")
    plt.title("Distribuição de Casos por Faixa Etária - Análise Hadoop (MapReduce)")
    plt.tight_layout()
    salvar_figura("distribuicao_faixa_etaria_mapreduce.png")
    return resultado
