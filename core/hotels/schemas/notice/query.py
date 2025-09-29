import graphene
from graphene_django.fields import DjangoConnectionField

from ...models import RoleAdmin
from ..schema_handler import is_admin, is_manager
from .input import InputForManagerQueryNotices, InputForQueryNotice, InputForQueryNotices
from .type import Notice, NoticeType


class QueryNotice(graphene.ObjectType):
    admin_get_notice_by_filters = DjangoConnectionField(
        NoticeType, input=InputForQueryNotices(required=True), required=True
    )
    admin_get_notice_by_id = graphene.NonNull(NoticeType, input=InputForQueryNotice(required=True))

    manager_get_notice_by_filters = DjangoConnectionField(
        NoticeType, input=InputForManagerQueryNotices(required=True), required=True
    )
    manager_get_notice_by_id = graphene.NonNull(NoticeType, input=InputForQueryNotice(required=True))

    def resolve_admin_get_notice_by_filters(self, info, input, **kwargs):
        is_admin(info=info, permission=RoleAdmin.Roles.DOCUMENT.value)
        notices = Notice.objects.all()

        if input.id_hotel:
            notices = notices.filter(hotel__id=input.id_hotel).order_by("id").distinct()
        if input.is_archive is not None:
            notices = notices.filter(is_archive=input.is_archive)
        if input.is_sent is not None:
            notices = notices.filter(is_sent=input.is_sent)
        if input.start_date and input.end_date:
            start_date = input.start_date.replace(hour=0, minute=0, second=0, microsecond=0)
            notices = notices.filter(create_at__gte=start_date).filter(create_at__lte=input.end_date)
        return notices

    def resolve_admin_get_notice_by_id(self, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.DOCUMENT.value)
        return Notice.objects.get(id=input.id)

    def resolve_manager_get_notice_by_filters(self, info, input, **kwargs):
        manager = is_manager(info=info, permission=["DOCUMENTS"])
        notices = Notice.objects.filter(is_sent=True, hotel__manager=manager).distinct()
        if input.start_date and input.end_date:
            start_date = input.start_date.replace(hour=0, minute=0, second=0, microsecond=0)
            notices = notices.filter(create_at__gte=start_date).filter(create_at__lte=input.end_date)
        return notices

    def resolve_manager_get_notice_by_id(self, info, input):
        manager = is_manager(info=info, permission=["DOCUMENTS"])
        return Notice.objects.filter(id=input.id, is_sent=True, hotel__manager=manager).first()
