import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import *
from cart.models import *
from product_management.models import *
from django.contrib import messages
from .forms import OrderForm
from account.models import *
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
def place_order_cod(request, total=0, quantity=0):

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
        if cart_item.quantity <= cart_item.variant.stock:
            total += cart_item.variant.sale_price * cart_item.quantity
            quantity += cart_item.quantity
        else:
            messages.error(request,f"Insufficient quantity. Available quantity is {cart_item.variant.stock} units.")
            return redirect('cart_app:cart_list')

    # cart_items = CartItem.objects.filter(cart=cart)  #if any issue comes here use get() instead of filter here or in above orm query or add this query above cart= Cart.objects.get(user=current_user)
    # for cart_item in cart_items:
    #     total += (cart_item.variant.sale_price * cart_item.quantity)
    #     quantity += cart_item.quantity
    
    print('Outside if method POST')
    print('Request Method:', request.method)

    if request.method == 'POST':
        print('Inside if method POST')
        # form = OrderForm(request.POST)
        data_inst = json.loads(request.body)
        print(data_inst)
        # if form.is_valid():
        #     print('FORM is valid')
            #Store all billing info inside order table
            # if 'differentaddress' in request.POST:
            #     home_address = Address.objects.filter(user=current_user, is_default=True).first()
            #     form.instance.user = current_user
            #     form.instance.first_name = home_address.first_name
            #     form.instance.last_name = home_address.last_name
            #     form.instance.phone_number = home_address.phone_number
                # form.instance.email = home_address.email
            #     form.instance.town_city = home_address.town_city
            #     form.instance.address = home_address.address
            #     form.instance.state = home_address.state
            #     form.instance.zip_code = home_address.zip_code
            #     form.instance.order_total = total
            #     form.instance.ip = request.META.get('REMOTE_ADDR')
            #     order_number = data.generate_order_number()
            #     form.instance.order_number = order_number
            #     order = form.save()
            # else:
        data = Order()
        data.user = current_user
        print('cccccccccccc',current_user)
        # data.first_name = data_inst['first_name']
        data.first_name = data_inst.get('formData').get('first_name')
        data.last_name = data_inst.get('formData').get('last_name')
        data.phone_number = data_inst.get('formData').get('phone_number')
        data.address = data_inst.get('formData').get('address')
        data.town_city = data_inst.get('formData').get('town_city')
        data.state = data_inst.get('formData').get('state')
        data.zip_code = data_inst.get('formData').get('zip_code')
        selected_payment_method = data_inst.get('formData').get('selected_payment_method')
        print(selected_payment_method,'ppppppppppppppppppppppppppppppppppppp')

        data.order_total = total
        data.ip = request.META.get('REMOTE_ADDR')
        order_number = data.generate_order_number()
        data.order_number = order_number
        data.save()

        order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)

        # Get necessary instances
        if selected_payment_method == 'razorpay':
            client = razorpay.Client(auth=("rzp_test_qoXpACMLfXbWKp", "ydDrIJw9JIb3RhaMLHSsGvyi"))
            amount = int(total * 100)  # Amount in paisa
            order_data = {
                'amount': amount,
                'currency': 'INR',
                'receipt': 'order_rcptid_11',
            }
            razorpay_order = client.order.create(data=order_data)
            # order_id = razorpay_order['id']

            payment_methods_instance = PaymentMethod.objects.get(method_name="Razorpay")
            payment = Payment.objects.create(user=current_user,amount_paid=0,payment_id=razorpay_order['id'],payment_order_id=order.order_number,payment_status='PENDING',payment_method=payment_methods_instance)

            context = {
                    'order_id': razorpay_order['id'],
                    'amount': razorpay_order['amount'],
                    # 'currency': order['currency'],
                    # 'key_id': settings.RAZOR_PAY_KEY_ID
                }
            
            # order_id = razorpay_order.get('id')
            # return JsonResponse({'order_id': order_id}, status=200)
            return JsonResponse({'context': context}, status=200)

        
        elif selected_payment_method == 'cod':
            payment_methods_instance = PaymentMethod.objects.get(method_name="CASH ON DELIVERY")
            print(payment_methods_instance,'iiiiiiiiiiiiiiiiCASH ON DELIVERY')

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
                "success":True,
            }
            return JsonResponse({'message': 'Order placed successfully', 'context': context}, status=200)

            # return render(request,'user_side/Week 2/order-success.html',context)
            # else:
            #     print('FORM is Invalid')
            #     print(form.errors)
            #     return render(request, 'user_side/shop-checkout.html')  #, {'form': form}
    else:
        # If request method is not POST, redirect to the checkout page
        # return redirect('cart_app:checkout')
        return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def success_page(request):
    return render(request,"user_side/Week 2/order-success.html")



@csrf_exempt
def place_order_razpay(request):
    print('Outside place_order_razpay POST')
    if request.method == "POST":
        print('Inside place_order_razpay POST')
        try:
            payment_id        = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature         = request.POST.get('razorpay_signature', '')

            print('2255',payment_id,'2255',razorpay_order_id,'2255',signature)

            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            client = razorpay.Client(auth=("rzp_test_qoXpACMLfXbWKp", "ydDrIJw9JIb3RhaMLHSsGvyi"))  
            result = client.utility.verify_payment_signature(params_dict)
            
            if not result :
                print('Inside if in place_order_razpay POST')
                return redirect('order_app:paymentfailed',razorpay_order_id,payment_id,signature)
            else:
                print('Inside else in place_order_razpay POST')
                return redirect('order_app:order_success',razorpay_order_id,payment_id,signature)  #####Need to write view fn

        except Exception as e:
            # pass
            print('Exception:', str(e))
            return redirect('order_app:paymentfailed',razorpay_order_id,payment_id,signature)
    else:
        messages.error(request,"Payment is Faied, Try Again")
        return redirect('checkout_app:checkout')





# @login_required
def order_success(request, razorpay_order_id,payment_id,signature):

    payment = Payment.objects.get(payment_id=razorpay_order_id)         
    payment.payment_status = 'SUCCESS'
    # payment.payment_id = payment_id
    payment.payment_signature = signature
    payment.is_paid = True
    current_user = payment.user
    total = 0
    quantity = 0
    payment.save()

    print('order no test',razorpay_order_id)


    cart = Cart.objects.filter(user=current_user).first()
    if not cart:
        return redirect('shop_app:home')
    
    cart_items = cart.cartitem_set.all()
    for cart_item in cart_items:
        if cart_item.quantity <= cart_item.variant.stock:
            total += cart_item.variant.sale_price * cart_item.quantity
            quantity += cart_item.quantity
        else:
            messages.error(request,f"Insufficient quantity. Available quantity is {cart_item.variant.stock} units.")
            return redirect('cart_app:cart_list')
    
    order = Order.objects.get(user=current_user, is_ordered=False, order_number=payment.payment_order_id)


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
        # variantt = Product_variant.objects.filter(id=cart_item.variant.id)

        variant.stock -= cart_item.quantity
        variant.save()

    #Clearing the cart
    cart.cartitem_set.all().delete()    

    context = {
        "success":True,
    }
    # return JsonResponse({'message': 'Order placed successfully', 'context': context}, status=200)
    return redirect('order_app:success_page')




def paymentfailed(request, razorpay_order_id,payment_id,signature):
    payment = Payment.objects.get(payment_id=razorpay_order_id)         
    payment.payment_status = 'FAILED'
    # payment.payment_id = payment_id
    payment.payment_signature = signature
    payment.is_paid = False
    current_user = payment.user
    payment.save()

    print('order no test',razorpay_order_id)


    cart = Cart.objects.filter(user=current_user).first()
    if not cart:
        return redirect('shop_app:home')
    
    cart_items = cart.cartitem_set.all()
    # for cart_item in cart_items:
    #     if cart_item.quantity <= cart_item.variant.stock:
    #         total += cart_item.variant.sale_price * cart_item.quantity
    #         quantity += cart_item.quantity
    #     else:
    #         messages.error(request,f"Insufficient quantity. Available quantity is {cart_item.variant.stock} units.")
    #         return redirect('cart_app:cart_list')
    
    order = Order.objects.get(user=current_user, is_ordered=False, order_number=payment.payment_order_id)


    # Saving the payment and is_ordered values in Order table.
    order.payment = payment  
    order.is_ordered = False
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
    return render(request, 'user_side/Week 3/payment-failed.html')