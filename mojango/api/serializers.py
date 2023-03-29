from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import Customer


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=150)
    password = serializers.CharField(min_length=8, max_length=128)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)

    class Meta:
        model = Customer
        fields = ['email', 'password', 'first_name', 'last_name']

    def validate(self, attrs):

        email_exists=Customer.objects.filter(email=attrs['email']).exists()
        if email_exists:
            raise ValidationError('Email already exists')

        return super().validate(attrs)


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            'id', 'first_name', 'last_name', 'email', 'password',
            'location',
        )
        
