import datetime
import logging

from captcha.models import CaptchaStore
from django.db.models import Avg
from pytz import UTC
from rest_framework import serializers
from utils import text_xray
from .models import Config, Report
from .utils import calculate_md5, validate_ip_address, get_protocol

logger = logging.getLogger(__name__)


class RetrieveConfigSerializer(serializers.ModelSerializer):
    protocol = serializers.SerializerMethodField(read_only=True)
    reports_count = serializers.SerializerMethodField(read_only=True)
    average_users_rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Config
        fields = ['uuid', 'url', 'ads_url', 'expired_at', 'created_at', 'is_verified',
                  'protocol', 'xray_result', 'last_xray_run', 'reports_count', 'average_users_rating']

    def get_protocol(self, instance):
        return instance.get_protocol_display()

    def get_reports_count(self, instance):
        return instance.reports.count()

    def get_average_users_rating(self, instance):
        return instance.reports.aggregate(Avg('user_rating'))['user_rating__avg']


class HitMeConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = ['url', 'ads_url']


class CreateConfigSerializer(serializers.ModelSerializer):
    captcha = serializers.CharField(write_only=True)
    captcha_key = serializers.CharField(write_only=True)

    class Meta:
        model = Config
        fields = ['url', 'ads_url', 'expired_at', 'protocol',
                  'use_fragment', 'num_fragment', 'use_cdn', 'use_random_subdomain',
                  'captcha', 'captcha_key']

    def validate_url(self, value):
        if get_protocol(value) is None:
            raise serializers.ValidationError("Invalid Link! Link must start with vmess:// or vless://")
        return value

    def validate_ads_url(self, value):
        if False:
            raise serializers.ValidationError("ads_url is not valid")
        return value

    def validate_expired_at(self, value):
        if False:
            raise serializers.ValidationError("expired_at is not valid")
        return value

    def validate(self, data):
        # validate non-field form logic
        # validate captcha
        try:
            stored_captcha = CaptchaStore.objects.get(hashkey=data['captcha_key'])
            if stored_captcha.challenge.lower() != data['captcha'].lower():
                raise serializers.ValidationError("Captcha is not valid!")
        except CaptchaStore.DoesNotExist:
            raise serializers.ValidationError("Captcha is not valid!")
        stored_captcha.delete()  # delete the used captcha

        # make sure a config with this hash is not existed already.
        try:
            Config.objects.get(hash=calculate_md5(data['url']))
            raise serializers.ValidationError("Config with this URL is already existed!")
        except Config.DoesNotExist:
            pass

        # test the config link with XRay
        success, result = text_xray(data['url'])
        data['xray_result'] = result
        data['last_xray_run'] = datetime.datetime.now(tz=UTC)
        if not success:
            logger.error(f"xray failed - {result}")
            raise serializers.ValidationError(
                "Config did not pass the XRay Test! please make sure the config is working!"
            )

        return data

    def create(self, validated_data):
        # Call the parent create() method to save the instance
        validated_data['hash'] = calculate_md5(validated_data['url'])
        validated_data['protocol'] = get_protocol(validated_data['url'])
        del validated_data['captcha']
        del validated_data['captcha_key']
        instance = super().create(validated_data)

        return instance


class CreateReportSerializer(serializers.ModelSerializer):
    config_hash = serializers.CharField(write_only=True)

    class Meta:
        model = Report
        fields = ['client_ip', 'subnet_ip', 'cdn_ip', 'ping_ms',
                  'fragment_switch', 'user_rating', 'app_version',
                  'os_type', 'os_version', 'config_hash', 'ads_report']

    def validate_client_ip(self, value):
        if not validate_ip_address(value):
            raise serializers.ValidationError("client_ip ip is not valid")
        return value

    def validate_subnet_ip(self, value):
        if not validate_ip_address(value):
            raise serializers.ValidationError("subnet_ip ip is not valid")
        return value

    def validate_cdn_ip(self, value):
        if not validate_ip_address(value):
            raise serializers.ValidationError("cdn_ip ip is not valid")
        return value

    def validate_config_hash(self, value):
        try:
            # try to find the config in db
            Config.objects.get(hash=value)
            return value
        except Config.DoesNotExist:
            raise serializers.ValidationError("cannot find the config using hash!")

    # other validation functions go here

    def create(self, validated_data):
        # Call the parent create() method to save the instance
        config = Config.objects.get(hash=validated_data['config_hash'])
        validated_data['config'] = config
        del validated_data['config_hash']  # config_hash is not a valid field in the report model
        instance = super().create(validated_data)

        return instance