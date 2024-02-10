from django.urls import path
from . import views

app_name = 'admin_app'
urlpatterns = [
    path('admin-login',views.admin_login,name='admin_login'),
    path('admin-logout',views.admin_logout,name='admin_logout'),
    path('admin-dashboard',views.admin_dashboard,name='admin_dashboard'),  
    path('admin-orders',views.admin_orders,name='admin_orders'),

    # path('admin-users-list',views.admin_users_list,name='admin_users_list'),
    # path('admin-products-list',views.admin_products_list,name='admin_products_list'),
    
    # path('admin-catagories',views.admin_catagories,name='admin_catagories'),
    # path('admin-add-products',views.admin_add_products,name='admin_add_products'),
    
        
    # path('admin-',views.admin_,name='admin_')
    # path('',views.adminhome,name='adminhome'),
    # path('login/',views.admin_login,name='admin_login'),
    # path('logout/',views.adminlogout,name='adminlogout'),
    # path('product/',views.productdetail,name='productdetail'),
    # path('add-product/',views.addproduct,name='addproduct'),
    # path('edit-product/<int:product_id>',views.editproduct,name='editproduct'),
    # path('add-category/',views.addcategory,name='addcategory'),
    
    # path('user-management/', views.user_management, name='user_management'),
    # path('category-management/',views.categorymanagement,name='categorymanagement'),

    # path('blockuser/<int:user_id>/', views.blockuser, name='blockuser'),
    # path('unblockuser/<int:user_id>/', views.unblockuser, name='unblockuser'),

    # path('deactivate-product/<int:product_id>/',views.deactivateproduct,name='deactivateproduct'),
    # path('activate-product/<int:product_id>/',views.activateproduct,name='activateproduct'),
]