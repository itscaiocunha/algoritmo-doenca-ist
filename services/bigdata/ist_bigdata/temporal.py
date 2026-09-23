"""Análise temporal: número de registros por ano de teste."""

import matplotlib.pyplot as plt
from pyspark.sql.functions import count, year

from ist_bigdata.graficos import salvar_figura


def adicionar_ano_teste(df):
    return df.withColumn("ano_teste", year("data_teste"))


def casos_por_ano(df):
    casos_por_ano_pd = df.groupBy("ano_teste").agg(count("id").alias("num_casos")).toPandas()

    plt.figure(figsize=(10, 6))
    plt.bar(casos_por_ano_pd["ano_teste"], casos_por_ano_pd["num_casos"], color='lightblue')
    plt.xlabel("Ano")
    plt.ylabel("Número de Testes")
    plt.title("Número de Testes Realizados por Ano (todos os registros)")
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    salvar_figura("casos_por_ano.png")
    return casos_por_ano_pd
