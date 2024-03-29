from django.urls import path, include
from . import views
app_name = 'user_management_app'

urlpatterns = [
    path('user-management',views.user_management,name='user_management'),
    path('user-activate/<int:id>',views.deactivate_user,name='deactivate_user'),
    path('user-deactivate/<int:id>',views.activate_user,name='activate_user'),
#     path('edit/<int:id>',views.user_management_edit,name='user_management_edit'),
#     path('status/<int:id>',views.user_management_active_inactive,name='status'),
#     path('search',views.user_management_search,name='search'),
]