import pdfkit
from docx import Document
from datetime import timedelta, datetime
from ..scripts import server_handler as SH
from shutil import copyfile
import os
from ..config import bucket as bucket
from ..config import core as core


class ContractBuilder:
    dict_sample_names = {
        'CONTRACT': 'contract.html',
    }

    __path_storage_prefix = f'/usr/local/share/minio/{bucket}'
    __path_sample_prefix = f'./{core}/scripts/sample'
    def __init__(self, *, path, type_report):

        self.path = path
        self.name_report = self.dict_sample_names.get(type_report)
        # путь для файла оконечный
        self.path = os.path.join(self.path, self.name_report)
        self.output_path = os.path.join(self.__path_storage_prefix, self.path)

        # проверяем есть ли в нашей ФС такой файл
        if os.path.isfile(os.path.join(self.__path_storage_prefix, self.path)):
            os.remove(os.path.join(self.__path_storage_prefix, self.path))
        os.makedirs(os.path.dirname(os.path.join(self.__path_storage_prefix, self.path)), exist_ok=True)
        with open(os.path.join(self.__path_sample_prefix, self.name_report), 'r', encoding='utf-8') as file:
            self.data = file.read()

    def executer_offer(self, *, fio: str, passport: str, passport_object: str, date: datetime) -> str:
        if date is None:
            date = datetime.now()

        self.data = self.data.replace('{FIO}', fio)
        self.data = self.data.replace('{DATE}',f'{str(date.day).zfill(2)}.{str(date.month).zfill(2)}.{date.year}')
        self.data = self.data.replace('{PASSPORT}', passport)
        self.data = self.data.replace('{PASSPORT_OBJECT}', passport_object)

        pdfkit.from_string(self.data,
                           os.path.splitext(self.output_path)[0]+'.pdf',
                           options={'page-size': 'Letter', 'margin-top': '0.2in', 'margin-right': '0.75in',
                                    'margin-bottom': '0.2in', 'margin-left': '0.75in'})

        return os.path.splitext(self.path)[0] + '.pdf'
