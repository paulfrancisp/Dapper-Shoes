from django.urls import path
from . import views
app_name = 'shop_app'

urlpatterns = [
    path('',views.index,name='index'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('home',views.home,name='home'),



    # path('product-detail',views.product_detail,name='product_detail'),
    # path('<slug:slug>',views.product_details,name='product_details'),
    
    # path('predict',views.search_predict, name="predict"),  
    # path('home/search',views.search_product,name='search_product'),
    # path('category/search/<int:id>',views.category_products,name='search_category'),
    # path('brand/search/<int:id>',views.brand_products,name='search_brand'),


    path('account',views.account,name='account')
]