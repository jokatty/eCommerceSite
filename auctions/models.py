from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Categories(models.Model):
    category = models.CharField(max_length = 64)

class Listing(models.Model):
    item = models.CharField(max_length = 64)
    item_category = models.ForeignKey(Categories, on_delete = models.CASCADE, related_name ='item_category')
    description = models.CharField(max_length =300)
    price = models.FloatField()

class Bid(models.Model):
    bid = models.FloatField()
    bid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_bid')

class Comment(models.Model):
    comment = models.CharField(max_length=300)
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
