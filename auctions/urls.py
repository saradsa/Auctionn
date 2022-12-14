from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create_listing, name="create"),
    path("categories/", views.categories, name="categories"),
    path("category_listing/<int:category_id>",
         views.category_listing, name="category_listing"),
    path("detail/<int:listing_id>/", views.detail, name="detail"),
    path("placebid/<int:listing_id>/", views.placebid, name="placebid"),
    path("comment/<int:listing_id>/", views.comment, name="comment"),
    path("removeWatchlist/<int:id>", views.removeWatchlist, name="removeWatchlist"),
    path("addWatchlist/<int:id>", views.addWatchlist, name="addWatchlist"),
    path("watchlist", views.watchlist, name="watchlist")
]
