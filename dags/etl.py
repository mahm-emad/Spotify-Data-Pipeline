from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {

    'owner' : 'mahm.emad',
    'retries' : 1,
    'retry_delay' : timedelta(minutes=5)

}


with DAG (
    dag_id='etl_process',
    description='Pyspart ETL for Spotify date',
    default_args=default_args,
    start_date=datetime(2025,6,5,2),
    schedule_interval='@monthly'

) as dag:

    etl_task = BashOperator(
        task_id='etl',
        bash_command='spark-submit --jars /opt/spark/jars/postgresql-42.7.3.jar /opt/airflow/spark/app/pyspark_etl.py',
        dag=dag

    )


    etl_task
