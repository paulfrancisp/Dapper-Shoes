from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Address(models.Model):
    user         = models.ForeignKey(User,on_delete=models.CASCADE,null=True, related_name = "user_address")
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    phone_number    = models.CharField(max_length=50)
    town_city       = models.CharField(max_length=100)
    address         = models.CharField(max_length=255,null=True)
    state           = models.CharField(max_length=50)
    country_region  = models.CharField(max_length=50)
    zip_code        = models.CharField(max_length=20)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    is_default      = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    user_image      = models.ImageField(upload_to='photos/user_images',blank=True)


    
    def save(self, *args, **kwargs):
        if self.is_default:
            # Set is_default=False for other addresses of the same user
            Address.objects.filter(account=self.account).exclude(pk=self.pk).update(is_default=False)
        super(Address, self).save(*args, **kwargs)

    def get_address_name(self):
        return f"{self.first_name} {self.last_name}" 

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.account.username} Address"