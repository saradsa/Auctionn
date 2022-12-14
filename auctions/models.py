from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Count

# Create your models here.


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Listing(models.Model):
    title = models.CharField(max_length=30)
    detail = models.CharField(max_length=300, null=True)
    image = models.CharField(max_length=1000)
    price = models.FloatField()
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="user")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True, related_name="category")
    created_at = models.DateTimeField(auto_now_add=True)
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="listingWatchlist")

    def __str__(self):
        return self.title


class Bid(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, null=True, blank=True, related_name="listing")
    bidder = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="bidder")
    new_bid = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True, related_name="commentfor")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="commenter")
    comment = models.CharField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)



