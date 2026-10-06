# Automação de Regularidade Fiscal: Tática Contabilidade

Automatiza a verificação mensal da regularidade fiscal dos clientes: baixa as certidões (SIEG, FGTS, CADIN,
municipais), analisa a Situação Fiscal e a PGFN, **envia as certidões regulares ao cliente** (e-mail + WhatsApp)
e **envia ao analista um relatório consolidado dos casos irregulares**.

- Requisitos: [`docs/REQUISITOS.md`](docs/REQUISITOS.md)
- Backlog: [`docs/BACKLOG.md`](docs/BACKLOG.md)
- Convenções para o Claude Code: [`CLAUDE.md`](CLAUDE.md)

## Arquitetura

Pipeline em lote, executado pela CLI (manualmente ou via cron). Organizado em camadas, com cada fonte
externa isolada atrás de um *adapter*:

```
                    ┌──────────────────────────── CLI / agendador (cron) ───────────────────────────┐
                    │                    automacao executar [--dry-run] [--cliente]                 │
                    └───────────────────────────────────────┬────────────────────────────────────────┘
                                                            ▼
                                              ┌──────────────────────────┐
                                              │  pipeline/ (orquestrador)│  para cada cliente ativo
                                              └────────────┬─────────────┘
              ┌────────────────────────────┬───────────────┼──────────────────┬──────────────────────┐
              ▼                            ▼               ▼                  ▼                      ▼
     ┌──────────────────┐   ┌──────────────────────────┐ ┌──────────────┐ ┌──────────────────┐ ┌──────────────┐
     │ integracoes/     │   │ analise/                 │ │ relatorios/  │ │ notificacoes/    │ │ persistencia/│
     │  omie (clientes) │   │                          │ │              │ │                  │ │              │
     │  sieg            │──▶│  classificador           │▶│  Jinja2→PDF  │▶│  email (SMTP)    │ │  SQLite      │
     │  fgts (falha)    │   │  parser situação fiscal  │ │  consolidado │ │  whatsapp/DigiSac│ │  execuções,  │
     │  ecac / pgfn     │   │  regras por certidão     │ │  por cliente │ │  (dry-run)       │ │  consultas,  │
     │  cadin           │   └──────────────────────────┘ └──────────────┘ └──────────────────┘ │  envios      │
     │  municipal SP    │                                                                      └──────────────┘
     └──────────────────┘
```

| Camada | Responsabilidade |
|---|---|
| `dominio/` | Modelos puros (`Cliente`, `Analista`, `Certidao`, `Debito`, `StatusRegularidade`, `ResultadoConsulta`). Não depende de nenhuma outra camada. |
| `integracoes/` | Um adapter por fonte externa, todos implementando a mesma interface (`consultar(cliente) -> ResultadoConsulta`). É o que permite o fallback do FGTS e o uso de mocks nos testes. |
| `analise/` | Regras de negócio: classificar regular/irregular, extrair códigos de débito da Situação Fiscal, cruzar com a PGFN. |
| `relatorios/` | Gera os relatórios do analista (HTML/PDF) a partir de templates Jinja2. |
| `notificacoes/` | Envio por e-mail (SMTP) e WhatsApp. Respeita `DRY_RUN`, que só registra o que seria enviado. |
| `persistencia/` | SQLite: cadastro de clientes/analistas, histórico de execuções, consultas e envios (idempotência). |
| `pipeline/` | Orquestra o fluxo por cliente, isolando falhas: uma fonte com erro não para as demais. |
| `cli.py` | Ponto de entrada (`automacao ...`). |

**Hospedagem:** instância na AWS (Lightsail, a confirmar), com o pipeline rodando uma vez por mês via cron.

**Princípios:** dry-run por padrão · segredos só em `.env`/`secrets/` · falhas isoladas por fonte/cliente ·
nada é reenviado ao cliente no mesmo mês · tudo fica registrado.

## Árvore de diretórios

```
Automacao Omie/
├── CLAUDE.md                     # convenções e preferências para o Claude Code
├── README.md                     # este arquivo
├── pyproject.toml                # dependências e configuração (uv, ruff, pytest)
├── .env.example                  # variáveis de ambiente necessárias (sem valores reais)
├── .gitignore                    # ignora .env, secrets/, data/, logs/
├── docs/
│   ├── REQUISITOS.md             # requisitos funcionais, não funcionais e questões em aberto
│   ├── BACKLOG.md                # backlog priorizado por fases
│   └── processo-manual.md        # passo a passo da análise da Geovânia (a levantar)
├── src/
│   └── automacao/
│       ├── __init__.py
│       ├── cli.py                # comandos: executar, clientes importar, ...
│       ├── config.py             # Settings (pydantic-settings) + DRY_RUN
│       ├── dominio/
│       │   ├── cliente.py        # Cliente, Analista
│       │   ├── certidao.py       # Certidao, TipoCertidao, StatusRegularidade
│       │   └── debito.py         # Debito, ResultadoConsulta
│       ├── integracoes/
│       │   ├── base.py           # interface FonteCertidao
│       │   ├── omie.py           # sincroniza clientes e analistas (RF-CLI-01)
│       │   ├── sieg.py           # certidões + Situação Fiscal (RF-CERT-01, RF-SF-01); API ou RPA
│       │   ├── fgts.py           # só detecta falha do FGTS no SIEG (RF-CERT-05)
│       │   ├── ecac.py           # Portal do Contribuinte, se necessário (Q-03)
│       │   ├── pgfn.py           # RF-RFB-03
│       │   ├── cadin.py          # RF-CADIN-*
│       │   └── municipais/
│       │       └── sao_paulo.py  # certidão da Prefeitura de SP (RF-MUN-01)
│       ├── analise/
│       │   ├── classificador.py  # regular / irregular / falha (RF-CERT-02)
│       │   └── situacao_fiscal.py# parser do PDF + códigos de débito (RF-SF-02, RF-RFB-02)
│       ├── relatorios/
│       │   ├── gerador.py        # HTML → PDF (RF-SF-03/04, RF-RFB-04, RF-FGTS-03)
│       │   └── templates/        # *.html.j2 (relatório do analista, e-mail ao cliente)
│       ├── notificacoes/
│       │   ├── email.py          # SMTP (RF-CERT-03, RF-CERT-04)
│       │   └── whatsapp.py       # DigiSac (RF-CERT-04)
│       ├── persistencia/
│       │   ├── banco.py          # engine SQLite / sessão
│       │   └── modelos.py        # tabelas: cliente, analista, execucao, consulta, envio
│       └── pipeline/
│           └── executar.py       # orquestração por cliente (fluxo em docs/REQUISITOS.md §3)
├── tests/
│   ├── fixtures/                 # PDFs e respostas de API fictícios (sem dados reais)
│   ├── test_classificador.py
│   ├── test_situacao_fiscal.py
│   └── integracoes/              # testes dos adapters com HTTP mockado (respx)
├── secrets/                      # certificado A1 (.pfx) etc. (NÃO versionado)
├── data/                         # certidões e relatórios baixados/gerados (NÃO versionado)
└── logs/                         # logs de execução (NÃO versionado)
```

> Hoje só existem `CLAUDE.md`, `README.md` e `docs/`. O restante da árvore é o alvo e será criado nos
> itens 0.3/0.4 do backlog.

## Uso (planejado)

```bash
uv sync
cp .env.example .env              # preencher credenciais
uv run automacao clientes importar clientes.csv
uv run automacao executar --dry-run                 # simula, sem enviar nada
uv run automacao executar --cliente 00.000.000/0001-00
```
