# Curitiba Public Finance ETL

Pipeline completo de engenharia de dados utilizando **Apache Airflow**, **PostgreSQL**, **Python** e **Docker** para processar dados públicos de **receitas** e **despesas** da Prefeitura de Curitiba.

O objetivo deste projeto é montar um fluxo de **ingestão, transformação e modelagem dimensional** em camadas (Staging, Silver e Gold), pronto para servir como base de análise em ferramentas de BI.

---

## Índice

- [Visão geral](#visão-geral)
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

Este projeto implementa:

- Ingestão de arquivos CSV de receitas e despesas da Prefeitura de Curitiba.
- Armazenamento em tabelas de **staging** no PostgreSQL.
- Transformações SQL para a camada **silver** com dados limpos e derivados.
- Construção de dimensões e fatos na camada **gold**, seguindo um modelo próximo de star schema.
- Orquestração de todo o fluxo com **Apache Airflow** usando **TaskGroups** para separar os pipelines.

É um projeto pensado para portfólio de engenharia de dados, simulando um ambiente próximo de produção.

---

## Arquitetura

```text
Arquivos CSV
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
Infraestrutura orquestrada via Docker Compose, com containers para:

Airflow Webserver

Airflow Scheduler

PostgreSQL

Tecnologias
Tecnologia	Uso principal
Apache Airflow	Orquestração de pipelines
PostgreSQL	Data Warehouse local
Docker Compose	Infraestrutura containerizada
Python	Ingestão e conexão com o banco
Pandas	Leitura e pré-processamento de CSV
SQL (Postgres)	Transformações e modelagem
Camadas de dados
Staging

Tabelas com dados mais próximos do CSV, porém tipados:

stg_receitas

stg_despesas

Silver

Tabelas com dados limpos, com colunas derivadas como ano e mês:

silver_receitas

silver_despesas

Gold

Dimensões:

dim_tempo

dim_orgao

dim_fonte

Fatos:

fato_receita

fato_despesa

Pipeline no Airflow

A DAG principal se chama etl_curitiba_financas e está organizada em TaskGroups:
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
Estrutura do repositório
curitiba-financas-airflow-etl/
│
├── dags/
│   ├── etl_curitiba_financas_dag.py   # DAG do Airflow
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
│       ├── ingest_receitas.py         # ingestão de receitas
│       └── ingest_despesas.py         # ingestão de despesas
│
├── airflow/
│   ├── docker-compose.yaml            # stack do Airflow + Postgres
│   └── Dockerfile                     # customizações de imagem (se houver)
│
└── README.md

Como executar
1. Clonar o repositório
git clone https://github.com/SEU-USUARIO/curitiba-financas-airflow-etl.git
cd curitiba-financas-airflow-etl

2. Subir o ambiente do Airflow
cd airflow
docker compose up -d


Acesse o Airflow em:

http://localhost:8081


Usuário e senha padrão (caso não tenha alterado):

usuário: admin

senha: admin

3. Configurar a conexão Postgres no Airflow

No menu do Airflow:

Admin → Connections → +

Preencha:

Conn Id: curitiba_postgres

Conn Type: Postgres

Host: postgres

Schema: curitiba_financas

Login: airflow

Password: airflow

Port: 5432

Clique em Test e salve.

4. Garantir que os SQLs estão acessíveis

Na máquina host:

cd C:\Users\vinic\curitiba-financas-airflow-etl
copy .\sql\*.sql .\dags\sql\


Dentro do container:

docker exec -it airflow-webserver-1 ls /opt/airflow/dags/sql


Os arquivos .sql devem aparecer listados.

5. Rodar a DAG

No Airflow:

Ative a DAG etl_curitiba_financas.

Clique em Trigger DAG.

Acompanhe a execução na aba Graph ou Grid.

Possíveis análises

Com a camada gold criada, é possível responder perguntas como:

Qual foi a evolução mensal da receita do município por exercício.

Quanto cada órgão gastou por mês, função, programa ou ação.

Comparação de valores empenhados, liquidados e pagos.

Distribuição de despesas por fonte de recurso.

Séries temporais de receitas e despesas ao longo dos anos.

Próximos passos

Ideias para evolução do projeto:

Ingestão incremental automática conforme novos CSVs são publicados.

Adição de data quality checks usando SQL ou Great Expectations.

Exportar a camada gold em Parquet para um data lake.

Conectar a camada gold em Metabase, Superset ou Power BI.

Adicionar testes automatizados para scripts de ingestão e SQL.
