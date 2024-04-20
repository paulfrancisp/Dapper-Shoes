from django.db import models
from django.utils.text import slugify
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True,max_length=200)
    description = models.TextField(blank=True,max_length=250, default='Write description here!')
    category_image = models.ImageField(upload_to='category_images/', blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active =  models.BooleanField(default=True)

    # New offer fields
    expire_date = models.DateField(null=True, blank=True)
    discount_percentage = models.IntegerField(default=0)
    offer_is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name        = 'category'
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)

        current_date = timezone.now().date()
        if self.expire_date:
            if self.expire_date < current_date:
                self.offer_is_active = False
            else:
                self.offer_is_active = True
        else:
            self.offer_is_active = False

        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category_name
    


class SubCategory(models.Model):
    sub_category_name = models.CharField(max_length=255)
    sub_slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='subcategory_set')
    sub_category_image = models.ImageField(upload_to='sub_category_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active =  models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.sub_slug:
            self.sub_slug = slugify(self.sub_category_name)
        super(SubCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.sub_category_name
