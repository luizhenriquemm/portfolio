from django.db import models

# Create your models here.

class Clientes(models.Model):
    class Meta:
        db_table = 'clientes'

    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    sexo = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    endereco = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    telefone = models.CharField(max_length=100)
    cpf = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    estado_civil = models.CharField(max_length=100)
    escolaridade = models.CharField(max_length=100)
