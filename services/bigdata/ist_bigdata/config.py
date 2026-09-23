"""Configurações e constantes de domínio da etapa de Big Data."""

import os
from pathlib import Path

# --- Ambiente ---
JAVA_HOME = "/usr/lib/jvm/java-8-openjdk-amd64"
SPARK_APP_NAME = "Analise de IST"
SPARK_CONFIG = {
    "spark.executor.memory": "2g",
    "spark.driver.memory": "2g",
}

# --- Entrada e saída ---
ARQUIVO_DADOS = os.environ.get("ARQUIVO_DADOS_TRATADOS", "/app/data/dados_ist_tratados.csv")
DIR_SAIDA = Path(os.environ.get("DIR_SAIDA", "output"))

# --- Domínio ---
ISTS = ["HIV", "Sífilis", "Gonorreia", "HPV", "Clamídia", "Herpes Genital"]
CURAVEIS = ["Sífilis", "Gonorreia", "Clamídia"]

# Colunas usadas como features. `doenca` fica de fora de propósito: o rótulo
# `tem_ist` é derivado dela, e incluí-la entrega a resposta ao modelo (vazamento de dados).
COLUNAS_CATEGORICAS = {
    # coluna original -> prefixo das colunas derivadas (Idx / Vec)
    "genero": "genero",
    "localidade": "localidade",
    "nivel_educacional": "nivelEducacional",
}
COLUNAS_NUMERICAS = ["idade", "renda_media"]

# --- Modelagem ---
SEED = 42
PROPORCAO_TREINO_TESTE = [0.7, 0.3]
K_CANDIDATOS = range(2, 8)
K_IDEAL = 4

# Coordenadas (latitude, longitude) das cidades presentes no dataset
COORDENADAS_CIDADES = {
    "Manaus": [-3.1019, -60.025],
    "Belém": [-1.4558, -48.5044],
    "Porto Velho": [-8.7619, -63.9039],
    "Rio Branco": [-9.9747, -67.8100],
    "Macapá": [0.0356, -51.0705],
    "Boa Vista": [2.8200, -60.6720],
    "Santarém": [-2.4385, -54.6996],
    "Palmas": [-10.1675, -48.3277],
    "Salvador": [-12.9747, -38.4767],
    "Fortaleza": [-3.7167, -38.5500],
    "Recife": [-8.0500, -34.9000],
    "São Luís": [-2.5297, -44.3044],
    "Maceió": [-9.6658, -35.7333],
    "Natal": [-5.8128, -35.2551],
    "João Pessoa": [-7.1200, -34.8800],
    "Teresina": [-5.0892, -42.8016],
    "Aracaju": [-10.9472, -37.0731],
    "Feira de Santana": [-12.2667, -38.9667],
    "Brasília": [-15.7939, -47.8828],
    "Goiânia": [-16.6869, -49.2648],
    "Campo Grande": [-20.4697, -54.6201],
    "Cuiabá": [-15.6014, -56.0979],
    "Anápolis": [-16.3281, -48.9528],
    "Dourados": [-22.2231, -54.8122],
    "Rio Verde": [-17.7923, -50.9192],
    "São Paulo": [-23.5505, -46.6333],
    "Rio de Janeiro": [-22.9068, -43.1729],
    "Belo Horizonte": [-19.9167, -43.9345],
    "Vitória": [-20.3155, -40.3128],
    "Campinas": [-22.9099, -47.0626],
    "São José dos Campos": [-23.1896, -45.8841],
    "Ribeirão Preto": [-21.1775, -47.8103],
    "Uberlândia": [-18.9141, -48.2749],
    "Curitiba": [-25.4284, -49.2733],
    "Porto Alegre": [-30.0346, -51.2177],
    "Florianópolis": [-27.5954, -48.5480],
    "Londrina": [-23.3045, -51.1696],
    "Maringá": [-23.4200, -51.9333],
    "Caxias do Sul": [-29.1678, -51.1794],
    "Pelotas": [-31.7649, -52.3371],
    "Joinville": [-26.3045, -48.8487],
}
CENTRO_MAPA = [-15.77972, -47.92972]
