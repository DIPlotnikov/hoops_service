import random
import uuid

from django.core.management.base import BaseCommand
from tqdm import tqdm

from ...models import PassportData, Executer, SimpleRequisite


class Command(BaseCommand):
    help = "Заполнение фейковых данных"

    def handle(self, *args, **options):
        passport_data = PassportData.objects.all()
        for pd in tqdm(passport_data, desc="passport data"):
            random_number = random.randint(0, 1000)
            pd.series = random_number
            pd.number = str(random_number + 1)
            pd.issued_by = "Отделом УФМС России"
            pd.subdivision_code = str(random_number - 1)
            pd.save()
            if pd.firstPage:
                fi = pd.firstPage
                fi.url = str(uuid.uuid4())
                fi.save()
            if pd.secondPage:
                fi = pd.secondPage
                fi.url = str(uuid.uuid4())
                fi.save()
        executers = Executer.objects.all()

        for executer in tqdm(executers, desc="executors data"):
            executer.phone_number = executer.phone_number[2:]
            executer.phone_number = executer.phone_number[::-1]
            executer.save()

        sqs = SimpleRequisite.objects.all()
        for sq in tqdm(sqs, desc="executor bank data"):
            sq.card_number = sq.card_number[::-1]
            sq.save()
