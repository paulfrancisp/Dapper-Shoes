from django.urls import path
from . import views

app_name = 'order_app'
urlpatterns = [
    path('place-order-cod', views.place_order_cod, name='place_order_cod'),
    path('success-page', views.success_page, name='success_page'),

    path('place_order_razpay/', views.place_order_razpay, name='place_order_razpay'),
    path('order-success/<razorpay_order_id>/<payment_id>/<signature>/', views.order_success, name='order_success'), #Razorpay
    

    path('success-page/<str:order_id>/<str:payment_id>/<str:signature>/', views.success_page, name='success_page'),  #COD/Razorpay/Wallet success page
    path('paymentfailed', views.paymentfailed, name='paymentfailed'),
]