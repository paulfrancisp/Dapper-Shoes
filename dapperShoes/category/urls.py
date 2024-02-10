from django.urls import path, include
from . import views
app_name = 'category_app'

urlpatterns = [
   path('admin-categories',views.admin_categories,name='admin_categories'),
   path('edit-category/<int:id>',views.edit_categories,name='edit_categories'),
   path('delete-category/<int:id>',views.delete_categories,name='delete_categories'),
   
   # path('admin-add-category',views.admin_add_categories,name='admin_add_categories'),
   # path('search',views.search,name='search'),


   # sub-categories
   path('admin-sub-categories',views.admin_sub_categories,name='admin_sub_categories'),
   path('edit-sub-category/<int:id>',views.edit_sub_categories,name='edit_sub_categories'),
   path('delete-sub-category/<int:id>',views.delete_sub_categories,name='delete_sub_categories'),
   

]