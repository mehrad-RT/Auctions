from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name
    
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True , related_name="userBid")
    bid = models.IntegerField(default=0)
    
class Listing(models.Model):
    title = models.CharField(max_length=64)
    image = models.CharField(max_length=2000)
    description = models.CharField(max_length=1000)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, related_name="bidPrice")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True , related_name="category")
    activity = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True , related_name="user")
    watchlist = models.ManyToManyField(User, blank=True , related_name="watchlistUser")

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True , related_name="userComment")
    comment = models.CharField(max_length=5000)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True , related_name="listingComment")

    def __str__(self):
        return "f{self.author} comment on {self.listing}"
    
