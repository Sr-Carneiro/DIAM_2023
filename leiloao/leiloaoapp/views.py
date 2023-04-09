from django.shortcuts import render
from django.http import HttpResponse

# TODO: Logins e Logouts
# TODO: Registar -> Form
# TODO: Adicionar uma foto de utilizador
# TODO: Adicionar Sales -> Form
# TODO: Adicionar uma foto a uma Sale
# TODO: Remover Sale
# TODO: Fazer uma Bid -> Form
# TODO: Ver Perfil
# TODO: As Minhas Sales
# TODO: As Minhas Bids
# TODO: Zona de Administrador
# TODO: Adicionar a minha Watchlist
# TODO: Watchlist

# INDEX -> Vai servir de template para heranca de estrutura HTML das outras
# paginas. Deve conter header, navigation bar, foto de perfil, opcoes
# de login/logout, footer, ect

def template(request):
    return render(request, 'leiloao/template.html')

def registar(request):
    return
