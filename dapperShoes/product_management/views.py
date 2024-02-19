from django.shortcuts import render,redirect
from product_management.models import Product, Brand, Product_Image
from category.models import Category, SubCategory
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404
from django.contrib import messages


# Create your views here.
@never_cache
def product_list(request):
    if request.user.is_authenticated and request.user.is_superuser:
        products = Product.objects.all().order_by('id')
        context = {
            'products' : products
        }
        return render(request,'admin_side/page-product-list.html',context)
    return redirect('admin_app:admin_login')


@never_cache
def edit_product(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        product = Product.objects.get(id=id)

        if request.method == 'POST':
            title = request.POST.get('product_title')
            brand_id = request.POST.get('brand')
            brand = get_object_or_404(Brand, pk=brand_id)
            description = request.POST.get('description')
            price = request.POST.get('price')
            category_id = request.POST.get('category_id')
            category = get_object_or_404(Category, pk=category_id)
            image = request.FILES.get('image')
            
            if title:
                product.product_name = title
            if brand_id:
                product.brand = brand
            if description:
                product.description = description
            if price:
                product.price = price
            if category_id:
                product.category = category
            if image:
                product.images = image

            product.save()

            return redirect('product_management_app:product_list')

        categories = Category.objects.all()
        subcategory = SubCategory.objects.all()
        brands = Brand.objects.all()

        context = {
            'product': product,
            'categories' : categories,
            'subcategory' : subcategory,
            'brands' : brands,
        }

        return render(request,'admin_side/page-edit-product-list.html',context)
    return redirect('admin_app:admin_login')                                                                            
    


def add_product(request):
    if request.user.is_authenticated and request.user.is_superuser:

        if request.method == 'POST':
            title = request.POST.get('product_title')
            brand_id = request.POST.get('brand')
            description = request.POST.get('description')
            price = request.POST.get('price')
            category_id = request.POST.get('category_id')
            sub_category_id = request.POST.get('sub_category_id')
            print(category_id, brand_id)
            image = request.FILES.get('image')
            additional_images = request.FILES.getlist('additional_image_1')


            try:
                image = request.FILES.get('image')
            except :
                messages.warning(request,"add product image")
                return redirect('product_management_app:add_product') 

            try:
                if title == '':
                    messages.warning(request,"Add product title")
                    return redirect('product_management_app:add_product')
                if Product.objects.get(product_name=title):
                    messages.warning(request,"product name is already exists")
                    return redirect('product_management_app:add_product')   
            except:
                pass
            
            
            category = Category.objects.get(id = category_id)
            sub_category = SubCategory.objects.get(id = sub_category_id)
            brand = Brand.objects.get(id = brand_id)
            print(brand)
            product = Product.objects.create(product_name=title, product_brand=brand , description=description, product_price=price ,category=category, sub_category=sub_category, images =image)
            product.save()

            
            for img in additional_images:
                Product_Image.objects.create(product_id=product,image=img)

        categories = Category.objects.all()
        subcategory = SubCategory.objects.all()
        brands = Brand.objects.all()

        context = {
            'categories' : categories,
            'subcategory' : subcategory,
            'brands' : brands,
        }
    
        return render(request,'admin_side/page-add-product.html',context)
    return redirect('admin_app:admin_login')


@never_cache
def delete_product(request,slug):
    if request.user.is_authenticated and request.user.is_superuser:
        category = Product.objects.get(product_slug=slug)
        category.delete()
        return redirect('product_management_app:product_list')
    


@never_cache
def activate_product(request, id):
    current = get_object_or_404(Product, id=id)
    current.is_active = True
    current.save()
    return redirect('product_management_app:product_list')

@never_cache
def deactivate_product(request, id):
    current = get_object_or_404(Product, id=id)
    current.is_active = False
    current.save()
    return redirect('product_management_app:product_list')