# Generated by Django 4.2.9 on 2024-04-19 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_alter_order_order_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('FAILED', 'Failed'), ('SUCCESS', 'Success'), ('Repayed User', 'Repayed User')], max_length=20),
        ),
    ]