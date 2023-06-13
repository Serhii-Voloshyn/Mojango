from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.sites.shortcuts import get_current_site

from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from .serializers.CustomerSerializers import (
    CustomerCreateSerializer, CustomerUpdateSerializer, CustomerGetSerializer,
)
from .serializers.OrderSerializers import (
    OrderCreateSerializer
)
from .serializers.OrderItemSerializers import (
    OrderItemCreateSerializer
)
from .serializers.ProductSerializers import (
    ProductCreateSerializer
)

from .models import Customer, Order, OrderItem, Product
from .tokens import create_jwt_pair_for_user, account_activation_token
from .tasks import send_activate_email_task

import logging


logger = logging.getLogger(__name__)


class CustomerActivateView(generics.RetrieveAPIView):
    serializer_class = CustomerGetSerializer

    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            response = {'message': 'Activated successfuly'}
            return Response(data=response, status=status.HTTP_201_CREATED)

        response = {'message': 'Activation denied'}
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class CustomerCreateView(generics.CreateAPIView):
    serializer_class = CustomerCreateSerializer

    def post(self, request):
        serializer = self.get_serializer(
            data=request.data
        )

        if serializer.is_valid():
            user = serializer.save()
            if send_activate_email_task.delay(
                get_current_site(request).domain,
                request.is_secure(),
                user.id, user.email
            ):
                response = {'message': 'Created successfuly'}
                return Response(data=response, status=status.HTTP_201_CREATED)
            else:
                user.delete()
                response = {'message': 'Email wasn\'t sent'}
                return Response(data=response, status=status.status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerListAllView(generics.ListAPIView):
    serializer_class = CustomerGetSerializer
    queryset = Customer.objects.all()


class CustomerListOneView(generics.ListAPIView):
    serializer_class = CustomerGetSerializer

    def get(self, request, pk):
        response = self.get_serializer(get_object_or_404(Customer, id=pk)).data
        return Response(response, status=status.HTTP_200_OK)


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


class CreateOrderView(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):

        user = self.request.user
        return Order.objects.get(customer_id=user.id)
    

class CreateItemView(generics.CreateAPIView):
    serializer_class = OrderItemCreateSerializer
    permission_classes = [IsAuthenticated,]


class CreateProductView(generics.CreateAPIView):
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAuthenticated, ]


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
