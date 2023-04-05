from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


# INDEX -> Vai servir de template para heranca de estrutura HTML das outras
# paginas. Deve conter header, navigation bar, foto de perfil, opcoes
# de login/logout, footer, ect

def template(request):
    return HttpResponse("Pagina de entrada da app votacao.")

