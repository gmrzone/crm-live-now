from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # For all 4 Password Reset Views


urlpatterns = [
    path('', views.get_home, name='home'),
    path('user_home/', views.user_home, name='user_home'),
    path('login/', views.login_method, name='login'),
    path('logout/', views.logout_method, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('account_settings/', views.account_settings, name='account_settings'),
    path('products/', views.get_products, name='products'),
    path('customers/<str:id>', views.get_customers, name='afzal'),
    path('create_order/', views.create_order, name="create_order"),
    path('customers/place_order/<str:id>', views.create_order_customer, name="create_order_customer"),
    path('update_order/<str:id>', views.update_order, name='update_order'),         # using create_order template also for update order because both contain same form
    path('delete_order/<str:id>', views.delete_order, name='delete_order'),
    path('create_customer/', views.create_customer, name='create_customer'),
    path('update_customer/<str:id>', views.update_customer, name='update_customer'), # using create_customer template also for update Customer because both contain same form
    path('delete_customer/', views.delete_customer, name='delete_customer'),
    path('customers/place_multiple_orders/<str:id>', views.place_multiple_order, name='multiple_order'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/reset_password/reset_password.html'), name='reset_password'),
    path('reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/reset_password_confirm/reset_password_confirm.html'), name='password_reset_confirm'),
    path('reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/reset_password_done/reset_password_done.html'), name='password_reset_done'),
    path('reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/reset_password_complete/reset_password_complete.html'), name='password_reset_complete')
]
