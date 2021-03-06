from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("closedlist", views.closelist, name="closelist"),
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newitem", views.newitem, name="newitem"),
    path("<int:item_id>", views.listing, name="listing"),
    path("comments", views.Commentsubmit, name="comment"),
    path("bidposted", views.Bidpost, name="bidpost"),
    path("watchlist", views.watchlistpage, name="watchlist"),
    path("adding",views.watchlistwork, name="watchlistwork"),
    path("closelisting",views.closelisting, name="closelisting"),
    path("category",views.categorylist, name="categorylist"),
    path("<str:category>",views.category, name="category")
]