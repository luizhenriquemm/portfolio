from django.urls import path
from . import views

urlpatterns = [
    #inicio
    #path('', views.index.as_view(), name="index"),
    path('', views.vendas, name="vendas"),
    path('ver-venda/<int:id>', views.ver_venda, name="ver_venda"),
    path('incluir-venda', views.incluir_venda),
    path('editar-venda/<int:id>', views.editar_venda),
    path('excluir-venda/<int:id>', views.excluir_venda),

    path('incluir-item/<int:id>', views.incluir_item),
    path('editar-item/<int:id>', views.editar_item),
    path('excluir-item/<int:id>', views.excluir_item),
    
    path('clientes', views.clientes),
    path('ver-cliente/<int:id>', views.ver_cliente),
    path('incluir-cliente', views.incluir_cliente),
    path('editar-cliente/<int:id>', views.editar_cliente),
    path('excluir-cliente/<int:id>', views.excluir_cliente),

    path('vendedores', views.vendedores),
    path('ver-vendedor/<int:id>', views.ver_vendedor),
    path('incluir-vendedor', views.incluir_vendedor),
    path('editar-vendedor/<int:id>', views.editar_vendedor),
    path('excluir-vendedor/<int:id>', views.excluir_vendedor),
]