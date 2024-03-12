from django.shortcuts import render, redirect
from .models import *
from cart.models import *
from django.contrib import messages

# Create your views here.
def place_order_cod(request):
    
    # user_id = request.user.id

    # # Get necessary instances
    # payment_methods_instance = PaymentMethod.objects.get(method_name="CASH ON DELIVERY")
    # user_instance = User.objects.get(id=user_id)

    # # address = Address.objects.get(is_default=True, account=user_instance)
    # cart_items = CartItem.objects.filter(user=user_instance, is_active=True)
    # for i in cart_items:
    #     if i.product.stock < 1:
    #         messages.error(request,"Product Variant is Out Of Stock")
    #         return redirect('checkout_app:checkout_payment')

    # total = 0
    # quantity = 0
    # total_with_orginal_price = 0

    # for cart_item in cart_items:
    #     total += cart_item.subtotal()
    #     total_with_orginal_price += (cart_item.product.max_price * cart_item.quantity)
    #     quantity += cart_item.quantity

    # discount = total_with_orginal_price - total

    # # Create ShippingAddress instance
    # address1 =[address.get_address_name(),address.street_address, address.town_city, address.state, address.state, address.country_region,address.zip_code,address.phone_number]
    

    # # Create Payment instance
    # payment = Payment.objects.create(user=user_instance,payment_method=payment_methods_instance,amount_paid=0,payment_status='PENDING')
    
    
    # draft_order= Order.objects.create(
    #         user=user_instance,
    #         shipping_address=address1,
    #         order_total=total,
    #         is_ordered  = True,
    #         payment = payment,
    #     )
    # for cart_item in cart_items:
    #     product= cart_item.product
    #     product.stock -= cart_item.quantity
    #     product.save()
        
    # for cart_item in cart_items:
    #         OrderProduct.objects.create(
    #             order           = draft_order,
    #             user            = user_instance,
    #             product_variant = cart_item.product.get_product_name(),
    #             product_id      = cart_item.product.id,
    #             quantity        = cart_item.quantity,
    #             product_price   = float(cart_item.product.sale_price),
    #             images          = cart_item.product.thumbnail_image,
    #             ordered         = True,
    #         )
    #         print(cart_item.product.get_product_name())

    # cart_items.delete()    
    
    # order_dtails=OrderProduct.objects.filter(user=user_instance,order=draft_order)
    # for i in order_dtails:
    #     address=i.order.shipping_address
    
    # print("address: ",address)

    # cleaned_string = address.replace('[', '').replace(']', '')

    # # Split the string by comma and remove empty strings and 'None' values
    # split_data = [item.strip() for item in cleaned_string.split(',') if item.strip() != '' and item.strip() != 'None']

    # # Remove single quotes from each item
    # cleaned_data = [item.replace("'", "") for item in split_data]
    # print(cleaned_data)
    # str1 = str()
    # k = 1
    # for i in cleaned_data:
    #     if k == 1:
    #         str1+=i
    #     else:
    #         str1+=" "+i
    #     k = 2

    # str1 = str1.replace(","," ")
    # print(str1)
         

    # draft_order.shipping_address = str1
    # draft_order.save()
    # print('order_dtails: ',draft_order)
    # print("address: ",str1)
    # print('order_product:  ',order_dtails)
    
    # context = {
    #             'order_dtails' : draft_order,
    #             'address' : str1,
    #             'order_product' : order_dtails,
    #             'grand_total':total,
    #             'total_with_orginal_price':total_with_orginal_price,
    #             'discount':discount,
    #             }

    return render(request,'user_side/Week 2/order-success.html') #,context