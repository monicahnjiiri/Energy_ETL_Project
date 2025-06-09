from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from datetime import datetime
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()
ALERT_EMAIL = os.getenv("ALERT_EMAIL")

# Define Python callables

def run_transform():
    subprocess.run(["python", "Transform.py"], check=True)

def run_load():
    subprocess.run(["python", "Load.py"], check=True)

# DAG Definition
with DAG(
    dag_id="energy_etl_dag",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["etl", "energy"]
) as dag:

    transform_task = PythonOperator(
        task_id="transform_data",
        python_callable=run_transform
    )

    load_task = PythonOperator(
        task_id="load_data",
        python_callable=run_load
    )

    notify_task = EmailOperator(
        task_id="send_success_email",
        to=ALERT_EMAIL,
        subject="ETL Pipeline Successful",
        html_content="<h3>Energy ETL pipeline ran successfully 🎉</h3>"
    )

    transform_task >> load_task >> notify_task