import django_filters
from .models import *


class OrderFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='date_created', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='date_created', lookup_expr='lte')  
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created']


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    class Meta:
        model = Products
        fields = ['price', 'category', 'tag']