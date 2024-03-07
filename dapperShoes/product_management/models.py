from django.db import models
from category.models import Category, SubCategory
from django.utils.text import slugify
from PIL import Image

# Create your models here.
class Brand(models.Model):
    brand_name = models.CharField(max_length=29,unique=True)
    brand_image = models.ImageField(upload_to='brand/',default="")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.brand_name


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

    images = models.ImageField(upload_to='products/', blank=True, default="")
    # product_price = models.DecimalField(max_digits=8, decimal_places=2, default="0.00")
    # stock = models.IntegerField()

    def __str__(self):
        return self.product_name


    def save(self,*args, **kwargs):
        slug = f"{self.product_brand.brand_name} {self.category.category_name} {self.product_name} {self.pk}"
        self.product_slug = slugify(slug)
        super(Product,self).save(*args, **kwargs)

        if not self.is_active:
            Product_variant.objects.filter(product=self, variant_is_active=True).update(variant_is_active=False)
        else:
            Product_variant.objects.filter(product=self, variant_is_active=False).update(variant_is_active=True)

        if self.images:
            img = Image.open(self.images.path)
            size = (679,679)
            img=img.resize(size, Image.BOX)
            img.save(self.images.path)


class Attribute(models.Model):
    atrribute_name = models.CharField(max_length=50,unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.atrribute_name
    

class Attribute_value(models.Model):
    attribute_id = models.ForeignKey(Attribute,on_delete=models.CASCADE,related_name='atribute_value_set')
    attribute_value = models.CharField(max_length=40,unique=True)
    attr_is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.attribute_value


class Product_variant(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_var')
    attribute = models.ManyToManyField(Attribute_value,max_length=100,related_name='attribute')
    variant_name = models.CharField( blank=True,max_length=200)
    stock = models.IntegerField(default=0)
    max_price = models.DecimalField(max_digits=8, decimal_places=2)
    sale_price = models.DecimalField(max_digits=8, decimal_places=2)
    thumbnail_image = models.ImageField(upload_to='product/product_thumbnail',blank=True)
    variant_slug  = models.SlugField(unique=True,max_length=300,blank=True)
    variant_is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # sku_id = models.CharField(max_length=30,unique=True,default='')
    # description = models.CharField(max_length=200)
    # discount_percentage = models.IntegerField(null=True,blank=True)
    
    def __str__(self):
        attribute_values_str = ', '.join([str(attr.attribute_value) for attr in self.attribute.all()])
        return f"{self.product} {self.product.product_brand} {attribute_values_str}"
    

    def save(self, *args, **kwargs):
        if not self.variant_slug:
            # Generate the initial slug based on the product and brand names
            slug = f"{self.product.product_brand.brand_name} {self.product.product_name}"
            base_slug = slugify(slug)

            # Check for existing slugs with the same base
            counter = 1
            while Product_variant.objects.filter(variant_slug=base_slug).exists():
                counter += 1
                base_slug = f"{slugify(slug)}-{counter}"

            self.variant_slug = base_slug
        
        super(Product_variant, self).save(*args, **kwargs)
      

        if self.thumbnail_image:
            img = Image.open(self.thumbnail_image.path)
            size = (679,679)
            img=img.resize(size, Image.BOX)
            img.save(self.thumbnail_image.path)
    

    # def __str__(self):
    #     return f"{self.product} {self.product.product_brand} {self.attribute.attribute_value}"

        # since attributes is a ManyToManyField, you need to loop through the attribute values to create a string representation.
        # attribute_values_str = ', '.join([str(attr.attribute_value) for attr in self.attributes.all()])
        # return f"{self.product_name} {self.product_name.product_brand} {attribute_values_str}"

        # attribute_values_str = ', '.join([str(attr.attribute_value) for attr in self.attributes.all()])
        # return f"{self.product_name.product_name} {self.product_name.product_brand.Brand_name} {attribute_values_str}"

        # attribute_values_str = ', '.join([str(attr.attribute_value) for attr in self.attributes.all()])
        # product_name_str = f"{self.product_name.product_name} {self.product_name.product_brand.Brand_name}"
        # return f"{product_name_str} {attribute_values_str}"
    

    # def save(self,*args, **kwargs):
    #     slug = f"{self.product_name} {self.product_name.product_brand}" 
    #     base_slug = slugify(slug)
    #     # self.product_variant_slug = slugify(slug)
    #     counter = Product_varient.objects.filter(product_variant_slug__startswith=base_slug).count()
    #     if counter > 0:
    #         self.product_variant_slug = f'{base_slug} {counter}'
    #     else:
    #         self.product_variant_slug = base_slug

    #     # Check if any attribute value is not active, set the variant as not active
    #     # for attr in self.attributes.all():
    #     #     if not attr.attr_is_active:
    #     #         is_active = False
    #     #         break
    #     # self.varient_is_active = is_active

    #     super(Product_varient,self).save(*args, **kwargs)




class Product_Image(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_image')
    image = models.ImageField(upload_to='product_image/')

    def __str__(self):
        return self.image.url
    
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            size = (679,679)
            img=img.resize(size, Image.BOX)
            img.save(self.image.path)