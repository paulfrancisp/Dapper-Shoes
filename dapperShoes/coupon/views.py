from django.shortcuts import render, redirect
from .models import *  
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from django.http import JsonResponse
import json
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404
from django.urls import reverse

# Create your views here.
def coupon_list(request):
    coupons = Coupon.objects.all().order_by('id')
    return render(request,'admin_side/Week 3/coupon_list.html',{'coupons':coupons})

def add_coupon(request):
    if request.method == 'POST':
        print('inside POST QQQQQQQQ')
        coupon_code = request.POST.get('coupon_code')
        discount_percentage = request.POST.get('discount_percentage')
        minimum_amount = request.POST.get('minimum_amount')
        max_uses = request.POST.get('max_uses')
        expire_date = request.POST.get('expire_date')
        total_coupons = request.POST.get('total_coupons')

        
        
        # Validate data
        try:
            discount_percentage = int(discount_percentage)
            minimum_amount = int(minimum_amount)
            max_uses = int(max_uses)
            total_coupons = int(total_coupons)
        except ValueError:
            messages.error(request, 'Invalid input. Please enter valid numbers.')
            return redirect('coupon_app:add_coupon')

        # Check if expire_date is a valid date
        try:
            expire_date = timezone.datetime.strptime(expire_date, '%Y-%m-%d').date()
            print("datae created")
        except ValueError:
            print("EXcetion in date")
            messages.error(request, 'Invalid date format. Please use YYYY-MM-DD format.')
            return redirect('coupon_app:add_coupon')

        # Create the coupon
        try:
            print('iiii',coupon_code,discount_percentage,minimum_amount,max_uses,expire_date,total_coupons)
            new_coupon = Coupon.objects.create(
                coupon_code=coupon_code,
                discount_percentage=discount_percentage,
                minimum_amount=minimum_amount,
                max_uses=max_uses,
                expire_date=expire_date,
                total_coupons=total_coupons
            )
            new_coupon.save()
            print('iiiijjjj11111')
            messages.success(request, 'Coupon added successfully.')
            return redirect('coupon_app:coupon_list')
        except Exception as e:
            print('exceptionnnnn',str(e))
            messages.error(request, f'An error occurred: {e}')
            print('iiiijjjj2222')
            return redirect('coupon_app:add_coupon')

    return render(request, 'admin_side/Week 3/add-coupon.html')



# def toggle_coupon_status(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         coupon_id = data.get('coupon_id')
#         activate = data.get('activate')
        
#         try:
#             coupon = Coupon.objects.get(id=coupon_id)
#             coupon.is_active = activate
#             coupon.save()
#             return JsonResponse({'success': True, 'active': coupon.is_active})
#         except Coupon.DoesNotExist:
#             return JsonResponse({'success': False, 'message': 'Coupon not found'})
#         except Exception as e:
#             return JsonResponse({'success': False, 'message': str(e)})


@never_cache
def deactivate_coupon(request, id):
    current = get_object_or_404(Coupon, id=id)
    current.is_active = False
    current.save()
    return redirect('coupon_app:coupon_list')

@never_cache
def activate_coupon(request, id):
    current = get_object_or_404(Coupon, id=id)
    current.is_active = True
    current.save()
    return redirect('coupon_app:coupon_list')

def delete_coupon(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        coupon = get_object_or_404(Coupon, id=id)
        # coupon_id = coupon.id
        coupon.delete()
    return redirect(reverse('coupon_app:coupon_list'))

