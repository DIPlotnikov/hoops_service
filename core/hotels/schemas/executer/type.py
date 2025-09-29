from datetime import datetime

from graphene import ObjectType, relay

from ..pagination import ExtendedConnection
from ..schema_fileinfo import *
from ...models import Executer


class ExecuterType(DjangoObjectType):
    class Meta:
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection
        model = Executer
        exclude = (
            "password",
            "requisites",
            "executerstate_set",
            "feedbackexecuter_set",
            "feedbackmanager_set",
            "favourites_hotel",
            "simplerequisite",
            "executerstatdoc_set",
            "manager_set",
            "is_active",
            "is_valid_number",
            "count_work_with_rating",
            "score",
            "created_at",
            "updated_at",
            "executerfiles_set",
        )

    birthday = graphene.DateTime(required=True)
    inn = graphene.String(required=True)
    profile_pic = graphene.List(graphene.NonNull(FileInfoType), required=True)
    rating = graphene.Float(required=False)
    id = graphene.ID(required=True)
    favorite_hotels = graphene.List(graphene.NonNull(graphene.ID), required=True)

    is_favorite = graphene.Boolean(required=True)
    is_blacklist = graphene.Boolean(required=True)

    def resolve_birthday(self, info):
        return datetime.combine(self.birthday, datetime.min.time())

    def resolve_id(self, info):
        return self.pk

    def resolve_rating(self, info):
        if bool(self.count_work_with_rating):
            return round(self.score / self.count_work_with_rating, 2)
        else:
            return None

    def resolve_inn(self, info):
        inn = str(self.inn)
        if inn == "0":
            return ""
        return inn.zfill(12)

    def resolve_profile_pic(self, info):
        return [self.profile_pic] if self.profile_pic is not None else []

    def resolve_favorite_hotels(self, info):
        return self.favourites_hotel.all().values_list("id", flat=True)


class ExecuterPermintsType(ObjectType):
    # files = graphene.List(graphene.NonNull(FileInfoType), required=True)
    work_expiration = graphene.DateTime(required=False)
    medical_book_expiration = graphene.DateTime(required=True)
