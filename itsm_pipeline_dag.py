from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'data_team',
    'start_date': days_ago(1),
    'retries': 1
}

with DAG(
    dag_id='itsm_data_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    description='Ingest ITSM tickets, transform with DBT, and validate run'
) as dag:

    ingest_csv = PostgresOperator(
        task_id='ingest_csv_to_postgres',
        postgres_conn_id='postgres_default',
        sql="""
            COPY tickets
            FROM '/path/to/cleaned_ticket_data.csv'
            DELIMITER ','
            CSV HEADER;
        """
    )

    run_dbt_transform = BashOperator(
        task_id='run_dbt_models',
        bash_command='cd /path/to/my_itsm_dbt_project && dbt run'
    )

    validate_dbt_run = BashOperator(
        task_id='validate_dbt',
        bash_command='cd /path/to/my_itsm_dbt_project && dbt test'
    )

    ingest_csv >> run_dbt_transform >> validate_dbt_run
