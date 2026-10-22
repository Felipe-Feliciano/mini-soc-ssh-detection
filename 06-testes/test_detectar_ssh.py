import sys
from pathlib import Path

# Permite importar o script principal do projeto
sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "05-scripts")
)

from detectar_ssh import analisar_log


def criar_log(tmp_path, conteudo):
    arquivo = tmp_path / "auth.log"
    arquivo.write_text(conteudo, encoding="utf-8")
    return arquivo


def test_gera_alerta_com_tres_falhas_em_cinco_minutos(
    tmp_path, capsys
):
    log = criar_log(
        tmp_path,
        "Oct 22 14:00:00 kali sshd[1]: Failed password for "
        "teste from 192.168.115.10 port 5001 ssh2\n"
        "Oct 22 14:02:00 kali sshd[2]: Failed password for "
        "teste from 192.168.115.10 port 5002 ssh2\n"
        "Oct 22 14:04:00 kali sshd[3]: Failed password for "
        "teste from 192.168.115.10 port 5003 ssh2\n"
    )

    analisar_log(str(log))
    saida = capsys.readouterr().out

    assert "ALERTA" in saida
    assert "192.168.115.10" in saida


def test_nao_gera_alerta_com_falhas_espacadas(
    tmp_path, capsys
):
    log = criar_log(
        tmp_path,
        "Oct 22 14:00:00 kali sshd[1]: Failed password for "
        "teste from 192.168.115.20 port 5001 ssh2\n"
        "Oct 22 14:06:00 kali sshd[2]: Failed password for "
        "teste from 192.168.115.20 port 5002 ssh2\n"
        "Oct 22 14:12:00 kali sshd[3]: Failed password for "
        "teste from 192.168.115.20 port 5003 ssh2\n"
    )

    analisar_log(str(log))
    saida = capsys.readouterr().out

    assert "ALERTA" not in saida
    assert "192.168.115.20: 3 falha(s) no total." in saida


def test_analisa_ips_independentemente(tmp_path, capsys):
    log = criar_log(
        tmp_path,
        "Oct 22 14:00:00 kali sshd[1]: Failed password for "
        "teste from 192.168.115.30 port 5001 ssh2\n"
        "Oct 22 14:01:00 kali sshd[2]: Failed password for "
        "teste from 192.168.115.30 port 5002 ssh2\n"
        "Oct 22 14:02:00 kali sshd[3]: Failed password for "
        "teste from 192.168.115.30 port 5003 ssh2\n"
        "Oct 22 14:00:30 kali sshd[4]: Failed password for "
        "teste from 192.168.115.40 port 6001 ssh2\n"
    )

    analisar_log(str(log))
    saida = capsys.readouterr().out

    assert "ALERTA" in saida
    assert "192.168.115.30" in saida
    assert "192.168.115.40: 1 falha(s) no total." in saida


def test_log_sem_falhas(tmp_path, capsys):
    log = criar_log(
        tmp_path,
        "Oct 22 14:00:00 kali sshd[5]: Accepted password for "
        "usuario from 192.168.115.50 port 7001 ssh2\n"
    )

    analisar_log(str(log))
    saida = capsys.readouterr().out

    assert "Nenhuma falha de autenticacao SSH encontrada." in saida
