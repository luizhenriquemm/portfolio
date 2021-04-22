from django import forms


from .models import Vendas, ItensVendas, Clientes, Vendedores

class VendasForm(forms.ModelForm):
    class Meta:
        model = Vendas
        fields = [
            'vendedor',
            'cliente',
            'data',
            'total'
        ]

class ItensVendasForm(forms.ModelForm):
    class Meta:
        model = ItensVendas
        fields = [
            'venda',
            'item',
            'quantidade',
            'valor',
            'ordem'
        ]

class ClientesForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = [
            'nome',
            'telefone',
            'endereco',
            'data_nascimento'
        ]

class VendedorForm(forms.ModelForm):
    class Meta:
        model = Vendedores
        fields = [
            'nome'
        ]