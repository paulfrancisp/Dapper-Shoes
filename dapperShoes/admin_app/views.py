from django.shortcuts import render


from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import cache_control
from django.http import JsonResponse
from django.db.models import Q, Sum, Count
# from order.forms import OrderStatusForm
# from admin_side.models import User
from django.contrib import messages
# from order.models import Order,OrderProduct,Payment
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import ExtractMonth,ExtractWeekDay,ExtractYear
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



# Create your views here.
def admin_logout(request):
    logout(request) 
    return render(request,'admin_side/page-account-login.html')

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



# #users_list
# def admin_users_list(request):

#     return render(request,'admin_side/page-users-list.html')





def admin_dashboard(request):
    return render(request,'admin_side/page-admin-dashboard.html')

def admin_products_list(request):
    return render(request,'admin_side/page-products-list.html')

def admin_orders(request):
    return render(request,'admin_side/page-orders-1.html')

def admin_add_products(request):
    return render(request,'admin_side/page-add-product.html')



