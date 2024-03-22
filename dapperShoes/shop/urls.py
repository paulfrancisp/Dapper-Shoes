from django.urls import path
from . import views
app_name = 'shop_app'

urlpatterns = [
    path('',views.index,name='index'),
    path('product-detail/<int:product_id>', views.product_detail, name='product_detail'),
    path('product-detail-attribute/<int:product_id>/<int:attribute_value>', views.product_detail_attribute, name='product_detail_attribute'),
    path('home',views.home,name='home'),
    path('search', views.search, name='search'),


    # path('low_to_high/',views.low_to_high, name='low_to_high'),
    # path('high_to_low/',views.high_to_low, name='high_to_low'),
    # path('pricebar/',views.pricebar, name='pricebar'),

    # path('product-detail',views.product_detail,name='product_detail'),
    # path('<slug:slug>',views.product_details,name='product_details'),
    
    # path('predict',views.search_predict, name="predict"),  
    # path('home/search',views.search_product,name='search_product'),
    # path('category/search/<int:id>',views.category_products,name='search_category'),
    # path('brand/search/<int:id>',views.brand_products,name='search_brand'),


]