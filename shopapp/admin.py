from django.contrib import admin

from image_cropping import ImageCroppingMixin
from .models import Product, Profile, ProductInCart, ImageModel, Category, Suplier, Tag, Cart

class ProductImageInline( admin.TabularInline):
    model = ImageModel
    extra = 1

class ProductInCartLine( admin.TabularInline):
    model = ProductInCart
    extra = 0

class ProductImageAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass
class ProductAdmin(admin.ModelAdmin):
    inlines = [ ProductImageInline, ]

class ProductCartAdmin(admin.ModelAdmin):
    inlines = [ ProductInCartLine, ]


admin.site.register(Product, ProductAdmin)
admin.site.register(Profile)
admin.site.register(Suplier)
admin.site.register(Tag)
admin.site.register(ProductInCart)
admin.site.register(Cart, ProductCartAdmin)
admin.site.register(Category)
