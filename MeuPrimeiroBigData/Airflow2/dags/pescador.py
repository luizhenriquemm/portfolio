from datetime import datetime, timedelta  
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator

default_args = {
	'owner': 'airflow',
	'depends_on_past': False,
	# Exemplo: Inicia em 20 de Janeiro de 2021
	'start_date': datetime(2021, 1, 20),
	'email': ['airflow@example.com'],
	'email_on_failure': False,
	'email_on_retry': False,
	# Em caso de erros, tente rodar novamente apenas 1 vez
	'retries': 1,
	# Tente novamente após 30 segundos depois do erro
	#'retry_delay': timedelta(seconds=30),
	# Execute uma vez a cada 15 minutos 
	'schedule_interval': '*/15 * * * *'
}

with DAG(	
	dag_id='pescador',
	default_args=default_args,
	schedule_interval=None,
	tags=['pescador'],
) as dag:	

	a = SparkSubmitOperator(
		task_id='executor',
		application="/root/script.py",
		conn_id="spark_default",
		driver_class_path="/root/Downloads/postgresql-42.2.20.jar",
	)