from django.urls import path
from .views import CustomerListView, SignUpView


urlpatterns = [
    path('customer_list', CustomerListView.as_view(), name='customer_list'),
    path('sign_up', SignUpView.as_view(), name='sign_up'),
]
