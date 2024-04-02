from django.urls import path
from . import views
app_name = 'shop_app'

urlpatterns = [
    path('',views.index,name='index'),
    path('product-detail/<int:product_id>', views.product_detail, name='product_detail'),
    path('product-detail-attribute/<int:product_id>/<int:attribute_value>', views.product_detail_attribute, name='product_detail_attribute'),
    path('home',views.home,name='home'),
    path('shop',views.shop,name='shop'),

    # path('navbar',views.navbar, name='navbar'),
    path('search', views.search, name='search'),


    path('filter-category/<str:category_filter>', views.filter_category, name='filter_category'),
    path('filter-subcategory/<str:subcategory_filter>', views.filter_subcategory, name='filter_subcategory'),


    path('low-to-high/<str:page>',views.low_to_high, name='low_to_high'),
    path('high-to-low/<str:page>',views.high_to_low, name='high_to_low'),
    path('price-range/<int:lower_price>/<int:upper_price>/', views.price_range, name='price-range'),
    

    path('wishlist',views.wishlist, name='wishlist'),
    path('add_wishlist/<int:id>/',views.add_wishlist, name='add_wishlist'),
    # path('wishlist_remove/<int:id>/',views.wishlist_remove, name='wishlist_remove'),

    # path('product-detail',views.product_detail,name='product_detail'),
    # path('<slug:slug>',views.product_details,name='product_details'),
    
    # path('predict',views.search_predict, name="predict"),  
    # path('home/search',views.search_product,name='search_product'),
    # path('category/search/<int:id>',views.category_products,name='search_category'),
    # path('brand/search/<int:id>',views.brand_products,name='search_brand'),


]