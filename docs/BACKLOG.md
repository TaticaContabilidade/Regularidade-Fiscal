# Backlog

Prioridade (MoSCoW): **M** = Must · **S** = Should · **C** = Could.
Status: `TODO` · `DOING` · `BLOQUEADO` · `DONE`.
Requisitos referenciados em [`REQUISITOS.md`](REQUISITOS.md).

## Fase 0: Descoberta e fundação

| # | Item | Requisitos | Prior. | Status |
|---|---|---|---|---|
| 0.1 | Responder às questões em aberto Q-01…Q-12 com a Geovânia/TI (acesso SIEG, Integra Contador, WhatsApp, lista de clientes) | — | M | DONE |
| 0.2 | Acompanhar a Geovânia em uma execução manual completa e documentar o "Método de Análise" passo a passo | RF-SF-02 | M | TODO |
| 0.3 | Inicializar o repositório git, `pyproject.toml` (uv), ruff, pytest, `.gitignore`, `.env.example` | RNF-01 | M | TODO |
| 0.4 | Criar o esqueleto de diretórios conforme o README | RNF-08 | M | DONE |
| 0.5 | Configuração (`pydantic-settings`), logging estruturado e flag `DRY_RUN` | RNF-05, RNF-06 | M | TODO |
| 0.6 | Banco SQLite: tabelas `cliente`, `analista`, `execucao`, `consulta`, `envio` | RNF-04, RNF-05 | M | TODO |
| 0.7 | Perguntar ao suporte do SIEG se existe API para certidões/Situação Fiscal; se não existir, fazer uma prova de conceito de RPA (Playwright) no portal | RF-CERT-01, Q-01 | M | TODO |
| 0.8 | Responder às novas questões Q-03, Q-13, Q-14 e Q-15 | — | M | TODO |

## Fase 1: MVP: certidões SIEG + alerta ao analista

| # | Item | Requisitos | Prior. | Status |
|---|---|---|---|---|
| 1.1 | Adapter Omie: sincronizar clientes ativos e analistas responsáveis | RF-CLI-01, RF-CLI-02 | M | TODO |
| 1.2 | Adapter SIEG: autenticação e download das certidões por cliente (API ou RPA, conforme 0.7) | RF-CERT-01 | M | BLOQUEADO (0.7) |
| 1.3 | Classificador de certidões: regular / irregular / falha | RF-CERT-02 | M | TODO |
| 1.4 | Notificador de e-mail (SMTP) com suporte a dry-run e anexos | RF-CERT-03, RNF-06 | M | TODO |
| 1.5 | Enviar as certidões irregulares ao analista responsável | RF-CERT-03 | M | TODO |
| 1.6 | Detectar a falha do FGTS no SIEG e notificar o analista | RF-CERT-05 | M | TODO |
| 1.7 | CLI `automacao executar [--dry-run] [--cliente CNPJ]` + resumo da execução | RF-NOT-02, RF-NOT-03 | M | TODO |

## Fase 2: Envio ao cliente

| # | Item | Requisitos | Prior. | Status |
|---|---|---|---|---|
| 2.1 | Enviar as certidões ao cliente por e-mail (modelo aprovado), só se **todas** estiverem regulares | RF-CERT-04 | M | TODO |
| 2.2 | Notificador WhatsApp via API do DigiSac | RF-CERT-04, RF-CERT-04a | M | TODO |
| 2.3 | Controle de idempotência: não reenviar no mesmo mês | RNF-04 | M | TODO |

## Fase 3: Situação Fiscal + PGFN

| # | Item | Requisitos | Prior. | Status |
|---|---|---|---|---|
| 3.1 | Baixar o relatório Situação Fiscal pelo SIEG | RF-SF-01 | M | TODO |
| 3.2 | Parser do PDF da Situação Fiscal: pendências e códigos de débito | RF-SF-02, RF-RFB-02 | M | TODO |
| 3.3 | Consultar os débitos na PGFN pelos códigos (fonte definida em Q-03) | RF-RFB-01, RF-RFB-03 | M | BLOQUEADO (Q-03) |
| 3.4 | Gerador de relatórios (Jinja2 → PDF): Situação Fiscal consolidada com PGFN | RF-SF-03, RF-SF-04, RF-RFB-04 | M | TODO |
| 3.5 | Enviar o relatório consolidado ao analista (um e-mail por cliente) | RF-SF-05, RF-NOT-01 | M | TODO |

## Fase 4: CADIN e municipal

| # | Item | Requisitos | Prior. | Status |
|---|---|---|---|---|
| 4.2 | Adapter CADIN: baixar a certidão e enviá-la ao analista se houver débito | RF-CADIN-01, RF-CADIN-02 | S | TODO |
| 4.3 | Certidão municipal de São Paulo | RF-MUN-01 | S | TODO |
| 4.4 | Incluir CADIN e falhas do FGTS no relatório consolidado do analista | RF-NOT-01 | S | TODO |

## Fase 5: Operação

| # | Item | Requisitos | Prior. | Status |
|---|---|---|---|---|
| 5.1 | Provisionar a instância AWS (Lightsail, `sa-east-1`) e agendar a execução mensal via cron | RNF-07, Q-14, Q-15 | S | TODO |
| 5.2 | Retentativas com backoff e isolamento de falhas por fonte | RNF-03 | S | TODO |
| 5.3 | Política de retenção/limpeza de PDFs e logs | RNF-02 | C | TODO |
| 5.4 | Painel simples do histórico de execuções (HTML estático) | RNF-05 | C | TODO |

## Fora do escopo

| Item | Motivo |
|---|---|
| Fallback FGTS com consulta direta à Caixa (RF-FGTS-01..04) | Decisão Q-04: só notificar o analista (item 1.6). |
| Certidões de outros municípios | Decisão Q-05: apenas São Paulo. |
