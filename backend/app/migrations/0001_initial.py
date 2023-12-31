# Generated by Django 4.2.3 on 2023-07-20 21:39

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('protocol', models.CharField(choices=[('vm', 'VMESS'), ('vl', 'VLESS'), ('tr', 'Trojan'), ('wg', 'Wireguard'), ('ss', 'ShadowSocks'), ('sc', 'SOCKS')], max_length=2)),
                ('url', models.CharField(max_length=1024, unique=True)),
                ('hash', models.CharField(db_index=True, max_length=32, unique=True)),
                ('ads_url', models.CharField(max_length=255)),
                ('num_consumed', models.PositiveIntegerField(default=0)),
                ('xray_result', models.JSONField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('edited_at', models.DateTimeField(auto_now=True)),
                ('expired_at', models.DateTimeField()),
                ('last_xray_run', models.DateTimeField(blank=True, default=None, null=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('use_fragment', models.BooleanField(default=False)),
                ('use_cdn', models.BooleanField(default=False)),
                ('use_random_subdomain', models.BooleanField(default=False)),
                ('num_fragment', models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_ip', models.CharField(max_length=255)),
                ('subnet_ip', models.CharField(max_length=255)),
                ('ping_ms', models.IntegerField()),
                ('fragment_switch', models.BooleanField()),
                ('cdn_ip', models.CharField(max_length=255)),
                ('ads_report', models.BooleanField()),
                ('user_rating', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('app_version', models.CharField(max_length=255)),
                ('os_type', models.CharField(max_length=255)),
                ('os_version', models.CharField(max_length=255)),
                ('reported_at', models.DateTimeField(auto_now_add=True)),
                ('config', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='app.config')),
            ],
        ),
    ]
