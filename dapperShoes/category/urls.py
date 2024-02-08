from django.urls import path, include
from . import views
app_name = 'category_app'

urlpatterns = [
   path('admin-categories',views.admin_categories,name='admin_categories'),
   # path('admin-add-category',views.admin_add_categories,name='admin_add_categories'),
   path('edit_category/<int:id>',views.edit_categories,name='edit_categories'),
   path('delete_category/<int:id>',views.delete_categories,name='delete_categories'),
#    path('search',views.search,name='search'),

   path('admin-sub-categories',views.admin_sub_categories,name='admin_sub_categories'),
   # Need to add for sub-categories

]