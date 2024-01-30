from django.shortcuts import render


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache,cache_control
from django.contrib import messages
from django.http import JsonResponse

from django.core.mail import send_mail
import random 
from django.contrib.auth.hashers import check_password
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse



# Create your views here.
def user_login(request):
    return render(request,'user_side/page-login.html')

def user_signup(request):
    return render(request,'user_side/page-signup.html')

def user_logout(request):
    return render(request,'user_side/index.html')

def user_otp_verification(request):
    # if request.method == "POST":
    #     otp = request.POST.get('enteredotp')
    #     storedotp=request.session['storedotp']
    #     storedemail = request.session['storedemail']

    #     if otp == storedotp:
    #         user = User.objects.get(email=storedemail)
    #         user.is_active = True
    #         user.save()
    #         subject = "Successful Login"
    #         sender_mail = "noreply@dappershoes.com"
    #         message = "Dear User,\n\nYour login to Dapper Shoes website was successful.\n\nThank you for choosing Dapper Shoes."

    #         send_mail(subject, message, sender_mail,[storedemail])
    #         login(request,user)
    #         return redirect ('home')
    #     else:
    #         messages.error(request,'Wrong Entry')
    #     context = {'email': storedemail}
    return render(request,'user_side/otp.html')#,context




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