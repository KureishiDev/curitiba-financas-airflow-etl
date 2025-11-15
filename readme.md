# 🚀 Curitiba Public Finance ETL

## Modern Data Engineering Pipeline with Airflow, Postgres and SQL

Este projeto é um *pipeline* ETL (Extract, Transform, Load) completo, projetado para processar dados públicos de **Receita e Despesa** da prefeitura de **Curitiba**. Ele demonstra orquestração de nível de produção, transformações em SQL, modelagem de dados e infraestrutura containerizada utilizando **Apache Airflow** e **Docker**.

A arquitetura segue a abordagem clássica de múltiplas camadas de dados: **Staging, Silver e Gold**.

---

## 🌟 Destaques do Projeto

* **Pipeline ETL Ponta a Ponta** orquestrado com **Airflow**.
* Orquestração do *pipeline* baseada em **TaskGroup** para modularidade.
* **Data Warehouse Multi-camadas:** Staging, Silver e Gold.
* Modelagem **Star Schema** com tabelas de fatos e dimensões.
* Transformações guiadas por **SQL** com arquivos modulares e limpos.
* Ambiente totalmente **containerizado** com **Docker Compose**.
* Utiliza *datasets* públicos e reais de fontes governamentais.
* **Ideal para entrevistas e demonstrações de portfólio.**

---

## 🏗️ Arquitetura do Data Pipeline

O fluxo de dados segue a progressão através das camadas do Data Warehouse:

```mermaid
graph LR
    A[CSV Data] --> B(Python Ingestion);
    B --> C(Postgres :: Staging);
    C --> D(SQL Transformations :: Silver);
    D --> E(Dimensional Modeling :: Gold);
    E --> F(Analytics Tools: Power BI, Metabase);
O que o projeto demonstra:ConceitoDescriçãoOrquestração AirflowAgendamento, retentativas, dependências de tarefas, SQL com Jinja, tarefas Python e pipelines modulares.Modelagem de DadosCriação de dimensões e fatos: dim_tempo, dim_orgao, dim_fonte, fato_receita e fato_despesa.SQL EngineeringScripts DDL (Data Definition Language) e DML (Data Manipulation Language) claros para cada etapa de transformação.Design de PipelineSeparação de camadas, idempotência, reprodutibilidade e engenharia modular.🔄 Visão Geral do Pipeline no AirflowO Directed Acyclic Graph (DAG) é estruturado em TaskGroups para representar as camadas do Data Warehouse:TaskGroupTarefas (Tarefas SQL)Objetivostagingcreate_staging_tablesIngestão inicial dos dados brutos para o PostgreSQL.silverbuild_silver_layerTransformações básicas e limpeza dos dados.gold_dimensionsdim_tempo, dim_orgao, dim_fonteConstrução das tabelas de Dimensão.gold_factsfato_receita, fato_despesaConstrução das tabelas de Fato (Star Schema).🛠️ Tech StackTecnologiaFinalidadeApache AirflowOrquestração e Agendamento do Pipeline.PostgreSQLData Warehouse (Staging, Silver, Gold).Docker ComposeGerenciamento e Configuração da Infraestrutura.PythonIngestão de dados CSV e Operadores Airflow.SQL (Postgres)Lógica de Transformação (T e L no ETL).📦 Estrutura do Repositóriocuritiba-financas-etl/
│
├── dags/
│   ├── etl_curitiba_financas_dag.py    # Definição do DAG principal do Airflow
│   └── sql/                           # Scripts SQL para transformações
│       ├── create_staging_tables.sql
│       ├── build_silver.sql
│       ├── dim_tempo.sql
│       ├── dim_orgao.sql
│       ├── dim_fonte.sql
│       ├── fato_receita.sql
│       └── fato_despesa.sql
│
├── airflow/                           # Arquivos para a construção do ambiente Airflow/Postgres
│   ├── docker-compose.yaml            # Definição dos serviços (Airflow, Postgres)
│   └── Dockerfile                     # Imagem customizada do Airflow (se aplicável)
│
└── README.md
📊 Possibilidades AnalíticasO modelo dimensional final (Camada Gold) permite análises robustas como:Monitoramento da tendência de Receita.Análise do comportamento de Despesas por Órgão.Comparações entre Orçamento planejado e valores executados.Análise das principais Fontes de Financiamento.Comportamento de séries temporais mês a mês.🎯 Por Que Este Projeto se DestacaUtiliza um dataset público e real com significado de negócio.Replica uma arquitetura de Data Warehouse profissional de múltiplas camadas.Demonstra domínio de Airflow, SQL e containerização.Código limpo e modular seguindo as melhores práticas de Engenharia de Dados.Ambiente pronto para rodar, reproduzir e apresentar em entrevistas.⚙️ Como Rodar o ProjetoPré-requisitos: Certifique-se de ter o Docker e o Docker Compose instalados.Clone o Repositório:Bashgit clone [https://github.com/seu-usuario/curitiba-financas-etl.git](https://github.com/seu-usuario/curitiba-financas-etl.git)
cd curitiba-financas-etl
Suba a Infraestrutura (via Docker Compose):Bashdocker-compose -f airflow/docker-compose.yaml up -d
Isso iniciará os serviços do Airflow e PostgreSQL.Acesse o Airflow:Acesse http://localhost:8080 (porta padrão do Airflow).Faça login (usuário e senha geralmente configurados no docker-compose.yaml, ex: airflow/airflow).Execute o DAG:Localize o DAG etl_curitiba_financas_dag.Ative-o e execute-o manualmente. O pipeline irá ingerir os dados e rodar todas as transformações SQL.Verifique os Dados:Conecte-se ao serviço PostgreSQL para inspecionar as tabelas nas camadas Staging, Silver e Gold.
