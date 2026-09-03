from django.urls import path, include
from products.models import Product, ProductTranslations
from category.models import Category
from core import views

urlpatterns=[
    path('', views.main, name='main'),
]