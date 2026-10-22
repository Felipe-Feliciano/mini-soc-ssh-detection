
import csv
import re
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

LIMITE_ALERTA = 3
JANELA_MINUTOS = 5

PADRAO = re.compile(
    r"(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}).*"
    r"sshd.*Failed password.*from\s+(\d{1,3}(?:\.\d{1,3}){3})"
)


def analisar_log(caminho, relatorio=""):
    eventos = defaultdict(list)
    ano_atual = datetime.now().year

    with open(caminho, "r", encoding="utf-8", errors="replace") as arquivo:
        for linha in arquivo:
            resultado = PADRAO.search(linha)

            if not resultado:
                continue

            data_texto, ip = resultado.groups()

            try:
                data = datetime.strptime(
                    f"{ano_atual} {data_texto}",
                    "%Y %b %d %H:%M:%S"
                )
            except ValueError:
                continue

            eventos[ip].append(data)

    if not eventos:
        print("Nenhuma falha de autenticacao SSH encontrada.")
        if relatorio:
            salvar_csv(relatorio, [])
        return []

    alertas = []

    for ip, datas in sorted(eventos.items()):
        datas.sort()
        inicio = 0
        gerou_alerta = False

        for fim, data in enumerate(datas):
            while data - datas[inicio] > timedelta(
                minutes=JANELA_MINUTOS
            ):
                inicio += 1

            quantidade = fim - inicio + 1

            if quantidade >= LIMITE_ALERTA:
                print(
                    f"ALERTA: {ip} registrou {quantidade} falhas "
                    f"em uma janela de {JANELA_MINUTOS} minutos."
                )

                alertas.append({
                    "ip": ip,
                    "quantidade_falhas": quantidade,
                    "horario_alerta": data.strftime("%Y-%m-%d %H:%M:%S"),
                    "severidade": "ALTA",
                })

                gerou_alerta = True
                break

        if not gerou_alerta:
            print(f"{ip}: {len(datas)} falha(s) no total.")

    if relatorio:
        salvar_csv(relatorio, alertas)

    return alertas


def salvar_csv(caminho, alertas):
    campos = [
        "ip",
        "quantidade_falhas",
        "horario_alerta",
        "severidade",
    ]

    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(alertas)

    print(f"Relatorio CSV salvo em: {caminho}")


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print(
            f"Uso: python3 {Path(sys.argv[0]).name} "
            "<arquivo_de_log> [relatorio.csv]"
        )
        sys.exit(1)

    try:
        caminho_log = sys.argv[1]
        caminho_csv = sys.argv[2] if len(sys.argv) == 3 else ""

        analisar_log(caminho_log, caminho_csv)

    except OSError as erro:
        print(f"Erro ao ler ou salvar arquivo: {erro}")
        sys.exit(1)
