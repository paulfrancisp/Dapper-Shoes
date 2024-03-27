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

# Create your views here.

def index(request):
            
    category = Category.objects.all()
    sub_category = SubCategory.objects.all()
    products = Product.objects.filter(is_active=True).order_by('product_name')
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
    
    
@never_cache
def product_detail(request,product_id): 

    # if size != None:
    #     products = Product.objects.get(id=product_id)
    #     images = Product_Image.objects.filter(product_id_id=product_id)
    #     variants = Product_variant.objects.filter(product_id=products.id,attribute__attribute_value=size)
    #     attributes = Attribute_value.objects.all()
    # else:
            
        # category = Category.objects.all()
        # sub_category = SubCategory.objects.all()
        # products = get_object_or_404(Product, id=product_id)
    products = Product.objects.get(id=product_id)
    images = Product_Image.objects.filter(product_id_id=product_id)
    variants = Product_variant.objects.filter(product_id=products.id).first()
    attributes = Attribute_value.objects.all()
    # print(variants)
    # in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),variant=variants) #Give a True or False value, if True won't show add to cart else it will show.
    # if request.user/
    context = {
        # 'categories' : category,
        # 'subcategories' : sub_category,
        'products' : products,
        'variants' : variants,
        'images' : images,
        'attributes': attributes,
        # 'in_cart' : in_cart,
        # 'product_detail_url': reverse('shop_app:product_detail', kwargs={'product_id': products.id}),
    }
    return render(request,'user_side/shop-detail-product-page.html',context)


def product_detail_attribute(request,product_id,attribute_value):

    variants = Product_variant.objects.get(product_id=product_id, attribute__attribute_value=attribute_value)
    products = Product.objects.get(id=product_id)
    images = Product_Image.objects.filter(product_id_id=product_id)
    attributes = Attribute_value.objects.all()

    # # Initialize in_cart with a default value
    # in_cart = False

    # if request.user.is_authenticated:
    #     in_cart = CartItem.objects.filter(cart=_cart_id(request),variant=variants).exists()  #Give a True or False value, if True won't show add to cart else it will show.

    # print(variants)
    # print(product_id)
    # print(attribute_value)

    context = {
        'products' : products,
        'variants' : variants,
        'images' : images,
        'attributes': attributes,
        # 'in_cart' : in_cart,
    }
    
    return render(request,'user_side/shop-detail-product-page.html',context)


def search(request):
    return HttpResponse('Search page')

def home(request):
    return render(request,'user_side/index.html')


