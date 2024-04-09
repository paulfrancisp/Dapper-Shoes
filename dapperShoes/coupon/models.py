from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Coupon(models.Model):
    coupon_code = models.CharField(max_length=100)
    is_expired = models.BooleanField(default=False)
    discount_percentage = models.IntegerField(default=10)
    minimum_amount = models.IntegerField(default=400)
    max_uses = models.IntegerField(default=10)
    expire_date = models.DateField()
    total_coupons = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Get the current date
        current_date = timezone.now().date()
        
        # Compare expire_date with current_date
        if self.total_coupons <= 0 or self.expire_date < current_date:
            self.is_expired = True
            # self.is_active = False
        else:
            self.is_expired = False
            # self.is_active = True
        
        # Call the parent class's save method
        super().save(*args, **kwargs)

    def __str__(self):
        return self.coupon_code
    

class UserCoupon(models.Model):
    user        = models.ForeignKey(User,on_delete=models.CASCADE)
    coupon      = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    usage_count = models.IntegerField(default=0, blank=True)

    def apply_coupon(self):
        if self.coupon.is_expired:
            print('Coupon is expired')
            return False  # Coupon i
        if self.usage_count >= self.coupon.max_uses:
            print('Maximum uses reached')
            return False
        
        # self.usage_count += 1
        # self.save()
        print('Coupon applied successfully In UserCoupon')
        return True