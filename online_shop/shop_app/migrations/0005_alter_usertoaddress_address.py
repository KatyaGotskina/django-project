# Generated by Django 4.1.7 on 2023-05-08 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0004_alter_orders_date_alter_orders_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertoaddress',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop_app.useraddresses'),
        ),
    ]
