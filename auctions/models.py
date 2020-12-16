from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Categories(models.Model):
    category = models.CharField(max_length = 64)

    def __str__(self):
        return f"{self.category}"

class Listing(models.Model):
    item = models.CharField(max_length = 64)
    item_category = models.ForeignKey(Categories, on_delete = models.CASCADE, related_name ='item_category', blank=True,null=True)
    description = models.CharField(max_length =300)
    price = models.FloatField()
    image = models.ImageField(blank=True, null=True)
    listed_by = models.ForeignKey(User, blank= True, null = True, on_delete=models.CASCADE, related_name='user_listing')
    

    def __str__(self):
        return f"Item: {self.item}, Category: {self.item_category}, Description: {self.description}, Price: ${self.price}"

class Bid(models.Model):
    bid = models.FloatField()
    bid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_bid')

    def __str__(self):
        return f"{self.bid} by {self.bid_by}"

class Comment(models.Model):
    comment = models.CharField(max_length=300)
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment', blank=True, null=True)

    def __str__(self):
        return f"{self.comment}. commented by: {self.comment_by} "

class Watchlist(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='list_item', blank=True, null=True)
    watched_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_watchlist', blank=True,null=True)

    def __str__(self):
        return f"{self.item} is watched by {self.watched_by}"

