import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType

from ..pagination import ExtendedConnection
from ..schema_coordinates import CoordinatesType
from ..schema_fileinfo import FileInfoType
from ..schema_personal_profession import PersonalProfessionType
from ...models import Hotel, Task


class HotelType(DjangoObjectType):
    class Meta:
        model = Hotel
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection
        exclude = ("manager_set", "requisites")

    inn = graphene.String(required=True)
    profile_pic = graphene.List(graphene.NonNull(FileInfoType), required=True)
    # tasks = graphene.List(graphene.NonNull(TaskType), required=True)
    count_tasks = graphene.Int(required=True)
    coordinates = graphene.NonNull(CoordinatesType)

    rating = graphene.Float(required=True)

    personalprofession_set = graphene.List(graphene.NonNull(PersonalProfessionType), required=True)
    id = graphene.ID(required=True)

    def resolve_id(self, info):
        return self.pk

    def resolve_personalprofession_set(self, info):
        return self.personalprofession_set.all().filter(active=True)

    def resolve_rating(self, info):
        return 4.99

    def resolve_inn(self, info):
        inn = str(self.inn)
        if inn == "0":
            return ""
        return inn.zfill(10)

    def resolve_profile_pic(self, info):
        return [self.profile_pic] if self.profile_pic is not None else []

    def resolve_tasks(self, info):
        tasks = Task.objects.filter(manager__hotel__id=self.pk)
        return tasks if tasks is not None else []

    def resolve_count_tasks(self, info):
        return Task.objects.filter(manager__hotel__id=self.pk).count()
