import graphene
from ..schema_fileinfo import fileInfoInput


class InputForCreateNotice(graphene.InputObjectType):
    id_hotel = graphene.ID(required=True)
    files = graphene.List(graphene.NonNull(fileInfoInput), required=True)
    subject = graphene.ID(required=True)


class InputIdsNotices(graphene.InputObjectType):
    ids = graphene.List(graphene.NonNull(graphene.ID), required=True)


class InputForQueryNotice(graphene.InputObjectType):
    id = graphene.ID(required=True)


class InputForQueryNotices(graphene.InputObjectType):
    id_hotel = graphene.ID(required=False)
    is_archive = graphene.Boolean(required=False)
    is_sent = graphene.Boolean(required=False)
    start_date = graphene.DateTime(required=False)
    end_date = graphene.DateTime(required=False)


class InputForManagerQueryNotices(graphene.InputObjectType):
    start_date = graphene.DateTime(required=False)
    end_date = graphene.DateTime(required=False)
