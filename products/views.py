from django.shortcuts import render
from .models import Product, ProductTranslations
from category.models import Category

# Create your views here.
def categories(request):
    category=Category.objects.all()
    print(category)
    return render(request, 'main.html', {'category': category})




