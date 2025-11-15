🚀 Curitiba Public Finance ETL

Modern Data Engineering Pipeline with Airflow, Postgres and SQL

Este projeto é um pipeline ETL (Extract, Transform, Load) completo e profissional, projetado para processar dados públicos de Receita e Despesa da cidade de Curitiba. Ele demonstra orquestração de nível de produção com Apache Airflow e um Data Warehouse multi-camadas utilizando PostgreSQL e Docker.

A arquitetura segue o modelo clássico de camadas: Staging, Silver e Gold.

🌟 Key Highlights

Categoria

Detalhe

Benefício para Portfólio

Orquestração

Pipeline ETL End-to-End com Airflow e TaskGroups.

Demonstra domínio em agendamento e modularidade.

Modelagem

Data Warehouse Multi-camadas (Staging/Silver/Gold) e Star Schema.

Prova conhecimento em arquitetura e design de dados.

Infraestrutura

Ambiente totalmente containerizado com Docker Compose.

Mostra proficiência em ferramentas DevOps e reprodutibilidade.

Transformação

SQL-Driven Transformations (DDL/DML) com scripts modulares.

Evidencia habilidades sólidas em SQL e Engenharia de Dados.

Dados

Utilização de datasets públicos e reais de fontes governamentais.

Agrega valor de negócio e relevância prática.

🏗️ Arquitetura do Data Pipeline

O fluxo de dados é rigorosamente dividido em camadas para garantir a qualidade, rastreabilidade e desempenho analítico.

graph LR
    A[CSV Data] --> B(Python Ingestion);
    B --> C(Postgres :: Staging);
    C --> D(SQL Transformations :: Silver);
    D --> E(Dimensional Modeling :: Gold);
    E --> F(Analytics Tools: Power BI, Metabase);


🧠 O que Este Projeto Demonstra

Airflow Orchestration: Uso de TaskGroup para organização, dependências claras e reutilização de código Python/SQL.

Data Modeling: Criação das dimensões (dim_tempo, dim_orgao, dim_fonte) e fatos (fato_receita, fato_despesa).

Pipeline Design: Princípios de idempotência e reprodutibilidade aplicados em todas as camadas.

🔄 Airflow Pipeline Overview

O DAG (etl_curitiba_financas_dag.py) é estruturado da seguinte forma:

TaskGroup

Responsabilidade

Tarefas SQL Chave

staging

Ingestão inicial dos dados brutos.

create_staging_tables

silver

Transformações de limpeza e padronização.

build_silver_layer

gold_dimensions

Construção das tabelas Dimensionais.

dim_tempo, dim_orgao, dim_fonte

gold_facts

Construção das tabelas de Fato (Star Schema).

fato_receita, fato_despesa

🛠️ Tech Stack

Tecnologia

Versão

Propósito

Apache Airflow

Latest (Docker)

Orquestração do Pipeline

PostgreSQL

Latest (Docker)

Data Warehouse e Repositório de Metadados

Docker Compose

Latest

Definição e Gerenciamento da Infraestrutura

Python

3.x

Ingestão (ETL) e Operadores Airflow

SQL (Postgres)

-

Transformações (DML e DDL)

📦 Repository Structure

curitiba-financas-etl/
│
├── dags/
│   ├── etl_curitiba_financas_dag.py    # Definição do DAG principal
│   └── sql/                           # Scripts SQL modularizados por camada
│       ├── create_staging_tables.sql
│       ├── build_silver.sql
│       ├── dim_tempo.sql
│       ├── dim_orgao.sql
│       ├── dim_fonte.sql
│       ├── fato_receita.sql
│       └── fato_despesa.sql
│
├── airflow/                           # Configuração do ambiente Docker
│   ├── docker-compose.yaml            # Definição dos serviços
│   └── Dockerfile                     # Imagem customizada do Airflow (se aplicável)
│
└── README.md


⚙️ Como Rodar o Projeto (Setup)

Pré-requisitos: Certifique-se de ter o Docker e o Docker Compose instalados.

Clone o Repositório:

git clone [https://github.com/seu-usuario/curitiba-financas-etl.git](https://github.com/seu-usuario/curitiba-financas-etl.git)
cd curitiba-financas-etl


Inicie a Infraestrutura:
Execute o Docker Compose para subir os serviços do Airflow e PostgreSQL:

docker-compose -f airflow/docker-compose.yaml up -d --build


Acesse o Airflow:

URL: http://localhost:8080

Login: Use as credenciais definidas no docker-compose.yaml (geralmente airflow/airflow).

Execute o DAG:

Localize o DAG etl_curitiba_financas_dag na interface.

Ative-o e dispare uma execução manual para iniciar o pipeline ETL completo.
