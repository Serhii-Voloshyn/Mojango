from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView,
)
from .views import (
    CustomerCreateView, LoginView, CustomerDeleteView,
    CustomerUpdateView, CustomerListAllView, CustomerListOneView,
    CustomerActivateView
)


urlpatterns = [
    path(
        'customer_create/', 
        CustomerCreateView.as_view(), 
        name='customer_create'
    ),
    path(
        'customer_get/', 
        CustomerListAllView.as_view(), 
        name='customer_get_all'
    ),
    path(
        'customer_get/<int:pk>/',
        CustomerListOneView.as_view(), 
        name='customer_get_one'
    ),
    path(
        'customer_delete/<int:pk>/', 
        CustomerDeleteView.as_view(), 
        name='customer_delete'
    ),
    path(
        'customer_update/<int:pk>/', 
        CustomerUpdateView.as_view(), 
        name='customer_update'
    ),
    path(
        'login/', 
        LoginView.as_view(), 
        name='login'
    ),
    path(
        'activate_customer/<uidb64>/<token>', 
        CustomerActivateView.as_view(), 
        name='activate'
    ),
    path(
        'jwt/token/', 
        TokenObtainPairView.as_view(), 
        name='token_obtain_pair'
    ),
    path(
        'jwt/token/refresh/', 
        TokenRefreshView.as_view(), 
        name='token_refresh'
    ),
    path(
        'jwt/token/verify/', 
        TokenVerifyView.as_view(), 
        name='token_verify'
    ),
]
