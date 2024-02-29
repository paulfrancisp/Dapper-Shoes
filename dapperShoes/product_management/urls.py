from django.urls import path
from . import views
app_name = 'product_management_app'
urlpatterns = [
    # products
    path('product-list',views.product_list,name='product_list'),
    path('add_product',views.add_product,name='add_product'),
    path('edit/<int:id>',views.edit_product,name='edit_product'),
    # path('delete/<slug:slug>',views.delete_product,name='delete_product'),
    path('product-activate/<int:id>',views.deactivate_product,name='deactivate_product'),
    path('product-deactivate/<int:id>',views.activate_product,name='activate_product'),


    # product variant
    path('variant-list/<int:id>',views.variant_list,name='variant_list'),
    path('add-variant/<int:id>',views.add_variant,name='add_variant'),
    path('edit-variant/<int:id>',views.edit_variant,name='edit_variant'),
    ### path('delete-variant/<int:id>',views.delete_variant,name='delete_variant'),
    
    # path('variant/status/<slug:slug>/<slug:p_slug>',views.variant_status,name='variant_status'),
    # path('variant/delete/image/<int:id>/<slug:slug>/<slug:p_slug>',views.image_variant,name='image_variant'),


    #attribute
    ### path('attribute-list',views.attribute_list,name='attribute_list'),
    ### path('add-attribute/<int:id>',views.add_attribute,name='add_attribute'),
    ### path('delete-attribute/<int:id>',views.delete_attribute,name='delete_attribute'),
    # path('attribute/status/<int:id>',views.attribute_status,name='attribute_status'),
    
    #attribute values
    ### path('attribute_values_list',views.attribute_values_list,name='attribute_values_list'),
    ### path('add-attribute-values/<int:id>',views.add_attribute_value,name='add_attribute_value'),
    ### path('delete-attribute/<int:id>',views.attribute_value_status,name='attribute_value_status'),
    


    # path('status/<slug:slug>',views.product_status,name='product_status'),
    # path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    # path('search',views.search,name='search'),
]