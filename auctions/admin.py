from django.contrib import admin
from .models import User,Listing,Comments,Bids,watchlist,Winner


# Register your models here.
class UserAdmin(admin.ModelAdmin):
     list_display = ("id", "email", "password", "username")

class ListingAdmin(admin.ModelAdmin):
     list_display = ("id", "title", "description", "category", "first_bid", "created_at", "active")



admin.site.register(User, UserAdmin)
admin.site.register(Comments)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bids)
admin.site.register(watchlist)
admin.site.register(Winner)