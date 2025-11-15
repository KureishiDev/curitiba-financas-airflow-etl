
# Curitiba Public Finance ETL

Pipeline de engenharia de dados utilizando **Apache Airflow**, **PostgreSQL**, **Python** e **Docker** para processar dados públicos de **Receitas** e **Despesas** da Prefeitura de Curitiba.

O objetivo deste projeto é montar um fluxo completo de **ingestão, transformação e modelagem dimensional** em camadas (Staging, Silver e Gold), pronto para servir como base de análise em ferramentas de BI.

---

## Índice

- [Visão geral](#visão-geral)
- [Fonte dos dados](#fonte-dos-dados)
- [Arquitetura](#arquitetura)
- [Tecnologias](#tecnologias)
- [Camadas de dados](#camadas-de-dados)
- [Pipeline no Airflow](#pipeline-no-airflow)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Como executar](#como-executar)
- [Possíveis análises](#possíveis-análises)
- [Próximos passos](#próximos-passos)
- [Resumo em inglês](#resumo-em-inglês)

---

## Visão geral

Este projeto implementa um fluxo de ETL com foco nas finanças públicas do município de Curitiba. A partir de arquivos CSV de **Receitas** e **Despesas**, o pipeline:

- faz ingestão dos dados em um banco PostgreSQL;
- organiza as informações em camadas de dados (Staging, Silver, Gold);
- constrói dimensões e fatos para análise financeira;
- orquestra todas as etapas com Apache Airflow, rodando em containers Docker.

O resultado é um pequeno Data Warehouse local, pronto para ser consumido por ferramentas de BI ou usado como case de portfólio em engenharia de dados.

---

## Fonte dos dados

Todos os dados utilizados neste projeto são públicos e foram obtidos no:

**Portal de Dados Abertos da Prefeitura de Curitiba**  
https://dadosabertos.curitiba.pr.gov.br

Os arquivos utilizados correspondem às bases de:

- **Receitas** do município de Curitiba, em formato CSV.
- **Despesas** do município de Curitiba, em formato CSV.

Esses dados são mantidos e publicados pela própria Prefeitura de Curitiba para fins de transparência e controle social. O projeto não altera o significado dos dados, apenas os organiza e modela para fins analíticos.

---

## Arquitetura

```text
Arquivos CSV (Receitas e Despesas)
    ↓
Python (ingestão) + SQLAlchemy
    ↓
PostgreSQL (camada STAGING)
    ↓
SQL (transformações para camada SILVER)
    ↓
SQL (modelagem DIMENSÕES e FATOS na camada GOLD)
    ↓
BI / Analytics (Power BI, Metabase, Superset)
```

A infraestrutura é orquestrada via **Docker Compose**, com containers separados para:

- Airflow Webserver
- Airflow Scheduler
- PostgreSQL

---

## Tecnologias

| Tecnologia      | Uso principal                         |
|-----------------|---------------------------------------|
| Apache Airflow  | Orquestração de pipelines de dados    |
| PostgreSQL      | Data Warehouse local                  |
| Docker Compose  | Infraestrutura containerizada         |
| Python          | Ingestão dos CSV e conexão com o banco|
| Pandas          | Leitura e pré-processamento dos CSV   |
| SQL (Postgres)  | Transformações e modelagem dimensional|

---

## Camadas de dados

### Staging

Camada bruta tipada, espelhando a estrutura dos CSV com o mínimo de tratamento necessário para armazenamento.

Tabelas principais:

- `stg_receitas`
- `stg_despesas`

### Silver

Camada refinada, com dados limpos e colunas derivadas, pronta para servir de base para modelagem analítica.

Tabelas principais:

- `silver_receitas`
- `silver_despesas`

Exemplos de tratamentos:

- padronização de tipos numéricos e datas;
- extração de ano e mês;
- limpeza de registros vazios ou inválidos.

### Gold

Camada de Data Warehouse, organizada em dimensões e fatos, próxima de um modelo estrela.

Dimensões:

- `dim_tempo`
- `dim_orgao`
- `dim_fonte`

Fatos:

- `fato_receita`
- `fato_despesa`

Essas tabelas podem ser conectadas diretamente a ferramentas de BI para construção de painéis e relatórios.

---

## Pipeline no Airflow

A DAG principal se chama **`etl_curitiba_financas`**. Ela está organizada em **TaskGroups** para deixar o fluxo mais legível e modular.

Fluxo lógico:

```text
pipeline_staging
    create_staging_tables

pipeline_silver
    build_silver_layer

pipeline_gold_dimensions
    build_dim_tempo
    build_dim_orgao
    build_dim_fonte

pipeline_gold_facts
    build_fato_receita
    build_fato_despesa
```

Os grupos de dimensões e fatos na camada gold são executados em paralelo dentro de seus respectivos TaskGroups, reduzindo o tempo total de execução.

---

## Estrutura do repositório

```text
curitiba-financas-airflow-etl/
│
├── dags/
│   ├── etl_curitiba_financas_dag.py   # DAG principal do Airflow
│   └── sql/                           # Scripts SQL usados pela DAG
│       ├── create_staging_tables.sql
│       ├── build_silver.sql
│       ├── dim_tempo.sql
│       ├── dim_orgao.sql
│       ├── dim_fonte.sql
│       ├── fato_receita.sql
│       └── fato_despesa.sql
│
├── src/
│   └── etl/
│       ├── ingest_receitas.py         # ingestão das receitas
│       └── ingest_despesas.py         # ingestão das despesas
│
├── airflow/
│   ├── docker-compose.yaml            # stack do Airflow + Postgres
│   └── Dockerfile                     # customizações de imagem (se houver)
│
├── sql/                               # SQL original usado em desenvolvimento
│
└── README.md
```

---

## Como executar

### 1. Clonar o repositório

```bash
git clone https://github.com/SEU-USUARIO/curitiba-financas-airflow-etl.git
cd curitiba-financas-airflow-etl
```

### 2. Subir o ambiente do Airflow

```bash
cd airflow
docker compose up -d
```

Por padrão, o Airflow estará acessível em:

```text
http://localhost:8081
```

Usuário e senha padrão (caso não tenha sido alterado):

- usuário: `admin`
- senha: `admin`

### 3. Configurar a conexão Postgres no Airflow

No menu do Airflow:

- `Admin` → `Connections` → `+`

Preencha:

- Conn Id: `curitiba_postgres`
- Conn Type: `Postgres`
- Host: `postgres`
- Schema: `curitiba_financas`
- Login: `airflow`
- Password: `airflow`
- Port: `5432`

Clique em **Test** e depois salve.

### 4. Garantir que os scripts SQL estão acessíveis

Na máquina host, certifique-se de que os arquivos SQL estão em `dags/sql`. Se necessário:

```bash
# Exemplo em Windows PowerShell
cd C:\Users\vinic\curitiba-financas-airflow-etl
copy .\sql\*.sql .\dags\sql\
```

Dentro do container do webserver:

```bash
docker exec -it airflow-webserver-1 ls /opt/airflow/dags/sql
```

Os arquivos `.sql` devem aparecer listados.

### 5. Rodar a DAG

No Airflow:

1. Ative a DAG `etl_curitiba_financas` na tela inicial.
2. Clique em `Trigger DAG` para iniciar a execução.
3. Acompanhe o fluxo na aba `Graph` ou `Grid`.

---

## Possíveis análises

Com a camada gold criada, este projeto permite responder perguntas como:

- Qual a evolução mensal da receita do município em cada exercício.
- Quais órgãos mais gastam e em que tipos de despesa.
- Quais programas, ações e funções concentram maior volume de despesas.
- Como se comparam valores empenhados, liquidados e pagos ao longo do tempo.
- Como diferentes fontes de recurso são distribuídas entre órgãos e programas.

---

## Próximos passos

Ideias de evolução do projeto:

- Ingestão incremental automática conforme novos CSVs forem publicados no portal.
- Criação de verificações de qualidade de dados (data quality checks) usando SQL ou Great Expectations.
- Exportar a camada gold para arquivos Parquet, simulando um data lake.
- Conectar diretamente a camada gold em Metabase, Superset ou Power BI.
- Adicionar testes automatizados para scripts de ingestão e para as principais transformações SQL.

---



This project implements a complete data engineering pipeline using public revenue and expense datasets from the city of Curitiba, obtained from the official open data portal (https://dadosabertos.curitiba.pr.gov.br). The pipeline runs on Apache Airflow and PostgreSQL, following a multilayer architecture with staging, silver and gold layers. The gold layer exposes dimension and fact tables that can be directly consumed by BI tools to analyze public revenue and spending over time.
"@ | Set-Content -Encoding UTF8 README.md
