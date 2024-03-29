# Generated by Django 4.2.9 on 2024-02-09 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0004_remove_product_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='images',
            field=models.ImageField(blank=True, default='', upload_to='products/'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_price',
            field=models.DecimalField(decimal_places=2, default='0.00', max_digits=8),
        ),
    ]
