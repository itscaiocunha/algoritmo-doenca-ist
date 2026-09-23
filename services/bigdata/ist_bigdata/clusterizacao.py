"""Clusterização K-Means para identificar perfis de pacientes."""

import matplotlib.pyplot as plt
import seaborn as sns
from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import PCA, StandardScaler

from ist_bigdata import config
from ist_bigdata.graficos import salvar_figura

COLUNA_FEATURES = "scaledFeatures"


def padronizar(df):
    """Coloca as features na mesma escala (média 0, desvio 1).

    O K-Means e o PCA se baseiam em distâncias/variância: sem padronização, a renda
    (em reais) domina todas as outras variáveis e os clusters viram apenas faixas de renda.
    """
    scaler = StandardScaler(inputCol="features", outputCol=COLUNA_FEATURES, withMean=True, withStd=True)
    return scaler.fit(df).transform(df)


def metodo_cotovelo(df, ks=config.K_CANDIDATOS):
    """Custo (WCSS) para cada K candidato — ajuda a escolher o número de clusters."""
    custos = []
    for k in ks:
        modelo = KMeans(featuresCol=COLUNA_FEATURES, k=k, seed=config.SEED).fit(df)
        custo = modelo.summary.trainingCost
        custos.append(custo)
        print(f"Custo para k={k}: {custo}")

    plt.figure(figsize=(8, 5))
    plt.plot(list(ks), custos, marker="o", color="blue")
    plt.xlabel("Número de Clusters (K)")
    plt.ylabel("Custo (WCSS)")
    plt.title("Método do Cotovelo para K-Means")
    plt.grid(True)
    salvar_figura("metodo_cotovelo.png")
    return custos


def agrupar(df, k=config.K_IDEAL):
    modelo = KMeans(featuresCol=COLUNA_FEATURES, k=k, seed=config.SEED).fit(df)
    return modelo.transform(df)


def plotar_clusters_pca(clusters, k=config.K_IDEAL):
    """Projeta as features em 2 componentes principais para visualizar os grupos."""
    pca_model = PCA(k=2, inputCol=COLUNA_FEATURES, outputCol="pca_features").fit(clusters)
    pca_pd = pca_model.transform(clusters).select("pca_features", "prediction").toPandas()
    pca_pd["x"] = pca_pd["pca_features"].apply(lambda v: v[0])
    pca_pd["y"] = pca_pd["pca_features"].apply(lambda v: v[1])

    plt.figure(figsize=(10, 8))
    sns.scatterplot(data=pca_pd, x="x", y="y", hue="prediction", palette="viridis", s=50, alpha=0.7)
    plt.title(f"Visualização dos Clusters K-Means (K={k}) com PCA")
    plt.xlabel("Componente Principal 1")
    plt.ylabel("Componente Principal 2")
    plt.legend(title="Cluster")
    plt.grid(True)
    salvar_figura("clusters_kmeans.png")
