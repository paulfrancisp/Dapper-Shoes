from django.urls import path
from . import views

app_name = 'account_app'
urlpatterns = [
    path('account',views.account,name='account'),

    path('account-my-orders',views.account_my_orders,name='account_my_orders'),
    path('account-edit-profile',views.account_edit_profile,name='account_edit_profile'),
    path('account-change-password',views.account_change_password,name='account_change_password'),
    
#     path('',views.account,name='account'),
#     path('address/<int:id>',views.address,name='address'),
#     path('address/delete/<int:id>',views.delete_address,name='delete_address'),
#     path('change_password',views.change_password,name='change_password'),
#     path('<int:id>',views.order_details,name= 'order_details'),

#     path('return_product/<int:id>',views.product_return,name='return_product'),
#     path('cancel_product/<int:id>',views.product_cancel,name='cancel_product'),

]