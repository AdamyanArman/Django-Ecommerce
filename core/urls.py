from django.urls import path, include
from products.models import Product, ProductTranslations
from category.models import Category
from core import views

urlpatterns=[
    path('', views.main, name='main'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<uuid:product_id>/', views.add_to_cart, name='add_to_cart'),
]