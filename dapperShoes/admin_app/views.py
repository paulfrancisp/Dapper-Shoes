from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import never_cache
from django.contrib import messages




# Create your views here.
@never_cache
def admin_logout(request):
    logout(request) 
    return render(request,'admin_side/page-account-login.html')

@never_cache
def admin_login(request):
    if request.method == 'POST':
        # email = request.POST['email']
        uname = request.POST.get('username')
        password = request.POST.get('password')
        admin = authenticate(request,username=uname, password=password)
        print(admin)
        if admin is not None and admin.is_superuser:
            login(request,admin)
            return redirect('admin_app:admin_dashboard')  
        else:
            messages.warning(request,'wrong credentials !')
            return redirect('admin_app:admin_login')
        
    return render(request,'admin_side/page-account-login.html')


@never_cache
def admin_dashboard(request):
    return render(request,'admin_side/page-admin-dashboard.html')

@never_cache
def admin_orders(request):
    return render(request,'admin_side/page-orders-1.html')


