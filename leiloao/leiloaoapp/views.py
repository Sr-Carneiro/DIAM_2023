from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse

import os

from django.conf.global_settings import MEDIA_URL
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.checks import messages
from django.utils import timezone
import urllib.request
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.template import loader
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import Sale, AppUser


## TODO: Login e Logout -> Falta por bonito
# TODO: Registar -> Form -> Emanuel
# TODO: Adicionar uma foto de utilizador ->
# TODO: Adicionar Sales -> Falta por bonito
# TODO: Adicionar uma foto a uma Sale
# TODO: Remover Sale
# TODO: Ver Todos as Sales -> Por isto no INDEX.HTML
# TODO: Fazer uma Bid -> Form
# TODO: Ver Perfil
# TODO: As Minhas Sales
# TODO: As Minhas Bids
# TODO: Zona de Administrador
# TODO: Adicionar a minha Watchlist
# TODO: Watchlist

# INDEX -> Vai servir de template para heranca de estrutura HTML das outras
# paginas. Deve conter header, navigation bar, foto de perfil, opcoes
# de login/logout, footer, etc


def template(request):
    return render(request, 'leiloaoapp/template.html')


def index(request):
    return render(request, 'leiloaoapp/index.html')


def registar(request):
    return render(request, 'leiloaoapp/registar.html')

def myBid(request):
    return render(request, 'leiloaoapp/myBid.html')


def add_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.user = request.user
            sale.save()

            # Save uploaded images
            multiuploader_image = MultiuploaderImage()
            multiuploader_image.user_key = sale.pk  # Set user key as the sale's primary key
            multiuploader_image.save(request)

            return redirect('leiloaoapp:index')
    else:
        form = SaleForm()

    return render(request, 'leiloaoapp/add_sale.html', {'form': form})

def perfil(request):
    user = request.user
    return render(request, 'leiloaoapp/perfil.html', {'user': user})

def mySale(request):
    return render(request, 'leiloaoapp/mySale.html')


def login_view(request):
    if request.method == 'GET':
        return render(request, 'leiloaoapp/login_view.html')
    else:
        utilizador = request.POST['username']
        palavra_passe = request.POST['password']
        user = authenticate(username=utilizador, password=palavra_passe)
        if user is not None:
            login(request, user)
            context = {
                'utilizador': user
            }
            return HttpResponseRedirect(reverse('leiloaoapp:index'))
        else:
            context = {
                'login_unsuccessful': 'Credenciais inválidas'
            }
            return render(request, 'leiloaoapp/login_view.html', context)


def logout_view(request):
    if not request.user.is_authenticated:
        return render(request, 'leiloaoapp/login_view.html')
    logout(request)
    return redirect('leiloaoapp:index')


def adicionarSale(request):
    if not request.user.is_authenticated:
        # TODO: mudar isto para ir para uma página de erro genérica
        return render(request, 'leiloaoapp/index.html')
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        initialAsk = request.POST['initialAsk']
        bidStartDate_str = request.POST['bidStartDate']
        bidEndDate_str = request.POST['bidEndDate']
        seller_username = request.user.username

        bidStartDate = datetime.strptime(bidStartDate_str, '%Y-%m-%dT%H:%M')
        bidEndDate = datetime.strptime(bidEndDate_str, '%Y-%m-%dT%H:%M')

        seller = get_object_or_404(AppUser, user__username=seller_username)

        creatingSale = Sale.objects.create(
            title=title,
            description=description,
            image_path="",
            isSold=False,
            initialAsk=initialAsk,
            bidStartDate=bidStartDate,
            bidEndDate=bidEndDate,
            lastBidDate=None,
            seller=seller,
            bidder=None,
            currentHighestBid=None
        )
        creatingSale.save()
        print("Sale gravada")
        return HttpResponseRedirect(reverse('leiloaoapp:index'))
    else:
        print("Sale não gravada!")
        return render(request, 'leiloaoapp/adicionarSale.html')

#TODO: chamar o remover Sale algures
def remove_sale(request, sale_id):
    if not request.user.is_authenticated:
        return render(request, 'leiloaoapp/index.html')

    sale = get_object_or_404(Sale, id=sale_id)

    if sale.seller != request.user.username:
        # TODO: redirect to a generic error page instead
        return render(request, 'leiloaoapp/index.html')

    sale.delete()

    return redirect('leiloao:index')
