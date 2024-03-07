from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(Product_Image)
admin.site.register(Brand)
admin.site.register(Product_variant)
admin.site.register(Attribute)
admin.site.register(Attribute_value)  