# Regra de Detecção — Falhas de Autenticação SSH

## Objetivo
Identificar endereços IP com múltiplas falhas de autenticação SSH.

## Fonte de dados
- Sistema monitorado: UbuntuCyberLab
- Serviço: OpenSSH
- Log: /var/log/auth.log

## Lógica da regra
1. Ler as linhas do log de autenticação.
2. Identificar eventos "Failed password".
3. Extrair o IP de origem.
4. Contar as falhas por endereço IP.
5. Gerar um alerta quando o mesmo IP apresentar 3 ou mais falhas.

## Resultado do teste controlado
- IP observado: 192.168.115.3
- Falhas encontradas na análise: 1
- Limite configurado: 3
- Alerta: não acionado

## Interpretação
O detector processou os registros reais e encontrou uma falha para o IP observado. Como o total ficou abaixo do limite configurado, nenhum alerta foi gerado.

O limite é uma regra inicial de laboratório. Várias falhas podem indicar comportamento suspeito, mas não comprovam, isoladamente, uma invasão.

## Limitações
- A análise é executada manualmente.
- O script lê um arquivo de log local.
- Não há monitoramento em tempo real nem painel de alertas.
- Os resultados dependem dos eventos presentes no arquivo analisado.
