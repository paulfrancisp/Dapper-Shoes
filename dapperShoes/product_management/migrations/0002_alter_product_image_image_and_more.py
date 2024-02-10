# Generated by Django 4.2.9 on 2024-02-09 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_image',
            name='image',
            field=models.ImageField(upload_to='product_image/'),
        ),
        migrations.AlterField(
            model_name='product_image',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_image', to='product_management.product'),
        ),
    ]
