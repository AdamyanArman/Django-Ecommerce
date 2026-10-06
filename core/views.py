from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from users.models import Customer
from products.models import Product
from orders.models import Cart, CartItem


@login_required
def main(request):

    customer = request.user

    products = Product.objects.filter(is_available=True).select_related('brand', 'type')[:50]


    context = {
        'customer': customer,
        'products': products,
    }
    return render(request, 'main.html', context)



    return render(request, 'main.html', context)


