from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    'app',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    broker_connection_retry_on_startup=True
)

celery_app.conf.beat_schedule = {
    'check-bookings-every-minute': {
        'task': 'check_bookings',
        'schedule': crontab(minute='*'),
    },
}

celery_app.conf.imports = ('app.tasks.booking_tasks',)
