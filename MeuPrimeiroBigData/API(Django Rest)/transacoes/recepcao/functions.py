from pyspark import SparkContext
from pyspark.sql import SparkSession
import boto3
import datetime
import json


class dl():
    dados = []
    s3 = boto3.resource('s3', region_name='us-east-1')

    def store(self, data):
        if (isinstance(data, dict)):
            self.dados.append(data)

            if (len(self.dados) >= 100):
                object = self.s3.Object('exercicio', 'transacoes/' + str(datetime.datetime.utcnow().isoformat()) + ".json")
                object.put(
                    Body=bytes(
                        json.dumps(self.dados).encode('UTF-8')
                    )
                )
                self.dados = []
                print ("json salvo no s3")

            return True
        return False



#s3 = boto3.resource('s3')

#bucket = s3.Bucket('exercicio')

#for file in bucket.objects.all():
#    obj = s3.Object(bucket, file.key)
#    a = json.loads(obj.get()['Body'].read().decode('utf-8'))