from ..models import FileInfo, ExecuterFiles
from graphene_django.types import DjangoObjectType
import graphene


class FileInfoType(DjangoObjectType):
    class Meta:
        model = FileInfo
        fields = ('fileName', 'fileSize', 'height', 'width', 'mimeType', 'timeStamp', 'url')


class ExecuterFileType(DjangoObjectType):
    class Meta:
        model = ExecuterFiles
        exclude = ('executer', 'type')

    file = graphene.NonNull(FileInfoType)


class fileInfoInput(graphene.InputObjectType):
    fileName = graphene.String(required=True)
    fileSize = graphene.Int(required=True, default=0)
    height = graphene.Int(required=True, default=0)
    width = graphene.Int(required=True, default=0)
    mimeType = graphene.String(required=True)
    timeStamp = graphene.String(required=True)
    url = graphene.String(required=True)


class executerFileInfoInput(graphene.InputObjectType):
    file = fileInfoInput(required=True)
