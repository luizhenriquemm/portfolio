from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse
from django.db.models import Sum, F
from django.contrib.auth.decorators import login_required, permission_required

from .models import Vendedores, Clientes, Vendas, ItensVendas
from .forms import VendasForm, ItensVendasForm, ClientesForm, VendedorForm
# Create your views here.

#class index(generic.ListView):
#    template_name = "loja/vendas.html"
#
#    def get_queryset(self):
#        return Vendas.objects.all()

@login_required

def vendas(request):
    template_name = "loja/vendas.html"
    context = {
        'vendas': Vendas.objects.all().order_by("-id")
    }

    return render(request, template_name, context)

def ver_venda(request, id):
    template_name = "loja/ver_venda.html"
    v = get_object_or_404(Vendas, pk=id)
    context = {
        'venda': v,
        'itens': ItensVendas.objects.filter(venda=id).order_by("ordem")
    }

    return render(request, template_name, context)

def clientes(request):
    template_name = "loja/clientes.html"
    context = {
        'clientes': Clientes.objects.all().order_by("-id")
    }

    return render(request, template_name, context)

def ver_cliente(request, id):
    template_name = "loja/ver_cliente.html"
    c = get_object_or_404(Clientes, pk=id)
    context = {
        'cliente': c
    }

    return render(request, template_name, context)

def vendedores(request):
    template_name = "loja/vendedores.html"
    context = {
        'vendedores': Vendedores.objects.all().order_by("-id")
    }

    return render(request, template_name, context)

def ver_vendedor(request, id):
    template_name = "loja/ver_vendedor.html"
    v = get_object_or_404(Vendedores, pk=id)
    context = {
        'vendedor': v
    }

    return render(request, template_name, context)


# Forms views

def incluir_venda(request):
    template_name = "loja/incluir_venda.html"

    if (request.method == "POST"):
        form = VendasForm(request.POST)

        if form.is_valid():
            a = form.save(commit=False)
            a.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse(ver_venda, args=(a.pk,)))

        else:
            context = {
                'form': request.POST,
                'status': False,
                'vendedores': Vendedores.objects.all().order_by("nome"),
                'clientes': Clientes.objects.all().order_by("nome")
            }

    else:
        context = {
            'form': None,
            'vendedores': Vendedores.objects.all().order_by("nome"),
            'clientes': Clientes.objects.all().order_by("nome")
        }

    return render(request, template_name, context)

def editar_venda(request, id):
    template_name = "loja/editar_venda.html"
    i = get_object_or_404(Vendas, pk=id)

    if (request.method == "POST"):
        form = VendasForm(request.POST, instance=i)

        if (form.is_valid()):
            post = form.save(commit=False)
            post.vendedor = form.cleaned_data['vendedor']
            post.cliente = form.cleaned_data['cliente']
            post.save()

            return HttpResponseRedirect(reverse(ver_venda, args=(id,)))

        else:
            context = {
                'form': form,
                'status': False,
                'venda': Vendas.objects.get(pk=i.venda.id),
                'itens': ItensVendas.objects.filter(venda=i.venda.id).order_by("ordem")
            }

    else:
        form = VendasForm(instance=i)

        context = {
            'form': form,
            'vendedores': Vendedores.objects.all().order_by("nome"),
            'clientes': Clientes.objects.all().order_by("nome")
        }

    return render(request, template_name, context)

def excluir_venda(request, id):
    Vendas.objects.filter(pk=id).delete()
    return HttpResponseRedirect(reverse(vendas))



def incluir_item(request, id):
    template_name = "loja/incluir_item.html"

    if (request.method == "POST"):
        form = ItensVendasForm(request.POST)

        if form.is_valid():
            form.save()

            q = Vendas.objects.get(pk=id)
            q.total = ItensVendas.objects.filter(venda=id).annotate(soma=F('valor') * F('quantidade')).aggregate(Sum('soma'))['soma__sum']
            q.save()

            return HttpResponseRedirect(reverse(ver_venda, args=(id,)))

        else:
            context = {
                'form': request.POST,
                'status': False,
                'venda': Vendas.objects.get(pk=id),
                'itens': ItensVendas.objects.filter(venda=id).order_by("ordem")
            }

    else:
        context = {
            'form': None,
            'venda': Vendas.objects.get(pk=id),
            'itens': ItensVendas.objects.filter(venda=id).order_by("ordem")
        }

    return render(request, template_name, context)

def editar_item(request, id):
    template_name = "loja/editar_item.html"
    i = get_object_or_404(ItensVendas, pk=id)

    if (request.method == "POST"):
        form = ItensVendasForm(request.POST, instance=i)

        if (form.is_valid()):
            post = form.save(commit=False)
            post.item = form.cleaned_data['item']
            post.quantidade = form.cleaned_data['quantidade']
            post.valor = form.cleaned_data['valor']
            post.save()

            q = Vendas.objects.get(pk=i.venda.id)
            q.total = ItensVendas.objects.filter(venda=i.venda.id).annotate(soma=F('valor') * F('quantidade')).aggregate(Sum('soma'))['soma__sum']
            q.save()

            return HttpResponseRedirect(reverse(ver_venda, args=(i.venda.id,)))

        else:
            context = {
                'form': form,
                'status': False,
                'venda': Vendas.objects.get(pk=i.venda.id),
                'itens': ItensVendas.objects.filter(venda=i.venda.id).order_by("ordem")
            }

    else:
        form = ItensVendasForm(instance=i)

        context = {
            'form': form,
            'venda': Vendas.objects.get(pk=i.venda.id),
            'itens': ItensVendas.objects.filter(venda=i.venda.id).order_by("ordem")
        }

    return render(request, template_name, context)

def excluir_item(request, id):
    i = ItensVendas.objects.get(pk=id)
    v = i.venda.id
    i.delete()
    return HttpResponseRedirect(reverse(ver_venda, args=(v,)))


def incluir_cliente(request):
    template_name = "loja/incluir_cliente.html"

    if (request.method == "POST"):
        form = ClientesForm(request.POST)

        if form.is_valid():
            a = form.save(commit=False)
            a.save()
            form.save_m2m()

            return HttpResponseRedirect(reverse(ver_cliente, args=(a.pk,)))

        else:
            context = {
                'form': request.POST,
                'status': False
            }
    else:
        context = {
            'form': None
        }

    return render(request, template_name, context)

def editar_cliente(request, id):
    template_name = "loja/editar_cliente.html"
    i = get_object_or_404(Clientes, pk=id)

    if (request.method == "POST"):
        form = ClientesForm(request.POST, instance=i)

        if (form.is_valid()):
            post = form.save(commit=False)
            post.nome = form.cleaned_data['nome']
            post.telefone = form.cleaned_data['telefone']
            post.endereco = form.cleaned_data['endereco']
            post.data_nascimento = form.cleaned_data['data_nascimento']
            post.save()

            return HttpResponseRedirect(reverse(ver_cliente, args=(id,)))

        else:
            context = {
                'form': form,
                'status': False,
            }

    else:
        form = ClientesForm(instance=i)

        context = {
            'form': form
        }

    return render(request, template_name, context)

def excluir_cliente(request, id):
    Clientes.objects.filter(pk=id).delete()
    return HttpResponseRedirect(reverse(clientes))


def incluir_vendedor(request):
    template_name = "loja/incluir_vendedor.html"

    if (request.method == "POST"):
        form = VendedorForm(request.POST)

        if form.is_valid():
            a = form.save(commit=False)
            a.save()
            form.save_m2m()

            return HttpResponseRedirect(reverse(ver_vendedor, args=(a.pk,)))

        else:
            context = {
                'form': request.POST,
                'status': False
            }
    else:
        context = {
            'form': None
        }

    return render(request, template_name, context)

def editar_vendedor(request, id):
    template_name = "loja/editar_vendedor.html"
    i = get_object_or_404(Vendedores, pk=id)

    if (request.method == "POST"):
        form = VendedorForm(request.POST, instance=i)

        if (form.is_valid()):
            post = form.save(commit=False)
            post.nome = form.cleaned_data['nome']
            post.save()

            return HttpResponseRedirect(reverse(ver_vendedor, args=(id,)))

        else:
            context = {
                'form': form,
                'status': False,
            }

    else:
        form = VendedorForm(instance=i)

        context = {
            'form': form
        }

    return render(request, template_name, context)

def excluir_vendedor(request, id):
    Vendedores.objects.filter(pk=id).delete()
    return HttpResponseRedirect(reverse(vendedores))