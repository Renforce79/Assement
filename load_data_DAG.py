from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime
import os
dag_folder = os.path.dirname(os.path.abspath(__file__))

# Define DAG
dag = DAG(
    'ejecutar_miproyecto',
    start_date=datetime(2023, 4, 12),
    schedule_interval=None
)

# Creating crear_tablas  BashOperator
crear_tablas = BashOperator(
    task_id='crear_tablas',
    bash_command=f'python {dag_folder}/create_tables.py',
    dag=dag
)

# Creating ejecutar_script  BashOperator
ejecutar_script = BashOperator(
    task_id='ejecutar_script',
    bash_command=f'python {dag_folder}/load_data.py',
    dag=dag
)

# Define task order
crear_tablas >> ejecutar_script

