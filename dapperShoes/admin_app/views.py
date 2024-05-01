from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import never_cache
from django.contrib import messages
from order.models import *
from wallet.models import *
from account.models import *
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from category.models import *
from product_management.models import *
from django.db.models import Sum
from django.db.models.functions import Coalesce
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
@never_cache
def admin_logout(request):
    logout(request) 
    return render(request,'admin_side/page-account-login.html')

@never_cache
def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            # email = request.POST['email']
            uname = request.POST.get('username')
            password = request.POST.get('password')
            admin = authenticate(request,username=uname, password=password)
            print(admin)
            if admin is not None and admin.is_superuser:
                login(request,admin)
                return redirect('admin_app:admin_dashboard')  
            else:
                messages.warning(request,'wrong credentials !')
                return redirect('admin_app:admin_login')
            
        return render(request,'admin_side/page-account-login.html')
    else:
        return render(request,'admin_side/page-account-login.html')



@login_required(login_url='admin_app:admin_login')
def admin_orders(request):
    if request.user.is_authenticated and request.user.is_superuser:
        order_list = Order.objects.filter(is_ordered=True).order_by("-created_at")

        context = {
            "order_lists":order_list,
            # "order_product":order_product
        }
        return render(request,'admin_side/Week_2/page-orders-list.html',context)
    else:
        return render(request,'admin_side/page-account-login.html')




@login_required(login_url='admin_app:admin_login')
def admin_orders_detail(request,user_id,order_number):
    if request.user.is_authenticated and request.user.is_superuser:
        user = User.objects.get(id=user_id)
        orders = Order.objects.filter(user_id=user.id)
        ord=Order.objects.get(order_number=order_number)

        print("Orders:", ord)

        if orders.exists():
            order = orders.first()
        else:
            order = None

        orderproduct = OrderProduct.objects.filter(order = ord).order_by("-created_at")

        order_actual_total = 0
        for i in orderproduct:
            order_actual_total += i.product_price
        

        context = {
            "ord":ord,
            "order":order,
            "orderproduct":orderproduct,
            'order_actual_total':order_actual_total,
            "user":user,
        }

        return render(request,'admin_side/Week_2/order_details.html',context)
    else:
        return render(request,'admin_side/page-account-login.html')


def change_order_status(request, order_id, status, user_id):
    order = get_object_or_404(OrderProduct, id=order_id)
    order.order_status = status
    order.save()
    ord = order.order
    print('Inside change_order_status()')

    if status == "Delivered":
        try:
            print("Inside try block")
            print('INSIDE Delivered',status)
            payment = Payment.objects.get(payment_order_id=order.order.order_number)
            payment.is_paid = True
            payment.payment_status = "SUCCESS"
            payment.save()

            print("status////", status)
            print("payment_status///", payment.payment_status)
        except ObjectDoesNotExist:
            print("Inside except block")
            print("Payment does not exist for order ID:", order_id)

    print('OUTSIDE Cancelled_Admin',status)

    if status == "Cancelled Admin":
        user = User.objects.get(id=user_id)
        user_wallet = Wallet.objects.get(user=user)
        wallet_transaction = WalletTransaction.objects.filter(wallet=user_wallet).order_by('-id')
        wallet_transaction = WalletTransaction.objects.create(
            wallet = user_wallet,
            transaction_type = "CREDIT",
            amount = order.total,
            wallet_payment_id = ord.order_number,
        )
        user_wallet.balance += order.total
        user_wallet.save()
        wallet_transaction.save()


    return redirect(reverse('admin_app:admin_orders_detail', kwargs={'user_id': user_id, 'order_number': order.order.order_number}))


@login_required(login_url='admin_app:admin_login')
def sales_report(request):
    if not request.user.is_superuser:
        return redirect('admin_app:admin_login')
    start_date_value = ""
    end_date_value = ""
    try:
        ("New", "New"),
        ("Accepted", "Accepted"),
        ("Delivered", "Delivered"),
        orders=Order.objects.filter(is_ordered = True).order_by('-created_at')
        order_products = OrderProduct.objects.filter(order__payment__payment_status__in=["SUCCESS"], order_status__in=["Delivered", "Accepted", "New"])

        total_amount = 0
        for i in order_products:
            total_amount += i.total

    except Exception as e:
        print("its exception",str(e))
        
    if request.method == 'POST':
       
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        start_date_value = start_date
        end_date_value = end_date
        if start_date and end_date:
          
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

           
            order_products = order_products.filter(created_at__range=(start_date, end_date))
            total_amount = 0
            for i in order_products:
                total_amount += i.total
   
    context={
        'orders':order_products,
        'start_date_value':start_date_value,
        'end_date_value':end_date_value,
        'total_amount':total_amount
    }

    return render(request,'admin_side/Week 3/sales_report.html',context)



@login_required(login_url='admin_app:admin_login')
def admin_dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.all().order_by("-created_at")

        if request.method == 'POST':
            date = request.POST.get('date')
            payment_status = request.POST.get('payment_status')


            if date and payment_status:

                orders = Order.objects.filter(created_at__contains=date,payment__payment_status = payment_status)
                print("order_product_status",orders)

                print("YES date",date)
            elif payment_status:
                print("yes paymant status",payment_status)
                orders = Order.objects.filter(payment__payment_status = payment_status)
                print(orders)
            
            elif date:
                orders = Order.objects.filter(created_at__contains=date)




        current_year = datetime.now().year
        current_month = datetime.now().month

        total_earnings = OrderProduct.objects.filter(
        created_at__year=current_year,
        created_at__month=current_month,
        order_status='Delivered'
        ).aggregate(total_earnings=Sum('total'))

        # If there are no earnings for the month, set total_earnings to 0
        total_earnings = total_earnings['total_earnings'] if total_earnings['total_earnings'] else 0

        top_selling_products = OrderProduct.objects.filter(order_status='Delivered') \
        .values('product_variant', 'variant_id') \
        .annotate(total_quantity=Coalesce(Sum('quantity'), 0)) \
        .order_by('-total_quantity')[:10]
        print("dddd................",top_selling_products)
        
        top_10_product = []
        top_selling_brands = []
        top_selling_categories = []
        product = []  # Initialize an empty list

        for i in top_selling_products:
            product_variant = i['product_variant']
            product_name = product_variant[0:] if len(product_variant) > 0 else product_variant
            product_name = product_name[:10]
            filtered_products = Product.objects.filter(product_name__contains=product_name)
            product.extend(filtered_products)  # Append filtered products to the list

        for i in product:
            top_10_product.append(i)
            top_selling_brands.append(i.product_brand.brand_name) 
            top_selling_categories.append(i.category.category_name)

        top_selling_brands = list(set(top_selling_brands))
        top_selling_categories = list(set(top_selling_categories))
        
        print('top_selling_brands',top_selling_brands)
        print('top_selling_categories',top_selling_categories)

        top_10_product = list(set(top_10_product))
                                            
        payment = Payment.objects.distinct("payment_status")
        categories = Category.objects.filter(is_active = True)
        order_products = OrderProduct.objects.filter(order_status = "Delivered")
        print("qqqqqqqqqqqqqqq",order_products)
        products = Product.objects.all()
        categories = Category.objects.all()
        
        revenue = 0
        for i in order_products:
            if i.total is not None:  # Check if total is not None
                revenue += i.total
        
        print("revvvvvvv",revenue)
        

        chart_month = []
        new_users = []
        orders_count= []
        for month in range(1, 13):
            c = 0
            user_count = 0
            order_c = 0
            for item in OrderProduct.objects.filter(order_status="Delivered"):
                if item.created_at.month == month:
                    c += item.quantity
                    order_c += 1

            chart_month.append(c)

            for user in User.objects.all():
                if user.date_joined.month == month:
                    user_count += 1
            new_users.append(user_count)

            # Count orders with payment status "SUCCESS" for the month
            for order in Order.objects.filter(payment__payment_status="SUCCESS", created_at__month=month):
                order_c += 1

            orders_count.append(order_c)
            total_orders = len(orders)
        

        context = {
            "orders":orders,
            "revenue":revenue,
            "total_orders":total_orders,
            "total_products":len(products),
            "total_categories":len(categories),
            "chart_month":chart_month,
            "new_users":new_users,
            "orders_count":orders_count,
            'categories':categories,
            'payment':payment,
            "top_selling_products":top_10_product,
            "top_selling_brands":top_selling_brands,
            "top_selling_categories":top_selling_categories,
            "total_earnings":total_earnings,


        }
        return render(request,'admin_side/page-admin-dashboard.html',context)
    else:
        return render(request,'admin_side/page-account-login.html')



