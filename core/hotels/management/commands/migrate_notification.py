from django.core.management.base import BaseCommand
from tqdm import tqdm

from ...models import Manager, RoleManager


class Command(BaseCommand):
    help = "Миграция Главных менеджеров"

    def handle(self, *args, **options):

        for manager in tqdm(Manager.objects.filter(is_admin=False), desc="Обновление менеджеров"):
            RoleManager.objects.create(manager=manager, role="TASK_ARCHIVE")
            RoleManager.objects.create(manager=manager, role="TASK_EDIT")
