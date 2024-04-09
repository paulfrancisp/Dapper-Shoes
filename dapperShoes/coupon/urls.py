from django.urls import path
from . import views

app_name = 'coupon_app'
urlpatterns = [
    path('coupon_list', views.coupon_list, name='coupon_list'),
    path('add_coupon', views.add_coupon, name='add_coupon'),
    # path('toggle_coupon_status/', views.toggle_coupon_status, name='toggle_coupon_status'),
    path('coupon-activate/<int:id>',views.deactivate_coupon,name='deactivate_coupon'),
    path('coupon-deactivate/<int:id>',views.activate_coupon,name='activate_coupon'),
    path('delete-coupon/<int:id>',views.delete_coupon,name='delete_coupon'),
]
