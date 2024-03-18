from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import never_cache
from django.contrib import messages
from order.models import *
from account.models import *
from django.shortcuts import get_object_or_404
from django.urls import reverse

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
    order_list = Order.objects.all().order_by("-created_at")
    # order_product = OrderProduct.objects.filter(order=order_list)

    context = {
        "order_lists":order_list,
        # "order_product":order_product
    }
    return render(request,'admin_side/Week_2/page-orders-list.html',context)
# def admin_orders(request):
#     order_list = Order.objects.all().order_by("-created_at")
    
#     # Initialize an empty list to store OrderProduct objects
#     order_products = []
    
#     # Iterate over each Order object in order_list
#     for order in order_list:
#         # Retrieve OrderProduct objects related to the current Order object
#         order_product = OrderProduct.objects.filter(order=order)
        
#         # Append the retrieved OrderProduct objects to the list
#         order_products.extend(order_product)
    
#     context = {
#         "order_lists": order_list,
#         "order_products": order_products
#     }
#     return render(request, 'admin_side/Week_2/page-orders-list.html', context)




def admin_orders_detail(request,user_id):

    user = User.objects.get(id=user_id)
    orders = Order.objects.filter(user_id=user.id)
    print("Orders:", orders)  # Print the orders queryset
    if orders.exists():
        order = orders.first()
        print("First Order:", order)  # Print the first order instance
        print("Address:", order.first_name, order.last_name, order.address, order.town_city, order.state, order.zip_code)  # Print address details
    else:
        order = None

    # user = User.objects.get(id = user_id)
    # order = Order.objects.filter(user_id = user.id)

    orderproduct = OrderProduct.objects.filter(user__id = user.id).order_by("-created_at")
    
    total_user_orders = Order.objects.filter(user=user_id)
    print("total_user_orders",total_user_orders)
    
    # try:
    #     user_address = Address.objects.get(is_default = True, account = user)
    # except:
    #     user_address = None
    # print("user address:",user_address)
    # total_product_price = 0
    # grant_total = 0
    # discount = 0
    # for i in orders:
        # total_product_price = i.product_price
        # grant_total = i.grand_totol

    # discount = grant_total-total_product_price


    context = {
        "orders":orders,
        "order":order,
        "orderproduct":orderproduct,
        # "user_address":user_address,
        "user":user,
        # "discount":discount,
        # "grant_total":grant_total,
        # "total_product_price":total_product_price
    }


    return render(request,'admin_side/Week_2/order_details.html',context)


def change_order_status(request, order_id, status, user_id):
    order = get_object_or_404(OrderProduct, id=order_id)
    order.order_status = status
    order.save()
    print("user_id",user_id)
    
    # Redirect to some page after changing status
    return redirect(reverse('admin_app:admin_orders_detail', kwargs={'user_id': user_id}))
