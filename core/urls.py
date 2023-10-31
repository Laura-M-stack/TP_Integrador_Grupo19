from django.contrib import admin
from django.urls import path, include
from . import views
from tienda_virtual import core


urlpatterns = [
   
    path(" ", views.index, name="index"),
    path("core", core, name= "core"),
    path("carrito", views.carrito, name="carrito"),
    path("login", views.login, name="login"),
    path("pedidos", views.pedidos, name="pedidos"),
    path("checkout", views.checkout, name="checkout"),
    path("registrarse", views.registrarse, name="registrarse"),
    ]
