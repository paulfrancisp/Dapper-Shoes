from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Category,SubCategory
from django.utils.text import slugify

# Create your views here.
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


def admin_categories(request):
    if request.user.is_authenticated and request.user.is_superuser:
        # Adding new category
        if request.method == 'POST':
            category = request.POST.get('category')
            description = request.POST.get('description')
            try:
                image = request.FILES.get('image')
                print(image)
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
        categories = Category.objects.all()
        context = {
            'categories': categories
        }
        return render(request,'admin_side/page-categories.html',context)
            # return redirect('category_app:admin_categories')
    return render(request,'admin_side/page-categories.html')
    # return redirect('admin_app:admin_login')



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
            
        
        category = Category.objects.get(id=id)
        context = {
            'category_object' : category
        }
        return render(request,'admin_side/page-edit-categories.html',context)
    else:
        return redirect('admin_app:admin_login')
    ####return render(request,'admin_side/page-edit-categories.html')


def delete_categories(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        category = Category.objects.get(id=id)
        category.delete()
        return redirect('category_app:admin_categories')


# Sub-categories

def admin_sub_categories(request):
    if request.user.is_authenticated and request.user.is_superuser:
        sub_categories = SubCategory.objects.all().order_by('id')
        context = {
            'sub_categories': sub_categories
        }
        return render(request,'admin_side/page-sub-categories.html',context)
    return redirect('admin_app:admin_login')