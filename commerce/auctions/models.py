from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    bid= models.IntegerField(null=False)
    image = models.ImageField(upload_to = "media/")
    options = (
        ("FASHION","fashion"),
        ("TOYS","toys"),
        ("ELECTRONICS","electronics"),
        ("HOME","home"),
        ("OTHER","other")
    )
    category = models.CharField(max_length=15, choices=options,default="None")
    active=models.BooleanField(default=True)

class bids(models.Model):
    bidder = models.ForeignKey(User,on_delete= models.CASCADE ,default=1,null=True)
    auction = models.ForeignKey(AuctionListing , on_delete=models.CASCADE)
    bids = models.IntegerField()


class comments(models.Model):
    user = models.ForeignKey(User,on_delete= models.CASCADE ,default=1,null=True)
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    comments = models.CharField(max_length=500)

class Watchlist(models.Model):
    user = models.ForeignKey(User,on_delete= models.CASCADE,null=True)
    listingid = models.ForeignKey(AuctionListing,on_delete= models.CASCADE)
