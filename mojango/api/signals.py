from .models import OrderItem
from django.db.models.signals import pre_save
from django.dispatch import receiver
import logging


logger = logging.getLogger(__name__)


@receiver(pre_save, sender=OrderItem)
def notify_supplier(sender, instance, **kwargs):
    logger.info("Here must be an email notofication")
