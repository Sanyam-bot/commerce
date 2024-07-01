from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create, name="create"),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('categories/', views.categories, name='categories'),
    path('categories/<str:key>', views.categories_key, name='categories_key'),
    path('listings/<int:listing_id>', views.listings, name='listings'),
    path('listings/<int:listing_id>/watchlist', views.add_to_watchlist, name='add_to_watchlist'),
    path('listings/<int:listing_id>/bid', views.bidfn, name='bid'),
    path('listings/<int:listing_id>/close', views.close, name='close'),   
    path('listing/<int:listing_id>/comment', views.comment, name='comment'),
]
