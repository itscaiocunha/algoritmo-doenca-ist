"""Modelos de classificação para prever a presença de IST (`tem_ist`)."""

import matplotlib.pyplot as plt
from pyspark.ml.classification import LogisticRegression, NaiveBayes, RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from sklearn.metrics import ConfusionMatrixDisplay, classification_report, confusion_matrix, roc_auc_score, roc_curve

from ist_bigdata import config
from ist_bigdata.graficos import salvar_figura


def dividir_treino_teste(encoded_df):
    dados = encoded_df.select("features", "tem_ist").withColumnRenamed("tem_ist", "label")
    return dados.randomSplit(config.PROPORCAO_TREINO_TESTE, seed=config.SEED)


def criar_modelos():
    return {
        "Regressão Logística": LogisticRegression(featuresCol="features", labelCol="label", maxIter=10),
        "Random Forest": RandomForestClassifier(featuresCol="features", labelCol="label", numTrees=10),
        "Naive Bayes": NaiveBayes(featuresCol="features", labelCol="label"),
    }


def treinar_e_prever(modelos, train_data, test_data):
    """Treina cada modelo e retorna `nome -> predições no conjunto de teste`."""
    return {nome: modelo.fit(train_data).transform(test_data) for nome, modelo in modelos.items()}


def avaliar_metricas(predicoes):
    metricas = {
        "Acurácia": "accuracy",
        "Precisão": "weightedPrecision",
        "Recall": "weightedRecall",
        "F1-Score": "f1",
    }
    resultados = {}
    for rotulo, metrica in metricas.items():
        avaliador = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName=metrica)
        resultados[rotulo] = avaliador.evaluate(predicoes)
        print(f"{rotulo}: {resultados[rotulo]:.4f}")
    return resultados


def plotar_matriz_confusao(predicoes):
    y_true = predicoes.select("label").toPandas()
    y_pred = predicoes.select("prediction").toPandas()

    ConfusionMatrixDisplay(confusion_matrix=confusion_matrix(y_true, y_pred)).plot(cmap="Blues")
    plt.title("Matriz de Confusão")
    salvar_figura("matriz_confusao.png")


def plotar_curva_roc(predicoes):
    """Curva ROC e AUC a partir da probabilidade da classe positiva (índice 1)."""
    preds = predicoes.select("probability", "label").toPandas()
    probs = preds["probability"].apply(lambda x: x[1])
    labels = preds["label"]

    auc = roc_auc_score(labels, probs)
    print(f"AUC: {auc:.4f}")

    fpr, tpr, _ = roc_curve(labels, probs)
    plt.figure(figsize=(6, 6))
    plt.plot(fpr, tpr, label=f"AUC = {auc:.4f}")
    plt.plot([0, 1], [0, 1], "k--")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("Curva ROC")
    plt.legend(loc="lower right")
    plt.grid(True)
    salvar_figura("curva_roc.png")
    return auc


def comparar_acuracias(predicoes_por_modelo):
    avaliador = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="accuracy")

    print("\nAcurácia dos Modelos de Classificação:")
    acuracias = {}
    for nome, predicoes in predicoes_por_modelo.items():
        acuracias[nome] = avaliador.evaluate(predicoes)
        print(f"{nome}: {acuracias[nome]:.4f}")
    return acuracias


def relatorio_classificacao(predicoes, nome_modelo):
    print(f"\nRelatório de Classificação para {nome_modelo} (melhor modelo):")
    pd_preds = predicoes.select("label", "prediction").toPandas()
    print(classification_report(pd_preds["label"], pd_preds["prediction"]))
