# Generated by Django 2.0.7 on 2018-07-17 06:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0014_auto_20180717_1302'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Item',
            new_name='Product',
        ),
        migrations.RenameModel(
            old_name='ItemInCart',
            new_name='ProductInCart',
        ),
    ]
