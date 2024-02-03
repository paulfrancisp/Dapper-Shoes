from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache,cache_control
from django.contrib import messages
from django.core.mail import send_mail
import random 
from django.http import HttpResponse


# Create your views here.
# @cache_control(no_cache=True, must_revalidate=True, no_store=True) 
@never_cache
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)  
    return render(request,'user_side/index.html')


# @cache_control(no_cache=True, must_revalidate=True, no_store=True) 
@never_cache
def user_signup(request):          
    if request.method == 'POST':
        uname = request.POST.get("username")
        email = request.POST.get("email")
        passw = request.POST.get("password")
        confpassw = request.POST.get("conf_password")

        if User.objects.filter(username = uname).exists():
            messages.warning(request,'User already exists')
            return redirect('user_app:user_signup')

        if User.objects.filter(email = email).exists():
            messages.warning(request,'Email already exists')
            return redirect('user_app:user_signup')

        print('Password before',passw)
        if ' ' in passw:
            messages.warning(request,'Password cannot have whitespaces')
            return redirect('user_app:user_signup')
        print('Password after',passw)

        if not email or '@' not in email:
            messages.info(request,'Email is not in correct format')
            return redirect('user_app:user_signup')

        if passw != confpassw:
            messages.warning(request,'Password is incorrect')
            return redirect('user_app:user_signup')

        if len(passw) < 8:
            messages.info(request,'Password should be of 8 character')
            return redirect('user_app:user_signup')

            
        request.session['username'] = uname
        request.session['password'] = passw
        request.session['email'] = email

        otp_value = random.randint(100000, 999999)
        request.session['otp_session'] = otp_value
        # request.session.modified = True 
        request.session.set_expiry(300)


        #send_mail( 'Subject', 'Message body', 'Senders email', ['Recipients email'], Fail silently)
        send_mail(
            'OTP verification from Dapper Shoes',
            f" Dear User,\n\n Your One-Time Password (OTP) for verification is:{request.session['otp_session']}. \n\nPlease use above OPT to complete your signup to Dapper Shoes website.",
            'dappershoes.official@gmail.com',
            [request.session['email']],
            fail_silently=False
        )

        return render(request,'user_side/otp.html',{'email':email})
    return render(request,'user_side/page-signup.html')

# @cache_control(no_cache=True, must_revalidate=True, no_store=True) 
@never_cache
def user_otp_verification(request):
    if request.method == "POST":
        otp_entered = request.POST.get('otp_entered')
        otp_session =request.session.get('otp_session')
        uname = request.session.get('username')
        email_session = request.session.get('email')
        passw = request.session.get('password')

        if str(otp_entered) == str(otp_session):
            customer = User.objects.create_user(username = uname, email = email_session, password = passw )
            customer.save()
            customer = authenticate(request, username = uname, password=passw)     #authenticate(email = email_session, password=passw)
            if customer is not None:
                login(request,customer)
                return redirect('user_app:user_index')
        else:
            messages.error(request,'Invalid OTP')
            return redirect('user_app:user-otp-verification') 
    return render(request,'user_side/otp.html',{'email': email_session})




# @cache_control(no_cache=True, must_revalidate=True, no_store=True) 
@never_cache
def user_login(request):
        # if request.user.is_authenticated:       
        #     return redirect('user_index')   
        if request.method=='POST':                  
            username=request.POST.get('username')   
            pass1=request.POST.get('pass')          
            user=authenticate(request,username=username,password=pass1)  

            if user is not None:
                login(request,user)                                      
                return redirect('user_app:user_index')                                  
            
            else:                                                        
                return HttpResponse('Username or password is incorrect !!!')  
        return render(request,'user_side/page-login.html')


# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def user_index(request):         
    if request.user.is_authenticated:       
        # if request.user.is_superuser:
        #     return redirect("admin_dashboard")
        return render(request,'user_side/index.html')  
    return redirect('user_login') 








#######################################################################
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