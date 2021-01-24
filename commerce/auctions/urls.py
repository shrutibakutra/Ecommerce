from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.create, name="create"),
    path("view",views.view_listing, name = "view_listing"),
    path("detailedView/<str:pk>", views.detailed_view, name= "detailed_view"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("addTowatchlist/<str:auction_id>",views.addTowatchlist,name="addTowatchlist"),
    path("watchlistPage",views.watchlist,name="watchlist"),
    path("removewatchlist/<str:auction_id>",views.removewatchlist , name = "removewatchlist"),
    path("addBid/<str:auction_id>",views.addBid , name="addBid"),
    path("category/<str:category>",views.category,name="category"),
    path("endAuction/<str:auction_id>",views.endAuction,name="endAuction")
]