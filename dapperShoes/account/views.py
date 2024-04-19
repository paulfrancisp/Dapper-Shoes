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
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders' : orders,
    }

    return render(request,'user_side/page-account/account-my-orders.html',context)


@login_required(login_url='user_app:user_login')
def account_order_detail(request,order_id):

    order = Order.objects.get(id = order_id)

    order_products = OrderProduct.objects.filter(order=order)
    # print("product_details order",order.id)

    order_actual_total = 0
    for i in order_products:
        order_actual_total += i.product_price

    context = {
        'order_detail':order,
        'order_products':order_products,
        'order_actual_total':order_actual_total,
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
    order.order_status = ordered_product.order_status
    order.save()
    # print("ordered Products:  ",order_products)
    # print("order :",order)
    
    return redirect("account_app:account_order_detail", order_id=order.id)


def return_product(request,item_id):
    ordered_product = OrderProduct.objects.get(id = item_id)
    print('helloo',ordered_product)
    ordered_product.order_status = "Returned User"
    # ordered_product.total = 0
    ordered_product.save()
    ordered_product_quantity = ordered_product.quantity

    variant_id = ordered_product.variant_id
    product_variant = Product_variant.objects.get(id = variant_id)
    product_variant.stock += ordered_product_quantity
    product_variant.save()

    order = ordered_product.order

    if order.payment.payment_method:
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


    
    order_products = OrderProduct.objects.filter(order = order)
    order = Order.objects.get(id = order.id)
    order.order_status = ordered_product.order_status
    order.save()


    return redirect("account_app:account_order_detail", order_id=order.id)


@login_required(login_url='user_app:user_login')
def get_invoice(request,id):

    user_id = request.user.id
    user = User.objects.get(id = user_id)
    order_actual_total = 0
    order = Order.objects.get(id = id)
    order_products = OrderProduct.objects.filter(order = order)

    for i in order_products:
        order_actual_total += i.product_price

    context = {
        "user" : user,
        "order" : order,
        "order_products" : order_products,
        "order_actual_total":order_actual_total,
    }


    return render(request,"user_side/page-account/order_invoice.html",context)




#####################################################


def repay_payment(request,id):  

    current_user = request.user
    order = Order.objects.get(id=id)
    orderproducts = OrderProduct.objects.filter(order=order)

    payment_methods_instance = PaymentMethod.objects.get(method_name="Wallet")   
    wallet = Wallet.objects.get(user = current_user)

    if order.order_total<= wallet.balance:

        payment = Payment.objects.get(payment_order_id=order.order_number)
        payment.payment_status = "SUCCESS"
        payment.payment_method = payment_methods_instance
        payment.is_paid = True
        payment.amount_paid = order.order_total        
        payment.save()

        order.is_ordered = True
        order.order_status = "New"  #####
        # if cart.coupon_applied:   ##### do "git push origin master" was not able to push code on 12:56am 4/19/2024
        # coupon_applied            #####
        # coupon_discount
        order.save()
        for orderproduct in orderproducts:
            orderproduct.order_status = "New"
            orderproduct.ordered = True
            product = Product_variant.objects.get(variant_name__icontains = orderproduct.product_variant)
            product.stock -= orderproduct.quantity
            product.save()
            orderproduct.save()


        # if cart.coupon_applied:
        #     coupon = Coupon.objects.get(id=cart.coupon_applied.id)
        #     coupon.total_coupons -= 1
        #     coupon.save()

        #     user_coupon = UserCoupon.objects.get(coupon_id=coupon.id,user_id=current_user)
        #     user_coupon.usage_count +=1
        #     user_coupon.save()

        
        
        wallet_transaction = WalletTransaction.objects.create(
            wallet = wallet,
            transaction_type = "DEBIT",
            amount = order.order_total,
            wallet_payment_id = order.order_number,
        )
        wallet.balance -= order.order_total
        wallet.save()
        wallet_transaction.save()
  
        # return redirect('account_app:account_order_detail',order_id=order.id)
        return redirect('order_app:success_page')
    else:
        messages.warning(request,"Insufficent wallet balance!! Please refill your wallet.")
        return redirect('order_app:success_page')
