from django.shortcuts import render, redirect
from .models import *
from cart.models import *
from product_management.models import *
from django.contrib import messages
from .forms import OrderForm

# Create your views here.
def place_order_cod(request, total=0, quantity=0):
    
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


    current_user = request.user

    #If cart count <= 0 then redirect to home page.
    # cart = Cart.objects.filter(user=current_user)
    # cart_count = cart.count()
    # if  cart_count <= 0:
    #     redirect(request,'shop_app:home')

    cart = Cart.objects.filter(user=current_user).first()
    if not cart:
        return redirect('shop_app:home')
    
    cart_items = cart.cartitem_set.all()
    for cart_item in cart_items:
        total += cart_item.variant.sale_price * cart_item.quantity
        quantity += cart_item.quantity

    # cart_items = CartItem.objects.filter(cart=cart)  #if any issue comes here use get() instead of filter here or in above orm query or add this query above cart= Cart.objects.get(user=current_user)
    # for cart_item in cart_items:
    #     total += (cart_item.variant.sale_price * cart_item.quantity)
    #     quantity += cart_item.quantity
    
    print('Outside if method POST')
    print('Request Method:', request.method)

    if request.method == 'POST':
        print('Inside if method POST')
        form = OrderForm(request.POST)
        if form.is_valid():
            print('FORM is valid')
            #Store all billing info inside order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone_number = form.cleaned_data['phone_number']
            data.email = form.cleaned_data['email']
            data.town_city = form.cleaned_data['town_city']
            data.address = form.cleaned_data['address']
            data.state = form.cleaned_data['state']
            # data.country_region = form.cleaned_data['country_region']
            data.zip_code = form.cleaned_data['zip_code']
            data.order_total = total
            data.ip = request.META.get('REMOTE_ADDR')
            order_number = data.generate_order_number()
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)

            # Get necessary instances
            payment_methods_instance = PaymentMethod.objects.get(method_name="CASH ON DELIVERY")
            print(payment_methods_instance)
            # Create Payment instance
            payment = Payment.objects.create(user=current_user,amount_paid=0,payment_status='PENDING',payment_method=payment_methods_instance)
            # print(payment)

            # Saving the payment and is_ordered values in Order table.
            order.payment = payment   #### ISSUE here
            order.is_ordered = True
            order.save()


            #Moving cart item to OrderProduct table.
            cart_items = cart.cartitem_set.all()
            for cart_item in cart_items:
                orderproduct = OrderProduct()
                orderproduct.order_id = order.id
                # orderproduct.payment = payment
                orderproduct.user_id = request.user.id
                orderproduct.variant_id = cart_item.variant.id
                orderproduct.product_variant = cart_item.variant.variant_name
                orderproduct.images = cart_item.variant.thumbnail_image
                orderproduct.quantity = cart_item.quantity
                orderproduct.product_price = cart_item.variant.sale_price
                orderproduct.ordered = True
                orderproduct.save()


                #Reduce quantity of sold products
                variant = Product_variant.objects.get(id=cart_item.variant.id)
                variantt = Product_variant.objects.filter(id=cart_item.variant.id)
                print(variant)
                print(variantt)
                variant.stock -= cart_item.quantity
                variant.save()

            #Clearing the cart
            cart.cartitem_set.all().delete()    

            context = {
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'payment' : payment,
            }

            return render(request,'user_side/Week 2/order-success.html',context)
        else:
            # If form is not valid, you may want to render the form again with errors
            print('FORM is Invalid')
            print(form.errors)
            return render(request, 'user_side/shop-checkout.html')  #, {'form': form}
    else:
        # If request method is not POST, redirect to the checkout page
        return redirect('cart_app:checkout')
