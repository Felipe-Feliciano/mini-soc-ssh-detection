# Mini SOC — Relatório Inicial

## 1. Objetivo
Monitorar eventos de autenticação SSH em um host Linux e identificar tentativas de login suspeitas.

## 2. Ambiente
- Estação de análise: Kali Linux
- Host monitorado: UbuntuCyberLab
- Serviço monitorado: OpenSSH
- Arquivo de log: /var/log/auth.log

## 3. Evidências coletadas
- Evento: Invalid user
- Evento: Failed password for invalid user
- IP de origem registrado: 192.168.115.3
- Contagem de registros Invalid user: 8
- Contagem observada de falhas SSH para o IP: 1

## 4. Interpretação
Os registros demonstram que o sistema registra tentativas de autenticação com usuários inexistentes. Os testes foram realizados de forma controlada no laboratório.

A presença desses eventos, isoladamente, não comprova um ataque real.

## 5. Próximas etapas
- Automatizar a análise dos logs.
- Criar uma regra de alerta para múltiplas falhas de autenticação.
- Documentar os resultados e limitações.
