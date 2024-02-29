from django.shortcuts import render,redirect
from product_management.models import Product, Brand, Product_Image, Product_varient, Attribute, Attribute_values
from category.models import Category, SubCategory
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from django.urls import reverse

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist



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

def variant_list(request,id):
    product_variants = Product_varient.objects.filter(product_name_id=id).order_by('id')
    # product_variants = get_object_or_404(Product_Variant,Product=id)
    product = Product.objects.get(id=id)
    context = {
        'product_variants' : product_variants,
        'product' : product
    }
    return render(request, 'admin_side/Week_2/product-variant-list.html',context)



# def edit_variant(request,id):
#     old_product = Product_varient.objects.get(id=id)
#     products =Product.objects.all()

#     attributes = Attribute.objects.filter(is_active=True)
#     print(attributes)
# #    to get the old varient
#     attr_values_list = [item['attribute_value'] for item in old_product.attributes.all().values('attribute_value')]
  
#     attribute_dict = {}
#     for attribute in attributes:
#         attribute_values = attribute.attribute_value.filter(is_active=True )
#         attribute_dict[attribute.atrribute_name] = attribute_values  
#          #to show how many atribute in fronend
#         attribute_values_count = attributes.count()  

#     try:    
#         if request.method == "POST":
            
#             product = request.POST['product']
#             sku_id = request.POST['sku_id']
#             max_price = request.POST['max_price']
#             product_image=request.FILES.getlist('product_image')
#             sale_price = request.POST['sale_price']
#             stock = request.POST['stock']      
#             thumbnail_image = request.FILES.get('existing_product_images')     
        
#             #getting all atributes  
#             attribute_values = request.POST.getlist('attributes')
        
#             attribute_ids = []
#             for req_atri in attribute_values:
#                 if req_atri != 'None':
#                   attribute_ids.append(req_atri)   

#             product_id =Product.objects.get(id=product)


#             # old_product.product = product_id,65
#             old_product.sku_id = sku_id
#             old_product.max_price  = max_price 
#             old_product.sale_price  = sale_price 
#             old_product.stock  = stock 

#             if thumbnail_image != None:
#                 old_product.thumbnail_image = thumbnail_image
             

#             old_product.save()
#             old_product.atributes.set(attribute_ids)
#             if not product_image :
#                 for image in product_image:
#                     Product_Image.objects.create(product_variant=old_product,image=image)
#             else:
#                 old_product.additional_product_images.all().delete()
#                 for image in product_image:
#                     Product_Image.objects.create(product_variant=old_product,image=image)
#             messages.success(request, 'Product variation Added.')
        
#             return redirect(reverse('product_varient_detail', kwargs={'product_id': product_id.id}))
   
#     except IntegrityError:
            
#             messages.error(request, 'Product already exists.')
#             return redirect(reverse('product_varient_detail', kwargs={'product_id': product_id.id}))
     
    
#     print(attribute_dict)
#     context={
#         "old_product":old_product,
#         "products": products, 
#         'attribute_dict': attribute_dict,
#         'attr':attr_values_list,
#     }

#     return render(request,"admin_side/Week_2/edit-product-variant.html",context)

def edit_variant(request,id):
    product_variant = get_object_or_404(Product_varient, id=id)
    attribute_value = Attribute_values.objects.all()

    if request.method == "POST":
        variant_name = request.POST.get('product_variant_name')
        max_price = request.POST.get('max_price')
        sale_price = request.POST.get('sale_price')
        stock = request.POST.get('stock')
        color = request.POST.getlist('color')  # Use getlist for multi-select  
        size = request.POST.getlist('size')  # Use getlist for multi-select
        # is_active = request.POST.get('is_active')
        thumbnail_image = request.FILES.get('thumbnail_image')

        if variant_name:
            product_variant.variant_name = variant_name
        if max_price:
            product_variant.max_price = max_price
        if sale_price:
            product_variant.sale_price = sale_price
        if stock:
            product_variant.stock = stock
        if color:
            # product_variant.color = color
            product_variant.attributes.set(color)  # Use set to update ManyToManyField
            # Clear existing colors and add selected colors
            # product_variant.attributes.clear()
            # for color_id in color:
            #     color_instance = Attribute_values.objects.get(id=color_id)
            #     product_variant.attributes.add(color_instance)
        # if is_active:
        #     product_variant.is_active = True if is_active == 'on' else False
        if size:
            product_variant.attributes.set(size)  # Use set to update ManyToManyField
        if thumbnail_image:
            product_variant.thumbnail_image = thumbnail_image

        product_variant.save()
        # return redirect('product_management_app:product-variant-list')
        return redirect(reverse('product_management_app:variant_list', kwargs={'id': product_variant.product_name.id}))

        # Redirect to a success page or back to the product variant detail page
        # Example: return redirect('product_variant_detail', id=product_variant.id)

    context = {
        'product_variant': product_variant,
        'attribute_value': attribute_value
    }

    return render(request, 'admin_side/Week_2/edit-product-variant.html',context)


# def add_variant(request,id):
#     if request.user.is_authenticated and request.user.is_superuser:
#         print("before entering post method")
#         if request.method == 'POST':
#             variant_name = request.POST.get('product_variant_name')
#             stock_qty = request.POST.get('stock')
#             # brand_id = request.POST.get('Brand')
#             description = request.POST.get('description')
#             # price = request.POST.get('price')
#             category_id = request.POST.get('category_id')
#             base_price = request.POST.get('base_price')
#             print("entering post method")
#             image = request.FILES.get('image')
#             # additional_images = request.FILES.getlist('additional_image_1')


#             # try:
#             #     # image = request.FILES.get('image')
#             # except :
#             #     messages.warning(request,"add product image")
#             #     return redirect('product_management_app:add_product') 

#             try:
#                 if title == '':
#                     messages.warning(request,"Add product title")
#                     return redirect('product_management_app:add_product')
#                 if Product.objects.get(product_name=title):
#                     messages.warning(request,"product name is already exists")
#                     return redirect('product_management_app:add_product')   
#             except:
#                pass
#             # if brand_id or price or category_id or stock_qty:
#             #     messages.warning(request,"All fields are required")
#             #     return redirect('product_management_app:add_product')
#             category = Category.objects.get(id = category_id)
#             brand = Brand.objects.get(id = brand_id)
#             product = Product(
#                 product_name = title,
#                 # stock = stock_qty,
#                 brand = brand,
#                 category = category,
#                 description = description,
#                 # price = price,
#                 # images = image,
#                 base_price = base_price
#             )
#             product.save()
            
#             # for img in additional_images:
#             #     Additional_Product_Image.objects.create(product=product,image=img)    
#             return redirect('product_management_app:admin_products_list')

#         categories = Category.objects.filter(is_active = True)
#         brands = Brand.objects.filter(is_active = True)
#         context = {
#             'categories':categories,
#             'brands':brands
#         }
            
#         return render(request,'admin_side/Week_2/add-product-variant.html',context)
#     return redirect('admin_app:admin_login')

# from django.shortcuts import render, redirect
# from .models import Product, Product_varient, Attribute, Attribute_values
# from django.contrib import messages
# from django.http import HttpResponse

# def add_variant(request, product_id):
#     if request.user.is_authenticated and request.user.is_superuser:
#         if request.method == 'POST':
#             product_variant_name = request.POST.get('product_variant_name')
#             max_price = request.POST.get('max_price')
#             sale_price = request.POST.get('sale_price')
#             stock_qty = request.POST.get('stock')
#             color_id = request.POST.get('color')
#             size_id = request.POST.get('size')
#             product_id = request.POST.get('product_id')
#             thumbnail_image = request.FILES.get('product_varient_image')
#             additional_images = request.FILES.getlist('additional_image_1')

#             # Validate input data
#             if not product_variant_name or not max_price or not sale_price or not stock_qty or not color_id or not size_id:
#                 messages.warning(request, "All fields are required")
#                 return redirect('product_management_app:add_variant', product_id=product_id)

#             try:
#                 product = Product.objects.get(id=product_id)
#             except Product.DoesNotExist:
#                 messages.warning(request, "Invalid product ID")
#                 return redirect('product_management_app:admin_products_list')

#             try:
#                 color_attribute = Attribute_values.objects.get(id=color_id, attribute_id__atrribute_name='Color')
#                 size_attribute = Attribute_values.objects.get(id=size_id, attribute_id__atrribute_name='Size')
#             except Attribute_values.DoesNotExist:
#                 messages.warning(request, "Invalid color or size attribute")
#                 return redirect('product_management_app:add_variant', product_id=product_id)

#             # Create product variant
#             product_variant = Product_varient(
#                 product_name=product,
#                 variant_name=product_variant_name,
#                 max_price=max_price,
#                 sale_price=sale_price,
#                 stock=stock_qty,
#                 thumbnail_image=thumbnail_image
#             )
#             product_variant.save()

#             # Add attributes to the product variant
#             product_variant.attributes.add(color_attribute, size_attribute)

#             # Save additional images
#             for img in additional_images:
#                 Product_Image.objects.create(product_id=product_variant, image=img)

#             return redirect('product_management_app:admin_products_list')

#         product = Product.objects.get(id=product_id)
#         categories = Category.objects.filter(is_active=True)
#         brands = Brand.objects.filter(is_active=True)
#         attribute_values = Attribute_values.objects.filter(attr_is_active=True)
#         context = {
#             'product': product,
#             'categories': categories,
#             'brands': brands,
#             'attribute_values': attribute_values
#         }

#         return render(request, 'admin_side/Week_2/add-product-variant.html', context)
    
#     return redirect('admin_app:admin_login')





def add_variant(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            product = Product.objects.get(id=id)
            variant_name = request.POST.get('product_variant_name')
            max_price = request.POST.get('max_price')
            sale_price = request.POST.get('sale_price')
            stock = request.POST.get('stock')
            color = request.POST.get('color')
            size = request.POST.get('size')

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

            if not color or not size:
                messages.warning(request, "Color and size are required.")
                return redirect('product_management_app:add_variant', id=id)

            # Additional validations
            if Product_varient.objects.filter(product_name=product, variant_name=variant_name).exists():
                messages.warning(request, f"A variant with the name '{variant_name}' already exists for this product.")
                return redirect('product_management_app:add_variant', id=id)

            # Ensure that the variant name is unique within the product
            if Product_varient.objects.filter(product_name=product, variant_name__iexact=variant_name).exists():
                messages.warning(request, "Variant names should be unique within the product.")
                return redirect('product_management_app:add_variant', id=id)

            try:
                product_var = Product_varient.objects.create(
                    product_name=product,
                    variant_name=variant_name,
                    max_price=max_price,
                    sale_price=sale_price,
                    stock=stock,
                )
                product_var.attributes.add(Attribute_values.objects.get(id=color))
                product_var.attributes.add(Attribute_values.objects.get(id=size))

                # Additional attribute validations and processing if needed

                product_var.save()
                messages.success(request, "Product variant added successfully.")
                return redirect('product_management_app:admin_products_list')

            except ObjectDoesNotExist:
                messages.warning(request, "Invalid attribute values.")
        else:
            product = Product.objects.get(id=id)
            attribute_values = Attribute_values.objects.all()  # You may need to filter based on your requirements

        categories = Category.objects.filter(is_active=True)
        brands = Brand.objects.filter(is_active=True)
        context = {
            'categories': categories,
            'brands': brands,
            'attribute_values': attribute_values,
            'product': product,
        }

        return render(request, 'admin_side/Week_2/add-product-variant.html', context)

    return redirect('admin_app:admin_login')

    