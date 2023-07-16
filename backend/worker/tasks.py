from celery import shared_task
from captcha.models import CaptchaStore


@shared_task
def check_configs():
    print("executing task")


@shared_task
def delete_expired_captcha_objects():
    # delete expired captcha store objects
    CaptchaStore.remove_expired()
