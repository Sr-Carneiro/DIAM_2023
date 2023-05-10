from django.urls import path
from . import views

app_name = 'leiloaoapp'
urlpatterns = [
    path("", views.template, name="template"),
    path('index/', views.index, name="index"),
    path('myBid/', views.myBid, name='myBid'),
    path('perfil/', views.perfil, name='perfil'),
    path('mySale/', views.mySale, name='mySale'),
    path('getSales/', views.getSales, name='getSales'), #renomeado para getSales
    path('template/', views.template, name="template"),
    path('registar/', views.registar, name="registar"),
    path("<int:sale_id>/", views.detalhe, name='detalhe'), # adicionado / ao final
    path('watchlist/', views.watchlist, name='watchlist'),
    path('login_view/', views.login_view, name='login_view'),
    path('logout_view/', views.logout_view, name='logout_view'),
    path('adicionarSale/', views.adicionarSale, name='adicionarSale'),
    path('<int:sale_id>/colocar_bid', views.colocarBid, name='colocarBid'),
    path('remove-sale/<int:sale_id>/', views.remove_sale, name='remove_sale'),
    path('addToWatchlist/<int:sale_id>/', views.addToWatchlist, name='addToWatchlist'),
    path('removeFromWatchlist/<int:watchlistline_id>/', views.removeFromWatchlist, name='removeFromWatchlist'),
]