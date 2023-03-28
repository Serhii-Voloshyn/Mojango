from django.db import models


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=50)
    created_at = models.DateField(auto_now_add=True)
    location = models.TextField(max_length=1000)
    status = models.CharField(max_length=100)



