from django.shortcuts import render, redirect, get_object_or_404
from product_management.models import *
from .models import *
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from order.models import *

# Create your views here.
@login_required(login_url='user_app:user_login')
def account(request):


    user = User.objects.get(id = request.user.id)
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()

    context = {
        'orders_count': orders_count,
        'user':user,
    }


    return render(request,'user_side/base-account.html', context)



def account_my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders' : orders,
    }

    return render(request,'user_side/page-account/account-my-orders.html',context)



def account_edit_profile(request):
    return render(request,'user_side/page-account/account-edit-profile.html')

def account_change_password(request):
    return render(request,'user_side/page-account/account-change-password.html')