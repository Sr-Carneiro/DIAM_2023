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
from django.contrib.auth import authenticate, login

# TODO: Logins e Logouts -> Eduardo
# TODO: Registar -> Form -> Emanuel
# TODO: Adicionar uma foto de utilizador
# TODO: Adicionar Sales -> Form
# TODO: Adicionar uma foto a uma Sale
# TODO: Remover Sale
# TODO: Ver Todos as Sales
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
            return HttpResponseRedirect(reverse('index'))
        else:
            context = {
                'login_unsuccessful': 'Credenciais inválidas'
            }
            return render(request, 'leiloaoapp/login_view.html', context)
