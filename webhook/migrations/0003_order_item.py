# Generated by Django 5.0.6 on 2024-07-03 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webhook', '0002_order_customer_last_name_order_customer_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='item',
            field=models.JSONField(default=list),
        ),
    ]
