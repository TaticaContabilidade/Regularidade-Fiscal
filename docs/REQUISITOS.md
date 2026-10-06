# Requisitos — Automação de Regularidade Fiscal

Origem: reunião de 01/09 com a analista Geovânia (`Reunião 01 09 Geovânia.md`).

## Glossário

| Termo | Significado |
|---|---|
| **SIEG** | Plataforma usada pelo escritório; em *Pendências → Situações fiscais* disponibiliza as certidões por cliente. |
| **Certidão negativa / regular** | Atesta que o cliente não tem débitos em aberto (referentes ao mês anterior). |
| **Certidão positiva / irregular** | Indica débitos pendentes. |
| **Situação Fiscal** | Relatório de Situação Fiscal da Receita Federal, que lista as pendências e os códigos dos débitos. |
| **PGFN** | Procuradoria-Geral da Fazenda Nacional: débitos inscritos em dívida ativa. |
| **e-CAC / Portal do Contribuinte** | Portal da Receita Federal para consultar a situação do contribuinte. |
| **CRF/FGTS** | Certificado de Regularidade do FGTS (Caixa). |
| **CADIN** | Cadastro informativo de créditos não quitados do setor público federal. |
| **Analista** | Pessoa do escritório responsável pelo cliente; recebe os casos irregulares. |

## Convenção de IDs

`RF-<MÓDULO>-NN` (requisito funcional) · `RNF-NN` (requisito não funcional).
Módulos: `CERT` (certidões/SIEG), `MUN` (municipais), `FGTS` (fora do escopo), `RFB` (portal do contribuinte/PGFN),
`SF` (situação fiscal), `CADIN`, `CLI` (cadastro), `NOT` (notificações).

> **Nota:** na ata original, vários itens listados como "não funcionais" descrevem comportamento do sistema
> (baixar, consultar, montar relatório). Aqui eles foram reclassificados como **funcionais**, e os
> requisitos não funcionais reais foram propostos na seção RNF para validação.

---

## 1. Requisitos Funcionais

### 1.1 Cadastro de clientes (CLI): pré-requisito implícito
| ID | Requisito | Origem |
|---|---|---|
| RF-CLI-01 | O sistema deve sincronizar com o **Omie** a lista de clientes a verificar (CNPJ, razão social, e-mails, WhatsApp, analista responsável, município, ativo/inativo). | Implícito + Q-08 |
| RF-CLI-02 | O sistema deve manter o cadastro de analistas (nome, e-mail), vinculado aos clientes pelo campo definido em Q-13. | Implícito + Q-13 |

### 1.2 Certidões via SIEG (CERT)
| ID | Requisito | Origem |
|---|---|---|
| RF-CERT-01 | O sistema deve baixar as certidões de cada cliente no SIEG (via API, se existir, ou RPA; ver Q-01). | Ata RF 1 |
| RF-CERT-02 | O sistema deve verificar se cada certidão está **regular** ou **irregular**. | Ata RF 2 / 2.1 |
| RF-CERT-03 | O sistema deve enviar a certidão irregular ao analista responsável por e-mail (SMTP). | Ata RF 2.2 |
| RF-CERT-04a | O WhatsApp ao cliente é enviado pelo **DigiSac**. | Q-06 |
| RF-CERT-04 | O sistema deve enviar as certidões regulares ao cliente por e-mail **e** WhatsApp, **somente quando todas as certidões do cliente estiverem regulares**. Se houver qualquer certidão irregular ou falha de consulta, nada é enviado ao cliente e o caso vai para o analista. | Ata RF 3 + Q-07 |
| RF-CERT-05 | O sistema deve notificar o analista quando a consulta do FGTS pelo SIEG falhar. | Ata RF 3 (2º) |

### 1.3 Certidões municipais (MUN)
| ID | Requisito | Origem |
|---|---|---|
| RF-MUN-01 | O sistema deve baixar as certidões municipais dos clientes de **São Paulo** (único município atendido). | Ata RNF 1 + Q-05 |

### 1.4 FGTS: consulta direta como fallback (FGTS): **fora do escopo** (Q-04)
Decisão: quando o FGTS falhar no SIEG, o sistema só notifica o analista (RF-CERT-05). Os itens abaixo ficam
registrados para eventual retomada, mas não serão implementados.

| ID | Requisito | Origem |
|---|---|---|
| ~~RF-FGTS-01~~ | ~~Se a consulta do FGTS pelo SIEG falhar, consultar a regularidade direto na Caixa.~~ | Ata RNF 2 |
| ~~RF-FGTS-02~~ | ~~Identificar se o cliente está irregular no FGTS.~~ | Ata RNF 2.1 |
| ~~RF-FGTS-03~~ | ~~Montar um relatório com as irregularidades de FGTS.~~ | Ata RNF 2.2 |
| ~~RF-FGTS-04~~ | ~~Enviar esse relatório ao analista.~~ | Ata RNF 2.3 |

### 1.5 Portal do Contribuinte / e-CAC / PGFN (RFB)
| ID | Requisito | Origem |
|---|---|---|
| RF-RFB-01 | O sistema deve consultar o portal do contribuinte e verificar se o cliente possui irregularidades. | Ata RNF 3 |
| RF-RFB-02 | O sistema deve extrair os códigos dos débitos do relatório "Situação Fiscal". | Ata RNF 4 |
| RF-RFB-03 | Com esses códigos, o sistema deve consultar a situação na PGFN pelo e-CAC. | Ata RNF 5 |
| RF-RFB-04 | O sistema deve montar um relatório dos débitos irregulares encontrados no portal do contribuinte e enviá-lo ao analista. | Ata RNF 6 |

### 1.6 CADIN (CADIN)
| ID | Requisito | Origem |
|---|---|---|
| RF-CADIN-01 | O sistema deve baixar a certidão do CADIN. | Ata CADIN 1 |
| RF-CADIN-02 | Havendo débito irregular, o sistema deve enviar a certidão do CADIN ao analista. | Ata CADIN 2 |

### 1.7 Situação Fiscal (SF)
| ID | Requisito | Origem |
|---|---|---|
| RF-SF-01 | O sistema deve baixar o relatório "Situação Fiscal" de cada cliente **pelo SIEG** (que consulta o e-CAC). | Ata SF 1 + Q-02 |
| RF-SF-02 | O sistema deve analisar o relatório e determinar se o cliente está regular. | Ata SF 2 |
| RF-SF-03 | O sistema deve gerar um relatório resumido da situação fiscal. | Ata SF 3 |
| RF-SF-04 | O sistema deve consolidar esse relatório com o resultado da PGFN (RF-RFB-03). | Ata SF 4 |
| RF-SF-05 | O sistema deve enviar o relatório consolidado ao analista. | Ata SF 5 |

### 1.8 Notificações e execução (NOT): derivados
| ID | Requisito | Origem |
|---|---|---|
| RF-NOT-01 | O sistema deve enviar ao analista **um único e-mail consolidado por cliente** (ou por analista) em cada execução, em vez de vários e-mails soltos. | Proposto |
| RF-NOT-02 | O sistema deve gerar um resumo da execução (clientes regulares, irregulares e com falha). | Proposto |
| RF-NOT-03 | O sistema deve permitir executar para todos os clientes ou para um único CNPJ. | Proposto |

---

## 2. Requisitos Não Funcionais (propostos: validar)

| ID | Categoria | Requisito |
|---|---|---|
| RNF-01 | Segurança | Credenciais e certificado digital A1 armazenados fora do código (`.env`/`secrets/`), nunca versionados nem logados. |
| RNF-02 | LGPD | Dados de clientes e PDFs ficam apenas na instância AWS do escritório (região `sa-east-1`, São Paulo, preferencialmente); testes usam dados fictícios. Definir política de retenção dos PDFs. |
| RNF-03 | Resiliência | Falhas em uma fonte (SIEG, FGTS, e-CAC…) não interrompem o processamento dos demais clientes/fontes; retentativas com backoff exponencial. |
| RNF-04 | Idempotência | Reexecutar o pipeline no mesmo mês não reenvia certidões já enviadas ao cliente. |
| RNF-05 | Rastreabilidade | Toda consulta, resultado e envio fica registrado (SQLite + logs estruturados) com data, cliente e fonte. |
| RNF-06 | Segurança operacional | Modo `--dry-run` ativo por padrão em ambientes que não sejam produção; nenhum envio real sem configuração explícita. |
| RNF-07 | Agendamento | Execução automática **uma vez por mês** (dia configurável, Q-15) via cron na instância AWS, além de execução manual pela CLI. |
| RNF-08 | Manutenibilidade | Cada fonte externa isolada atrás de uma interface (adapter) com testes usando mocks. |
| RNF-09 | Desempenho | Processar toda a carteira de clientes em uma janela aceitável (a definir; ex.: < 2 h), respeitando os limites de requisição das APIs. |
| RNF-10 | Usabilidade | Relatórios ao analista em PDF/HTML legível, com o débito, o código, a fonte e o link/anexo da certidão. |

---

## 3. Fluxo do processo (visão alvo)

```
0. Sincronizar clientes ativos do Omie .................. RF-CLI-01
Para cada cliente ativo:
  1. Baixar certidões no SIEG ............................ RF-CERT-01
     └─ FGTS falhou no SIEG? → só notificar o analista ... RF-CERT-05 (Q-04)
  2. Baixar certidão municipal (São Paulo) ............... RF-MUN-01
  3. Baixar CADIN ........................................ RF-CADIN-01
  4. Baixar Situação Fiscal pelo SIEG → extrair códigos .. RF-SF-01, RF-RFB-02
     └─ consultar PGFN pelos códigos ..................... RF-RFB-03 (Q-03)
  5. Classificar cada item: regular / irregular / falha .. RF-CERT-02, RF-SF-02
  6. TODAS regulares         → enviar certidões ao cliente (e-mail + WhatsApp/DigiSac) .... RF-CERT-04
     Alguma irregular/falha  → nada vai ao cliente; relatório consolidado ao analista
                               (SF + PGFN + CADIN + falha FGTS) ... RF-CERT-03, RF-SF-03..05, RF-RFB-04, RF-CADIN-02
  7. Registrar tudo e enviar o resumo da execução ........ RF-NOT-02
```

Regra de envio (Q-07, decidida): o cliente só recebe as certidões quando **todas** estão regulares.

---

## 4. Questões em aberto

| ID | Questão | Impacta |
|---|---|---|
### 4.1 Pendentes

| ID | Questão | Impacta |
|---|---|---|
| Q-01 | **Parcialmente respondida.** A [API SIEG para Clientes](https://integracoes.sieg.com/clientes-sieg/docs/introducao) existe, mas **não tem endpoints de certidões, Situação Fiscal nem pendências**. Analisei os 24 contratos OpenAPI publicados (em 06/10/2026), que cobrem só: XMLs fiscais (baixar/contar/enviar NF-e, CT-e, NFS-e, NFC-e, CF-e), manifestação, relatórios de XML, gestão de certificados (listar/registrar/status) e autenticação JWT/API Key. **Próximo passo:** perguntar ao suporte do SIEG se existe API (mesmo não documentada/beta) para o módulo de certidões/situação fiscal. Se não existir, a integração será por **automação do navegador (RPA, Playwright)** no portal do SIEG. | RF-CERT-*, RF-SF-01, RF-CADIN-01 |
| Q-03 | **Escopo reduzido.** A Situação Fiscal vem pelo SIEG (Q-02). Falta saber se a consulta dos débitos na PGFN pelos códigos (RF-RFB-03) também pode ser feita pelo SIEG, ou se precisa de acesso próprio ao e-CAC (Integra Contador/SERPRO, que é pago e exige certificado/procuração). Confirmar também se o relatório de Situação Fiscal já traz a seção da PGFN, o que dispensaria a consulta extra. | RF-RFB-03 |
| Q-11 | Detalhar o "Método de Análise Geovânia" (está incompleto na ata: só o passo 1, "Consultar situação fiscal"). **A definir depois.** | RF-SF-02 |
| Q-12 | Qual o texto/modelo dos e-mails e mensagens ao cliente e ao analista? **A definir depois.** | RF-NOT-* |
| Q-13 | No Omie, qual campo identifica o **analista responsável** por cada cliente, e onde ficam o e-mail e o WhatsApp de contato para envio das certidões? | RF-CLI-01, RF-CLI-02 |
| Q-14 | Confirmar a infraestrutura: "AWS lightway" é o **Amazon Lightsail**? Se o SIEG exigir RPA, a instância precisa de pelo menos 2 GB de RAM para rodar o navegador headless. | Infra |
| Q-15 | Em que dia do mês o sistema deve rodar (ex.: dia 5, após a atualização das certidões no SIEG)? | RNF-07 |

### 4.2 Resolvidas

| ID | Decisão | Impacto |
|---|---|---|
| Q-02 | A Situação Fiscal é **baixada pelo SIEG**, que por sua vez acessa o e-CAC. | RF-SF-01 usa o adapter do SIEG, não o e-CAC direto. |
| Q-04 | Se o FGTS falhar no SIEG, o fallback é **apenas notificar o analista**. Não haverá consulta direta à Caixa. | RF-FGTS-01..04 saem do escopo; RF-CERT-05 cobre o caso. |
| Q-05 | Certidões municipais: **apenas São Paulo**. | RF-MUN-01 terá um único adapter (Prefeitura de SP). |
| Q-06 | WhatsApp pelo **DigiSac**. | `notificacoes/whatsapp.py` integra com a API do DigiSac. |
| Q-07 | Enviar ao cliente **somente quando todas as certidões estiverem regulares**. | RF-CERT-04. |
| Q-08 | A lista de clientes será **obtida do Omie** (API). | Novo adapter `integracoes/omie.py`; RF-CLI-01 vira sincronização. |
| Q-09 | Execução **uma vez por mês**. | RNF-07 (dia a definir em Q-15). |
| Q-10 | Hospedagem na **nuvem AWS** (Lightsail, a confirmar em Q-14). | Agendamento por cron na instância; segredos e PDFs ficam no servidor. |
