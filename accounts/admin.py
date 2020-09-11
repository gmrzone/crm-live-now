from django.contrib import admin
# from .models import *
from .models import Customers, Products, Order, Tag

# Register your models here.
@admin.register(Customers)  # We Can Also Register a model using this Decorator But We Have To Create Below Class forThis Decorator To Work
class CustomerAdmin(admin.ModelAdmin): # For Customer Model this Class Should Always Inherit admin.ModelAdmin
    list_display = ['user', 'name', 'phone', 'email']   # Every item in list_display will be shown as field name in selected model


@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'products', 'status']



admin.site.register(Tag) # Another Method To Register A Model not Rcommanded