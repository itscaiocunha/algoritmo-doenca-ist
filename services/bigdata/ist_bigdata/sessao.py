"""Inicialização da SparkSession e leitura dos dados tratados."""

import os

import findspark

from ist_bigdata import config


def iniciar_spark():
    """Cria (ou reaproveita) a SparkSession — a porta de entrada para o Spark no Python."""
    os.environ["JAVA_HOME"] = config.JAVA_HOME
    findspark.init()

    from pyspark.sql import SparkSession

    builder = SparkSession.builder.appName(config.SPARK_APP_NAME)
    for chave, valor in config.SPARK_CONFIG.items():
        builder = builder.config(chave, valor)
    spark = builder.getOrCreate()

    print("Apache Spark configurado e iniciado!")
    print("Versão do Spark:", spark.version)
    return spark


def carregar_dados(spark, caminho=config.ARQUIVO_DADOS):
    """Lê o CSV tratado pela etapa em R, inferindo o schema a partir dos dados."""
    df = spark.read.csv(caminho, header=True, inferSchema=True)

    print("\nSchema do DataFrame:")
    df.printSchema()
    print("\nPrimeiras 5 linhas:")
    df.show(5)
    return df
