from django.urls import path
from . import views

app_name = 'admin_app'
urlpatterns = [
    path('admin-login',views.admin_login,name='admin_login'),
    path('admin-logout',views.admin_logout,name='admin_logout'),
    path('admin-dashboard',views.admin_dashboard,name='admin_dashboard'),  
    
    path('admin-orders',views.admin_orders,name='admin_orders'),
    path('admin-orders-detail/<int:user_id>/<str:order_number>',views.admin_orders_detail,name='admin_orders_detail'),
    path('change_status/<int:order_id>/<str:status>/<int:user_id>/', views.change_order_status, name='change_status'),
    path('sales_report/',views.sales_report,name='sales_report'),


]