from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    category = models.CharField(max_length=20)
    first_bid = models.DecimalField(max_digits=64,decimal_places=2)
    image_url = models.URLField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    active = models.BooleanField(default = True)


    def __str__(self):
        return f"{self.title} {self.description} {self.category} {self.first_bid} {self.image_url} {self.created_at}"

class Comments(models.Model):
     item_id = models.ForeignKey(Listing, on_delete = models.CASCADE)
     user_id = models.ForeignKey(User, on_delete = models.CASCADE)
     comment = models.CharField(max_length=400)

     def __str__(self):
         return f"{self.item_id} {self.user_id} {self.comment}"

class watchlist(models.Model):
     item_id = models.ForeignKey(Listing, on_delete = models.CASCADE)
     user_id = models.ForeignKey(User, on_delete = models.CASCADE)
     watchlist = models.BooleanField(default = False)

     def __str__(self):
         return f"{self.item_id} {self.user_id}{self.watchlist}"


class Bids(models.Model):
     item_id = models.ForeignKey(Listing, on_delete = models.CASCADE)
     user_id = models.ForeignKey(User, on_delete = models.CASCADE)
     bids = models.DecimalField(max_digits=8,decimal_places=2)
     

     def __str__(self):
         return f"{self.item_id} {self.user_id}{self.bids}"

class Winner(models.Model):
     item_id = models.ForeignKey(Listing, on_delete = models.CASCADE)
     user_id = models.ForeignKey(User, on_delete = models.CASCADE)

     def __str__(self):
         return f"{self.item_id} {self.user_id}"