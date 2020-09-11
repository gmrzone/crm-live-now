from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Products, Customers, Order
from .forms import Order_form, Customer_form, Customer_delete, SignUp, ProfileForm # Importing all forms from forms.py
from django.contrib.auth.forms import UserCreationForm   # django default user Creation Form
from django.contrib.auth import authenticate, login, logout # This Import is Used to Authenticate user and login them and logout them
from django.contrib import messages   # importing django flash message to display on sucesss
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group # importing group model to assign customer group to new user as soon as they signup so they can visit user_home page
from .filters import OrderFilter, ProductFilter  # Importing all filters from filters.py
from django.forms import inlineformset_factory  # to rendr multiple forms based on single form
from .decorators import authenticated_user    # Decorater Created in decorator.py for restricting login user to access login and signup page
from .decorators import unauthenticated_user    # Decorater for restricting unauthenticated user to access certain page
from .decorators import allowed_profile # This decorator Ristrict Access Based on group created in admin profile = [admins, customers, delivery staff]
# Create your views here.

@authenticated_user  # DECORATOR FUNCTION TO RISTRICT LOGIN USER TO ACCESS LOGIN PAGE
def login_method(request):
    if request.method == "POST":
        username = request.POST.get('username') # request.POST will return all input fields data as dictionary and the key will be name attribute of input field in login.html.
        password = request.POST.get('password') # using dictionary get() method to get value of key without getting error if key doesnot exist

        auth_user = authenticate(request, username=username, password=password)
        if auth_user is not None: # if user is Authenticated it will return authenticated user object use login(request, auth_user)
            login(request, auth_user)
            return redirect('home')
        else: # if auth_user is None Which Means Username or Password is Incorrect
            messages.info(request, 'Username or Password Incorrect')
            
    context = {}
    return render(request, 'accounts/login/login.html', context)

def logout_method(request):
    if request.user.is_authenticated:
        username = request.user.username          # Getting username of Request User
        messages.success(request, 'User {0} Successfully Logged Out.'.format(username))
        logout(request)      
    else:
        pass
    return redirect('login')

# Old Signup View without post_save signal for creating customer profile and add user to group
# @authenticated_user     # DECORATOR FUNCTION TO RISTRICT LOGIN USER TO ACCESS SIGNUP PAGE
# def signup(request):
#     signup_form = SignUp()
#     if request.method == 'POST':
#         signup_form = SignUp(request.POST)
#         if signup_form.is_valid():
#             new_user = signup_form.save()  # Assigning new signup user object to a variable so we can assign group to this user
#             newuser_group = Group.objects.get(name='customer') # Getting customer group object USING NAME PERAMETER
#             new_user.groups.add(newuser_group) # Assingning customer group to new user
#             # Creating a customer profile for user during signup
#             username = signup_form.cleaned_data.get('username') # Extracting cleaned username from signup_form using get
#             email = signup_form.cleaned_data.get('email')       # Extracting cleaned email from signup_form using get
#             Customers.objects.create(user=new_user,name=username, email=email)
#             messages.success(request, 'Account Was Created Sucessfully For {0} You Can Login Now'.format(username))
#             return redirect('login')
#     context = {'signup_form': signup_form}
#     return render(request, 'accounts/signup/signup.html', context)


@authenticated_user     # DECORATOR FUNCTION TO RISTRICT LOGIN USER TO ACCESS SIGNUP PAGE
def signup(request):
    signup_form = SignUp()
    if request.method == 'POST':
        signup_form = SignUp(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            username = signup_form.cleaned_data.get('username') # Extracting cleaned username from signup_form using get
            messages.success(request, 'Account Was Created Sucessfully For {0} You Can Login Now'.format(username))
            return redirect('login')
    context = {'signup_form': signup_form}
    return render(request, 'accounts/signup/signup.html', context)


# @login_required(login_url='login')
@unauthenticated_user('login')  # Decorater for restricting unauthenticated user to access certain page created in decorators.py
@allowed_profile(['admin'], redirect_url='user_home')
def get_home(request):
    customers = Customers.objects.all()
    orders = Order.objects.all()
    order_count = orders.count()
    order_delivered = Order.objects.filter(status='Delivered').count()
    order_pending = Order.objects.filter(status='Pending').count()
    filter_form = OrderFilter(request.GET, queryset=orders)
    content = {'order_list': orders, 'order_count': order_count, 'order_delivered': order_delivered, 
               'order_pending': order_pending, 'customers_list': customers, 'order_filter_form': filter_form}
    return render(request, 'accounts/home/admin_home.html', content)

@login_required(login_url='login')
@allowed_profile(['customer', 'delivery', 'admin'], redirect_url='home')
def user_home(request):
    user_orders = request.user.customers.order_set.all()    # Getting all order of login Customer using one to one relation
    order_count = user_orders.count()
    order_delivered = user_orders.filter(status='Delivered').count()
    order_pending = user_orders.filter(status='Pending').count()
    context = {'order_list': user_orders, 'order_count': order_count, 'order_delivered': order_delivered, 
               'order_pending': order_pending}
    return render(request, 'accounts/home/user_home.html', context)


@login_required(login_url='login')
def get_products(request):
    products = Products.objects.all()
    Product_filter = ProductFilter(request.GET, queryset=products) # This Will Filter products based on request.GET if there is filter data submited through form
    context = {'Product_filter': Product_filter}                    # if no filter field is selected it wont filter anything from queryset you can access filtered data using 
    return render(request, 'accounts/products/products.html', context)# Product_filter.qs

@login_required(login_url='login')
def get_customers(request, id):
    customer = Customers.objects.get(id=id)
    order_filter = OrderFilter(request.GET, queryset=customer.order_set.all()) # This Will Filter All order From Queryset based on request.GET 
    content = {"customers_detail": customer, 'filterform': order_filter}       # which will be whatever filter we applied during search
    return render(request, "accounts/customers/customers.html", content)


@login_required(login_url='login')
def account_settings(request):
    target_customer = request.user.customers
    profile_form = ProfileForm(instance=target_customer)  # Getting profile form with target_customer Details So We Can Update
    if request.method == "POST": # if there is submit POST request
        profile_form = ProfileForm(request.POST, request.FILES, instance=target_customer) # Create Another Instance With request.POST to save 
        if profile_form.is_valid():
            profile_form.save()
    customer_designation = request.user.groups.all()[0]   # Getting first group of login user
    context = {'profile_form': profile_form, 'designation': customer_designation}
    return render(request, 'accounts/account_settings/account_settings.html', context)


@login_required(login_url='login')
def create_order(request):
    form = Order_form()
    if request.method == 'POST':
        form = Order_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    content = {'Order_form': form}
    return render(request, 'accounts/create_order/create_order.html', content)

@login_required(login_url='login')
def update_order(request, id):
    selected_order = Order.objects.get(id=id)
    form = Order_form(instance=selected_order)
    if request.method == 'POST':
        form = Order_form(request.POST, instance=selected_order)
        if form.is_valid():
            form.save()
            return redirect('/')
    content = {'Order_form': form}
    return render(request, 'accounts/create_order/create_order.html', content)

@login_required(login_url='login')
def delete_order(request, id):
    order = Order.objects.get(id=id)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    content = {'order': order}
    return render(request, 'accounts/delete_order/delete_order.html', content)

@login_required(login_url='login')
def create_customer(request):
    form = Customer_form()
    if request.method == 'POST':
        form = Customer_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    content = {'form': form}
    return render(request, 'accounts/create_customer/create_customer.html', content)

@login_required(login_url='login')
def update_customer(request, id):
    selected_customer = Customers.objects.get(id=id)
    form = Customer_form(instance=selected_customer)
    if request.method == 'POST':
        form = Customer_form(request.POST, instance=selected_customer)
        if form.is_valid():
            form.save()
            return redirect('/')
    content = {"form": form}
    return render(request, 'accounts/create_customer/create_customer.html', content)

@login_required(login_url='login')
def delete_customer(request):
    form = Customer_delete()
    
    if request.method == 'POST':
        selected_customer = Customers.objects.get(id=request.POST['customer']) # request.POST returns a dictionary 'customer' is key and value is selected customer id
        selected_customer.delete()
        return redirect('/')
    context = {'del_form': form}
    return render(request, 'accounts/delete_customer/delete_customer.html', context)

@login_required(login_url='login')
def create_order_customer(request, id):
    selected_customer = Customers.objects.get(id=id)
    form = Order_form(initial={'customer': selected_customer}) # Adding customers initials to order form will select selected customer in order form
    if request.method == 'POST':
        form = Order_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    content = {'Order_form': form, 'selected_cust': selected_customer}
    return render(request, 'accounts/create_order/create_order.html', content)

@login_required(login_url='login')  
def place_multiple_order(request, id):
    OrderFormSet = inlineformset_factory(Customers, Order, fields=('products', 'status'), extra=5)
    selected_customer = Customers.objects.get(id=id)
    form_set = OrderFormSet(queryset=Order.objects.none(), instance=selected_customer) # this queryset will tet not to have any instance which is same as removing instance
    if request.method == "POST":
        form_set = OrderFormSet(request.POST, instance=selected_customer)
        if form_set.is_valid():
            form_set.save()
            return redirect('/')


    context = {'Order_form_set': form_set, 'selected_cust': selected_customer}
    return render(request, 'accounts/create_order/create_order.html', context)
