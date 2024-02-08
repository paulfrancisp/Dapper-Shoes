from django.db import models
from django.utils.text import slugify

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True,max_length=200)
    description = models.TextField(blank=True,max_length=250, default='Write description here!')
    category_image = models.ImageField(upload_to='category_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active =  models.BooleanField(default=True)
    # parent_category = models.ForeignKey('self', null=True, blank=True, related_name='child_categories', on_delete=models.CASCADE)
    # category_thumbnail = models.ImageField(upload_to='category_thumbnails/', null=True, blank=True)

    class Meta:
        verbose_name        = 'category'
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category_name
    


class SubCategory(models.Model):
    sub_category_name = models.CharField(max_length=255)
    sub_slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    sub_category_image = models.ImageField(upload_to='sub_category_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active =  models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.sub_slug:
            self.sub_slug = slugify(self.sub_category_name)
        super(SubCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.sub_category_name
