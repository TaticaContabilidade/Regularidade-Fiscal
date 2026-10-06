# CLAUDE.md

Guia para o Claude Code trabalhar neste repositório.

## Contexto do projeto

Automação do processo de **verificação de regularidade fiscal de clientes** da Tática Contabilidade
(certidões negativas, Situação Fiscal, PGFN, FGTS e CADIN), hoje feito manualmente pela analista Geovânia.

- Fonte dos requisitos: `~/Documentos/Tatica-gestao-contabil/Reunião 01 09 Geovânia.md` (reunião de 01/09).
- Requisitos detalhados: [`docs/REQUISITOS.md`](docs/REQUISITOS.md)
- Backlog priorizado: [`docs/BACKLOG.md`](docs/BACKLOG.md)
- Arquitetura e árvore de diretórios: [`README.md`](README.md)

> Fora do escopo atual: o dashboard de dados do Omie (reunião de 25/09 com Priscila & Gerson,
> `~/Documentos/Tatica-gestao-contabil/Reunião 25 09 Priscila.md`). Será tratado como projeto/épico separado.

## Preferências de trabalho

### Idioma
- Toda comunicação, documentação, comentários e mensagens de commit em **português (pt-BR)**.
- Identificadores de código em português para termos de domínio (`certidao`, `cliente`, `situacao_fiscal`,
  `analista`), sem acentos. Termos técnicos genéricos podem ficar em inglês (`client`, `retry`, `settings`).

### Stack
- **Python 3.12**, gerenciado com **uv** (`pyproject.toml`).
- HTTP: `httpx` · Configuração: `pydantic-settings` (`.env`) · Modelos: `pydantic`.
- Persistência: SQLite (histórico de execuções, status por cliente/certidão) via SQLAlchemy.
- Relatórios: Jinja2 (HTML) → PDF com WeasyPrint.
- Testes: `pytest` (+ `respx` para mockar HTTP) · Lint/format: `ruff`.
- Agendamento: cron/systemd timer chamando a CLI (sem processo residente).

### Comandos
```bash
uv sync                          # instala dependências
uv run pytest                    # testes
uv run ruff check . && uv run ruff format .
uv run automacao executar --dry-run          # roda o pipeline sem enviar nada
uv run automacao executar --cliente <CNPJ>   # roda para um único cliente
```

### Regras importantes
1. **Nunca enviar e-mail ou WhatsApp real** a clientes/analistas durante desenvolvimento. Todo envio passa
   pela camada `notificacoes/` e respeita `DRY_RUN=true` (padrão). Desligar o dry-run só com confirmação
   explícita do usuário.
2. **Segredos fora do código**: credenciais (SIEG, SMTP, WhatsApp, certificado digital A1 `.pfx`) ficam em
   `.env` / `secrets/` — ambos no `.gitignore`. Nunca ler, imprimir ou commitar o conteúdo deles.
3. **Dados de clientes são sensíveis (LGPD)**: não usar CNPJs/dados reais em testes ou fixtures; usar dados
   fictícios em `tests/fixtures/`. PDFs baixados ficam em `data/` (ignorado pelo git).
4. **Toda integração externa atrás de uma interface** em `integracoes/`, para poder ser mockada e trocada
   (ex.: FGTS via SIEG → fallback direto).
5. Ao concluir um item, **atualizar `docs/BACKLOG.md`** (status) e referenciar o ID do requisito
   (ex.: `RF-CERT-02`) no commit/PR.
6. Antes de implementar uma integração cuja API não foi validada (ver "Questões em aberto" em
   `docs/REQUISITOS.md`), confirmar com o usuário em vez de supor endpoints.
7. Mudanças pequenas e incrementais; um item do backlog por vez.
