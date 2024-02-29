from django.shortcuts import render

# Create your views here.
def cart(request):
    return render(request, 'user_side/shop-cart.html')