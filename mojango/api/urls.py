from django.urls import path
from .views import CustomerListView, CustomerCreateView, LoginView


urlpatterns = [
    path('customer_list', CustomerListView.as_view(), name='customer_list'),
    path('customer_create', CustomerCreateView.as_view(), name='customer_create'),
    path('login', LoginView.as_view(), name='login')
]
