from django.contrib import admin
from .models import Product, Cart, Category, SoldOutItem
# Register your models here.




admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(SoldOutItem)
# admin.site.register(Product)
