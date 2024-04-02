from django.db import models
from product_management.models import Product_variant
from django.contrib.auth.models import User

# Create your models here.
class Wishlist(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)   
    
    def __str__(self): 
        return str(self.user)
    
    def get_items_count(self):
       return self.wishlistitem_set.filter(is_active=True).count()

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist,on_delete=models.CASCADE)
    product = models.ForeignKey(Product_variant,on_delete=models.CASCADE, related_name = 'wishlist')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.product)