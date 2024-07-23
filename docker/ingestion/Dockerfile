FROM docker.getcollate.io/openmetadata/ingestion:1.5.0-SNAPSHOT
USER airflow
COPY --chown=airflow:0 src /home/airflow/app/src
COPY --chown=airflow:0 pyproject.toml /home/airflow/app
WORKDIR /home/airflow/app
RUN pip install .
