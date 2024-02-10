from django.db import models
from category.models import Category, SubCategory
from django.utils.text import slugify

# Create your models here.
class Brand(models.Model):
    Brand_name = models.CharField(max_length=29,unique=True)
    brand_image = models.ImageField(upload_to='brand/',default="")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.Brand_name


class Product(models.Model):
    product_name = models.CharField(max_length=60,unique=True,blank=False)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL, null=True)
    sub_category = models.ForeignKey(SubCategory,on_delete=models.SET_NULL, null=True)
    product_brand = models.ForeignKey(Brand,on_delete=models.SET_NULL, null= True)
    description = models.CharField(max_length=250)
    product_slug = models.SlugField(unique=True,max_length=300,blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    product_price = models.DecimalField(max_digits=8, decimal_places=2, default="0.00")
    images = models.ImageField(upload_to='products/', blank=True, default="")
    # stock = models.IntegerField()

    def __str__(self):
        return self.product_name


    def save(self,*args, **kwargs):
        slug = f"{self.product_name} {self.category.category_name} {self.product_brand.Brand_name}"
        self.product_slug = slugify(slug)
        super(Product,self).save(*args, **kwargs)


class Product_Image(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_image')
    image = models.ImageField(upload_to='product_image/')

    def __str__(self):
        return self.image.url
    
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)

