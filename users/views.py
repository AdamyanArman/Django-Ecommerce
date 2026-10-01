from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Customer


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

        if Customer.objects.filter(phone=phone).exists():
            messages.error(request, "Այս հեռախոսահամարով արդեն գրանցված են")
            return render(request, "register.html")

        # Ստեղծում ենք հաճախորդին create_user-ի միջոցով (որպեսզի գաղտնաբառը հեշավորվի)
        customer = Customer.objects.create_user(
            phone=phone,
            username=phone,  # Օգտագործում ենք հեռախոսահամարը որպես username
            password=password
        )

        # Ավտոմատ մուտք ենք գործում գրանցվելուց հետո
        login(request, customer)

        messages.success(request, f"Բարի գալուստ, {customer.full_name or customer.phone}։ Գրանցումը հաջողվեց։")
        return redirect("main")  # Փոխիր քո գլխավոր էջի անունով

    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        phone = request.POST.get("phone", "").strip()
        password = request.POST.get("password", "")

        if not phone or not password:
            messages.error(request, "Լրացրեք բոլոր դաշտերը")
            return render(request, "login.html")

        # Authenticate-ը ստուգում է տվյալները (քանի որ USERNAME_FIELD-ը phone է)
        customer = authenticate(request, phone=phone, password=password)

        if customer is not None:
            if customer.is_active:
                login(request, customer)
                messages.success(request, f"Բարի վերադարձ, {customer.full_name or customer.phone}։")
                return redirect("main")
            else:
                messages.error(request, "Հաշիվը ակտիվ չէ")
        else:
            messages.error(request, "Սխալ հեռախոսահամար կամ գաղտնաբառ")

    return render(request, "login.html")


def logout_view(request):
    logout(request)  # Մաքրում է Django-ի հավաստագրման session-ը
    messages.success(request, "Դուք դուրս եկաք համակարգից")
    return redirect("login")