📊 Curitiba Public Finance ETL – Data Engineering Pipeline with Airflow

This project implements a complete ETL pipeline using public Revenue and Expense datasets from the city of Curitiba (Brazil).
The entire workflow is orchestrated by Apache Airflow, uses PostgreSQL as a Data Warehouse, and follows a modern multi-layer architecture (Staging → Silver → Gold) aligned with Data Engineering standards.

🚀 Project Purpose

Build a modular, scalable and production-style data pipeline that:

Ingests monthly CSV datasets published by the city

Creates raw staging tables

Cleans and transforms data into the silver layer

Builds analytical dimensional models (star schema)

Generates fact tables for financial analysis

Automates everything using Apache Airflow

This pipeline enables deep insights into public spending and revenue behavior.

🏗️ Architecture Overview
📁 CSV Data → 🐍 Python Ingestion → 🗄️ Postgres (Staging)
       ↓
   🛠️ SQL Transformations (Silver)
       ↓
 🌟 Gold Layer (Dimensions + Facts)
       ↓
📊 Analytics (Metabase / PowerBI / Superset)

🔄 Airflow Pipeline Flow
pipeline_staging
   └── create_staging_tables
        ↓
pipeline_silver
   └── build_silver_layer
        ↓
pipeline_gold_dimensions  (runs in parallel)
   ├── build_dim_tempo
   ├── build_dim_orgao
   └── build_dim_fonte
        ↓
pipeline_gold_facts  (runs in parallel)
   ├── build_fato_receita
   └── build_fato_despesa


Airflow uses TaskGroup to visually separate logical steps.

📸 Example Airflow UI

(Replace with your own screenshots)

Staging → Silver → Gold Dimensions (parallel) → Gold Facts (parallel)

📂 Project Structure
curitiba-financas-airflow-etl/
│
├── dags/
│   ├── etl_curitiba_financas_dag.py     # Airflow DAG with pipelines
│   └── sql/                             # SQL scripts used by the pipeline
│       ├── create_staging_tables.sql
│       ├── build_silver.sql
│       ├── dim_tempo.sql
│       ├── dim_orgao.sql
│       ├── dim_fonte.sql
│       ├── fato_receita.sql
│       └── fato_despesa.sql
│
├── src/etl/
│   ├── ingest_receitas.py               # optional ingestion scripts
│   ├── ingest_despesas.py
│
├── airflow/                             # Docker-based Airflow environment
│   ├── docker-compose.yaml
│   └── Dockerfile (if used)
│
├── sql/                                  # SQL originals (local dev)
│
└── README.md

🛠️ Technologies Used
Technology	Purpose
Apache Airflow 2.8+	Pipeline orchestration
PostgreSQL 13	Data warehouse (staging, silver, gold layers)
Docker Compose	Environment containerization
Python 3.10+	CSV ingestion and transformations
Pandas	Raw data handling
SQL (PostgreSQL)	Silver and gold layer modeling
TaskGroup	Organized pipeline grouping in Airflow
⚙️ How to Run the Project
1. Clone the Repository
git clone https://github.com/YOUR-USER/curitiba-financas-airflow-etl.git
cd curitiba-financas-airflow-etl

2. Start the Airflow Environment

Inside the Airflow folder:

cd airflow
docker compose up -d


Access the Airflow UI:

http://localhost:8080


Default login:

User: admin

Password: admin

3. Set Up the Airflow Connection

Navigate to:
Admin → Connections → Add Connection

Field	Value
Conn Id	curitiba_postgres
Conn Type	Postgres
Host	postgres
Schema	curitiba_financas
Login	airflow
Password	airflow
Port	5432

Click Test — it must show Success.

4. Make SQL scripts available to Airflow
copy .\sql\*.sql .\dags\sql\


Verify inside the container:

docker exec -it airflow-webserver-1 ls /opt/airflow/dags/sql

5. Run the Pipeline

In the Airflow UI:

Enable the DAG etl_curitiba_financas

Click Trigger DAG

Watch the Staging → Silver → Gold pipeline run

📚 Data Warehouse Modeling
🟪 Silver Layer

Standardized fields and derived attributes:

Year/Month fields

Cleaned and normalized values

Proper typing (numeric/date)

⭐ Gold Dimensions

dim_tempo — calendar dimension

dim_orgao — government organizations

dim_fonte — funding source (merged from expenses + revenues)

💠 Gold Facts
Fact Tables

fato_receita

Aggregated revenue by date, source, company, and type

fato_despesa

Summarized expenses by date, orgão, program, action, and function

📊 Possible Analytics

This DW enables analyses like:

Monthly revenue trends

Expense behavior by government organization

Budget vs actual spending

Analysis by program, action, or function

Comparison between funding sources

Revenue vs payments over time

🔮 Future Improvements (Roadmap)

 Add file sensors for automated ingestion

 Build ingestion directly from Curitiba Transparency Portal

 Add Data Quality checks (SQL or Great Expectations)

 Publish Gold layer in Parquet (Lakehouse)

 Add dashboards (Superset / Metabase / PowerBI)

 Make pipeline incremental by month

📝 License

MIT License - free for academic, personal, and professional use.
