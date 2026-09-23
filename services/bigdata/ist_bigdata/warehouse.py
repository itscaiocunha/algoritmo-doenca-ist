"""Data Warehouse: modelo dimensional (esquema estrela) registrado como views SQL."""

from pyspark.sql.functions import col, dayofmonth, month, when, year

from ist_bigdata import config


def construir_modelo_dimensional(df):
    """Retorna um dicionário `nome_da_tabela -> DataFrame` com a fato e as dimensões."""
    dim_tempo = (
        df.select("data_teste").dropDuplicates()
          .withColumn("ano", year("data_teste"))
          .withColumn("mes", month("data_teste"))
          .withColumn("dia", dayofmonth("data_teste"))
    )
    dim_doenca = (
        df.select("doenca").dropDuplicates()
          .withColumn("curavel", when(col("doenca").isin(config.CURAVEIS), "Sim").otherwise("Não"))
    )
    fato_casos = df.select(
        "id", "idade", "renda_media", "data_teste", "localidade",
        "doenca", "nivel_educacional", "genero", "tem_ist", "curavel"
    )

    tabelas = {
        "fato_casos": fato_casos,
        "dim_tempo": dim_tempo,
        "dim_localidade": df.select("localidade").dropDuplicates(),
        "dim_doenca": dim_doenca,
        "dim_escolaridade": df.select("nivel_educacional").dropDuplicates(),
        "dim_genero": df.select("genero").dropDuplicates(),
    }
    print("\nTabelas de dimensões e fato criadas com sucesso!")
    return tabelas


def registrar_views(tabelas):
    """Registra cada tabela como view temporária para consultas em Spark SQL."""
    for nome, tabela in tabelas.items():
        tabela.createOrReplaceTempView(nome)
