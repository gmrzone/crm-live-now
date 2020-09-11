from django.db import models
from django.contrib.auth.models import User   # Importing Default user Model To Create A one To one Relation With Profile or Customer

# Create your models here.

class Customers(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(null=True, blank=True, default='default_profile.png')  # Directly useing image name because static media files is setup up to this location
    date_created  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Products(models.Model):
    CATAGORY_CHOISE = (('outdoor', 'outdoor'),('indoor', 'indoor'))
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    category = models.CharField(max_length=200, choices=CATAGORY_CHOISE)
    description = models.CharField(max_length=300, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOISE = (
                    ('Pending', 'Pending'),
                      ('Out For Delivery', 'Out For Delivery'),
                      ('Delivered', 'Delivered')
                    )
    customer = models.ForeignKey(Customers, null=True, on_delete=models.SET_NULL)
    products = models.ForeignKey(Products, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, choices=STATUS_CHOISE)

    def __str__(self):
        return self.products.name