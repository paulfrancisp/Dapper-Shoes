from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Category,SubCategory

# Create your views here.
# def categories(request):
#     if request.user.is_authenticated and request.user.is_superuser:
#         categories = Category.objects.all()
#         context = {
#             'categories': categories
#         }
#         return render(request,'admin_side/page-categories.html',context)
#     return redirect('admin_app:admin_login')


def admin_categories(request):
    if request.user.is_authenticated and request.user.is_superuser:
        categories = Category.objects.all()
        context = {
            'categories': categories
        }
        return render(request,'admin_side/page-categories.html',context)
    return redirect('admin_app:admin_login')

    # return render(request,'admin_side/page-categories.html')

def admin_sub_categories(request):
    if request.user.is_authenticated and request.user.is_superuser:
        sub_categories = SubCategory.objects.all()
        context = {
            'sub_categories': sub_categories
        }
        return render(request,'admin_side/page-sub-categories.html',context)
    return redirect('admin_app:admin_login')