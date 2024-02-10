from django.urls import path
from . import views
app_name = 'product_management_app'
urlpatterns = [
    # products
    path('product-list',views.product_list,name='product_list'),
    path('add_product',views.add_product,name='add_product'),
    path('edit/<int:id>',views.edit_product,name='edit_product'),
    path('delete/<slug:slug>',views.delete_product,name='delete_product'),
    

    # path('status/<slug:slug>',views.product_status,name='product_status'),
    # path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    # path('search',views.search,name='search'),
]