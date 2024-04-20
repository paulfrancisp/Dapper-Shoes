from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Category,SubCategory
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache
from datetime import datetime
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

# Create your views here.
# Note: These functions are being used in admin side.

@login_required(login_url='admin_app:admin_login')
def admin_categories(request):
    if request.user.is_authenticated and request.user.is_superuser:
        # Adding new category
        if request.method == 'POST':
            category = request.POST.get('category')
            discount_percentage = request.POST.get('discount_percentage')
            expire_date_str = request.POST.get('expire_date')
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
                if discount_percentage and not discount_percentage.isdigit():
                    raise ValidationError("Discount percentage must be a number")
                if discount_percentage:
                    discount_percentage = int(discount_percentage)
                    if discount_percentage < 0 or discount_percentage > 100:
                        raise ValidationError("Discount percentage must be between 0 and 100")
                if Category.objects.filter(category_name=category).exists():
                    messages.warning(request,"Category name is already taken")
                    return redirect('category_app:admin_categories')
            except ValidationError as e:
                messages.warning(request, e.message)
                return redirect('category_app:admin_categories')

            # Convert the expire_date string to a datetime.date object
            if expire_date_str:
                expire_date = datetime.strptime(expire_date_str, '%Y-%m-%d').date()                
            else:
                expire_date = None

            if discount_percentage:
                categories = Category.objects.create(category_image=image, category_name=category,
                                                  description=description, discount_percentage=discount_percentage,
                                                  expire_date=expire_date)
            else:
                categories = Category.objects.create(category_image=image, category_name=category,
                                                  description=description)
            categories.save()
        
        # Displaying the category from DB
        categories = Category.objects.all().order_by('id')
        context = {
            'categories': categories
        }
        return render(request,'admin_side/page-categories.html',context)
    return render(request,'admin_side/page-categories.html')



@login_required(login_url='admin_app:admin_login')
def edit_categories(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            category = Category.objects.get(id=id)
            category_name = request.POST.get('name')
            description = request.POST.get('description')
            category_image = request.FILES.get('image')
            discount_percentage = request.POST.get('discount_percentage')
            expire_date = request.POST.get('expire_date')
            
        
            if category_name:
                category.category_name = category_name
                category.slug = slugify(category_name)  # Updates the slug
            
            if discount_percentage:
                category.discount_percentage = discount_percentage

            if  expire_date:
                # Convert the string to a datetime.date object
                expire_date_str = datetime.strptime(expire_date, '%Y-%m-%d').date()
                category.expire_date = expire_date_str

            if description:
                category.description = description

            if category_image:
                category.category_image = category_image

            category.save()
            
            messages.success(request,"Category updated")
            return redirect('category_app:admin_categories')
            
        
        category_object = Category.objects.get(id=id)

        # Check if discount_percentage is 0 and set expire_date_disabled accordingly
        expire_date_disabled = False
        if category_object.discount_percentage == 0:
            expire_date_disabled = True

        context = {
            'category_object' : category_object,
            'expire_date_disabled': expire_date_disabled
        }
        return render(request,'admin_side/page-edit-categories.html',context)
    else:
        return redirect('admin_app:admin_login')

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
@login_required(login_url='admin_app:admin_login')
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

@login_required(login_url='admin_app:admin_login')
def edit_sub_categories(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            subcategory = SubCategory.objects.get(id=id)
            subcategory_name = request.POST.get('name')
            description = request.POST.get('description')
            subcategory_image = request.FILES.get('image')
        
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

        context = {
            'sub_category_object' : sub_category_object
        }
        return render(request,'admin_side/page-edit-sub-categories.html',context)
    else:
        return redirect('admin_app:admin_login')

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