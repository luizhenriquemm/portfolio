from django.contrib import admin
from .models import Vendedores, Clientes, Vendas, ItensVendas

# Register your models here.

admin.site.register(Vendedores)
admin.site.register(Clientes)
admin.site.register(Vendas)
admin.site.register(ItensVendas)