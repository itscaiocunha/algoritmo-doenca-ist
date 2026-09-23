"""Pré-processamento: variáveis-alvo e montagem do vetor de features."""

from pyspark.ml import Pipeline
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
from pyspark.sql.functions import col, when

from ist_bigdata import config


def adicionar_variaveis_alvo(df):
    """Cria as colunas binárias `tem_ist` e `curavel`."""
    return (
        df.withColumn("tem_ist", when(col("doenca").isin(config.ISTS), 1).otherwise(0))
          .withColumn("curavel", when(col("doenca").isin(config.CURAVEIS), 1).otherwise(0))
    )


def construir_pipeline_features():
    """StringIndexer -> OneHotEncoder -> VectorAssembler.

    - StringIndexer converte categorias em índices (`handleInvalid='keep'` evita
      erro com valores não vistos);
    - OneHotEncoder evita que o modelo interprete uma ordem inexistente entre categorias;
    - VectorAssembler reúne tudo na coluna `features`, consumida pelos modelos.
    """
    indexers = [
        StringIndexer(inputCol=coluna, outputCol=f"{prefixo}Idx", handleInvalid="keep")
        for coluna, prefixo in config.COLUNAS_CATEGORICAS.items()
    ]
    encoders = [
        OneHotEncoder(inputCol=f"{prefixo}Idx", outputCol=f"{prefixo}Vec")
        for prefixo in config.COLUNAS_CATEGORICAS.values()
    ]
    assembler = VectorAssembler(
        inputCols=config.COLUNAS_NUMERICAS + [f"{p}Vec" for p in config.COLUNAS_CATEGORICAS.values()],
        outputCol="features",
    )
    return Pipeline(stages=indexers + encoders + [assembler])


def codificar_features(df):
    encoded_df = construir_pipeline_features().fit(df).transform(df)
    encoded_df.select("id", "idade", "renda_media", "genero", "localidade", "doenca", "tem_ist", "curavel").show(5)
    return encoded_df
