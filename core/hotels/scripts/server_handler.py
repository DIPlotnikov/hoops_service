import io

from minio import Minio
import datetime
import urllib3
from django.conf import settings
from ..scripts import exception_handler as EH


class minioDocuments(object):
    def __init__(self):

        __SERVER_MINIO = settings.MINIO_SERVER
        __ACCESS_KEY_MINIO = settings.MINIO_ACCESS_KEY
        __SECRET_KEY_MINIO = settings.MINIO_SECRET_KEY
        self.prefix = settings.MINIO_PREFIX
        self.bucket = settings.MINIO_BUCKET

        httpClient = urllib3.PoolManager(
            cert_reqs="CERT_NONE")

        try:
            self.client = Minio(
                __SERVER_MINIO,
                access_key=__ACCESS_KEY_MINIO,
                secret_key=__SECRET_KEY_MINIO,
                secure=False,
                http_client=httpClient,)

        except Exception as e:
            print(str(e))
            raise ValueError('медиа данные не доступны!')

    def getUrlForFile(self, path, delta=datetime.timedelta(days=7), response_headers=None):
        try:
            path = self.client.presigned_get_object(self.bucket, path, delta, response_headers=None)
            return path
        except Exception as e:
            print(str(e))
            raise EH.customError('Ошибка', 'медиа данные не доступны.')

    def getUrlForUploadFile(self, path, delta=datetime.timedelta(minutes=2)):
        try:
            return self.client.presigned_put_object(self.bucket, path, delta)
        except Exception as e:
            raise EH.customError('Ошибка', 'медиа данные не доступны')

    def deleteFile(self, path):
        try:
            self.client.remove_object(self.bucket, path)
        except Exception as e:
            print(str(e))
            raise EH.customError('Ошибка', 'медиа данные не доступны..')

    def put(self, key, data):
        if type(data) is not bytes:
            data = data.encode('windows-1251')
        data_io = io.BytesIO(data)
        self.client.put_object(self.bucket, key, data_io, length=len(data))


if __name__ == '__main__':
    print(minioDocuments().getUrlForFile('temp.name'))