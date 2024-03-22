from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Category,SubCategory
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache

# Create your views here.
# Note: These functions are being used in admin side.


# def categories(request):
#     if request.user.is_authenticated and request.user.is_superuser:
#         categories = Category.objects.all()
#         context = {
#             'categories': categories
#         }
#         return render(request,'admin_side/page-categories.html',context)
#     return redirect('admin_app:admin_login')


# def admin_categories(request):
#     if request.user.is_authenticated and request.user.is_superuser:
        # categories = Category.objects.all()
        # context = {
        #     'categories': categories
        # }
        # return render(request,'admin_side/page-categories.html',context)
    # return redirect('admin_app:admin_login')
        # pass

@never_cache
def admin_categories(request):
    if request.user.is_authenticated and request.user.is_superuser:
        # Adding new category
        if request.method == 'POST':
            category = request.POST.get('category')
            description = request.POST.get('description')
            try:
                image = request.FILES.get('image')
            except :
                messages.warning(request,"Add category image")
                return redirect('category_app:admin_categories')
            try:
                if category == '':
                    messages.warning(request,"Add category name")
                    return redirect('category_app:admin_categories')
                if Category.objects.get(category_name=category):
                    messages.warning(request,"Category is taken")
                    return redirect('category_app:admin_categories')
            except:
                pass
            categories = Category.objects.create(category_image=image,category_name=category,description=description)
            categories.save()
        
        # Displaying the category from DB
        categories = Category.objects.all().order_by('id')
        context = {
            'categories': categories
        }
        return render(request,'admin_side/page-categories.html',context)
            # return redirect('category_app:admin_categories')
    return render(request,'admin_side/page-categories.html')
    # return redirect('admin_app:admin_login')


@never_cache
def edit_categories(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            category = Category.objects.get(id=id)
            category_name = request.POST.get('name')
            description = request.POST.get('description')
            category_image = request.FILES.get('image')
            # try:
            #     image = request.FILES.get('image')
            #     print(image)
            # except :
            #     messages.warning(request,"Add category image")
            #     return redirect('category_app:edit_categories')
        
            if category_name:
                category.category_name = category_name
                category.slug = slugify(category_name)  # Updates the slug

            if description:
                category.description = description

            if category_image:
                category.category_image = category_image

            category.save()
            
            messages.success(request,"Category updated")
            return redirect('category_app:admin_categories')
            
        
        category_object = Category.objects.get(id=id)
        context = {
            'category_object' : category_object
        }
        return render(request,'admin_side/page-edit-categories.html',context)
    else:
        return redirect('admin_app:admin_login')
    ####return render(request,'admin_side/page-edit-categories.html')

@never_cache
def delete_categories(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        category = Category.objects.get(id=id)
        category.delete()
        return redirect('category_app:admin_categories')
    


@never_cache
def activate_category(request, id):
    current_category = get_object_or_404(Category, id=id)
    current_subcategories = SubCategory.objects.filter(category_id=id) #cannot use get_object_or_404() because it only returns sign object

    current_category.is_active = True
    current_category.save()

    # Update is_active for all related subcategories.
    # Updating is_active field for all related subcategories directly with a single database query is more efficient and faster than individually retrieving each subcategory.
    current_subcategories.update(is_active=True)

    return redirect('category_app:admin_categories')

@never_cache
def deactivate_category(request, id):
    current_category = get_object_or_404(Category, id=id)
    current_subcategories = SubCategory.objects.filter(category_id=id)

    current_category.is_active = False
    current_category.save()

    current_subcategories.update(is_active=False)

    return redirect('category_app:admin_categories')



#---------------------------------------------
#---------------------------------------------

##### Sub-categories #####
@never_cache
def admin_sub_categories(request):
    if request.user.is_authenticated and request.user.is_superuser:
        # Adding new sub-category
        if request.method == 'POST':
            subcategory = request.POST.get('sub-category')
            parent_category = request.POST.get('parent-category')
            description = request.POST.get('description')
            try:
                image = request.FILES.get('image')
            except :
                messages.warning(request,"Add category image")
                return redirect('category_app:admin_categories')
            try:
                if subcategory == '':
                    messages.warning(request,"Add sub-category name")
                    return redirect('category_app:admin_categories')
                if SubCategory.objects.get(sub_category_name=subcategory):
                    messages.warning(request,"Category is taken")
                    return redirect('category_app:admin_categories')
            except:
                pass

            # Retrieve the Category instance based on the parent_category_name
            parent_category_object = get_object_or_404(Category, category_name=parent_category)


            sub_categories = SubCategory.objects.create(sub_category_image=image,sub_category_name=subcategory,category=parent_category_object,description=description)
            sub_categories.save()
        

        # Displaying the sub-category from DB
        sub_categories = SubCategory.objects.all().order_by('id')

        # Fetch all categories for dynamic display in the template #Added in 2nd week
        categories = Category.objects.filter(is_active = True).all()


        context = {
            'sub_categories': sub_categories,
            'categories' : categories
        }

        return render(request,'admin_side/page-sub-categories.html',context)
    return redirect('admin_app:admin_login')

@never_cache
def edit_sub_categories(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            subcategory = SubCategory.objects.get(id=id)
            subcategory_name = request.POST.get('name')
            description = request.POST.get('description')
            subcategory_image = request.FILES.get('image')

            # try:
            #     image = request.FILES.get('image')
            #     print(image)
            # except :
            #     messages.warning(request,"Add category image")
            #     return redirect('category_app:edit_categories')
        
            if subcategory_name:
                subcategory.sub_category_name = subcategory_name
                subcategory.sub_slug = slugify(subcategory_name)  # Updates the slug

            if description:
                subcategory.description = description

            if subcategory_image:
                subcategory.sub_category_image = subcategory_image

            subcategory.save()
            
            messages.success(request,"Category updated")
            return redirect('category_app:admin_sub_categories')
            
        
        sub_category_object = SubCategory.objects.get(id=id)

        # Fetch all categories for dynamic display in the template #Added in 2nd week
        # subcategories = SubCategory.objects.filter(is_active = True).all()

        context = {
            'sub_category_object' : sub_category_object
        }
        return render(request,'admin_side/page-edit-sub-categories.html',context)
    else:
        return redirect('admin_app:admin_login')
#     ####return render(request,'admin_side/page-edit-categories.html')

@never_cache
def delete_sub_categories(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        Subcategory = SubCategory.objects.get(id=id)
        Subcategory.delete()
        return redirect('category_app:admin_sub_categories')
    


@never_cache
def activate_sub_category(request, id):
    current = get_object_or_404(SubCategory, id=id)
    current.is_active = True
    current.save()
    return redirect('category_app:admin_sub_categories')

@never_cache
def deactivate_sub_category(request, id):
    current = get_object_or_404(SubCategory, id=id)
    current.is_active = False
    current.save()
    return redirect('category_app:admin_sub_categories')