from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView,
)
from .views import (
    CustomerListView, CustomerCreateView, LoginView
)


urlpatterns = [
    path(
        'customer_list', 
        CustomerListView.as_view(), 
        name='customer_list'
    ),
    path(
        'customer_create', 
        CustomerCreateView.as_view(), 
        name='customer_create'
    ),
    path(
        'login', 
        LoginView.as_view(), 
        name='login'
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
