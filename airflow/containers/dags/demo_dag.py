#!/usr/bin/python3
# -*- coding: utf-8 -*-
from airflow import DAG
from airflow.models import Variable
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator 
from airflow.operators.dummy_operator import DummyOperator

# adding on_failure_callback and on_success_callback, when email are way too much, slack is better

default_args = {
    "owner": "Leyner_Bejarano",
    "email": "personaltraingcp@gmail.com",
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=10)

}

with DAG(
    dag_id="demo_dag",
    start_date=datetime(2018, 6, 1),
    schedule_interval="@hourly",
    max_active_runs=2,
    default_args=default_args,
    catchup=False,
    tags=["demo","POC"]
) as dag:
    ENV = Variable.get("ENV")
    QUEUE_URL = Variable.get("QueueUrl")
    AWS_ACCESS_KEY = Variable.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_KEY = Variable.get("AWS_SECRET_ACCESS_KEY")
    DH = "{{ '{:02}'.format(execution_date.hour)}}"
    DT = "{{ '{}-{:02}-{:02}'.format(execution_date.year, execution_date.month, execution_date.day)}}"
    start = DummyOperator(task_id="start")
    executor_task =  BashOperator(
        task_id = "executor_task",
        bash_command = f""" 
        cd /opt/airflow/dags/scripts &&
        pip install -r requirements.txt &&
        python lambdaExecutor.py -dt {DT} -dh {DH} -q {QUEUE_URL} -ak {AWS_ACCESS_KEY} -sk {AWS_SECRET_KEY} &&
        pip freeze
        """
    )
    end = DummyOperator(task_id="end")

    start >> executor_task >> end       
