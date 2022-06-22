from django.urls import path

from .views import index, cart, removecart

urlpatterns = [
    path('', index),
    path('cart', cart),
    path('cart/remove/<int:id>', removecart),
]