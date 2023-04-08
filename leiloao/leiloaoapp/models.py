import os

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import datetime

#AppUser: Representa um utilizador da aplicação
class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    #TODO: Caminho do image_path
    image_path = models.CharField(max_length=255, default='.png')

    def __str__(self):
        return self.name

# UserType: Representa um tipo de Utilizador(Admin, user, etc)
class UserType(models.Model):
    description = models.CharField(max_length=255)
    def __str__(self):
        return self.description

class Sale(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    # TODO: Caminho do image_path
    image_path = models.CharField('Caminho da Imagem', max_length=255, default='.png')
    isSold = models.BooleanField('Artigo Vendido')
    initialAsk = models.DecimalField(max_digits=10, decimal_places=2)
    bidStartDate = models.DateTimeField('Data Publicação')
    bidEndDate = models.DateTimeField('Data Publicação')
    lastBidDate = models.DateTimeField('Data Publicação')
    seller = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='Seller')
    bidder = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='Bidder')
    currentHighestBid = models.ForeignKey('Bid', on_delete=models.CASCADE, null=True, blank=True, related_name='HighestBid')

class Bid(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=2)
    bidder = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='BidSale')


class WatchListLine(models.Model):
    appUser = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='AppUser')
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='WatchingSale')

