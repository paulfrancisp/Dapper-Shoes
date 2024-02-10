from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from category.models import Category, SubCategory
from product_management.models import Product, Product_Image
# from django.shortcuts import get_object_or_404


# Create your views here.

def index(request):
            
    category = Category.objects.all()
    sub_category = SubCategory.objects.all()
    products = Product.objects.all().order_by('product_name')

    
    context = {
        'categories' : category,
        'subcategories' : sub_category,
        'products' : products,
    }
    
    return render(request,'user_side/index.html',context)
    
    
@never_cache
def product_detail(request,product_id):
    
    # category = Category.objects.all()
    # sub_category = SubCategory.objects.all()
    # products = get_object_or_404(Product, id=product_id)
    products = Product.objects.get(id=product_id)
    product_images = Product_Image.objects.filter(product_id_id=product_id)


        
    context = {
        # 'categories' : category,
        # 'subcategories' : sub_category,
        'products' : products,
        'product_images' : product_images,
    }
    
    return render(request,'user_side/shop-detail-product-page.html',context)

