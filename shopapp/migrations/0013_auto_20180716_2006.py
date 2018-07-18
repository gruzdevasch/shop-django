# Generated by Django 2.0.7 on 2018-07-16 13:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shopapp', '0012_auto_20180716_1713'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.ManyToManyField(blank=True, to='shopapp.ItemInCart')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='profile',
            name='orders',
        ),
        migrations.AddField(
            model_name='order',
            name='is_complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='is_delivered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='is_delivering',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='is_moderating',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='item',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='categories', to='shopapp.Category'),
        ),
    ]