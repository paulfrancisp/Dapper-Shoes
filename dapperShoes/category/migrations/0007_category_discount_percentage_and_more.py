# Generated by Django 4.2.9 on 2024-04-10 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0006_alter_subcategory_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='discount_percentage',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='category',
            name='offer_is_active',
            field=models.BooleanField(default=True),
        ),
    ]