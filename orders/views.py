from django.shortcuts import render, get_object_or_404
from .models import Cart, CartItem
from products.models import Product, ProductTranslations
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.
@login_required
def add_to_cart(request, product_id):
    customer=request.user


    cart, _=Cart.objects.get_or_create(customer=customer)

    cart_item, _=CartItem.objects.get_or_create(cart=cart, product_id=product_id)


    product=get_object_or_404(Product, id=product_id, is_available=True)

    cart_item.quantity+=1
    cart_item.price=product.price

    cart_item.save()

    return JsonResponse({
        "success": True,
        "quantity": cart_item.quantity,
    })





