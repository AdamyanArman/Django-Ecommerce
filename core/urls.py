from django.urls import path, include
from products.models import Product, ProductTranslations
from category.models import Category
from core import views

urlpatterns=[
    path('', views.main, name='main'),
    path('add_to_cart/<uuid:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('minus_to_cart/<uuid:product_id>/', views.minus_to_cart, name='minus-from-cart'),
    path('product_count_in_cart/<uuid:product_id>/', views.product_in_cart_count, name='check-product-count'),
    path('cart/', views.cart, name='cart'),
]