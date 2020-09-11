from django.db.models.signals import post_save
from .models import Customers
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.dispatch import receiver

#Sender is the model class which is saved, instance is instance of that model,  # if created is true means somthind new is created in db
# #created is a boolean if created its true else false, and **kwargs for extra keyargss


# def create_customer_profile(sender, instance, created, **kwargs):
#     if created:
#         Customers.objects.create(user=instance)
                                             
                                                             
       
                                                               
# post_save.connect(create_customer_profile, sender=User)

def add_to_group(sender, instance, created, **kwargs):
    if created:
        default_group = Group.objects.get(name = 'customer')
        instance.groups.add(default_group)
        Customers.objects.create(user=instance, name=instance.username, email=instance.email)


post_save.connect(add_to_group, sender=User)

@receiver(post_save, sender=User)
def update_customer(sender, instance, created, **kwargs):
    if not created:
        update_customer = Customers.objects.get(user_id=instance.id)  # Getting Customer whose username has been updated 
        update_customer.name = instance.username                       # assigning new username to customer name
        update_customer.save()                                         # Saving Changes
