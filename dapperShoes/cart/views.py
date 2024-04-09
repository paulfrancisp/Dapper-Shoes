from django.shortcuts import render, redirect, get_object_or_404
from product_management.models import *
from .models import *
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from account.models import *
from wallet.models import *
import razorpay


# Create your views here.
# def _cart_id(request):
#     cart = request.session.session_key
#     print("already exit cart id: ",cart)
#     if not cart:
#         cart = request.session.create()
#         print("created cart Id: ",cart)
#     return cart

# def _cart_id(request):
#     current_user = request.user

#     # Check if the user is authenticated
#     try:
#         cart= Cart.objects.get(user=current_user)
#     except Cart.DoesNotExist:
#         # For anonymous users, use some other logic to identify the cart (if needed)
#         cart= Cart.objects.create(user=current_user)
#     return cart 

@login_required(login_url='user_app:user_login')
def add_cart(request, variant_id):
    current_user = request.user
    variant = Product_variant.objects.get(id=variant_id)
    try:
        cart= Cart.objects.get(user=current_user)
    except Cart.DoesNotExist:
        # For anonymous users, use some other logic to identify the cart (if needed)
        cart= Cart.objects.create(user=current_user)
    # try:
    #     cart = Cart.objects.get(id=_cart_id(request))
    # except Cart.DoesNotExist:
    #    pass
    # cart.save()

    try:
        cart_item = CartItem.objects.get(variant=variant , cart=cart) #,user = current_user
        if cart_item.quantity < variant.stock:
            cart_item.quantity +=1
            cart_item.save()
        else:
            messages.error(request,"No more stock available for this product")
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            variant=variant,
            cart=cart,
            quantity = 1,
            # user = current_user
        )
        cart_item.save()
    # return HttpResponse(cart_item.quantity)
    ## return redirect(reverse('store_app:product_detail', kwargs={'id': product.id}))
    # Instead of using reverse, you can directly use the URL
    return redirect('cart_app:cart_list')
    ## return render(request, 'user_side/shop-detail-product-page.html')


def cart_list(request, total=0, quantity=0, cart_items=None):

    current_user = request.user
    if current_user.is_authenticated:
        try:
            cart= Cart.objects.get(user=current_user)
        except Cart.DoesNotExist:
            # For anonymous users, use some other logic to identify the cart (if needed)
            cart= Cart.objects.create(user=current_user)


        
        cart_items = CartItem.objects.filter(cart=cart, is_active=True).order_by('id') #,user = current_user
        for cart_item in cart_items:
            total += (cart_item.variant.sale_price * cart_item.quantity)
            quantity += cart_item.quantity

        context={
            'total': total,
            'quantity' : quantity,
            'cart_items' : cart_items
        }
    else:
        context = {}
    
    return render(request, 'user_side/shop-cart.html', context)


def remove_cart(request, variant_id):
    current_user = request.user
    try:
        cart= Cart.objects.get(user=current_user)
    except Cart.DoesNotExist:
        # For anonymous users, use some other logic to identify the cart (if needed)
        # cart= Cart.objects.create(user=current_user)
        pass

    variant = get_object_or_404(Product_variant, id=variant_id)
    cart_item = CartItem.objects.get(variant=variant, cart=cart)
    if cart_item.quantity>1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_app:cart_list')


def remove_cart_item(request, variant_id):
    current_user = request.user
    try:
        cart= Cart.objects.get(user=current_user)
    except Cart.DoesNotExist:
        # For anonymous users, use some other logic to identify the cart (if needed)
        # cart= Cart.objects.create(user=current_user)
        pass

    variant = get_object_or_404(Product_variant, id=variant_id)
    cart_item = CartItem.objects.get(variant=variant, cart=cart)
    cart_item.delete()
    return redirect('cart_app:cart_list')



def checkout(request, total=0, quantity=0, cart_items=None):
    current_user = request.user
    
    try:
        cart= Cart.objects.get(user=current_user)
    except Cart.DoesNotExist:
        # For anonymous users, use some other logic to identify the cart (if needed)
        # cart= Cart.objects.create(user=current_user)
        pass
    

    cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    for cart_item in cart_items:
        if cart_item.quantity <= cart_item.variant.stock:
            total += (cart_item.variant.sale_price * cart_item.quantity)
            quantity += cart_item.quantity
            
            try:
                address = Address.objects.get(user=current_user)
                
            except Address.DoesNotExist:
                # Handle the case where the user doesn't have an address yet
                address = None

            try:
                user_wallet = Wallet.objects.get(user=current_user)
            except:
                pass


            # #Razorpay creating order
            # total_amount = int(total * 100)
            # client = razorpay.Client(auth=("rzp_test_qoXpACMLfXbWKp", "ydDrIJw9JIb3RhaMLHSsGvyi"))

            # data = { "amount": total_amount, "currency": "INR", "receipt": "order_rcptid_11" }
            # payment = client.order.create(data=data)

            # print('11111111111',payment)

            context={
                'total': total,
                'quantity' : quantity,
                'cart_items' : cart_items,
                'address':address,
                # 'payment': payment,
                'user_wallet': user_wallet,
            }
            return render(request,'user_side/shop-checkout.html',context)

        else:
            
            messages.error(request,f"Insufficient quantity. Reduce quantity to {cart_item.variant.stock} to proceed!!")
            return redirect('cart_app:cart_list')