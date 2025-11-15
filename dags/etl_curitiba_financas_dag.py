from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.task_group import TaskGroup


default_args = {
    "owner": "vini",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="etl_curitiba_financas",
    description="Pipeline completo de staging -> silver -> gold (dims + facts) para dados públicos de Curitiba",
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["curitiba", "finance", "pipeline", "etl"],
) as dag:

    # PIPELINE 1 - STAGING
    with TaskGroup("pipeline_staging") as pipeline_staging:
        create_staging_tables = PostgresOperator(
            task_id="create_staging_tables",
            postgres_conn_id="curitiba_postgres",
            sql="sql/create_staging_tables.sql",
        )

    # PIPELINE 2 - SILVER
    with TaskGroup("pipeline_silver") as pipeline_silver:
        build_silver_layer = PostgresOperator(
            task_id="build_silver_layer",
            postgres_conn_id="curitiba_postgres",
            sql="sql/build_silver.sql",
        )

    # PIPELINE 3 - GOLD DIMENSIONS (PARALELO)
    with TaskGroup("pipeline_gold_dimensions") as pipeline_gold_dimensions:
        dim_tempo = PostgresOperator(
            task_id="build_dim_tempo",
            postgres_conn_id="curitiba_postgres",
            sql="sql/dim_tempo.sql",
        )

        dim_orgao = PostgresOperator(
            task_id="build_dim_orgao",
            postgres_conn_id="curitiba_postgres",
            sql="sql/dim_orgao.sql",
        )

        dim_fonte = PostgresOperator(
            task_id="build_dim_fonte",
            postgres_conn_id="curitiba_postgres",
            sql="sql/dim_fonte.sql",
        )

        # aqui dentro elas não dependem uma da outra
        # então dim_tempo, dim_orgao e dim_fonte rodam em paralelo

    # PIPELINE 4 - GOLD FACTS (PARALELO)
    with TaskGroup("pipeline_gold_facts") as pipeline_gold_facts:
        fato_receita = PostgresOperator(
            task_id="build_fato_receita",
            postgres_conn_id="curitiba_postgres",
            sql="sql/fato_receita.sql",
        )

        fato_despesa = PostgresOperator(
            task_id="build_fato_despesa",
            postgres_conn_id="curitiba_postgres",
            sql="sql/fato_despesa.sql",
        )

        # fato_receita e fato_despesa são independentes entre si
        # e vão rodar em paralelo, desde que as dims já estejam prontas

    # ORDEM DOS PIPELINES
    pipeline_staging >> pipeline_silver >> pipeline_gold_dimensions >> pipeline_gold_facts
