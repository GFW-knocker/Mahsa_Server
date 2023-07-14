from django.contrib import admin
from app.models import Config, Report


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    pass


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    pass