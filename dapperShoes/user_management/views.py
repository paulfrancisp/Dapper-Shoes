from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
def user_management(request):
    if request.user.is_authenticated and request.user.is_superuser:
        # if request.method == 'POST':
    #         search_word = request.POST.get('search-box', '')
    #         data = User.objects.filter(Q(username__icontains=search_word)| Q(email__icontains=search_word)).order_by('id').values()
    #     else:
        customer = User.objects.all().order_by('id').exclude(is_superuser=True)
        context = {
            'customer_details' : customer
        }
        return render(request,"admin_side/page-users-list.html", context)
    return render(request,'admin_side/page-account-login.html') 