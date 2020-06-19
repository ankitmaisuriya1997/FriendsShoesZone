from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.


class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    brand = models.CharField(max_length=50, default="")
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = RichTextField()
    product_date = models.DateField()
    image = models.ImageField(upload_to="images", default="")
    image1 = models.ImageField(upload_to="images", default="")
    image2 = models.ImageField(upload_to="images", default="")
    image3 = models.ImageField(upload_to="images", default="")
    image4 = models.ImageField(upload_to="images", default="")

    def __str__(self):
        return self.product_name


class Contact(models.Model):
    massage_id = models.AutoField(primary_key=True)
    contact_us = models.CharField(max_length=5000, default="")
    name = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    email = models.CharField(max_length=70, default="")
    description = models.CharField(max_length=300, default="")

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    amount = models.IntegerField(default=0)
    items_json = models.CharField(max_length=5000)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, default="")
    email = models.CharField(max_length=100, default="")
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_description = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_description[0:9] + "....."