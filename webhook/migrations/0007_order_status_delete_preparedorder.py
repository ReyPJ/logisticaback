# Generated by Django 5.0.6 on 2024-07-05 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webhook', '0006_alter_preparedorder_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('new', 'Nueva Orden'), ('prepared', 'Lista para enviar'), ('shipped', 'Enviada')], default='new', max_length=30),
        ),
        migrations.DeleteModel(
            name='PreparedOrder',
        ),
    ]
