from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from users.models import Customer
from products.models import Product
from orders.models import Cart, CartItem


@login_required
def main(request):

    customer = request.user

    products = Product.objects.filter(
        is_available=True
    ).select_related(
        'brand',
        'type'
    )[:50]

    context = {
        'customer': customer,
        'products': products,
    }

    return render(request, 'main.html', context)


@login_required
def add_to_cart(request, product_id):

    customer = request.user

    product = get_object_or_404(
        Product,
        id=product_id,
        is_available=True
    )

    cart, created = Cart.objects.get_or_create(
        customer=customer
    )

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect(f'/#{product_id}')


@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(
        customer=request.user
    )

    return render(
        request,
        'cart.html',
        {
            'cart': cart,
        }
    )