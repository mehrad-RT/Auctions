from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("makeListing", views.makeListing, name="makeListing"),
    path("selectedCategory", views.selected_category, name="selected_category"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("removeFromWatchlist/<int:id>", views.removeFromWatchlist, name="removeFromWatchlist"),
    path("addToWatchlist/<int:id>", views.addToWatchlist, name="addToWatchlist"),
    path("watchlist", views.showWatchlist, name="watchlist"),
    path("addToComment/<int:id>", views.addToComment, name="addToComment"),
    path("addToBid/<int:id>", views.addToBid, name="addToBid"),
    path("closeAuction/<int:id>", views.closeAuction, name="closeAuction"),
]
