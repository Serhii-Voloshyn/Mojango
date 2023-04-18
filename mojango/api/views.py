from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers.CustomerSerializers import (
    CustomerCreateSerializer, CustomerUpdateSerializer, CustomerGetSerializer
)
from .models import Customer
from .tokens import create_jwt_pair_for_user


class CustomerCreateView(generics.CreateAPIView):
    serializer_class = CustomerCreateSerializer


class CustomerListAllView(generics.ListAPIView):
    serializer_class = CustomerGetSerializer
    queryset = Customer.objects.all()


class CustomerListOneView(generics.ListAPIView):
    serializer_class = CustomerGetSerializer

    def get(self, request, pk):
        response = self.get_serializer(get_object_or_404(Customer, id=pk)).data
        return Response(response)


class CustomerUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = CustomerUpdateSerializer
    queryset = Customer.objects.all()

    def put(self, request, pk):

        if request.user.id != pk:
            response = {'message': 'You don\'t have permissions'}
            return Response(data=response, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        user = get_object_or_404(Customer, id=pk)
        serializer = CustomerUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {'message': 'Updated successfuly'}
            return Response(data=response, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated,]
    
    def delete(self, request:Request, pk):

        if request.user.id != pk and not request.user.is_staff:
            response = {'message': 'You don\'t have permissions'}
            return Response(data=response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        customer = get_object_or_404(Customer, id=pk)
        customer.is_active = False
        customer.save()

        response = {'message': 'Successfuly deleted'}
        return Response(data=response, status=status.HTTP_204_NO_CONTENT)


class LoginView(views.APIView):

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

    def get(self, request: Request):

        if request.user.id:
            content = {"user": str(request.user), "auth": str(request.auth)}

            return Response(data=content, status=status.HTTP_200_OK)
        else:
            response = {"message": "You aren't authorized to refresh tokens"}
            return Response(data=response, status=status.HTTP_401_UNAUTHORIZED)
