"""Processamento, análise e modelagem dos dados de ISTs com Apache Spark.

Cada módulo corresponde a uma etapa do notebook `main.ipynb`:

- sessao            -> inicialização do Spark e leitura dos dados
- preprocessamento  -> variáveis-alvo e vetor de features
- pln               -> TF-IDF sobre a coluna de doença
- warehouse         -> modelo dimensional (fato + dimensões)
- olap              -> consultas analíticas em Spark SQL
- mapreduce         -> agregações no paradigma MapReduce (RDD)
- temporal          -> evolução dos casos por ano
- geo               -> mapa interativo de casos por localidade
- classificacao     -> Regressão Logística, Random Forest e Naive Bayes
- clusterizacao     -> K-Means com método do cotovelo e PCA
"""
