from django.contrib import admin
from neraApp.models import *
 
admin.site.register(User)
from django.contrib import admin
from .models import Product, ProductImage

admin.site.register(Tag)
admin.site.register(CodePromo)
admin.site.register(Panier)
admin.site.register(Order)
admin.site.register(Company)
admin.site.register(Wilaya)
admin.site.register(Commune)
admin.site.register(Delivery)
admin.site.register(PaymentConfirm)
admin.site.register(Request)
class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
 
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin ]
 
    class Meta:
       model = Product
 
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass

# admin.site.register(Product)
 
