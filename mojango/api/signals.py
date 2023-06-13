from .models import OrderItem
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .tasks import send_activate_email_task, send_supplier_notification_email_task

import logging



logger = logging.getLogger(__name__)


@receiver(pre_save, sender=OrderItem)
def notify_supplier(sender, instance, **kwargs):
    supplier = instance.product_id.supplier_id

    send_supplier_notification_email_task.delay(
        supplier.id,
        supplier.email
    )
