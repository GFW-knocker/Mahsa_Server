import uuid as uuid
from django.db import models

PROTOCOL_CHOICES = (
    ('vm', 'VMESS'),
    ('vl', 'VLESS'),
)


class Config(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    protocol = models.CharField(max_length=2, choices=PROTOCOL_CHOICES)
    url = models.CharField(max_length=1024, unique=True)
    hash = models.CharField(max_length=32, db_index=True, unique=True)
    ads_url = models.CharField(max_length=255)
    # number of time that a config is consumed (provided as free config to app)
    num_consumed = models.PositiveIntegerField(default=0)
    xray_score = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    expired_at = models.DateTimeField()
    last_tested_at = models.DateTimeField(default=None, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # optional fields
    use_fragment = models.BooleanField(default=False)
    use_cdn = models.BooleanField(default=False)
    use_random_subdomain = models.BooleanField(default=False)
    num_fragment = models.PositiveIntegerField(null=True, blank=True)


class Report(models.Model):
    config = models.ForeignKey(Config, related_name='reports', on_delete=models.CASCADE)
    client_ip = models.CharField(max_length=255)
    subnet_ip = models.CharField(max_length=255)
    ping_ms = models.IntegerField()
    fragment_switch = models.BooleanField()
    cdn_ip = models.CharField(max_length=255)
    ads_report = models.BooleanField()
    user_rating = models.IntegerField(choices=[(x, x) for x in range(1, 6)])
    app_version = models.CharField(max_length=255)
    os_type = models.CharField(max_length=255)
    os_version = models.CharField(max_length=255)
    reported_at = models.DateTimeField(auto_now_add=True)

