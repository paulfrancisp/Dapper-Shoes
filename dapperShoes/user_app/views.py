from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache,cache_control
from django.contrib import messages
from django.core.mail import send_mail
import random 
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from account.models import *
# from cart.models import *
# from cart.views import _cart_id


# Create your views here.
# @cache_control(no_cache=True, must_revalidate=True, no_store=True) 
@never_cache
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)  
    return redirect('shop_app:index')


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
        request.session['email_session'] = email
        print('Email in signup111',email)
        print('Email in signup222',request.session['email_session'])

        return redirect('user_app:user_send_otp')
    return render(request,'user_side/page-signup.html')



@never_cache
def user_send_otp(request):            
    otp_value = random.randint(100000, 999999)
    request.session['otp_session'] = otp_value
    request.session.set_expiry(300)
    
    # Assign email session before sending the email
    email = request.session['email_session']
    
    print('Email in session in user_send_otp()', email)
    
    send_mail(
        'OTP verification from Dapper Shoes',
        f"Dear User,\n\nYour One-Time Password (OTP) for verification is: {request.session['otp_session']}. \n\nPlease use the above OTP to complete your signup to Dapper Shoes website.",
        'dappershoes.official@gmail.com',
        [request.session['email_session']],
        fail_silently=False
    )
    
    request.session['email_session'] = email
    print('Email in session in user_send_otp()11111111111111111', request.session['email_session'])
    return render(request, 'user_side/otp.html', {'email': email})



@never_cache
def user_otp_verification(request):

    uname = request.session.get('username')
    email_session = request.session.get('email_session')
    passw = request.session.get('password')

    if request.method == "POST":
        otp_entered = request.POST.get('otp_entered')
        otp_session =request.session.get('otp_session')

        # Check if the username already exists
        existing_user = User.objects.filter(username=uname).first()
        if existing_user:
            # User exists, update the password
            existing_user.password = make_password(passw)
            existing_user.save()
            return redirect('user_app:user_login')

        elif str(otp_entered) == str(otp_session):
            print('Email in session in user_otp_verification()',email_session)
            customer = User.objects.create_user(username = uname, email = email_session, password = passw ) #if create() is used then password won't be hashed it needs to be hashed seperately.
            customer.save()
            # address = Address.objects.create(user=customer,)
            # address.save()
            customer = authenticate(request, username = uname, password=passw)     #authenticate(email = email_session, password=passw)
            
            if customer is not None:
                login(request,customer)
                return redirect('shop_app:index')
            
        else:
            messages.error(request,'Invalid OTP. Please enter again.')
            return redirect('user_app:user_otp_verification') 
        
        
    return render(request,'user_side/otp.html',{'email': email_session})
    


# @cache_control(no_cache=True, must_revalidate=True, no_store=True) 
@never_cache
def user_login(request):
        if request.user.is_authenticated:       
            return redirect('shop_app:index')
        if request.method=='POST':                  
            username=request.POST.get('username')   
            pass1=request.POST.get('pass')          
            user=authenticate(request,username=username,password=pass1)  

            if user is not None:
                # try:
                #     cart=Cart.objects.get(cart_id=_cart_id(request))  
                #     is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                #     print(is_cart_item_exists)

                #     if  is_cart_item_exists:
                #         cart_item = CartItem.objects.filter(cart=cart)
                #         print(cart_item)

                #         for item in cart_item:
                #             item.user = user
                #             item.save()
                # except:
                #     print('Entering inside except block')
                #     pass    
                
                login(request,user)                                      
                return redirect('shop_app:index')                                  
            else:      
                messages.error(request,"Invalid credentials!!")                                                  
                return redirect('user_app:user_login')  
        return render(request,'user_side/page-login.html')


@never_cache
def forgot_password(request):
    if request.method=='POST':
        email = request.POST.get("email")
        uname = request.POST.get("username")
        passw = request.POST.get("new_password")
        
        request.session['username'] = uname
        request.session['password'] = passw
        request.session['email_session'] = email

        if User.objects.filter(Q(email=email) | Q(username=uname)).exists() :
            return redirect('user_app:user_send_otp')
        else:
            messages.warning(request,"Email not found!!")       
    return render(request,'user_side/forgot_password.html')


