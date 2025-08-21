import sys
sys.path.append('/opt/airflow')
from scripts.fetch_stock_data import fetch_and_store
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'retries': 2,
    'retry_delay': timedelta(minutes=3),
}

def fetch_and_store_stock_data(**kwargs):
    from scripts.fetch_stock_data import fetch_and_store
    fetch_and_store()

with DAG(
    dag_id='stock_data_pipeline',
    default_args=default_args,
    start_date=datetime(2023, 1, 1),
    schedule_interval='@hourly',  # or '@daily'
    catchup=False,
    description='Fetch and store stock data in Postgres',
) as dag:

    task_fetch_and_store = PythonOperator(
        task_id='fetch_and_store_stock_data',
        python_callable=fetch_and_store_stock_data,
        provide_context=True
    )
