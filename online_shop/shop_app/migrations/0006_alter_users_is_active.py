# Generated by Django 4.1.7 on 2023-05-26 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0005_alter_usertoaddress_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
