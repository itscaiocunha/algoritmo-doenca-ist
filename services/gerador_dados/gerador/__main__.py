"""Ponto de entrada: `python -m gerador`."""

import pandas as pd

from gerador import config
from gerador.geradores import gerar_registro


def main():
    df = pd.DataFrame([gerar_registro() for _ in range(config.TOTAL_REGISTROS)])
    df.to_csv(config.ARQUIVO_SAIDA, index=False, encoding='utf-8')
    print("Dados gerados com realismo e erros humanos incluídos!")


if __name__ == "__main__":
    main()
