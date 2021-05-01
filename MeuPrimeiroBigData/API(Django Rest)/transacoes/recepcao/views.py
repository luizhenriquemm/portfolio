from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status

from .models import Clientes
from .serializers import ClientesSerializer 
from .functions import *

import uuid
import datetime
from decimal import Decimal

import boto3
dyndb = boto3.resource('dynamodb', region_name='us-east-1')

dl = dl()

# Create your views here.

class recebe_dados(APIView):
    def post(self, request):
        global buffer_dados
        if ("tipo" in request.data): # Verifica se a chave tipo foi passada, opera com base no tipo
            print (request.data['tipo'])
            if (request.data['tipo'] == "deposito"): # Tipo depósito
                saldo = dyndb.Table("saldo")
                r = saldo.get_item(Key={"cliente": request.data['cliente']}) # Tenta localizar o saldo do cliente

                if ("Item" in r): # O cliente ja possui algum saldo, será somado o valor do deposito
                    item = r['Item']
                    item['saldo'] = str(float(item['saldo']) + float(request.data['valor']))
                    r = saldo.put_item(Item=item)

                else: # Não está, o saldo é iniciado com o valor do depósito
                    r = saldo.put_item(
                        Item={
                                'cliente': request.data['cliente'],
                                'saldo': str(request.data['valor'])
                            }
                        )

                transacoes = dyndb.Table("transacoes")
                r = transacoes.put_item( # Registra a transacao
                    Item={
                        'id': str(uuid.uuid1()),
                        'tipo': request.data['tipo'],
                        'cliente': int(request.data['cliente']),
                        'valor': Decimal(str(request.data['valor'])),
                        'descricao': "Depósito de valor em conta",
                        'timestamp': datetime.datetime.utcnow().isoformat() # Todas as datas em UTC salvas em ISO_8601 !!!
                    }
                )

                # Construção do objeto a ser enviado para o data lake:
                d = {}
                c = get_object_or_404(Clientes.objects.using('clientes'), id=request.data['cliente'])
                d['transacao_tipo'] = request.data['tipo']
                d['cliente_sexo'] = c.sexo
                d['cliente_estado'] = c.estado
                d['cliente_cidade'] = c.cidade
                d['cliente_data_nascimento'] = str(c.data_nascimento)
                d['cliente_estado_civil'] = c.estado_civil
                d['cliente_escolaridade'] = c.escolaridade
                d['transacao_valor'] = request.data['valor']
                d['transacao_timestamp'] = str(datetime.datetime.utcnow().isoformat())
                dl.store(d)

                return Response({"status": "sucesso"}) # Retorna sucesso

            elif (request.data['tipo'] == "transferencia"): # Tipo transferencia
                saldo = dyndb.Table("saldo")
                r = saldo.get_item(Key={"cliente": request.data['cliente-origem']}) # Tenta localizar o saldo do cliente de origem do valor

                if ("Item" in r): # Existe algum saldo para o cliente de origem
                    item = r['Item']
                    if (float(item['saldo']) >= float(request.data['valor'])): # O cliente de origem possui saldo maior que o valor do saque?
                        item['saldo'] = str(float(item['saldo']) - float(request.data['valor'])) # Subtrai o valor a ser transferido
                        r = saldo.put_item(Item=item) # Salva o novo saldo

                        # Aqui é o meio tempo da transferência, o valor está "no ar"

                        r = saldo.get_item(Key={"cliente": request.data['cliente']}) # Tenta localizar o saldo do cliente de destino
                        if ("Item" in r): # Existe algum saldo
                            item = r['Item']
                            item['saldo'] = str(float(item['saldo']) + float(request.data['valor']))
                            r = saldo.put_item(Item=item)

                        else: # O cliente não existe na tabela de saldos
                            r = saldo.put_item(
                                Item={
                                        'cliente': request.data['cliente'],
                                        'saldo': str(request.data['valor'])
                                    }
                                )

                        transacoes = dyndb.Table("transacoes")
                        r = transacoes.put_item( # Registra a transação para o cliente de origem
                            Item={
                                'id': str(uuid.uuid1()),
                                'tipo': request.data['tipo'],
                                'cliente': int(request.data['cliente-origem']),
                                'valor': Decimal(str(request.data['valor'])),
                                'descricao': "Transferência para o cliente #" + str(request.data['cliente']),
                                'timestamp': datetime.datetime.utcnow().isoformat() # Todas as datas em UTC salvas em ISO_8601 !!!
                            }
                        )
                        r = transacoes.put_item( # Registra a transação para o cliente de destino
                            Item={
                                'id': str(uuid.uuid1()),
                                'tipo': request.data['tipo'],
                                'cliente': int(request.data['cliente']),
                                'valor': Decimal(str(request.data['valor'])),
                                'descricao': "Transferência recebida do cliente #" + str(request.data['cliente-origem']),
                                'timestamp': datetime.datetime.utcnow().isoformat() # Todas as datas em UTC salvas em ISO_8601 !!!
                            }
                        )

                        # Construção do objeto a ser enviado para o data lake:
                        d = {}
                        c = get_object_or_404(Clientes.objects.using('clientes'), id=request.data['cliente'])
                        d['transacao_tipo'] = request.data['tipo'] + "_recebida"
                        d['cliente_sexo'] = c.sexo
                        d['cliente_estado'] = c.estado
                        d['cliente_cidade'] = c.cidade
                        d['cliente_data_nascimento'] = str(c.data_nascimento)
                        d['cliente_estado_civil'] = c.estado_civil
                        d['cliente_escolaridade'] = c.escolaridade
                        d['transacao_valor'] = request.data['valor']
                        d['transacao_timestamp'] = str(datetime.datetime.utcnow().isoformat())
                        dl.store(d)

                        d = {}
                        c = get_object_or_404(Clientes.objects.using('clientes'), id=request.data['cliente-origem'])
                        d['transacao_tipo'] = request.data['tipo'] + "_enviada"
                        d['cliente_sexo'] = c.sexo
                        d['cliente_estado'] = c.estado
                        d['cliente_cidade'] = c.cidade
                        d['cliente_data_nascimento'] = str(c.data_nascimento)
                        d['cliente_estado_civil'] = c.estado_civil
                        d['cliente_escolaridade'] = c.escolaridade
                        d['transacao_valor'] = request.data['valor']
                        d['transacao_timestamp'] = str(datetime.datetime.utcnow().isoformat())
                        dl.store(d)
                        
                        return Response({"status": "sucesso"})

                    else: # O valor a ser transferido é maior que o saldo do cliente
                        return Response({"status": "erro", "msg": "Saldo insuficiente."})  

                else: # O cliente não existe na tabela de saldos
                    return Response({"status": "erro", "msg": "Saldo insuficiente."})

            elif (request.data['tipo'] == "saque"): # Tipo saque
                saldo = dyndb.Table("saldo")
                r = saldo.get_item(Key={"cliente": request.data['cliente']}) # Localiza o saldo do cliente

                if ("Item" in r): # O cliente possui algum saldo?
                    item = r['Item']
                    if (float(item['saldo']) >= float(request.data['valor'])): # O cliente possui saldo maior que o valor do saque?
                        item['saldo'] = str(float(item['saldo']) - float(request.data['valor'])) # Subtrai o valor sacado
                        r = saldo.put_item(Item=item)

                        transacoes = dyndb.Table("transacoes")
                        r = transacoes.put_item( # Registra a transação
                            Item={
                                'id': str(uuid.uuid1()),
                                'tipo': request.data['tipo'],
                                'cliente': int(request.data['cliente']),
                                'valor': Decimal(str(request.data['valor'])),
                                'descricao': "Retirada de valor de conta",
                                'timestamp': datetime.datetime.utcnow().isoformat() # Todas as datas em UTC salvas em ISO_8601 !!!
                            }
                        )

                        # Construção do objeto a ser enviado para o data lake:
                        d = {}
                        c = get_object_or_404(Clientes.objects.using('clientes'), id=request.data['cliente'])
                        d['transacao_tipo'] = request.data['tipo']
                        d['cliente_sexo'] = c.sexo
                        d['cliente_estado'] = c.estado
                        d['cliente_cidade'] = c.cidade
                        d['cliente_data_nascimento'] = str(c.data_nascimento)
                        d['cliente_estado_civil'] = c.estado_civil
                        d['cliente_escolaridade'] = c.escolaridade
                        d['transacao_valor'] = request.data['valor']
                        d['transacao_timestamp'] = str(datetime.datetime.utcnow().isoformat())
                        dl.store(d)

                        return Response({"status": "sucesso"}) # Retorna sucesso

                    else: # O saldo do cliente é inferior ao valor do saque
                        return Response({"status": "erro", "msg": "Saldo insuficiente."})
                    
                else: # O cliente nem existe na tabela de saldos, saldo 0...
                    return Response({"status": "erro", "msg": "Saldo insuficiente."})

            elif (request.data['tipo'] == "saldo"): # Tipo saldo
                saldo = dyndb.Table("saldo")
                r = saldo.get_item(Key={"cliente": request.data['cliente']}) # Tenta localizar o saldo do cliente

                if ("Item" in r): # Existe algum saldo para o cliente (zero ou mais)
                    return Response({"status": "sucesso", "saldo": r['Item']['saldo']})

                else: # O cliente não existe na tabela de saldos
                    return Response({"status": "sucesso", "saldo": 0})

            elif (request.data['tipo'] == "extrato"): # Tipo extrato
                transacoes = dyndb.Table("transacoes")
                r = transacoes.scan( # Pesquisa em toda a base para transações do cliente
                    ScanFilter={
                        "cliente": {
                            "AttributeValueList": [int(request.data["cliente"])],
                            "ComparisonOperator": "EQ"
                        }
                    }
                )
                if ('Items' in r):
                    return Response({"status": "sucesso", "extrato": r['Items']})
                else:
                    return Response({"status": "erro", "msg": "Não existem movimentações para a conta atual"})

        else: # Erro
            raise NotFound(detail="Invalid request", code=404)

        a = get_object_or_404(Clientes.objects.using('clientes'), id=3) #request.data['id']
        s = ClientesSerializer(a)
        r = t.get_item(Key={'id':'1'})
        return Response({"status": "sucesso", "somedata": s.data, "d": r, "echo": request.data})