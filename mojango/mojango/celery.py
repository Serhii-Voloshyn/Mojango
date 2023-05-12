from __future__ import absolute_import, unicode_literals

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mojango.settings')
from celery import Celery

app = Celery('mojango')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()