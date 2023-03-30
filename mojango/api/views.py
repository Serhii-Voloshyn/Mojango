from django.contrib.auth import authenticate
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import CustomerListSerializer, CustomerCreateSerializer
from .models import Customer
from .tokens import create_jwt_pair_for_user


class CustomerListView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerListSerializer


class CustomerCreateView(generics.CreateAPIView):
    serializer_class = CustomerCreateSerializer


class LoginView(views.APIView):
    permission_classes = []

    def post(self, request:Request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)
        if user is not None:
            tokens = create_jwt_pair_for_user(user)
            response = {
                'message': 'Login successful',
                'token': tokens,
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'Invalid email or password'}
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request:Request):
        content = {
            'user': str(request.user),
            'auth': str(request.auth),
        }
        return Response(data=content, status=status.HTTP_200_OK)
