
from datetime import datetime, timedelta
from sqlite3 import OperationalError

from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone


from .models import Sale, Bid, AppUser


## TODO: Login e Logout -> Falta por bonito
# TODO: Registar -> Form -> Emanuel
# TODO: Adicionar uma foto de utilizador ->
# TODO: Adicionar Sales -> Falta por bonito
# TODO: Adicionar uma foto a uma Sale
# TODO: Remover Sale
# TODO: Ver Todos as Sales -> Por isto no INDEX.HTML -> ESCOLHER CAMPOS E POR BONITO
# TODO: Fazer uma Bid -> Form
# TODO: Ver Perfil
# TODO: As Minhas Sales
# TODO: As Minhas Bids
# TODO: Zona de Administrador
# TODO: Adicionar a minha Watchlist
# TODO: Watchlist



def template(request):
    return render(request, 'leiloaoapp/template.html')


def index(request):
    sales_list = Sale.objects.order_by('title')[:5]
    context = {
        'sales_list': sales_list
    }
    return render(request, 'leiloaoapp/index.html', context)


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


def adicionarSale(request, timezone=None):
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
        return HttpResponseRedirect(reverse('leiloaoapp:index'))
    else:
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


def getSales(request):
    try:
        sales = Sale.objects.all()
        return render(request, 'index.html', {'sales': sales})
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
            return redirect('leilao:detalhe', sale_id=sale.id)
        else:
            return redirect('login')
    else:
        return render(request, 'leiloaoapp/detalhe.html', {'sale': sale})

