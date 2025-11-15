ARG AIRFLOW_VERSION=2.8.1
ARG PYTHON_VERSION=3.8
ARG CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

FROM apache/airflow:${AIRFLOW_VERSION}

USER root

RUN pip install --no-cache-dir \
    --constraint "${CONSTRAINT_URL}" \
    pandas \
    sqlalchemy \
    psycopg2-binary

USER airflow
