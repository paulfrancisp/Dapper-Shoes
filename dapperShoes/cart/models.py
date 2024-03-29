from django.db import models
from product_management.models import Product_variant
from django.contrib.auth.models import User

# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    # cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    
    def __str__(self):
        return self.id

class CartItem(models.Model):
    # user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    variant = models.ForeignKey(Product_variant,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)   # null is for anonymous users 
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)


    def sub_total(self):
        return self.variant.sale_price * self.quantity

    def __str__(self):
        return str(self.variant)