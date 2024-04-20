from django.urls import path, include
from . import views
app_name = 'user_management_app'

urlpatterns = [
    path('user-management',views.user_management,name='user_management'),
    path('user-activate/<int:id>',views.deactivate_user,name='deactivate_user'),
    path('user-deactivate/<int:id>',views.activate_user,name='activate_user'),
]