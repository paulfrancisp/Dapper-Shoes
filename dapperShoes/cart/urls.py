from django.urls import path
from . import views

app_name = 'cart_app'
urlpatterns = [
    path('cart-list',views.cart_list,name='cart_list'),
    path('add-cart/<int:variant_id>/',views.add_cart,name='add_cart'),
    path('remove-cart/<int:variant_id>/',views.remove_cart,name='remove_cart'),
    path('remove-cart-item/<int:variant_id>/',views.remove_cart_item,name='remove_cart_item'),
    path('checkout',views.checkout,name='checkout'),
]