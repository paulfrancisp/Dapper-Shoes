from django.shortcuts import render,redirect, get_object_or_404
from product_management.models import Product, Brand, Product_Image, Product_variant, Attribute, Attribute_value
from category.models import Category, SubCategory
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.db import IntegrityError
from django.urls import reverse

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.images import ImageFile
from django.core.exceptions import ValidationError
from datetime import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='admin_app:admin_login')
def product_list(request):
    if request.user.is_authenticated and request.user.is_superuser:
        products = Product.objects.all().order_by('id')
        context = {
            'products' : products
        }
        return render(request,'admin_side/page-product-list.html',context)
    return redirect('admin_app:admin_login')


@login_required(login_url='admin_app:admin_login')
def edit_product(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        product = get_object_or_404(Product, id=id)

        if request.method == 'POST':
            title = request.POST.get('product_title')
            brand_id = request.POST.get('brand')
            brand = get_object_or_404(Brand, pk=brand_id)
            description = request.POST.get('description')
            # price = request.POST.get('price')
            category_id = request.POST.get('category_id')
            category = get_object_or_404(Category, id=category_id)
            subcategory_id = request.POST.get('subcategory_id')
            subcategory = get_object_or_404(SubCategory, id=subcategory_id)
            image = request.FILES.get('image')
            discount_percentage = request.POST.get('discount_percentage')
            expire_date = request.POST.get('expire_date')
            print(".......",discount_percentage,".............",expire_date)

            if title:
                product.product_name = title
            if brand_id:
                product.product_brand = brand
            if description:
                product.description = description
            # if price:
            #     product.price = price
            if category_id:
                product.category = category
            if subcategory_id:
                product.sub_category = subcategory
            if image:
                product.images = image
            
            if discount_percentage:
                product.discount_percentage = discount_percentage

            if  expire_date:
                # Convert the string to a datetime.date object
                expire_date_str = datetime.strptime(expire_date, '%Y-%m-%d').date()
                product.expire_date = expire_date_str
            

            product.save()

            return redirect('product_management_app:product_list')

        categories = Category.objects.all()
        subcategory = SubCategory.objects.all()
        brands = Brand.objects.all()

        # Check if discount_percentage is 0 and set expire_date_disabled accordingly
        # expire_date_disabled = False
        # if product.discount_percentage == 0:
        #     expire_date_disabled = True

        context = {
            'product': product,
            'categories' : categories,
            'subcategory' : subcategory,
            'brands' : brands,
        }

        return render(request,'admin_side/page-edit-product-list.html',context)
    return redirect('admin_app:admin_login')                                                                            
    

@login_required(login_url='admin_app:admin_login')
def add_product(request):
    if request.user.is_authenticated and request.user.is_superuser:

        if request.method == 'POST':
            title = request.POST.get('product_title')
            brand_id = request.POST.get('brand')
            description = request.POST.get('description')
            price = request.POST.get('price')
            category_id = request.POST.get('category_id')
            sub_category_id = request.POST.get('sub_category_id')
            discount_percentage = request.POST.get('discount_percentage')
            expire_date_str = request.POST.get('expire_date')
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
                if Product.objects.filter(product_name=title).exists():
                    messages.warning(request, "Product name already exists")
                    return redirect('product_management_app:add_product')
                if discount_percentage and not discount_percentage.isdigit():
                    raise ValidationError("Discount percentage must be a number")
                if discount_percentage:
                    discount_percentage = int(discount_percentage)
                    if discount_percentage < 0 or discount_percentage > 100:
                        raise ValidationError("Discount percentage must be between 0 and 100")
                 
            except ValidationError as e:
                messages.warning(request, e.message)
                return redirect('product_management_app:add_product')
            
            if expire_date_str:
                expire_date = datetime.strptime(expire_date_str, '%Y-%m-%d').date()                
            else:
                expire_date = None

            category = Category.objects.get(id = category_id)
            sub_category = SubCategory.objects.get(id = sub_category_id)
            brand = Brand.objects.get(id = brand_id)
            print(brand)

            ################# NEED TO CHECK THIS  PART ####################
            if discount_percentage:
                product = Product.objects.create(product_name=title, product_brand=brand , description=description, category=category, sub_category=sub_category, images =image, discount_percentage=discount_percentage, expire_date=expire_date)
            else:
                product = Product.objects.create(product_name=title, product_brand=brand , description=description, category=category, sub_category=sub_category, images =image)
            
            product.save()
            return redirect('product_management_app:product_list')
            
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


# @never_cache
# def delete_product(request,slug):
#     if request.user.is_authenticated and request.user.is_superuser:
#         category = Product.objects.get(product_slug=slug)
#         category.delete()
#         return redirect('product_management_app:product_list')
    


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



################ ------- WEEK 2 ------- ################
@login_required(login_url='admin_app:admin_login')
def variant_list(request,id):
    product_variants = Product_variant.objects.filter(product_id=id).order_by('id')
    # product_variants = get_object_or_404(Product_Variant,Product=id)
    product = Product.objects.get(id=id)
    context = {
        'product_variants' : product_variants,
        'product' : product
    }
    return render(request, 'admin_side/Week_2/product-variant-list.html',context)



@login_required(login_url='admin_app:admin_login')
def edit_variant(request,id):
    product_variant = get_object_or_404(Product_variant, id=id)
    attribute_value = Attribute_value.objects.all()

    if request.method == "POST":
        variant_name = request.POST.get('product_variant_name')
        max_price = request.POST.get('max_price')
        sale_price = request.POST.get('sale_price')
        stock = request.POST.get('stock')
        # color = request.POST.getlist('color')  # Use getlist for multi-select  
        size = request.POST.getlist('size')  # Use getlist for multi-select
        # is_active = request.POST.get('is_active')
        thumbnail_image = request.FILES.get('product_varient_image')

        if variant_name:
            product_variant.variant_name = variant_name
        if max_price:
            product_variant.max_price = max_price
        if sale_price:
            product_variant.sale_price = sale_price
        if stock:
            product_variant.stock = stock


        # Clear existing sizes and add selected sizes
        product_variant.attribute.clear()
        for size_id in size:
            size_instance = Attribute_value.objects.get(id=size_id)
            product_variant.attribute.add(size_instance)

        if thumbnail_image:
            product_variant.thumbnail_image = thumbnail_image

        product_variant.save()
        # return redirect('product_management_app:product-variant-list')
        return redirect(reverse('product_management_app:variant_list', kwargs={'id': product_variant.product.id}))

        # Redirect to a success page or back to the product variant detail page
        # Example: return redirect('product_variant_detail', id=product_variant.id)

    context = {
        'product_variant': product_variant,
        'attribute_value': attribute_value
    }

    return render(request, 'admin_side/Week_2/edit-product-variant.html',context)

@login_required(login_url='admin_app:admin_login')
def add_variant(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            product = Product.objects.get(id=id)
            variant_name = request.POST.get('product_variant_name')
            max_price = request.POST.get('max_price')
            sale_price = request.POST.get('sale_price')
            stock = request.POST.get('stock')
            # size = request.POST.get('size')
            size = request.POST.getlist('size')  # Modified to get a list of sizes
            thumbnail_image = request.FILES.get('product_variant_image')

            # Basic validations
            if not variant_name or not max_price or not sale_price or not stock:
                messages.warning(request, "All fields are required.")
                return redirect('product_management_app:add_variant', id=id)

            try:
                max_price = float(max_price)
                sale_price = float(sale_price)
                stock = int(stock)
            except ValueError:
                messages.warning(request, "Invalid numeric input for prices or stock.")
                return redirect('product_management_app:add_variant', id=id)

            if max_price < 0 or sale_price < 0 or stock < 0:
                messages.warning(request, "Prices and stock should be non-negative.")
                return redirect('product_management_app:add_variant', id=id)

            if not size:
                messages.warning(request, "Color and size are required.")  # Modified error message
                return redirect('product_management_app:add_variant', id=id)

            # Additional validations
            if Product_variant.objects.filter(product=product, variant_name=variant_name).exists():
                messages.warning(request, f"A variant with the name '{variant_name}' already exists for this product.")
                return redirect('product_management_app:add_variant', id=id)

            # Ensure that the variant name is unique within the product
            if Product_variant.objects.filter(product=product, variant_name__iexact=variant_name).exists():
                messages.warning(request, "Variant names should be unique within the product.")
                return redirect('product_management_app:add_variant', id=id)

            try:
                product_var = Product_variant.objects.create(
                    product=product,
                    variant_name=variant_name,
                    max_price=max_price,
                    sale_price=sale_price,
                    stock=stock,
                    thumbnail_image=thumbnail_image,
                )
                # product_var.attributes.add(Attribute_value.objects.get(id=color))
                product_var.attribute.add(*size)  # Modified to add all sizes to attributes

                # Additional attribute validations and processing if needed

                product_var.save()
                # messages.success(request, "Product variant added successfully.")
                return redirect(reverse('product_management_app:variant_list', kwargs={'id': id}))

            except ObjectDoesNotExist:
                messages.warning(request, "Invalid attribute values.")
        else:
            product = Product.objects.get(id=id)
            attribute_value = Attribute_value.objects.all()  # You may need to filter based on your requirements

        categories = Category.objects.filter(is_active=True)
        brands = Brand.objects.filter(is_active=True)
        context = {
            'categories': categories,
            'brands': brands,
            'attribute_value': attribute_value,
            'product': product,
        }

        return render(request, 'admin_side/Week_2/add-product-variant.html', context)

    return redirect('admin_app:admin_login')





def delete_variant(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        product_variant = get_object_or_404(Product_variant, id=id)
        product_id = product_variant.product.id
        product_variant.delete()

    return redirect(reverse('product_management_app:variant_list', kwargs={'id': product_id}))

    