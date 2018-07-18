# Generated by Django 2.0.7 on 2018-07-17 14:18

from django.db import migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0017_auto_20180717_2114'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cropping',
            field=image_cropping.fields.ImageRatioField('showup_image', '430x360', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='cropping'),
        ),
    ]
