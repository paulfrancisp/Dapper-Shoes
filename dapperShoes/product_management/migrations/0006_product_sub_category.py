# Generated by Django 4.2.9 on 2024-02-09 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0005_alter_category_category_image'),
        ('product_management', '0005_product_images_product_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sub_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='category.subcategory'),
        ),
    ]
