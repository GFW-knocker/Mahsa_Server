from datetime import datetime
from celery import shared_task
from captcha.models import CaptchaStore
from celery.utils.log import get_task_logger
from app.models import Config

logger = get_task_logger(__name__)


def xray_config(config):
    # run xray
    # calculate a simple score between 0 and 1 based on download/upload speed and other factors
    score = 1  # score=0 means xray test failed!
    return score


@shared_task
def check_configs():
    logger.info("start testing all configs with xray")
    for config in Config.objects.all():
        logger.info(f"testing {config.url} with xray")
        score = xray_config(config)
        logger.info(f"score: {score}")
        config.xray_score = score
        config.last_tested_at = datetime.now()
        config.save()
    logger.info("all done.")


@shared_task
def delete_expired_captcha_objects():
    # delete expired captcha store objects
    CaptchaStore.remove_expired()
