from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from products.models import Product, ProductTranslations
from users.models import Customer
from products.models import Product
from orders.models import Cart, CartItem, Order, OrderItem
from decimal import Decimal
from django.contrib import messages
from django.db import transaction


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




@login_required
def cart(request):
    cart, _ = Cart.objects.get_or_create(
        customer=request.user
    )

    items = cart.items.select_related('product').all()
    total_price = Decimal('0.00')

    for item in items:
        if item.product:
            item.item_subtotal = (
                item.product.price * item.quantity
            )
            total_price += item.item_subtotal
        else:
            item.item_subtotal = Decimal('0.00')

    context = {
        'cart': cart,
        'items': items,
        'total_price': total_price,
    }

    return render(request, 'cart.html', context)


@login_required
def checkout_view(request):
    # Ստանում ենք օգտատիրոջ զամբյուղը
    try:
        cart = Cart.objects.get(customer=request.user)
    except Cart.DoesNotExist:
        messages.error(request, "Զամբյուղը գոյություն չունի:")
        return redirect('main')

    items = cart.items.filter(product__isnull=False)

    # Եթե զամբյուղը դատարկ է
    if not items.exists():
        messages.warning(request, "Ձեր զամբյուղը դատարկ է:")
        return redirect('cart')

    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        location = request.POST.get('location')
        phone = request.POST.get('phone')
        comment = request.POST.get('comment', '')
        payment_method = request.POST.get('payment_method')

        if not all([name, surname, location, phone, payment_method]):
            messages.error(request, "Խնդրում ենք լրացնել բոլոր պարտադիր դաշտերը:")
            return render(request, 'checkout.html', {'cart': cart, 'items': items})

        # Տրանզակցիայով ստեղծում ենք Order-ը և OrderItem-ները, ապա մաքրում Cart-ը
        try:
            with transaction.atomic():
                order = Order.objects.create(
                    customer=request.user,
                    name=name,
                    surname=surname,
                    location=location,
                    phone=phone,
                    comment=comment,
                    payment_method=payment_method,
                    status=Order.Status.NEW,
                )

                for item in items:
                    current_price = item.product.price if item.product else Decimal('0.00')
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        price=current_price,
                        quantity=item.quantity
                    )

                # Մաքրում ենք զամբյուղի ապրանքները
                cart.items.all().delete()

                messages.success(request, f"Պատվեր #{order.id}-ը հաջողությամբ ձևակերպվեց:")
                return redirect('main')

        except Exception as e:
            messages.error(request, f"Պատվերը ձևակերպելիս տեղի ունեցավ սխալ: {str(e)}")

    return render(request, 'checkout.html', {
        'cart': cart,
        'items': items
    })

