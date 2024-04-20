from django.urls import path
from . import views

app_name = 'account_app'
urlpatterns = [

    path('account',views.account,name='account'),
    path('account-my-orders',views.account_my_orders,name='account_my_orders'),
    path('account-change-password',views.account_change_password,name='account_change_password'),
    path('account-edit-address',views.account_edit_address,name='account_edit_address'),

    path('account-order-detail/<int:order_id>',views.account_order_detail,name='account_order_detail'),
    path('get_invoice/<int:id>/', views.get_invoice, name='get_invoice'),

    path('cancel-product/<int:item_id>/', views.cancel_product, name='cancel_product'),
    path('return-product/<int:item_id>/', views.return_product, name='return_product'),

    

    path('repay_payment/<int:id>/', views.repay_payment, name='repay_payment'),

]