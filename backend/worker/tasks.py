import os
import random
from datetime import datetime
import requests
from celery import group
from captcha.models import CaptchaStore
from celery.utils.log import get_task_logger
from django.conf import settings
from pytz import UTC

from app.models import Config
from utils import text_xray
from worker.app import celery_app

logger = get_task_logger(__name__)


@celery_app.task
def run_xray_test(uuid):
    config = Config.objects.get(uuid=uuid)
    result = None
    success = False
    try:
        success, result = text_xray(config.url)
    except ConnectionError as e:
        logger.error(f"Connection error: {e}")

    logger.info(f"result: {result}")
    config.xray_result = result
    config.last_xray_run = datetime.now(tz=UTC)
    config.save()

    return result  # can check this result in flower


@celery_app.task
def check_configs():
    # worker_number = celery_app.control.inspect().stats()
    pid = os.getpid()
    logger.info(f"start testing all configs with xray - {pid}")
    tasks = []
    for config in Config.objects.all():
        logger.info(f"run xray on config {config.uuid} - {config.url}")
        tasks.append(run_xray_test.si(str(config.uuid)))
    group(tasks).apply_async()
    logger.info(f"{len(tasks)} tasks created!")


@celery_app.task
def delete_expired_captcha_objects():
    # delete expired captcha store objects
    CaptchaStore.remove_expired()
