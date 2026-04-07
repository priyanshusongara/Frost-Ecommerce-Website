from django.contrib import admin
from django.urls import path

from .models import Cart,CartItem

admin.site.register(Cart)
admin.site.register(CartItem)
