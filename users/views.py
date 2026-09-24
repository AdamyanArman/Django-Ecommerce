from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import User


# Create your views here.


def register_view(request):
    if request.method == "POST":
        phone = request.POST.get("phone", "").strip()
        password = request.POST.get("password", "")
        password2 = request.POST.get("password2", "")

        # Ստուգումներ
        if not phone:
            messages.error(request, "Հեռախոսահամարը պարտադիր է")
            return render(request, "register.html")

        if not password or len(password) < 6:
            messages.error(request, "Գաղտնաբառը պետք է լինի առնվազն 6 նիշ")
            return render(request, "register.html")

        if password != password2:
            messages.error(request, "Գաղտնաբառերը չեն համընկնում")
            return render(request, "register.html")

        if User.objects.filter(phone=phone).exists():
            messages.error(request, "Այս հեռախոսահամարով արդեն գրանցված են")
            return render(request, "register.html")

        # Ստեղծում ենք հաճախորդին
        customer = User(
            phone=phone,
        )
        customer.set_password(password)  # գաղտնաբառը hash ենք անում
        #customer.last_login = timezone.now()
        #customer.save(update_fields=["last_login"])
        request.session["customer_id"] = customer.id
        request.session["customer_phone"] = customer.phone

        messages.success(request, f"Բարի գալուստ, {customer.full_name or customer.phone}։")
        customer.save()

        messages.success(request, "Գրանցումը հաջողվեց։ Կարող եք մուտք գործել։")
        return redirect("main")  # փոխիր քո գլխավոր էջի անունով
        return redirect("users:login")

    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        phone = request.POST.get("phone", "").strip()
        password = request.POST.get("password", "")

        print('customer_phone: '+phone)
        print('customer_password: '+password )

        if not phone or not password:
            messages.error(request, "Լրացրեք բոլոր դաշտերը")
            return render(request, "login.html")

        try:
            customer = User.objects.get(phone=phone)
            print('successful login!')
            if customer.check_password(password) and customer.is_active:
                # Մուտքը հաջողվեց
                #customer.last_login = timezone.now()
                #customer.save(update_fields=["last_login"])

                # Session-ում պահում ենք տվյալները
                request.session["customer_id"] = customer.id
                request.session["customer_phone"] = customer.phone

                print("it reeacheee!")

                messages.success(request, f"Բարի գալուստ, {customer.full_name or customer.phone}։")
                #return redirect("main")  # փոխիր քո գլխավոր էջի անունով
                return render(request, 'main.html')
            else:
                messages.error(request, "Սխալ գաղտնաբառ կամ հաշիվը ակտիվ չէ")

        except User.DoesNotExist:
            messages.error(request, "Այս հեռախոսահամարով հաճախորդ չի գտնվել")

    return render(request, "login.html")


def logout_view(request):
    request.session.flush()  # մաքրում ենք ամբողջ session-ը
    messages.success(request, "Դուք դուրս եկաք համակարգից")
    return redirect("login")