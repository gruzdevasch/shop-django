# Generated by Django 2.0.7 on 2018-07-19 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0022_auto_20180718_1920'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='tech_data',
            field=models.TextField(null=True),
        ),
    ]
