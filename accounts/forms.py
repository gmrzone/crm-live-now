from django.forms import ModelForm
from .models import Order, Customers
from django.contrib.auth.forms import UserCreationForm # Importing django default user creation form
from django.contrib.auth.models import User # importing user model so we can sue it inside our class model

class Order_form(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class Customer_form(ModelForm):
    class Meta:
        model = Customers
        fields = ['name', 'phone', 'email']

class ProfileForm(ModelForm):
    class Meta:
        model = Customers
        fields = '__all__'
        exclude = ['user']
        
class Customer_delete(ModelForm):
    class Meta:
    # adding model as Order because order has a attribute customer which inherits Customer Model and we can get id of customer 
    # and this will also give drop down input field for customer with all customers list to select 
        model = Order 
        fields = ['customer']

# Customizing django default usercreation form

class SignUp(UserCreationForm):
    class Meta:
        model = User
        fields = ['username',  'email', 'password1', 'password2']


