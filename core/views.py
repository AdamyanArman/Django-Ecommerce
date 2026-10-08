from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from products.models import Product, ProductTranslations
from users.models import Customer
from products.models import Product
from orders.models import Cart, CartItem
from decimal import Decimal


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
        "quantity": int(cart_item.quantity),
    })



@login_required
def minus_to_cart(request, product_id):
    customer=request.user


    cart, _=Cart.objects.get_or_create(customer=customer)

    cart_item, _=CartItem.objects.get_or_create(cart=cart, product_id=product_id)


    product=get_object_or_404(Product, id=product_id, is_available=True)

    cart_item.quantity-=1
    cart_item.price=product.price

    cart_item.save()

    return JsonResponse({
        "success": True,
        "quantity": cart_item.quantity,
    })


@login_required
def product_in_cart_count(request, product_id):
    user = request.user

    # Փնտրում ենք CartItem-ը տվյալ օգտատիրոջ և ապրանքի համար
    cart_item = CartItem.objects.filter(
        cart__customer=user,
        product_id=product_id
    ).first()

    # Եթե ապրանքը զամբյուղում է, վերադարձնում ենք դրա քանակը, հակառակ դեպքում՝ 0
    count = cart_item.quantity if cart_item else 0



    count=Decimal(str(count)).normalize()
    count=float(count) if 'e' in str(count).lower() else count

    return JsonResponse({
        'count': count
    })



