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


    
#     path('',views.account,name='account'),
#     path('address/<int:id>',views.address,name='address'),
#     path('address/delete/<int:id>',views.delete_address,name='delete_address'),
#     path('change_password',views.change_password,name='change_password'),
#     path('<int:id>',views.order_details,name= 'order_details'),

#     path('return_product/<int:id>',views.product_return,name='return_product'),
#     path('cancel_product/<int:id>',views.product_cancel,name='cancel_product'),

]