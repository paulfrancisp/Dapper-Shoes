from django.shortcuts import render, redirect, get_object_or_404
from product_management.models import *
from .models import *
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    print("already exit cart id: ",cart)
    if not cart:
        cart = request.session.create()
        print("created cart Id: ",cart)
    return cart

@login_required(login_url='user_app:user_login')
def add_cart(request, variant_id):
    current_user = request.user
    variant = Product_variant.objects.get(id=variant_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request),
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(variant=variant , cart=cart,user = current_user)
        cart_item.quantity +=1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            variant=variant,
            cart=cart,
            quantity = 1,
            user = current_user
        )
        cart_item.save()
    # return HttpResponse(cart_item.quantity)
    ## return redirect(reverse('store_app:product_detail', kwargs={'id': product.id}))
    # Instead of using reverse, you can directly use the URL
    return redirect('cart_app:cart_list')
    ## return render(request, 'user_side/shop-detail-product-page.html')


def cart_list(request, total=0, quantity=0, cart_items=None):
    current_user = request.user
    try:
        # if request.user.is_authenticated:
            # cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        # else:
        print("cart_listssssssssssssssssssssssssssssssssss1")

        cart=Cart.objects.get(cart_id=_cart_id(request))
        print("cart_listssssssssssssssssssssssssssssssssss2")

        cart_items = CartItem.objects.filter(cart=cart, is_active=True,user = current_user)
        for cart_item in cart_items:
            total += (cart_item.variant.sale_price * cart_item.quantity)
            quantity += cart_item.quantity

        print("cart_listssssssssssssssssssssssssssssssssss")
    except :
        print("eXceptionnnnnnnnnnnnnnnnnnnnnn")
        pass

    context={
        'total': total,
        'quantity' : quantity,
        'cart_items' : cart_items
    }
    return render(request, 'user_side/shop-cart.html', context)

def remove_cart(request, variant_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    variant = get_object_or_404(Product_variant, id=variant_id)
    cart_item = CartItem.objects.get(variant=variant, cart=cart)
    if cart_item.quantity>1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_app:cart_list')

def remove_cart_item(request, variant_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    variant = get_object_or_404(Product_variant, id=variant_id)
    cart_item = CartItem.objects.get(variant=variant, cart=cart)
    cart_item.delete()
    return redirect('cart_app:cart_list')



def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.variant.sale_price * cart_item.quantity)
            quantity += cart_item.quantity
    except :
        pass

    context={
        'total': total,
        'quantity' : quantity,
        'cart_items' : cart_items
    }
    return render(request,'user_side/shop-checkout.html',context)