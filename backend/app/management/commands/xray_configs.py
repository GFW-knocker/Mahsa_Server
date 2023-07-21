from django.core.management.base import BaseCommand
from worker.tasks import check_configs


class Command(BaseCommand):
    help = 'Run xray on all configs'

    def handle(self, *args, **options):
        check_configs.si().apply_async()