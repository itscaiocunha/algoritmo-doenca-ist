"""Utilitários compartilhados para salvar os artefatos gerados."""

import matplotlib.pyplot as plt

from ist_bigdata import config


def caminho_saida(nome_arquivo):
    return config.DIR_SAIDA / nome_arquivo


def salvar_figura(nome_arquivo):
    """Salva a figura corrente no diretório de saída e a exibe no notebook."""
    plt.savefig(caminho_saida(nome_arquivo))
    plt.show()
