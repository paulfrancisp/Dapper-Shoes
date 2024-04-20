from django.urls import path
from . import views

app_name = 'coupon_app'
urlpatterns = [
    ########## --- Admin side urls --- ##########
    path('coupon_list', views.coupon_list, name='coupon_list'),
    path('add_coupon', views.add_coupon, name='add_coupon'),
    path('coupon-activate/<int:id>',views.deactivate_coupon,name='deactivate_coupon'),
    path('coupon-deactivate/<int:id>',views.activate_coupon,name='activate_coupon'),
    path('delete-coupon/<int:id>',views.delete_coupon,name='delete_coupon'),


    ########## --- User side urls --- ##########
    path('apply_coupon', views.apply_coupon, name='apply_coupon'),
]
