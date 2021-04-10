from datetime import timedelta

from airflow import DAG, utils
from airflow.operators.bash_operator import BashOperator


start_date = utils.dates.days_ago(1)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': start_date,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('test_bash_single',
          default_args=default_args,
          schedule_interval='40 14 * * *',
          catchup=False)

t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag)
