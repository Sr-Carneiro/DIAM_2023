from urllib import request
from django.urls import path
from . import views

urlpatterns = [
  path("", views.template, name="template"),
  path('index/', views.index, name="index"),
  path('template/', views.template, name="template"),
  path('registar/', views.registar, name="registar"),
  path('login_view/', views.login_view, name='login_view'),

]