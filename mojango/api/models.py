from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser has to have is_staff being True')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser has to have is_superuser being True')

        return self.create_user(email=email, password=password, **extra_fields)


class Customer(AbstractUser):
    username = None
    email = models.EmailField(max_length=150, unique=True)
    location = models.TextField(max_length=1000, null=True)
    phone_number = PhoneNumberField(blank=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    def update_password(self, new_password):
        self.set_password(new_password)
        self.save()

    def __str__(self):
        return self.email


class Order(models.Model):

    class OrderStatus(models.TextChoices):
        UNPURCHASED = 'Unpurchased'
        PURCHASED = 'Purchased'
        DENIED = 'Denied'
        COMPLETED = 'Completed'

    customer_id = models.ForeignKey(
        Customer,
        related_name='order_customer',
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    purchased_at = models.DateTimeField(null=True)

    status = models.CharField(
        max_length = 11,
        choices=OrderStatus.choices,
        default=OrderStatus.UNPURCHASED,
    )

    description = models.TextField(max_length=2000)


class Product(models.Model):

    supplier_id = models.ForeignKey(
        Customer,
        related_name='product_supplier',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=1000)
    price = models.FloatField(
        validators=[MinValueValidator(0)]
    )
    is_aviable = models.BooleanField(default=False)
    description = models.TextField(max_length=2000)


class OrderItem(models.Model):
    order_id = models.ForeignKey(
        Order,
        related_name='order_item',
        on_delete=models.CASCADE
    )
    product_id = models.ForeignKey(
        Product,
        related_name='product_item',
        on_delete=models.CASCADE
    )
    amount = models.IntegerField(
        validators=[MinValueValidator(0)]
    )


class Message(models.Model):

    class MessageStatus(models.TextChoices):
        SENT = "Sent"
        RECEIVED = "Received"
        READ = "Read"
        DENIED = "DENIED"

    sender_id = models.ForeignKey(
        Customer,
        related_name='message_sender',
        on_delete=models.CASCADE
    )
    receiver_id = models.ForeignKey(
        Customer,
        related_name='message_receiver',
        on_delete=models.CASCADE
    )
    message = models.TextField(max_length=2000)
    date_sent = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=8,
        choices=MessageStatus.choices,
        default=MessageStatus.SENT
    )
