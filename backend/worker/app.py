

# Create a Celery app instance
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

app = Celery('app',
             broker_connection_retry=False,
             broker_connection_retry_on_startup=True,)

# Configure Celery
app.conf.broker_url = f'redis://{settings.REDIS_HOST}:6379/0'
app.conf.result_backend = app.conf.broker_url

app.conf.beat_schedule = {
    'check-configs-every-hour': {
        'task': 'worker.tasks.check_configs',
        'schedule': crontab(hour='*/1')
    },
    'delete-expired-captcha': {
        'task': 'worker.tasks.delete_expired_captcha_objects',
        'schedule': crontab(hour='*/1')
    },
}

# Optional: Set other Celery configuration options
# app.conf.task_default_queue = 'default'
# app.conf.worker_prefetch_multiplier = 1
# ...

# Define the tasks module to include
app.autodiscover_tasks(['worker'])


