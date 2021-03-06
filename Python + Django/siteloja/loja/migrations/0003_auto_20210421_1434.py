# Generated by Django 3.2 on 2021-04-21 17:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0002_itensvendas_ordem'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientes',
            name='data_nascimento',
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='clientes',
            name='endereco',
            field=models.CharField(default=' ', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clientes',
            name='telefone',
            field=models.CharField(default=' ', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='vendas',
            name='data',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='vendas',
            name='total',
            field=models.FloatField(default=0),
        ),
    ]
