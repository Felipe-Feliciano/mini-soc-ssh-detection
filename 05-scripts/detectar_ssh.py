#!/usr/bin/env python3

import re
import sys
from collections import Counter
from pathlib import Path

LIMITE_ALERTA = 3


def analisar_log(caminho):
    arquivo = Path(caminho)

    if not arquivo.is_file():
        print(f"Erro: arquivo não encontrado: {arquivo}")
        sys.exit(1)

    falhas_por_ip = Counter()
    padrao = re.compile(
        r"sshd.*Failed password.*from (\d{1,3}(?:\.\d{1,3}){3})"
    )

    with arquivo.open("r", encoding="utf-8", errors="replace") as log:
        for linha in log:
            resultado = padrao.search(linha)
            if resultado:
                falhas_por_ip[resultado.group(1)] += 1

    if not falhas_por_ip:
        print("Nenhuma falha de autenticação SSH encontrada.")
        return

    print("=== Mini SOC | Análise de falhas SSH ===")

    for ip, quantidade in falhas_por_ip.most_common():
        print(f"{ip}: {quantidade} falha(s)")

        if quantidade >= LIMITE_ALERTA:
            print(
                f"ALERTA: {ip} registrou "
                f"{quantidade} falhas de autenticação."
            )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Uso: python3 {sys.argv[0]} CAMINHO_DO_LOG")
        sys.exit(1)

    analisar_log(sys.argv[1])
