🚀 Curitiba Public Finance ETL
Modern Data Engineering Pipeline with Airflow, Postgres and SQL

This project is a complete ETL pipeline designed to process public revenue and expense data from the city of Curitiba. It demonstrates production-level orchestration, SQL transformations, modeling and containerized infrastructure using Airflow and Docker. The architecture follows the classic Staging, Silver and Gold multi-layer data approach.

🌟 Key Highlights

End to end ETL pipeline with Airflow

TaskGroup based pipeline orchestration

Multi layered Data Warehouse: Staging, Silver and Gold

Star Schema modeling with facts and dimensions

SQL driven transformations with clean modular files

Fully containerized environment with Docker Compose

Public real world datasets from government sources

Ideal for interviews and portfolio demonstrations

🏗️ Architecture
CSV Data → Python Ingestion → Postgres (Staging)
                 ↓
           SQL Transformations (Silver)
                 ↓
         Dimensional Modeling (Gold)
                 ↓
     Analytics Tools (Power BI, Metabase)

🧠 What This Project Demonstrates
Airflow Orchestration

Scheduling, retries, task dependencies, jinja templated SQL, Python tasks and modular pipelines.

Data Modeling

Creation of dimensions and facts, including dim_tempo, dim_orgao, dim_fonte, fato_receita and fato_despesa.

SQL Engineering

Clear DDL and DML scripts for each transformation step.

Data Pipeline Design

Separation of layers, idempotency, reproducibility and modular engineering.

🔄 Airflow Pipeline Overview
TaskGroup: staging
    create_staging_tables

TaskGroup: silver
    build_silver_layer

TaskGroup: gold_dimensions
    dim_tempo
    dim_orgao
    dim_fonte

TaskGroup: gold_facts
    fato_receita
    fato_despesa

🛠️ Tech Stack
Technology	Purpose
Apache Airflow	Orchestration
PostgreSQL	Data Warehouse
Docker Compose	Infrastructure
Python	Ingestion and operators
SQL (Postgres)	Transformations
📦 Repository Structure
curitiba-financas-etl/
│
├── dags/
│   ├── etl_curitiba_financas_dag.py
│   └── sql/
│       ├── create_staging_tables.sql
│       ├── build_silver.sql
│       ├── dim_tempo.sql
│       ├── dim_orgao.sql
│       ├── dim_fonte.sql
│       ├── fato_receita.sql
│       └── fato_despesa.sql
│
├── airflow/
│   ├── docker-compose.yaml
│   └── Dockerfile
│
└── README.md

📊 Analytical Possibilities

Revenue trend monitoring

Expense behavior by organization

Budget and actual comparisons

Funding source analysis

Month to month time series behavior

🎯 Why This Project Stands Out

Uses a real public dataset with business meaning

Replicates professional warehouse architecture

Shows mastery of Airflow, SQL and containerization

Ready to run, reproduce and showcase in interviews

Clean and modular code following best practices
