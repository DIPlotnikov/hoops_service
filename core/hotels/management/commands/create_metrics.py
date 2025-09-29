from django.core.management.base import BaseCommand

from executor.models import Metrics
from ...models import Executer, ExecuterState


class Command(BaseCommand):
    help = "Заполнение метрик Исполнителя"

    def handle(self, *args, **options):
        ee = Executer.objects.filter(is_active=True)
        for e in ee:
            es = ExecuterState.objects.filter(executer=e).last()
            if not es:
                continue
            Metrics.objects.create(executor=e, last_request_task=es.task.start_at)
