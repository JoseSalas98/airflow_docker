# Importamos las librerías requeridas
from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator

with DAG(
            "tutorial_dags", 
            description = "Este es un tutorial de dags",
            schedule_interval = timedelta(days = 1),
            start_date = datetime(2022, 8, 17)
        ) as dag:
        tarea01 = DummyOperator(task_id='tarea01', dag=dag)
        tarea02 = DummyOperator(task_id='tarea02', dag=dag)
        tarea03 = DummyOperator(task_id='tarea03', dag=dag)

        tarea01 >> [tarea02, tarea03]
