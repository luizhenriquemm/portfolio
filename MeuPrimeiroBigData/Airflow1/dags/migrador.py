from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.providers.apache.hive.operators.hive import HiveOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator

hql = """
USE TRANSACOES;
load data inpath '/migracao/arq/*.csv' into table transacoes;
"""

default_args = {
	'owner': 'airflow',
	'depends_on_past': False,
	'start_date': datetime(2021, 4, 20),
	'email': ['airflow@example.com'],
	'email_on_failure': False,
	'email_on_retry': False,
	# Em caso de erros, tente rodar novamente apenas 1 vez
	'retries': 1,
	# Tente novamente após 30 segundos depois do erro
	'retry_delay': timedelta(minutes=5),
	'schedule_interval': '0 3 * * *'
}

with DAG(
	dag_id='migrador',
	default_args=default_args,
	schedule_interval=timedelta(days=1),
	tags=['exercicio'],
) as dag:

	recebe_dados = SparkSubmitOperator(
		task_id='recebe_dados',
		application="/root/script.py",
		conn_id="spark_default"
	)

	