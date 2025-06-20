from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'loveday',
    'depends_on_past': False,
    'start_date': datetime(2025, 6, 12),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'scrapy_auto_news_dag',
    default_args=default_args,
    description='Run Scrapy auto_news spider every 30 mins',
    schedule_interval='*/30 * * * *',  # Every 30 minutes
    catchup=False
)

run_scrapy = BashOperator(
    task_id='run_auto_news_spider',
    bash_command='cd C:/Users/DELL/Documents/GitHub/Project Test Auto Intel/auto_intel_project && airflow_env/Scripts/activate && scrapy crawl auto_news',
    dag=dag
)
