import requests
from django.conf import settings
from rest_framework import status


def text_xray(url):
    payload = {
        "url": url
    }
    result = requests.post(f"http://{settings.XRAY_HOST}:8001/run-test", json=payload)
    r = result.json()
    if result.status_code == status.HTTP_400_BAD_REQUEST:
        return False, r
    else:
        return True, r