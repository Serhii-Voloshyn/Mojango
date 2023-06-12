from django.apps import AppConfig
from django.db.models.signals import pre_save
#from .models import OrderItem


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        from .signals import notify_supplier
