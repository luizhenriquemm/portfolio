from pyspark.sql import SparkSession
from pyspark.sql.functions import col

from pyspark import SparkContext
sc = SparkContext("local", "StramTest") 

spark = SparkSession.builder.appName('pescador').master("local[*]").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

import json
import decimal
import boto3
import datetime

dyndb = boto3.resource('dynamodb', region_name='us-east-1')

transacoes = dyndb.Table("transacoes")
momento = str((datetime.datetime.utcnow() - datetime.timedelta(days=90)).isoformat()) # Momento para o criterio de consulta e exclusão

x = 0
d = []

while True: # Loop para trazer todos os arquivos do datalake
	if (x > 0):
		r = transacoes.scan( # Constroi o scan de pagina
			ScanFilter = {
				"timestamp": {
					"AttributeValueList": [momento],
					"ComparisonOperator": "LE"
				}
			},
			Limit = 100,
			ExclusiveStartKey=r['LastEvaluatedKey'] # Coninua do item seguinte da consulta anterior
		)
	else:
		r = transacoes.scan( # Constroi o scan inicial
			ScanFilter = {
				"timestamp": {
					"AttributeValueList": [momento],
					"ComparisonOperator": "LE"
				}
			},
			Limit = 100 # Blocos de 100 itens
		)

	if (len(r['Items']) > 0):
		item = r['Items']

		# Converte os decimal para float
		for i in range(len(item)):
			for j in item[i]:
				if (isinstance(item[i][j], decimal.Decimal)):
					item[i][j] = float(item[i][j])

		d.append(json.dumps(item))

		# Exclui os itens do banco
#		for i in r['Items']:
#			transacoes.delete_item(
#				TableName = 'transacoes',
#				Key = {'id': str(i['id'])}
#			)

		x = x + 1

	else: # Fim
		break

df = spark.read.json(sc.parallelize(d))

df.printSchema()
print(df.count())
df.show()

df \
	.select( # Ordena as colunas para ser compativel com o schema do hive
		col("id"),
		col("cliente"),
		col("descricao"),
		col("timestamp").alias("ts"), # O hive nao aceita o nome timestamp como nome de campo
		col("tipo"),
		col("valor")
	) \
	.write \
	.save('hdfs:///migracao/arq', format="csv", mode='append')