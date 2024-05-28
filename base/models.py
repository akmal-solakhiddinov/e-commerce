from django.db import models
from django.contrib.auth.models import User
import os
import uuid


def generate_new_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join(filename)


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(blank=True, null=True, upload_to=generate_new_filename)
    description = models.TextField(blank=True, null=True)
    availability = models.BooleanField(default=False)
    rate = models.DecimalField(max_digits=5, decimal_places=1)
    product_quantity = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

    def is_available(self):
        return self.availability and self.product_quantity > 0


class Category(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(blank=True, null=True, upload_to=generate_new_filename)
    # products = models.ManyToManyField(Product, related_name='product_category')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, default=1, decimal_places=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def add_to_cart(self, product, quantity):
        if product.is_available():
            self.product = product
            self.quantity = quantity
            self.save()

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_price(self):
        return self.quantity * self.product.price


class Chekout(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, related_name='product_name', on_delete=models.CASCADE)
    quantity = models.ForeignKey(Cart, related_name='product_quantity', on_delete=models.CASCADE)
    price = models.ForeignKey(Product, related_name='product_price', on_delete=models.CASCADE)
    total_price = models.ForeignKey(Cart, related_name='product_total_price', on_delete=models.CASCADE)


class SoldOutItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
