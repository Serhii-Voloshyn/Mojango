from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import CustomerSerializer, SignUpSerializer
from .models import Customer


class CustomerListView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class SignUpView(generics.CreateAPIView):
    serializer_class = SignUpSerializer
