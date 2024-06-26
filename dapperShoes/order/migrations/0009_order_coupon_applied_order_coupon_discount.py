# Generated by Django 4.2.9 on 2024-04-10 06:49

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0001_initial'),
        ('order', '0008_remove_order_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon_applied',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='coupon.coupon'),
        ),
        migrations.AddField(
            model_name='order',
            name='coupon_discount',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
        ),
    ]
