# Curitiba Public Finance ETL

## Modern Data Engineering Pipeline with Airflow, Postgres and SQL

Este projeto é um pipeline ETL (Extract, Transform, Load) completo e profissional, projetado para processar dados públicos de Receita e Despesa da cidade de Curitiba. Ele demonstra orquestração de nível de produção com **Apache Airflow** e um Data Warehouse multi-camadas utilizando **PostgreSQL** e **Docker**.

A arquitetura segue o modelo clássico de camadas: **Staging, Silver e Gold**.

## Destaques

| Categoria | Detalhe | Benefício para Portfólio | 
 | ----- | ----- | ----- | 
| **Orquestração** | Pipeline ETL End-to-End com Airflow e TaskGroups. | Demonstra domínio em agendamento e modularidade. | 
| **Modelagem** | Data Warehouse Multi-camadas (Staging/Silver/Gold) e Star Schema. | Prova conhecimento em arquitetura e design de dados. | 
| **Infraestrutura** | Ambiente totalmente containerizado com Docker Compose. | Mostra proficiência em ferramentas DevOps e reprodutibilidade. | 
| **Transformação** | SQL-Driven Transformations (DDL/DML) com scripts modulares. | Evidencia habilidades sólidas em SQL e Engenharia de Dados. | 
| **Dados** | Utilização de datasets públicos e reais de fontes governamentais. | Agrega valor de negócio e relevância prática. | 

## Arquitetura do Data Pipeline

O fluxo de dados é rigorosamente dividido em camadas para garantir a qualidade, rastreabilidade e desempenho analítico:

`CSV Data` → `Python Ingestion` → `Postgres (Staging)` → `SQL Transformations (Silver)` → `Dimensional Modeling (Gold)` → `Analytics Tools`

### O que Este Projeto Demonstra

* **Airflow Orchestration:** Uso de `TaskGroup` para organização, dependências claras e reutilização de código Python/SQL.

* **Data Modeling:** Criação das dimensões (`dim_tempo`, `dim_orgao`, `dim_fonte`) e fatos (`fato_receita`, `fato_despesa`).

* **Pipeline Design:** Princípios de idempotência e reprodutibilidade aplicados em todas as camadas.

## Airflow Pipeline Overview

O DAG (`etl_curitiba_financas_dag.py`) é estruturado da seguinte forma:

| TaskGroup | Responsabilidade | Tarefas SQL Chave | 
 | ----- | ----- | ----- | 
| `staging` | Ingestão inicial dos dados brutos. | `create_staging_tables` | 
| `silver` | Transformações de limpeza e padronização. | `build_silver_layer` | 
| `gold_dimensions` | Construção das tabelas Dimensionais. | `dim_tempo`, `dim_orgao`, `dim_fonte` | 
| `gold_facts` | Construção das tabelas de Fato (Star Schema). | `fato_receita`, `fato_despesa` | 

## Tech Stack

| Tecnologia | Versão | Propósito | 
 | ----- | ----- | ----- | 
| **Apache Airflow** | Latest (Docker) | Orquestração do Pipeline | 
| **PostgreSQL** | Latest (Docker) | Data Warehouse e Repositório de Metadados | 
| **Docker Compose** | Latest | Definição e Gerenciamento da Infraestrutura | 
| **Python** | 3.x | Ingestão (ETL) e Operadores Airflow | 
| **SQL (Postgres)** | \- | Transformações (DML e DDL) | 

## Repository Structure
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
