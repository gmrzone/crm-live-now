from django.http import HttpResponse
from django.shortcuts import redirect

# Decorater for restricting logged in user to access certain page
def authenticated_user(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:       # if user is Authenticated redirect user to home page
            return redirect('home')
        else:                                   # if user is not run view function
            return view_func(request, *args, **kwargs)
    return wrapper


# Decorater for restricting unauthenticated user to access certain page
def unauthenticated_user(redirect_url):       # Creating Decorator inside a function because decorators can only have functions as arguement and we wanted to add redirect url arguement
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(redirect_url)
            else:
                return view_func(request, *args, **kwargs)
                
        return wrapper
    return decorator

def allowed_profile(profiles: list, redirect_url): # Ristrict Access Based on group created in admin profile = [admins, customers, delivery staff]
    def decorator(view_funct):
        def wrapper(request, *args, **kwargs):
            user_group = None
            if request.user.groups.exists():                    # Check if request.user has group
                user_group = request.user.groups.all()[0].name        # getting all group and slice Name of Group bcoz user can have multiple groups 
            if user_group not in profiles:                 # Check if Group is in Allowed Profiles
                return redirect(redirect_url)
            else:
                return view_funct(request, *args, **kwargs)
        return wrapper
    return decorator
