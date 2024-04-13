from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from category.models import Category, SubCategory
from product_management.models import *
from django.urls import reverse
# from django.shortcuts import get_object_or_404
from cart.models import *
# from cart.views import _cart_id
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Min
from .models import *
from django.contrib import messages
from django.db.models import Q
from wallet.models import *
from cart.models import *

# Create your views here.

def index(request):

    user = request.user        
    category = Category.objects.filter(is_active=True)
    sub_category = SubCategory.objects.filter(is_active=True)
    products = Product.objects.filter(is_active=True).order_by('product_name')
    variants = Product_variant.objects.filter(product__in=products)
    
    if user.is_authenticated:
        try:
            user_wallet = Wallet.objects.get(user=user)
        except Wallet.DoesNotExist:
            user_wallet = Wallet.objects.create(user=user, balance=0)
    else:
        user_wallet = None

    three_days_ago = timezone.now() - timezone.timedelta(days=3)
    is_new = {}
    for product in products:
        if product.updated_at > three_days_ago:
            is_new[product.id] = True
  
    
    context = {
        'categories' : category,
        'subcategories' : sub_category,
        'products' : products,
        'variants' : variants,
        'is_new':is_new,
        'user_wallet':user_wallet,
        # 'category_subcategories': category_subcategories,
    }
    
    return render(request,'user_side/index.html',context)
    
    
@never_cache
def product_detail(request,product_id): 
    products = Product.objects.get(id=product_id)
    images = Product_Image.objects.filter(product_id_id=product_id)
    variants = Product_variant.objects.filter(product_id=products.id).first()
    attributes = Attribute_value.objects.all()

    current_user = request.user
    if current_user.is_authenticated:
        try:
            cart= Cart.objects.get(user=current_user)
        except Cart.DoesNotExist:
            # For anonymous users, use some other logic to identify the cart (if needed)
            cart= Cart.objects.create(user=current_user)
    

    # Initialize in_cart with a default value
    in_cart = False

    if request.user.is_authenticated:
        in_cart = CartItem.objects.filter(cart=cart,variant=variants).exists()  #Give a True or False value, if True won't show add to cart else it will show.


    context = {
        # 'categories' : category,
        # 'subcategories' : sub_category,
        'products' : products,
        'variants' : variants,
        'images' : images,
        'attributes': attributes,
        'in_cart' : in_cart,
    }
    return render(request,'user_side/shop-detail-product-page.html',context)


def product_detail_attribute(request,product_id,attribute_value):

    variants = Product_variant.objects.get(product_id=product_id, attribute__attribute_value=attribute_value)
    products = Product.objects.get(id=product_id)
    images = Product_Image.objects.filter(product_id_id=product_id)
    attributes = Attribute_value.objects.all()

    current_user = request.user
    if current_user.is_authenticated:
        try:
            cart= Cart.objects.get(user=current_user)
        except Cart.DoesNotExist:
            # For anonymous users, use some other logic to identify the cart (if needed)
            cart= Cart.objects.create(user=current_user)
    

    # Initialize in_cart with a default value
    in_cart = False

    if request.user.is_authenticated:
        in_cart = CartItem.objects.filter(cart=cart,variant=variants).exists()  #Give a True or False value, if True won't show add to cart else it will show.


    context = {
        'products' : products,
        'variants' : variants,
        'images' : images,
        'attributes': attributes,
        'in_cart' : in_cart,
    }
    
    return render(request,'user_side/shop-detail-product-page.html',context)


def search(request):
    if request.method == "POST":
        print('Inside search POST')
        search_query = request.POST.get('search', '')
        print('Inside search POST',search_query)
        if search_query:
            # Use Q objects to perform a case-insensitive search across multiple fields
            products = Product.objects.filter(product_name__icontains=search_query)  # Search product name
            print('qqqqqqqqqq')
            return render(request, 'user_side/index.html', {'products': products, 'search_query': search_query})
        else:
            # If search query is empty, return an empty result or an appropriate message
            print('wwwwwwwwwww')
            return render(request, 'user_side/index.html', {'products': None, 'search_query': search_query})
    else:
        # Handle GET requests to the search page (if needed)
        print('eeeeeeeeee')
        return render(request, 'user_side/index.html')




def home(request):
    return render(request,'user_side/index.html')

def shop(request):
    category = Category.objects.filter(is_active=True)
    sub_category = SubCategory.objects.filter(is_active=True)
    products = Product.objects.filter(is_active=True).order_by('product_name')
    variants = Product_variant.objects.filter(product__in=products)

    context = {
        'categories' : category,
        'subcategories' : sub_category,
        'products' : products,
        'variants' : variants,
    }
    return render(request,'user_side/shop-fullwidth.html',context)


def filter_category(request,category_filter):
    category = Category.objects.filter(is_active=True)
    sub_category = SubCategory.objects.filter(is_active=True)
    filtered_category = Category.objects.filter(category_name=category_filter)
    products = Product.objects.filter(sub_category__category__category_name=category_filter, is_active=True).order_by('product_name')
    variants = Product_variant.objects.filter(product__in=products)
    

    context = {
        'categories' : category,
        'subcategories' : sub_category,
        'filtered_category': filtered_category,
        'products' : products,
        'variants' : variants,
    }
    return render(request,'user_side/shop-fullwidth.html',context)

def filter_subcategory(request,subcategory_filter):
    category = Category.objects.filter(is_active=True)
    sub_category = SubCategory.objects.filter(is_active=True)
    filtered_subcategory = SubCategory.objects.filter(sub_category_name=subcategory_filter)
    products = Product.objects.filter(sub_category__sub_category_name=subcategory_filter, is_active=True).order_by('product_name')
    variants = Product_variant.objects.filter(product__in=products)

    context = {
        'categories' : category,
        'subcategories' : sub_category,
        'filtered_subcategory' : filtered_subcategory,
        'products' : products,
        'variants' : variants,
    }
    return render(request,'user_side/shop-fullwidth.html',context)

def low_to_high(request, page):

    category = Category.objects.filter(is_active=True)
    sub_category = SubCategory.objects.filter(is_active=True)

    if page == 'index':
        template_name = 'user_side/index.html'
    elif page == 'shop':
        template_name = 'user_side/shop-fullwidth.html'

    products = Product.objects.filter(is_active=True).annotate(min_sale_price=Min('product_var__sale_price')).order_by('min_sale_price')
    variants = Product_variant.objects.filter(product__in=products)

    three_days_ago = timezone.now() - timezone.timedelta(days=3)
    is_new = {}
    for product in products:
        if product.updated_at > three_days_ago:
            is_new[product.id] = True

    print(is_new)

    
    
    context = {
        'categories' : category,
        'subcategories' : sub_category,
        'products' : products,
        'variants' : variants,
        'is_new':is_new,
    }
    
    return render(request,template_name,context)



def high_to_low(request, page):

    category = Category.objects.filter(is_active=True)
    sub_category = SubCategory.objects.filter(is_active=True)

    if page == 'index':
        template_name = 'user_side/index.html'
    elif page == 'shop':
        template_name = 'user_side/shop-fullwidth.html'

    products = Product.objects.filter(is_active=True).annotate(min_sale_price=Min('product_var__sale_price')).order_by('-min_sale_price')
    variants = Product_variant.objects.filter(product__in=products)

    three_days_ago = timezone.now() - timezone.timedelta(days=3)
    is_new = {}
    for product in products:
        if product.updated_at > three_days_ago:
            is_new[product.id] = True

    print(is_new)

    
    
    context = {
        'categories' : category,
        'subcategories' : sub_category,
        'products' : products,
        'variants' : variants,
        'is_new':is_new,
    }
    
    return render(request,template_name,context)



def price_range(request,lower_price=0,upper_price=100000):
    category = Category.objects.filter(is_active=True)
    sub_category = SubCategory.objects.filter(is_active=True)
    if lower_price == 1:
        products = Product.objects.filter(is_active=True).order_by('product_name')
    else:
        products = Product.objects.filter(
            is_active=True,
            product_var__sale_price__gte=lower_price,
            product_var__sale_price__lte=upper_price
        ).annotate(
            min_sale_price=Min('product_var__sale_price')
        ).order_by('-min_sale_price')

    variants = Product_variant.objects.filter(product__in=products)

    three_days_ago = timezone.now() - timezone.timedelta(days=3)
    is_new = {}
    for product in products:
        if product.updated_at > three_days_ago:
            is_new[product.id] = True

    print(is_new)

    
    
    context = {
        'categories' : category,
        'subcategories' : sub_category,
        'products' : products,
        'variants' : variants,
        'is_new':is_new,
    }
    return render(request,'user_side/index.html',context)



def wishlist(request):
    user_id = request.user.id
    user = User.objects.get(id = user_id)
    try:
        user_wishlist = Wishlist.objects.get(user=user)
    except:
        user_wishlist = Wishlist.objects.create(user=user)

    wishlist_items = WishlistItem.objects.filter(wishlist=user_wishlist)

    context = {
       'wishlist_items':wishlist_items ,
    }
    return render(request,'user_side/Week 3/wishlist.html',context) #

def add_wishlist(request,id):
    user_id = request.user.id
    user = User.objects.get(id = user_id)
    product_variant = Product_variant.objects.get(id=id)

    try:
        user_wishlist = Wishlist.objects.get(user=user)
    except:
        user_wishlist = Wishlist.objects.create(user=user)

    wishlist_items = WishlistItem.objects.filter(wishlist=user_wishlist,product = product_variant)

    if not wishlist_items:
       WishlistItem.objects.create(wishlist=user_wishlist,product = product_variant)
    else:
        messages.error(request,'item is already in your wishlist')
        # id = product_variant.id
        # return redirect('shop_app:product_detail',id)
    return redirect('shop_app:wishlist')



def wishlist_remove(request,id):
    user_id = request.user.id
    user = User.objects.get(id = user_id)
    product_variant = Product_variant.objects.get(id=id)
    user_wishlist = Wishlist.objects.get(user=user)
    wishlist_items = WishlistItem.objects.get(wishlist=user_wishlist,product = product_variant)
    wishlist_items.delete()
    return redirect('shop_app:wishlist')