import graphene

from ...schema_handler import is_admin
from ....config import bucket as bucket
import uuid

from ....models import RoleAdmin
from ....scripts import server_handler as SH
import time
from ...agreement.input import InputTypeMedia


class AdminUploadMedia(graphene.Mutation):
    class Arguments:
        input = InputTypeMedia(required=True)

    url = graphene.String(required=True, description='URL для FileInfo')
    path = graphene.String(required=True, description='Путь для PUT')

    @staticmethod
    def mutate(root, info, input):
        is_admin(info=info, permission=[RoleAdmin.Roles.SEO.value, RoleAdmin.Roles.CUSTOMER.value, RoleAdmin.Roles.EXECUTER.value, RoleAdmin.Roles.DOCUMENT.value, RoleAdmin.Roles.SETTINGS.value])
        server = SH.minioDocuments()
        path = f'admin/{input.type}/{str(int(time.time()))}/{uuid.uuid4()}/{uuid.uuid4()}/{input.fileName}'
        urlUpload = server.getUrlForUploadFile(path)
        pre_url = f'{server.prefix}/{path}'
        return AdminUploadMedia(path=pre_url, url=path)


class MutationAdminMedia(graphene.ObjectType):
    admin_upload_media = AdminUploadMedia.Field(required=True)
