#spark-submit --driver-class-path /root/Downloads/postgresql-42.2.20.jar airflow/dags/a.py

from pyspark.sql import SparkSession

from pyspark import SparkContext
sc = SparkContext("local", "StramTest") 

spark = SparkSession.builder.appName('pescador').master("local[*]").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

import boto3
s3 = boto3.resource('s3', region_name='us-east-1')
bucket = s3.Bucket('exercicio')

d = []

for file in bucket.objects.all(): # Baixa todos os arquivos no momento
	obj = s3.Object(bucket.name, file.key)
	s = obj.get()['Body'].read().decode('utf-8')
	d.append(s)
	obj.delete()

df = spark.read.json(sc.parallelize(d)) # Cria um dataframe com os itens baixados

df.printSchema()
print(df.count())
df.show()

df.write.option('driver', 'org.postgresql.Driver').jdbc(url="jdbc:postgresql://exercicio.crb23nbjpep1.us-east-1.rds.amazonaws.com/transacoes_analitico", 
			  table="public.transacoes", 
			  mode="overwrite", 
			  properties={"user": "postgres", "password": "wy8JcHQh4rypF4A"}
			  )
