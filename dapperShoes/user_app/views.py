from django.shortcuts import render

# Create your views here.
def user_login(request):
    return render(request,'user_side/page-login.html')

def user_signup(request):
    return render(request,'user_side/page-signup.html')

def user_logout(request):
    return render(request,'user_side/index.html')


#####
def user_index(request):
    return render(request,'user_side/index.html')

def user_404(request):
    return render(request,'user_side/page-404.html')

def user_account(request):
    return render(request,'user_side/page-account.html')

def user_contact(request):
    return render(request,'user_side/page-contact.html')

def user_cart(request):
    return render(request,'user_side/shop-cart.html')

def user_checkout(request):
    return render(request,'user_side/shop-checkout.html')

def user_fullwidth(request):
    return render(request,'user_side/shop-fullwidth.html')

def user_product_full(request):
    return render(request,'user_side/shop-product-full.html')

def user_wishlist(request):
    return render(request,'user_side/shop-wishlist.html')

# def user_logout(request):
#     pass