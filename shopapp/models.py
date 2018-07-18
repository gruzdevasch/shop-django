from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

from image_cropping import ImageRatioField

class Category(models.Model):
    title = models.CharField(max_length=200)
    def __str__(self):
        return self.title

class Suplier(models.Model):
    bar = models.FloatField(default = 0)
    title = models.CharField(max_length=200)
    def __str__(self):
        return self.title

class Tag(models.Model):
    title = models.CharField(max_length=200)
    def __str__(self):
        return self.title

class Product(models.Model):
    article = models.CharField(max_length=6, primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    showup_image = models.ImageField(upload_to='media/', null = True)

    cropping = ImageRatioField('showup_image', '430x360')
    price = models.FloatField()
    count = models.IntegerField()
    discount = models.IntegerField()
    created_date = models.DateTimeField(default=timezone.now)
    sold_count = models.IntegerField(null = True, default = 0)
    categories = models.ManyToManyField(Category, related_name='categories', blank = True)
    tags = models.ManyToManyField(Tag, related_name='tags', blank = True)

    suplier = models.ForeignKey(Suplier, related_name='products', on_delete=models.CASCADE, null = True)
    def __str__(self):
        return self.title
    def get_real_price(self):
        return  float('{:.2f}'.format(self.price / 100 * (100 - self.discount)))

class ImageModel(models.Model):

    item = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE, null = True)
    img = models.ImageField(upload_to='media/')

    cropping = ImageRatioField('img', '430x360')
    def __str__(self):
        return self.item.title

class Cart(models.Model):

    user = models.ForeignKey(User, related_name='order', on_delete=models.CASCADE)
    summary = models.FloatField(default=0)
    status_code = models.IntegerField(default=0)
    ordered_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.user.username

class ProductInCart(models.Model):
    cart = models.ForeignKey(Cart, related_name='products', on_delete=models.CASCADE, null = True)
    item = models.ForeignKey(Product, related_name='cartproducts', on_delete=models.CASCADE)
    quanity = models.IntegerField()
    summary = models.FloatField(default=0)
    def __str__(self):
        return self.cart.user.username

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    phone = PhoneNumberField(blank = True)
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
       if created:
          Profile.objects.create(user=instance)
          Cart.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
        instance.cart.save()

    def __str__(self):
        return self.user.username
