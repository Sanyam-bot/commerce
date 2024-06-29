from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create, name="create"),
    path('listings/<int:listing_id>', views.listings, name='listings'),
    path('listings/<int:listing_id>/watchlist', views.watchlist, name='watchlist'),
    path('listings/<int:listing_id>/bid', views.bidfn, name='bid'),    
]
