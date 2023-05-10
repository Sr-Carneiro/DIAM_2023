
from datetime import datetime, timedelta
from sqlite3 import OperationalError
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import AppUser
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.core.checks import messages
from django.contrib import messages
from django.contrib.auth.models import User, Permission

from .models import Sale, Bid, AppUser, WatchListLine

    # FALTA FAZER
# TODO: Mostrar foto de utilizador lá em cima do lado esquerdo, e no Perfil
# TODO: Adicionar uma foto de utilizador -> Mudar do Registar para o Perfil?
# TODO: Adicionar uma foto a uma Sale
# TODO: Mostrar a foto da Sale
# TODO: Zona de Administrador -> SuperUsers podem remover qualquer Sale, desativar outros users. Ver lista de users.
# TODO: Remover item da watchlist

    # NICE TO HAVE -> Se der tempo
# TODO: NICETOHAVE: Mostrar nas Minhas Bids, quais as que eu ganhei
# TODO: NICETOHAVE: As Minhas Sales -> identificar quais tiveram bids e quais não tiveram no final
# TODO: NICETOHAVE: Pesquisa de Sales no Index
# TODO: NICETOHAVE: Ordenar tabela de Sales no Index por coluna escolhida
# TODO: NICETOHAVE:

    # POR BONITO
# TODO: Watchlist -> POR BONITO
# TODO: As Minhas Bids -> POR BONITO
# TODO: Ver Perfil -> POR BONITO, ADICIONAR COISAS(Mostrar foto)
# TODO: Login e Logout -> POR BONITO
# TODO: Registar -> Form -> Emanuel -> POR BONITO
# TODO: Ver Todos as Sales -> POR BONITO
# TODO: Adicionar Sales -> POR BONITO
# TODO: Adicionar à minha Watchlist DONE

    # DONE
# TODO: Remover Sale -> DONE
# TODO: Fazer uma Bid (Form) -> DONE(TESTAR)


def template(request):
    return render(request, 'leiloaoapp/template.html')


def index(request):
    sales_list = Sale.objects.filter(bidEndDate__gt=timezone.now())
    context = {
        'sales_list': sales_list
    }
    return render(request, 'leiloaoapp/index.html', context)

def perfil(request):
    return render(request, 'leiloaoapp/perfil.html')


def registar(request):
    if request.method == "GET":
        return render(request, 'leiloaoapp/registar.html')
    else:
        utilizador = request.POST['username']
        palavra_passe = request.POST['password']
        email = request.POST['email']
        primeiro_nome = request.POST['primeiro_nome']
        ultimo_nome = request.POST['ultimo_nome']
        image = request.FILES.get('image', None)  # Obter o arquivo de imagem (se existir)

        # Check if the user already exists
        if User.objects.filter(username=utilizador).exists():
            return render(request, 'leiloaoapp/erro.html')

        user = User.objects.create_user(
            username=utilizador,
            email=email,
            password=palavra_passe,
            first_name=primeiro_nome,
            last_name=ultimo_nome
        )
        appuser = AppUser.objects.create(user=user, name=utilizador, email=email)

        if image:  # Se a imagem existir
            # Salvar a imagem no diretório de mídia
            filename = default_storage.save('images/{}'.format(image.name), image)
            # Definir o caminho da imagem no modelo AppUser
            appuser.image = filename

            # Redimensionar a imagem e salvá-la no mesmo caminho
            filepath = 'media/{}'.format(filename)
            with Image.open(filepath) as img:
                tamanho = (300, 300)  # Novo tamanho da imagem
                img = img.resize(tamanho)
                img.save(filepath)

        appuser.save()

        messages.add_message(request, messages.SUCCESS, 'Utilizador criado com sucesso')

        # authenticate user and login
        user = authenticate(request, username=utilizador, password=palavra_passe)
        if user is not None:
            login(request, user)
            return redirect('leiloaoapp:perfil')  # redireciona para a URL nomeada 'perfil'
        else:
            return redirect('index')

# TODO VER SE ISTO VAI SER USADO
# def add_sale(request):
#     if request.method == 'POST':
#         form = SaleForm(request.POST)
#         if form.is_valid():
#             sale = form.save(commit=False)
#             sale.user = request.user
#             sale.save()
#
#             # Save uploaded images
#             multiuploader_image = MultiuploaderImage()
#             multiuploader_image.user_key = sale.pk  # Set user key as the sale's primary key
#             multiuploader_image.save(request)
#
#             return redirect('leiloaoapp:index')
#     else:
#         form = SaleForm()
#
#     return render(request, 'leiloaoapp/add_sale.html', {'form': form})


def perfil(request):
    user = request.user
    return render(request, 'leiloaoapp/perfil.html', {'user': user})


def myBid(request):
    apuser = request.user.appuser
    bid_list = Bid.objects.filter(bidder=apuser)
    context = {
        'bid_list': bid_list
    }
    return render(request, 'leiloaoapp/myBid.html', context)


def mySale(request):
    apuser = request.user.appuser
    sales_list = Sale.objects.filter(seller=apuser)
    context = {
        'sales_list': sales_list
    }
    return render(request, 'leiloaoapp/mySale.html', context)


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


def adicionarSale(request, timezone=None):
    if not request.user.is_authenticated:
        # TODO: mudar isto para ir para uma página de erro genérica
        return render(request, 'leiloaoapp/adicionarSale.html',
                  { 'error_message': 'Tem de fazer Login para criar Sales.'})
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
        return HttpResponseRedirect(reverse('leiloaoapp:index'))
    else:
        return render(request, 'leiloaoapp/adicionarSale.html')


def remove_sale(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)

    if not request.user.is_authenticated:
        return render(request, 'leiloaoapp/detalhe.html',
                      {'sale': sale, 'error_message': 'Tem de fazer Login para interagir com as Sale.'})


    if sale.seller != request.user.appuser:
        return render(request, 'leiloaoapp/detalhe.html',
                      {'sale': sale, 'error_message': 'Não pode cancelar Sales de outro Seller.'})

    sale.bidEndDate = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    sale.save()

    return render(request, 'leiloaoapp/detalhe.html', {'sale': sale})


def getSales(request):
    try:
        sales = Sale.objects.all()
        return render(request, 'index.html', {'sales': sales})
    except OperationalError as e:
        print(f"Database error: {e}")


def getBids(request):
    apuser = request.user.appuser
    bid_list = Bid.objects.filter(bidder=apuser)
    context = {
        'bid_list': bid_list
    }
    try:
        return render(request, 'myBid.html', context)
    except OperationalError as e:
        print(f"Database error: {e}")


def detalhe(request, sale_id):
    try:
        sale = Sale.objects.get(id=sale_id)
    except Sale.DoesNotExist:
        raise Http404("A Sale nao existe")
    now = timezone.now()
    bid_end_date = sale.bidEndDate.astimezone(now.tzinfo)
    time_remaining = bid_end_date - now
    if time_remaining < timedelta():
        time_remaining = timedelta()
    days, seconds, microseconds = time_remaining.days, time_remaining.seconds, time_remaining.microseconds
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    context = {
        'sale': sale,
        'days_remaining': days,
        'hours_remaining': hours,
        'minutes_remaining': minutes,
        'seconds_remaining': seconds if seconds else 0,
    }
    return render(request, 'leiloaoapp/detalhe.html', context=context)


def colocarBid(request, sale_id):
    sale = get_object_or_404(Sale, pk=sale_id)
    if request.method == 'POST':
        value = request.POST['new_bid']
        if not value:
            return render(request, 'leiloaoapp/detalhe.html', {'sale': sale, 'error_message': 'Por favor insira um valor.'})
        value = float(value)
        if value <= sale.initialAsk:
            return render(request, 'leiloaoapp/detalhe.html', {'sale': sale, 'error_message': 'O valor do Bid deve ser maior que o preço inicial.'})
        if timezone.now() > sale.bidEndDate:
            return render(request, 'leiloaoapp/detalhe.html', {'sale': sale, 'error_message': 'Esta Sale já terminou.'})
        if timezone.now() < sale.bidStartDate:
            print(timezone.now())
            print(sale.bidStartDate)
            return render(request, 'leiloaoapp/detalhe.html', {'sale': sale, 'error_message': 'Esta Sale ainda não começou.'})
        if sale.isSold:
            return render(request, 'leiloaoapp/detalhe.html', {'sale': sale, 'error_message': 'O artigo já foi vendido.'})
        if request.user.is_authenticated:
            bidder = request.user.appuser
            if not bidder:
                return render(request, 'leiloaoapp/detalhe.html', {'sale': sale, 'error_message': 'Deve registar-se para colocar Bids.'})
            if bidder == sale.seller:
                return render(request, 'leiloaoapp/detalhe.html', {'sale': sale, 'error_message': 'Não pode colocar Bids nas suas próprias Sales.'})
            if sale.currentHighestBid and value <= sale.currentHighestBid.value:
                return render(request, 'leiloaoapp/detalhe.html', {'sale': sale, 'error_message': 'O valor da sua Bid deve ser maior do que a Bid mais alta.'})

            bid = Bid.objects.create(value=value, bidder=bidder, sale=sale)
            sale.currentHighestBid = bid
            sale.bidder = bidder
            sale.lastBidDate = timezone.now()
            sale.save()
            return redirect('leiloaoapp:detalhe', sale_id=sale.id)
        else:
            return redirect('login')
    else:
        return render(request, 'leiloaoapp/detalhe.html', {'sale': sale})

def watchlist(request):
    apuser = request.user.appuser
    watchlist = WatchListLine.objects.filter(appUser=apuser)
    context = {
        'watchlist': watchlist
    }
    return render(request, 'leiloaoapp/watchlist.html', context)

def addToWatchlist(request, sale_id):
    apuser=request.user.appuser
    sale = Sale.objects.get(id=sale_id)
    watchlistline=WatchListLine.objects.create(sale=sale, appUser=apuser)
    watchlistline.save()
    return render(request, 'leiloaoapp/detalhe.html', {'sale': sale})

def removeFromWatchlist(request, watchlistline_id):
    line = WatchListLine.objects.get(id=watchlistline_id)
    line.delete()
    return redirect('leiloaoapp:watchlist')



