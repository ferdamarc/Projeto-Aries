<h1 align="center">Projeto ARIES</h1>
<h3 align="center">Pipeline ETL para Dados SIH/SUS em um Data Lake House</h3>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10"/>
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas"/>
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/FAPESP-Financiado-00A693?style=flat-square" alt="FAPESP"/>
  <img src="https://img.shields.io/badge/UNIFESP%2FICT-Iniciação%20Científica-003F7F?style=flat-square" alt="UNIFESP"/>
  <img src="https://img.shields.io/badge/CEPID--ARIES-Resistência%20Antimicrobiana-8B0000?style=flat-square" alt="CEPID-ARIES"/>
</p>

---

## Sobre o Projeto

O **Projeto ARIES** é uma Iniciação Científica financiada pela [FAPESP](https://fapesp.br/) que desenvolve um pipeline ETL (Extract, Transform, Load) para integrar dados do **SIH/SUS** (Sistema de Informações Hospitalares do SUS) em um **Data Lake House** dimensional. O objetivo é criar uma infraestrutura de dados robusta para subsidiar pesquisas sobre **resistência antimicrobiana (RAM)** em hospitais públicos brasileiros.

| Campo | Informação |
|---|---|
| **Bolsista** | Fernando Daniel Marcelino |
| **Orientador** | Prof. Dr. Elbert Einstein Nehrer Macau |
| **Coorientadora** | Profa. Dra. Daniela Leal Musa |
| **Instituição** | Universidade Federal de São Paulo — Instituto de Ciência e Tecnologia |
| **Grupo de Pesquisa** | CEPID-ARIES (Instituto Paulista de Resistência aos Antimicrobianos) |
| **Financiamento** | FAPESP — Fundação de Amparo à Pesquisa do Estado de São Paulo |

---

## Motivação

A resistência antimicrobiana é um dos maiores desafios de saúde pública do século XXI:

- Estima-se que **7,7 milhões de pessoas** morrem anualmente por infecções bacterianas
- Projeções indicam que esse número pode chegar a **10 milhões até 2050**
- O Brasil, com seu extenso sistema público de saúde, gera dados hospitalares em larga escala via SIH/SUS que são subutilizados para vigilância epidemiológica

Este projeto utiliza esses dados para mapear a incidência e distribuição da RAM nos hospitais públicos brasileiros, transformando registros brutos do DATASUS em informação analítica estruturada.

---

## Arquitetura

```
┌─────────────┐     ┌──────────────────┐     ┌──────────────────────┐     ┌───────────────┐
│   DATASUS   │────▶│    Extração      │────▶│    Transformação     │────▶│  Data Lake    │
│  (SIH/SUS)  │     │ pysus / DBC/CSV  │     │ limpeza · CID-10 ·  │     │   House       │
│             │     │ Staging Postgres  │     │ star schema · chaves │     │  PostgreSQL   │
└─────────────┘     └──────────────────┘     └──────────────────────┘     └───────┬───────┘
                                                                                   │
                                                                           ┌───────▼───────┐
                                                                           │   Dashboard   │
                                                                           │   Streamlit   │
                                                                           └───────────────┘
```

O pipeline é composto por três subsistemas orquestrados pelo `scheduler.py`:

| Subsistema | Arquivo | Responsabilidade |
|---|---|---|
| **Extract** | `subsystem_extract.py` | Baixa arquivos SIH/SUS do DATASUS via `pysus` e persiste no Postgres de staging |
| **Transform** | `subsystem_trans.py` | Lê o staging, aplica limpeza e deriva o esquema estrela |
| **Load** | `subsystem_load.py` | Escreve as tabelas dimensionais e de fato no banco analítico |

> O subsistema de extração (`pysus`) requer ambiente Linux; em Windows, o scheduler executa apenas a etapa de transformação/carga.

---

## Modelo Dimensional (Star Schema)

```
                        ┌──────────────────┐
                        │   dim_tempo      │
                        │  (ID_TEMPO)      │
                        └────────┬─────────┘
                                 │
  ┌──────────────────┐  ┌────────▼──────────┐  ┌──────────────────┐
  │  dim_paciente    │  │  fato_internacao  │  │   dim_hospital   │
  │  (ID_PACIENTE)   │──│                   │──│   (ID_HOSPITAL)  │
  └──────────────────┘  │  • VAL_TOT        │  └──────────────────┘
                        │  • DIAS_PERM.     │
  ┌──────────────────┐  │  • VAL_MEDIO_DIA  │  ┌──────────────────┐
  │ dim_localizacao  │  │  • PASSOU_UTI     │  │ dim_diagnostico  │
  │ (ID_LOCALIZACAO) │──│  • MORTE          │──│ (ID_DIAGNOSTICO) │
  └──────────────────┘  └────────┬──────────┘  └──────────────────┘
                                 │
                        ┌────────▼─────────┐
                        │ dim_procedimento │
                        │ (ID_PROCEDIMENTO)│
                        └──────────────────┘
```

Chaves surrogate são geradas com prefixo por domínio: `H{CNES}` (hospital), `D{DIAG_PRINC}` (diagnóstico), `L{MUNIC_RES}` (localização).

---

## Dashboard

O dashboard Streamlit oferece seis visões analíticas sobre os dados do SIH/SUS:

| Aba | Conteúdo |
|---|---|
| **Visão Geral** | Indicadores consolidados de internações |
| **Análise Temporal** | Séries históricas de admissões e custos |
| **Análise Geográfica** | Distribuição por município e estado |
| **Análise de Diagnósticos** | Frequência de CID-10, grupos e subgrupos |
| **Análise de Custos** | Distribuição de valores por procedimento e UTI |
| **Análise de Desfechos** | Óbitos, tempo de permanência, uso de UTI |

---

## Tecnologias

| Categoria | Tecnologia | Uso |
|---|---|---|
| Linguagem | Python 3.10 | Pipeline e dashboard |
| Banco de Dados | PostgreSQL + PgAdmin 4 | Staging e Data Lake House |
| Acesso a dados | PySUS | Download de arquivos SIH/SUS do DATASUS |
| Manipulação | Pandas / NumPy | Transformação e limpeza dos dados |
| ORM / Conexão | SQLAlchemy | Interface com o PostgreSQL |
| Visualização | Streamlit | Dashboard analítico interativo |
| Agendamento | Schedule | Execução diária automatizada do pipeline |

---

## Estrutura do Repositório

```
Projeto-Aries/
│
├── simple-OLAP-model/           # Pipeline de referência (arquivo → CSV)
│   ├── main.py                  # ETL: limpeza → CID-10 → star schema → exportação CSV
│   ├── dashboard.py             # Dashboard Streamlit (consome os CSVs)
│   ├── modules/                 # Um módulo por aba do dashboard
│   └── utils/                   # Funções auxiliares compartilhadas
│
├── Scripts/Python/
│   ├── subsistemas-etl/         # Pipeline com banco de dados (produção)
│   │   ├── scheduler.py         # Orquestrador — roda diariamente às 21h59
│   │   ├── subsystem_extract.py # Extração via pysus → Postgres staging
│   │   ├── subsystem_trans.py   # Transformação staging → star schema
│   │   ├── subsystem_load.py    # Carga no banco analítico
│   │   ├── database_operations.py # Definição de colunas e operações SQLAlchemy
│   │   └── conectando_bd.py     # Factory do engine PostgreSQL
│   │
│   └── cid-10/                  # Scripts de carga da tabela CID-10 (DBF → CSV → Postgres)
│
├── OLAP-fato-epidemiologia/     # Visão epidemiológica alternativa (Streamlit)
├── Notebooks/                   # Exploração e prototipagem (não produção)
└── requirements.txt
```

---

## Como Executar

### Pré-requisitos

- Python 3.10+
- PostgreSQL 13+ em execução local
- Linux (ou WSL2) para o subsistema de extração via `pysus`

### Instalação

```bash
git clone https://github.com/ferdamarc/Projeto-Aries.git
cd Projeto-Aries

# requirements.txt é codificado em UTF-16
pip install -r requirements.txt
```

### Configuração

Antes de executar, edite os arquivos abaixo com suas credenciais e caminhos locais:

| Arquivo | O que configurar |
|---|---|
| `simple-OLAP-model/main.py` | `file_path` (CSV de entrada) e `output_path` |
| `simple-OLAP-model/dashboard.py` | `base_dir` em `carregar_dados()` |
| `Scripts/Python/subsistemas-etl/subsystem_extract.py` | Credenciais do Postgres + `STAGE_PATH` |
| `Scripts/Python/subsistemas-etl/subsystem_trans.py` | Credenciais do Postgres + caminho do CSV |

### Execução

```bash
# Pipeline de referência (arquivo → CSVs do star schema)
python simple-OLAP-model/main.py

# Dashboard principal
streamlit run simple-OLAP-model/dashboard.py

# Dashboard epidemiológico alternativo
streamlit run OLAP-fato-epidemiologia/dashboardEpidemiologia.py

# Pipeline com banco de dados (agendado para rodar diariamente às 21h59)
cd Scripts/Python/subsistemas-etl
python scheduler.py
```

---

## Licença

Este projeto é resultado de pesquisa acadêmica financiada com recursos públicos via FAPESP. Uso e reprodução devem citar a fonte e os autores.
