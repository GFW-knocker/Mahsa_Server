from django.db import models


class Config(models.Model):
    protocol = models.CharField(max_length=255)
    hash = models.CharField(max_length=32)
    base64 = models.TextField()
    ads = models.TextField()
    created_at = models.DateTimeField()
    edited_at = models.DateTimeField()
    expired_at = models.DateTimeField()


class Report(models.Model):
    config = models.ForeignKey(Config, related_name='configs', on_delete=models.CASCADE)
    hash_config = models.CharField(max_length=255)
    client_ip = models.CharField(max_length=255)
    subnet_ip = models.CharField(max_length=255)
    reported_at = models.DateTimeField()
    ping_ms = models.IntegerField()
    fragment_switch = models.BooleanField()
    cdn_ip = models.CharField(max_length=255)
    ads_report = models.BooleanField()
    user_rating = models.IntegerField()
    app_version = models.CharField(max_length=255)
    os_type = models.CharField(max_length=255)
    os_version = models.CharField(max_length=255)

