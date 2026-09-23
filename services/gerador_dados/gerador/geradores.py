"""Funções que geram cada atributo de um registro de paciente.

Os dados incluem, propositalmente, ruídos típicos de preenchimento humano
(grafias inconsistentes, campos vazios, outliers e datas futuras), que são
tratados nas etapas seguintes do pipeline.
"""

import random
from datetime import date, timedelta

import numpy as np
from faker import Faker

from gerador import config

fake = Faker('pt_BR')  # Gerar dados em português


def escolher_cidade():
    if random.random() < config.PROB_CIDADE_INFORMADA:
        return random.choice(config.CIDADES_BRASILEIRAS)
    return None


def escolher_doenca():
    if random.random() < config.PROB_DOENCA_SER_IST:
        return random.choice(list(config.ISTS.keys()))
    return random.choice(list(config.OUTRAS_DOENCAS.keys()))


def gerar_idade(doenca):
    base = config.ISTS.get(doenca) or config.OUTRAS_DOENCAS[doenca]
    idade = int(np.random.normal(base["idade_media"], base["idade_desvio"]))
    if random.random() < config.PROB_IDADE_OUTLIER:
        idade = random.choice([random.randint(0, 5), random.randint(90, 100)])
    return max(0, idade)


def gerar_genero_nome():
    prob = random.random()
    if prob < 0.6:
        nome = fake.name_male()
        genero = random.choice(["Masculino", "masculino", "M", "m"])
    elif prob < 0.8:
        nome = fake.name_female()
        genero = random.choice(["Feminino", "feminino", "F", "f"])
    elif prob < 0.2:
        nome = fake.name()
        genero = "Não informado"
    else:
        nome = fake.name()
        genero = None

    return nome, genero


def gerar_data_teste():
    if random.random() < config.PROB_DATA_FUTURA:
        return (date.today() + timedelta(days=random.randint(1, 1000))).isoformat()
    return fake.date_this_decade().isoformat()


def gerar_renda(nivel_educacional):
    if nivel_educacional is None:
        base_renda = random.randint(800, 2500)
    else:
        nivel = nivel_educacional.lower()
        if "fundam" in nivel:
            base_renda = random.randint(800, 1800)
        elif "medio" in nivel:
            base_renda = random.randint(1200, 3000)
        elif "super" in nivel:
            base_renda = random.randint(2500, 8000)
        else:
            base_renda = random.randint(1000, 2500)

    if random.random() < config.PROB_RENDA_OUTLIER:
        base_renda = random.choice([random.randint(5, 100), random.randint(30000, 100000)])

    if random.random() < config.PROB_RENDA_AUSENTE:
        return None

    return base_renda


def gerar_registro():
    registro = {}
    registro["id"] = fake.uuid4()
    registro["nome"], registro["genero"] = gerar_genero_nome()

    if random.random() < config.PROB_TER_DOENCA:
        doenca = escolher_doenca()
        registro["idade"] = gerar_idade(doenca)
        registro["doenca"] = doenca
    else:
        registro["idade"] = random.randint(0, 90)
        registro["doenca"] = "Nenhuma"

    registro["localidade"] = escolher_cidade()
    registro["nivel_educacional"] = random.choice(config.NIVEIS_EDUCACIONAIS)
    registro["renda_media"] = gerar_renda(registro["nivel_educacional"])
    registro["data_teste"] = gerar_data_teste()

    return registro
