"""Processamento de Linguagem Natural: representação TF-IDF da coluna `doenca`."""

from pyspark.ml import Pipeline
from pyspark.ml.feature import IDF, HashingTF, StopWordsRemover, Tokenizer


def aplicar_tfidf(df, num_features=100):
    """Tokeniza, remove stopwords e gera a coluna vetorial `textFeatures`."""
    pipeline = Pipeline(stages=[
        Tokenizer(inputCol="doenca", outputCol="palavras"),
        StopWordsRemover(inputCol="palavras", outputCol="palavras_filtradas"),
        HashingTF(inputCol="palavras_filtradas", outputCol="rawFeatures", numFeatures=num_features),
        IDF(inputCol="rawFeatures", outputCol="textFeatures"),
    ])
    tfidf_data = pipeline.fit(df).transform(df)

    print("\nResultados do TF-IDF:")
    tfidf_data.select("doenca", "textFeatures").show(5, truncate=False)
    return tfidf_data
