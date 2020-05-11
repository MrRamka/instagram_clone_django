import os
import sys

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'instagram_clone_django.settings')
app = Celery('stat', broker=settings.CELERY_BROKER_URL)
app.config_from_object('django.conf:settings')

app.conf.CELERYBEAT_SCHEDULE = {
    "Save stat": {
        "task": "core.tasks.update_statistics",
        "schedule": 300.0
    }
}

app.autodiscover_tasks()

# celery worker -A instagram_clone_django -l info --pool=solo
# celery -A instagram_clone_django beat -l info
# flower -A instagram_clone_django
