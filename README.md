# Mini SOC — Detecção de Falhas de Autenticação SSH

## Sobre o projeto

Projeto prático de cibersegurança com foco em monitoramento de logs Linux, análise de eventos de autenticação e detecção de tentativas de login suspeitas utilizando Python.

O laboratório foi desenvolvido com Kali Linux como estação de análise e UbuntuCyberLab como host monitorado.

## Objetivos

- Analisar registros de autenticação SSH.
- Identificar falhas de login e usuários inexistentes.
- Agrupar falhas por endereço IP.
- Criar uma regra de alerta baseada em um limite configurável.
- Documentar evidências e resultados.

## Tecnologias utilizadas

- Kali Linux
- Ubuntu Linux
- OpenSSH
- Python 3
- Bash e ferramentas de análise de logs

## Estrutura do projeto

- `02-configuracao/` — regra de detecção documentada.
- `03-evidencias/` — logs fictícios de teste e resultado da análise real.
- `04-relatorios/` — relatório inicial.
- `05-scripts/` — detector de falhas SSH em Python.

## Regra de detecção

O script identifica eventos `Failed password`, agrupa as falhas por IP e gera um alerta quando um endereço apresenta três ou mais falhas no arquivo analisado.

O limite é experimental e pode ser ajustado conforme o contexto.

## Validação

O detector foi validado com um log fictício contendo três falhas do mesmo IP, gerando o alerta esperado.

Também foi executado sobre o arquivo `/var/log/auth.log` do UbuntuCyberLab, onde encontrou uma falha associada ao IP `192.168.115.3`. Como o total estava abaixo do limite configurado, nenhum alerta foi emitido.

## Limitações

- A análise é executada manualmente.
- Não há monitoramento contínuo nem painel SIEM.
- Falhas de autenticação isoladas não comprovam uma invasão.
- Os resultados dependem dos registros disponíveis no momento da análise.

## Próximas melhorias

- Automatizar a execução periódica.
- Adicionar análise de usuários inexistentes.
- Implementar alertas para padrões de falha.
- Criar testes automatizados e ampliar a documentação.

## Aviso

Este projeto foi desenvolvido para fins educacionais em um laboratório controlado, com sistemas sob autorização.


