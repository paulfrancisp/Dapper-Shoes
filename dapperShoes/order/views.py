import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import *
from cart.models import *
from product_management.models import *
from django.contrib import messages
from .forms import OrderForm
from account.models import *
from wallet.models import *
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
def place_order_cod(request, total=0, quantity=0):

    current_user = request.user

    cart = Cart.objects.filter(user=current_user).first()
    if not cart:
        return redirect('shop_app:home')
    
    cart_items = cart.cartitem_set.all()
    for cart_item in cart_items:
        if cart_item.quantity <= cart_item.variant.stock:
            total += cart_item.variant.calculate_discounted_price() * cart_item.quantity
            quantity += cart_item.quantity
        else:
            messages.error(request,f"Insufficient quantity. Available quantity is {cart_item.variant.stock} units.")
            return redirect('cart_app:cart_list')
    
    print('.............total.............',total)
    if cart.coupon_applied:
        total  -= cart.coupon_discount

    print('.............total.............',total)
    
    print('Outside if method POST')
    print('Request Method:', request.method)

    if request.method == 'POST':
        print('Inside if method POST')
        # form = OrderForm(request.POST)
        data_inst = json.loads(request.body)
        print(data_inst)

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
            print('Amount inside razorpay total',total,' amount in paise ',amount)
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
            
            return JsonResponse({'context': context}, status=200)

        elif selected_payment_method == 'wallet':
            payment_methods_instance = PaymentMethod.objects.get(method_name="Wallet")   
            wallet = Wallet.objects.get(user = current_user)

            if total<= wallet.balance: 
                payment = Payment.objects.create(user=current_user,amount_paid=total,payment_status='SUCCESS',payment_method=payment_methods_instance,payment_order_id=order.order_number)
                order.payment = payment   
                order.is_ordered = True
                if cart.coupon_applied:
                    order.coupon_applied = cart.coupon_applied
                    order.coupon_discount = cart.coupon_discount
                    order.order_total = cart.total_after_discount
                else:
                    order.order_total = total
                order.save()

                if cart.coupon_applied:
                    coupon = Coupon.objects.get(id=cart.coupon_applied.id)
                    coupon.total_coupons -= 1
                    coupon.save()

                    user_coupon = UserCoupon.objects.get(coupon_id=coupon.id,user_id=current_user)
                    user_coupon.usage_count +=1
                    user_coupon.save()

                
                
                wallet_transaction = WalletTransaction.objects.create(
                    wallet = wallet,
                    transaction_type = "DEBIT",
                    amount = total,
                    wallet_payment_id = order.order_number,
                )
                wallet.balance -= total
                wallet.save()
                wallet_transaction.save()

    
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
                    orderproduct.product_price = cart_item.variant.calculate_discounted_price()
                    orderproduct.ordered = True
                    orderproduct.total = total
                    orderproduct.save()


                    #Reduce quantity of sold products
                    variant = Product_variant.objects.get(id=cart_item.variant.id)
                    variant.stock -= cart_item.quantity
                    variant.save()

                #Clearing the cart
                cart.cartitem_set.all().delete()    

                context = {
                    "success":True,
                }
                return JsonResponse({'message': 'Order placed successfully', 'context': context}, status=200)
            else:
                messages.warning(request,"Insufficent wallet balance!! Use other payment methods.") 
                return JsonResponse({'message': 'Insufficent wallet balance'}, status=400)
        
        elif selected_payment_method == 'cod':
            if total<= 1000: 
                payment_methods_instance = PaymentMethod.objects.get(method_name="CASH ON DELIVERY")
                print(payment_methods_instance,'iiiiiiiiiiiiiiiiCASH ON DELIVERY')

                # Create Payment instance
                payment = Payment.objects.create(user=current_user,amount_paid=0,payment_status='PENDING',payment_method=payment_methods_instance,payment_order_id=order.order_number)
                # print(payment)

                # Saving the payment and is_ordered values in Order table.
                order.payment = payment   #### ISSUE here
                order.is_ordered = True
                if cart.coupon_applied:
                    order.coupon_applied = cart.coupon_applied
                    order.coupon_discount = cart.coupon_discount
                    order.order_total = cart.total_after_discount
                else:
                    order.order_total = total
                order.save()

                if cart.coupon_applied:
                    coupon = Coupon.objects.get(id=cart.coupon_applied.id)
                    coupon.total_coupons -= 1
                    coupon.save()

                    user_coupon = UserCoupon.objects.get(coupon_id=coupon.id,user_id=current_user)
                    user_coupon.usage_count +=1
                    user_coupon.save()

                    # cart.coupon_applied = None
                    # cart.coupon_discount = 0.00
                    # cart.total_after_discount = 0.00
                    # cart.save()

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
                    orderproduct.product_price = cart_item.variant.calculate_discounted_price()
                    orderproduct.ordered = True
                    orderproduct.total = total
                    orderproduct.save()


                    #Reduce quantity of sold products
                    variant = Product_variant.objects.get(id=cart_item.variant.id)
                    variant.stock -= cart_item.quantity
                    variant.save()

                #Clearing the cart
                cart.cartitem_set.all().delete()    

                context = {
                    "success":True,
                }
                return JsonResponse({'message': 'Order placed successfully', 'context': context}, status=200)
            else:
                messages.warning(request,"Cash on delivery is only available for payments less than ₹1000") 
                return JsonResponse({'message': 'Cash on delivery is only available for payments less than ₹1000'}, status=400)
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
                return redirect('order_app:paymentfailed')
            else:
                print('Inside else in place_order_razpay POST')
                return redirect('order_app:order_success',razorpay_order_id,payment_id,signature)  #####Need to write view fn

        except Exception as e:
            # pass
            print('Exception:', str(e))
            # print('qqqqqqq',payment_id,'qqqqqqqqqqqq',razorpay_order_id,'qqqqqqq',signature)
            return redirect('order_app:paymentfailed')
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
            total += cart_item.variant.calculate_discounted_price() * cart_item.quantity
            quantity += cart_item.quantity
        else:
            messages.error(request,f"Insufficient quantity. Available quantity is {cart_item.variant.stock} units.")
            return redirect('cart_app:cart_list')
    
    if cart.coupon_applied:
        total  -= cart.coupon_discount
    
    order = Order.objects.get(user=current_user, is_ordered=False, order_number=payment.payment_order_id)


    # Saving the payment and is_ordered values in Order table.
    order.payment = payment   
    order.is_ordered = True
    if cart.coupon_applied:
        order.coupon_applied = cart.coupon_applied
        order.coupon_discount = cart.coupon_discount
        order.order_total = cart.total_after_discount
    else:
        order.order_total = total
    order.save()

    if cart.coupon_applied:
        coupon = Coupon.objects.get(id=cart.coupon_applied.id)
        coupon.total_coupons -= 1
        coupon.save()

        user_coupon = UserCoupon.objects.get(coupon_id=coupon.id,user_id=current_user)
        user_coupon.usage_count +=1
        user_coupon.save()
    


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
        orderproduct.product_price = cart_item.variant.calculate_discounted_price()
        orderproduct.ordered = True
        orderproduct.total = total
        orderproduct.save()


        #Reduce quantity of sold products
        variant = Product_variant.objects.get(id=cart_item.variant.id)
        variant.stock -= cart_item.quantity
        variant.save()

    #Clearing the cart
    cart.cartitem_set.all().delete()    

    context = {
        "success":True,
    }
    # return JsonResponse({'message': 'Order placed successfully', 'context': context}, status=200)
    return redirect('order_app:success_page')




def paymentfailed(request):   #, razorpay_order_id,payment_id,signature

    current_user = request.user
    total = 0
    quantity = 0

    payment_method = PaymentMethod.objects.get(method_name = "Razorpay")
    order = Order.objects.filter(user=current_user, is_ordered=False).order_by("-id").first()  
    order_prod = OrderProduct.objects.filter(order=order)

    # payment = Payment.objects.create(
    #     user = current_user,
    #     payment_status = 'FAILED',
    #     payment_method = payment_method,
    #     payment_order_id = order.order_number,
    #     amount_paid = 0,
    #     is_paid = False,
    # )

    payment = Payment.objects.get(payment_order_id=order.order_number)
    payment.payment_status = "FAILED"
    payment.save()


    cart = Cart.objects.filter(user=current_user).first()
    if not cart:
        return redirect('shop_app:home')
    
    cart_items = cart.cartitem_set.all()
    for cart_item in cart_items:
        if cart_item.quantity <= cart_item.variant.stock:
            total += cart_item.variant.calculate_discounted_price() * cart_item.quantity
            quantity += cart_item.quantity
        else:
            # messages.error(request,f"Insufficient quantity. Available quantity is {cart_item.variant.stock} units.")
            return redirect('cart_app:cart_list')
    
    if cart.coupon_applied:
        total  -= cart.coupon_discount

    # Saving the payment and is_ordered values in Order table.
    
    order.payment = payment
    order.order_status = 'Pending Payment'
    if cart.coupon_applied:
        order.coupon_applied = cart.coupon_applied
        order.coupon_discount = cart.coupon_discount
        order.order_total = cart.total_after_discount
    else:
        order.order_total = total
    order.save()

    if cart.coupon_applied:
        coupon = Coupon.objects.get(id=cart.coupon_applied.id)
        coupon.total_coupons -= 1
        coupon.save()

        user_coupon = UserCoupon.objects.get(coupon_id=coupon.id,user_id=current_user)
        user_coupon.usage_count +=1
        user_coupon.save()
    
    # order = Order.objects.filter(user=current_user, is_ordered=False).first()  
    # # Saving the payment and is_ordered values in Order table.
    # order.payment = payment
    # order.save()


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
        orderproduct.product_price = cart_item.variant.calculate_discounted_price()
        orderproduct.ordered = True
        orderproduct.total = total
        orderproduct.order_status = 'Pending Payment'
        orderproduct.save()
    
    #Clearing the cart
    cart.cartitem_set.all().delete()


    return render(request, 'user_side/Week 3/payment-failed.html')


