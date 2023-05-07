from urllib import request
from django.urls import path
from . import views

app_name = 'leiloaoapp'
urlpatterns = [
  path("", views.template, name="template"),
  path('index/', views.index, name="index"),
  path('template/', views.template, name="template"),
  path('registar/', views.registar, name="registar"),
  path('login_view/', views.login_view, name='login_view'),
  path('logout_view/', views.logout_view, name='logout_view'),
  path('adicionarSale/', views.adicionarSale, name='adicionarSale'),
  path('mySale/', views.mySale, name='mySale'),
  path('myBid/', views.myBid, name='myBid'),
  path('perfil/', views.perfil, name='perfil'),
  path('index/', views.getSales, name='getSales'),
  path("<int:sale_id>", views.detalhe, name='detalhe'),
  path('<int:sale_id>/colocar_bid', views.colocarBid, name='colocarBid'),

]