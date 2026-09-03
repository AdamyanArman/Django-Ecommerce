from django.db import models
from products.models import Product, ProductTranslations
from category.models import Category
from django.shortcuts import render

# Create your models here.
def main(request):
    products=Product.objects.filter(is_available=True)

    body={
        'products': products
    }
    return render(request, 'main.html', body)
