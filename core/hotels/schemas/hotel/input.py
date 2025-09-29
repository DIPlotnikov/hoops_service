import graphene
from ..schema_coordinates import coordinatesInput
from ..schema_fileinfo import fileInfoInput
from ..scheme_requisites import requisitesInput


class inputForQueryById(graphene.InputObjectType):
    id = graphene.ID(required=True)


class inputForCreateHotel(graphene.InputObjectType):
    email = graphene.String(required=True)
    inn = graphene.String(required=True)
    nameLegalEntity = graphene.String(required=True)
    password = graphene.String(required=True)
    nameHotel = graphene.String(required=True)
    undergroundStation = graphene.String(required=False)
    coordinates = coordinatesInput(required=True)


class inputForUpdateHotel(graphene.InputObjectType):
    email = graphene.String()
    inn = graphene.String(required=True)
    nameLegalEntity = graphene.String()
    postalAddress = graphene.String()
    nameHotel = graphene.String()
    undergroundStation = graphene.String()

    profile_pic = graphene.List(graphene.NonNull(fileInfoInput), required=True,
                                description='Список из 1 элемента с типом метаданных файла')
    coordinates = coordinatesInput(required=True)


class inputForUploadFile(graphene.InputObjectType):
    fileName = graphene.String(required=True)
