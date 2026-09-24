from django.shortcuts import render, redirect


# Create your views here.
def main(request):
    customer_phone=request.session.get('customer_phone')

    context={
        'phone': customer_phone
    }

    if customer_phone:
        return render(request, 'main.html', context)
    else: return redirect('login')