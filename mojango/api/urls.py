from django.urls import path
from .views import CustomerView


urlpatterns = [
    path('customer_create', CustomerView.as_view(), name='customer_create')
]
