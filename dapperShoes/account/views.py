from django.shortcuts import render, redirect, get_object_or_404
from product_management.models import *
from .models import *
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from order.models import *
from django.contrib import messages
from django.contrib.auth.models import User
from wallet.models import *

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


@login_required(login_url='user_app:user_login')
def account_my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders' : orders,
    }

    return render(request,'user_side/page-account/account-my-orders.html',context)


@login_required(login_url='user_app:user_login')
def account_order_detail(request,order_id):

    order = Order.objects.get(id = order_id)

    order_products = OrderProduct.objects.filter(order=order)
    # print("product_details order",order.id)
    context = {
        'order_detail':order,
        'order_products':order_products,
    }

    return render(request,'user_side/page-account/account-order-detail.html',context)



# @login_required(login_url='user_app:user_login')
# def account_my_address(request):
#     return render(request,'user_side/page-account/account-my-address.html')


@login_required(login_url='user_app:user_login')
def account_change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        
        user = User.objects.get(username__exact=request.user.username)
        print(user)

        if ' ' in new_password:
            messages.warning(request,'Password cannot have whitespaces')
            return redirect('account_app:account_change_password')
        
        if len(new_password) < 8:
            messages.info(request,'Password should be of 8 character')
            return redirect('account_app:account_change_password')

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request,"Password updated successfully")
                return redirect("account_app:account_change_password")
            else:
                messages.error(request, 'Please enter the valid current password')
                return redirect("account_app:account_change_password")
        else:
            messages.error(request, 'Password and confirm password are not matching')
            return redirect("account_app:account_change_password")

    return render(request,'user_side/page-account/account-change-password.html')



# @login_required(login_url='user_app:user_login')
# def account_create_address(request):
#     print('outside POST')
#     if request.method == 'POST':
#         print('inside POST')
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         address_line = request.POST.get('address')
#         town_city = request.POST.get('town_city')
#         state = request.POST.get('state')
#         zip_code = request.POST.get('zip_code')
#         phone_number = request.POST.get('phone_number')

        
#         # Create a new Address object for the current user
#         address = Address.objects.create(user=request.user,first_name=first_name, last_name=last_name , address=address_line, town_city=town_city ,state=state, zip_code=zip_code, phone_number =phone_number)
#         address.save()

#         return render(request,'user_side/page-account/account-my-address.html')

    
#     # context = {
#     #     'product': product,
#     #     'categories' : categories,
#     #     'subcategory' : subcategory,
#     #     'brands' : brands,
#     # }

#     return render(request,'user_side/page-account/account-create-address.html')  #,context


@login_required(login_url='user_app:user_login')
def account_edit_address(request):
    current_user = request.user
    try:
        address = Address.objects.get(user=current_user)
    except Address.DoesNotExist:
        # Handle the case where the user doesn't have an address yet
        address = None

    user = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address_line = request.POST.get('address')
        town_city = request.POST.get('town_city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        phone_number = request.POST.get('phone_number')

        if address:  # Update existing address
            if any(field.strip() == '' for field in [first_name, last_name, address_line, town_city, state, zip_code, phone_number]):
                messages.warning(request, 'Avoid whitespaces. Please enter proper details!!')

                
            else:
                if first_name:
                    address.first_name = first_name
                if last_name:
                    address.last_name = last_name
                if address_line:
                    address.address = address_line
                if town_city:
                    address.town_city = town_city
                if state:
                    address.state = state
                if zip_code:
                    address.zip_code = zip_code
                if phone_number:
                    address.phone_number = phone_number
                address.save()
        else:  # Create a new address if one doesn't exist
            address = Address.objects.create(
                user=current_user,
                first_name=first_name,
                last_name=last_name,
                address=address_line,
                town_city=town_city,
                state=state,
                zip_code=zip_code,
                phone_number=phone_number
            )
            return redirect('account_app:account_edit_address')
    context = {
        'address': address,
        'user':user,
    }

    return render(request,'user_side/page-account/account-edit-address.html', context)





def cancel_product(request, item_id):
    ordered_product = OrderProduct.objects.get(id = item_id)
    ordered_product.order_status = "Cancelled User"
    # ordered_product.total = 0
    ordered_product.save()
    ordered_product_quantity = ordered_product.quantity

    variant_id = ordered_product.variant_id
    product_variant = Product_variant.objects.get(id = variant_id)
    product_variant.stock += ordered_product_quantity
    product_variant.save()

    order = ordered_product.order
    print('1111111111111',order.payment.payment_method)
    order_products = OrderProduct.objects.filter(order = order)

    if str(order.payment.payment_method) != 'CASH ON DELIVERY':
        print('inside if satement',order.payment.payment_method )
        user_wallet = Wallet.objects.get(user=request.user)
        wallet_transaction = WalletTransaction.objects.filter(wallet=user_wallet).order_by('-id')
        wallet_transaction = WalletTransaction.objects.create(
            wallet = user_wallet,
            transaction_type = "CREDIT",
            amount = ordered_product.total,
            wallet_payment_id = order.order_number,
        )
        user_wallet.balance += ordered_product.total
        user_wallet.save()
        wallet_transaction.save()

    order = Order.objects.get(id = order.id)
    order.order_total -= ordered_product.total

    # print("ordered_product.grand_totol:  ",ordered_product.grand_totol)
    # print("order.order_total:  ",order.order_total)

    order.save()
    # print("ordered Products:  ",order_products)
    # print("order :",order)
    
    return redirect("account_app:account_order_detail", order_id=order.id)


def return_product(request,item_id):
    ordered_product = OrderProduct.objects.get(id = item_id)
    print('helloo',ordered_product)
    ordered_product.order_status = "Returned User"
    ordered_product.total = 0
    ordered_product.save()
    ordered_product_quantity = ordered_product.quantity

    variant_id = ordered_product.variant_id
    product_variant = Product_variant.objects.get(id = variant_id)
    product_variant.stock += ordered_product_quantity
    product_variant.save()


    order = ordered_product.order
    order_products = OrderProduct.objects.filter(order = order)
    order = Order.objects.get(id = order.id)
    order.order_total -= ordered_product.total

    order.save()


    return redirect("account_app:account_order_detail", order_id=order.id)

