from django.db import models
from product_management.models import Product_variant
from django.contrib.auth.models import User
from coupon.models import *
from decimal import Decimal

# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    # cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    coupon_applied = models.ForeignKey(Coupon,on_delete=models.CASCADE, default = None,null = True)
    coupon_discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_after_discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    def __str__(self):
        return self.id

class CartItem(models.Model):
    # user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    variant = models.ForeignKey(Product_variant,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)   # null is for anonymous users 
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)


    def sub_total(self):
        # return self.variant.calculate_discounted_price * self.quantity
        return self.variant.calculate_discounted_price() * self.quantity

    def __str__(self):
        return str(self.variant)