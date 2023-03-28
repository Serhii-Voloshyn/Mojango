from django.shortcuts import render
from rest_framework import generics
from .serializers import CustomerSerializer
from .models import Customer


class CustomerView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
