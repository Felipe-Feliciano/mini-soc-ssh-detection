# Mini SOC — Detecção de Falhas de Autenticação SSH

## Sobre o projeto

Projeto prático de cibersegurança com foco em análise de logs Linux, detecção de tentativas de autenticação SSH suspeitas e geração de alertas utilizando Python.

O laboratório foi desenvolvido com Kali Linux como estação de análise e UbuntuCyberLab como host monitorado.

## Objetivos

- Analisar registros de autenticação SSH.
- Identificar falhas de autenticação.
- Agrupar eventos por endereço IP.
- Detectar múltiplas falhas dentro de uma janela temporal.
- Exportar alertas para relatórios CSV.
- Validar o comportamento do detector com testes automatizados.
- Documentar evidências e resultados.

## Tecnologias utilizadas

- Kali Linux
- Ubuntu Linux
- OpenSSH
- Python 3
- pytest
- CSV
- Bash e ferramentas de análise de logs

## Estrutura do projeto

- `02-configuracao/` — regra de detecção documentada.
- `03-evidencias/` — logs de teste e resultados da análise.
- `04-relatorios/` — relatórios e exportações CSV.
- `05-scripts/` — script Python de detecção SSH.
- `06-testes/` — testes automatizados com pytest.

## Regra de detecção

O script identifica eventos `Failed password` nos logs, agrupa as falhas por endereço IP e gera um alerta quando encontra três ou mais falhas do mesmo IP dentro de uma janela de cinco minutos.

O limite e a janela temporal são configuráveis no código.

A regra é experimental e deve ser ajustada conforme o ambiente e o contexto de monitoramento.

## Relatórios CSV

Quando um alerta é identificado, o script pode exportar os resultados para um arquivo CSV com os seguintes campos:

- `ip` — endereço IP associado às falhas.
- `quantidade_falhas` — número de falhas na janela detectada.
- `horario_alerta` — horário do evento que atingiu o limite.
- `severidade` — classificação definida pela regra atual (`ALTA`).

Exemplo de execução:

```bash
python3 05-scripts/detectar_ssh.py 03-evidencias/log-teste-janela.txt 04-relatorios/alertas-ssh.csv
```

O relatório é gerado no caminho informado como segundo argumento.

## Testes automatizados

Os testes são executados com pytest:

```bash
python3 -m pytest -v 06-testes/
```

Os quatro cenários validados são:

1. Geração de alerta para três falhas dentro de cinco minutos.
2. Ausência de alerta para falhas espaçadas por mais de cinco minutos.
3. Análise independente de diferentes endereços IP.
4. Tratamento de logs sem falhas de autenticação.

Resultado validado durante o desenvolvimento: **4 testes aprovados**.

## Validação em laboratório

O detector foi testado com logs fictícios controlados, incluindo cenários positivos e negativos.

Também foi executado sobre registros reais de autenticação do UbuntuCyberLab, identificando uma falha associada ao IP `192.168.115.3`. Como o evento observado estava abaixo do limite de detecção, nenhum alerta foi emitido.

## Limitações

- A análise é executada manualmente.
- Não há monitoramento contínuo nem integração com uma plataforma SIEM.
- A severidade é definida por uma regra experimental, não por uma avaliação completa do risco.
- Os resultados dependem dos registros disponíveis e do formato das datas.
- Falhas de autenticação, isoladamente, não comprovam uma invasão.
- Os logs de teste são fictícios e não representam ataques reais.

## Próximas melhorias

- Adicionar testes para formatos de log e datas adicionais.
- Melhorar a validação dos endereços IP e o tratamento de eventos incomuns.
- Criar execução periódica e monitoramento contínuo.
- Avaliar correlação com outros eventos de segurança.

## Aviso

Este projeto foi desenvolvido para fins educacionais em um laboratório controlado, com sistemas sob autorização.
