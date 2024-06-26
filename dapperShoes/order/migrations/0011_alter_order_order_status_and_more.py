# Generated by Django 4.2.9 on 2024-04-18 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_alter_order_order_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('New', 'New'), ('Pending Payment', 'Pending Payment'), ('Accepted', 'Accepted'), ('Delivered', 'Delivered'), ('Cancelled_Admin', 'Cancelled Admin'), ('Cancelled_User', 'Cancelled User'), ('Returned_User', 'Returned User')], default='New', max_length=20),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='order_status',
            field=models.CharField(choices=[('New', 'New'), ('Pending Payment', 'Pending Payment'), ('Accepted', 'Accepted'), ('Delivered', 'Delivered'), ('Cancelled_Admin', 'Cancelled Admin'), ('Cancelled_User', 'Cancelled User'), ('Returned_User', 'Returned User'), ('Return_pending', 'Returned pending')], default='New', max_length=20),
        ),
    ]
