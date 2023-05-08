from rest_framework import serializers
from rest_framework.validators import ValidationError
from ..models import Customer


class CustomerCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=150)
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
    
    def create(self, validated_data):
        validated_data['is_active'] = False
        user = Customer.objects.create_user(**validated_data)

        return user


class CustomerGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = "__all__"


class CustomerUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=150)
    password = serializers.CharField(min_length=8, max_length=128)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    location = serializers.CharField(max_length=1000)
    phone = serializers.CharField(max_length=150)

    class Meta:
        model = Customer
        fields = "__all__"

    def validate(self, attrs):
        if 'email' in attrs:
            email_exists=Customer.objects.filter(email=attrs['email']).exists()
            if email_exists:
                raise ValidationError('Email already exists')

        return super().validate(attrs)
    
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            new_password = validated_data.pop('password')
            instance.update_password(new_password)
        return super().update(instance=instance, validated_data=validated_data)
