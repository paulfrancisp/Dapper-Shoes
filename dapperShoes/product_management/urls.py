from django.urls import path
from . import views
app_name = 'product_management_app'
urlpatterns = [
    # products
    path('product-list',views.product_list,name='product_list'),
    path('add_product',views.add_product,name='add_product'),
    path('edit/<int:id>',views.edit_product,name='edit_product'),
    path('product-activate/<int:id>',views.deactivate_product,name='deactivate_product'),
    path('product-deactivate/<int:id>',views.activate_product,name='activate_product'),

    # product variant
    path('variant-list/<int:id>',views.variant_list,name='variant_list'),
    path('add-variant/<int:id>',views.add_variant,name='add_variant'),
    path('edit-variant/<int:id>',views.edit_variant,name='edit_variant'),
    path('delete-variant/<int:id>',views.delete_variant,name='delete_variant'),
]