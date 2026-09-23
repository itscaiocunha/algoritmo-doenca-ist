"""Parâmetros do domínio usados na geração dos dados simulados."""

import os

ARQUIVO_SAIDA = os.environ.get("ARQUIVO_DADOS_BRUTOS", "/data/dados_ist_realistas.csv")
TOTAL_REGISTROS = 10000

# Distribuição de idade (média, desvio padrão) por doença
ISTS = {
    "HIV": {"idade_media": 35, "idade_desvio": 7},
    "Sífilis": {"idade_media": 30, "idade_desvio": 10},
    "Gonorreia": {"idade_media": 28, "idade_desvio": 8},
    "HPV": {"idade_media": 26, "idade_desvio": 6},
    "Clamídia": {"idade_media": 24, "idade_desvio": 5},
    "Herpes Genital": {"idade_media": 29, "idade_desvio": 6},
}

OUTRAS_DOENCAS = {
    "Gripe": {"idade_media": 25, "idade_desvio": 15},
    "Câncer": {"idade_media": 60, "idade_desvio": 12},
    "AVC": {"idade_media": 65, "idade_desvio": 10},
    "Diabetes": {"idade_media": 50, "idade_desvio": 10},
    "Asma": {"idade_media": 20, "idade_desvio": 10},
}

# Níveis educacionais com variações (erros de digitação simulam preenchimento humano)
NIVEIS_EDUCACIONAIS = [
    "Fundamental", "Médio", "Superior", "fundamnetal", "medio incompleto", "superio", None
]

CIDADES_BRASILEIRAS = [
    # Norte
    "Manaus", "Belém", "Porto Velho", "Rio Branco", "Macapá", "Boa Vista", "Santarém", "Palmas",
    # Nordeste
    "Salvador", "Fortaleza", "Recife", "São Luís", "Maceió", "Natal", "João Pessoa", "Teresina", "Aracaju", "Feira de Santana",
    # Centro-Oeste
    "Brasília", "Goiânia", "Campo Grande", "Cuiabá", "Anápolis", "Dourados", "Rio Verde",
    # Sudeste
    "São Paulo", "Rio de Janeiro", "Belo Horizonte", "Vitória", "Campinas", "São José dos Campos", "Ribeirão Preto", "Uberlândia",
    # Sul
    "Curitiba", "Porto Alegre", "Florianópolis", "Londrina", "Maringá", "Caxias do Sul", "Pelotas", "Joinville"
]

# Probabilidades que controlam a composição e a "sujeira" do dataset
PROB_TER_DOENCA = 0.6          # registro possui alguma doença
PROB_DOENCA_SER_IST = 0.6      # dado que possui doença, ela é uma IST
PROB_CIDADE_INFORMADA = 0.9
PROB_IDADE_OUTLIER = 0.01
PROB_RENDA_OUTLIER = 0.01
PROB_RENDA_AUSENTE = 0.02
PROB_DATA_FUTURA = 0.02
