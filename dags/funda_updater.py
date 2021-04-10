from airflow import DAG, utils
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from datetime import *
import logging

# default arguments
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

dag = DAG('funda_updater',
          default_args=default_args,
          schedule_interval='05 * * * *',
          catchup=False)


def get_data_from_bq(**kwargs):
    hook = BigQueryHook(bigquery_conn_id='google_cloud_default',
                        delegate_to=None,
                        use_legacy_sql=False)
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT link FROM '
                   '`portfolio-projects-310210.funda.funda_den_haag` '
                   'WHERE update_date >= DATE_SUB(CURRENT_DATE(), '
                   'INTERVAL 3 DAY)')
    result = cursor.fetchall()
    print('result', result)
    return result


fetch_data = PythonOperator(
    task_id='fetch_data_public_dataset',
    provide_context=True,
    python_callable=get_data_from_bq,
    dag=dag
)

fetch_data