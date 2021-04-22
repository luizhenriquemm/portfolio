from django.db import models
from datetime import date

# Create your models here.

class Vendedores(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Clientes(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=100)
    endereco = models.CharField(max_length=100)
    data_nascimento = models.DateField()

    def __str__(self):
        return self.nome

class Vendas(models.Model):
    vendedor = models.ForeignKey(Vendedores, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    data = models.DateField(blank=True, default=date.today)
    total = models.FloatField(blank=True, default=0)

class ItensVendas(models.Model):
    venda = models.ForeignKey(Vendas, on_delete=models.CASCADE)
    item = models.CharField(max_length=100)
    quantidade = models.IntegerField()
    valor = models.FloatField()
    ordem = models.IntegerField()

    def __str__(self):
        return self.item