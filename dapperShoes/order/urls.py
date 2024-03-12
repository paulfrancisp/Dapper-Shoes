from django.urls import path
from . import views

app_name = 'order_app'
urlpatterns = [
    path('place-order-cod', views.place_order_cod, name='place_order_cod'),
#     path('profile-order-details/<int:id>/', views.profile_order_details, name='profile_order_details'),
#     path('cancel-product/<int:item_id>/', views.cancel_product, name='cancel_product'),
#     path('return-product/<int:item_id>/', views.return_product, name='return_product'),
]