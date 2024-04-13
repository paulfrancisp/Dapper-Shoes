from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404


# Create your views here.
# Note: These functions are being used in admin side.
@never_cache
def user_management(request):
    if request.user.is_authenticated and request.user.is_superuser:
        customer = User.objects.all().order_by('id').exclude(is_superuser=True)
        context = {
            'customer_details' : customer
        }
        return render(request,"admin_side/page-users-list.html", context)
    return render(request,'admin_side/page-account-login.html') 

@never_cache
def activate_user(request, id):
    current = get_object_or_404(User, id=id)
    current.is_active = True
    current.save()
    return redirect('user_management_app:user_management')

@never_cache
def deactivate_user(request, id):
    current = get_object_or_404(User, id=id)
    current.is_active = False
    current.save()
    return redirect('user_management_app:user_management')