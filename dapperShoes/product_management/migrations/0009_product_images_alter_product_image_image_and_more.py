# Generated by Django 4.2.9 on 2024-02-24 06:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0008_attribute_attribute_values_product_varient'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='images',
            field=models.ImageField(blank=True, default='', upload_to='products/'),
        ),
        migrations.AlterField(
            model_name='product_image',
            name='image',
            field=models.ImageField(upload_to='product_varient_image/'),
        ),
        migrations.AlterField(
            model_name='product_image',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_varient_image', to='product_management.product_varient'),
        ),
    ]
