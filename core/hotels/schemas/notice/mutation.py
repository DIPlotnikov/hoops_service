import graphene
from .input import InputForCreateNotice, InputIdsNotices
from .type import NoticeType
from ..schema_handler import is_admin
from ...models import Notice, Hotel, FileInfo, RoleAdmin


class CreateNotice(graphene.Mutation):
    class Arguments:
        input = InputForCreateNotice(required=True)

    notice = graphene.Field(graphene.NonNull(NoticeType))

    @staticmethod
    def mutate(root, info, input):

        admin = is_admin(info=info, permission=RoleAdmin.Roles.DOCUMENT.value, model=True)
        notice = Notice(admin=admin, subject=input.subject, hotel=Hotel.objects.get(id=input.id_hotel))
        notice.save()
        for file in input.files:
            fileInfo = FileInfo(**file)
            fileInfo.save()
            notice.files.add(fileInfo)
        notice.save()
        return CreateNotice(notice=notice)


class SendNotice(graphene.Mutation):
    class Arguments:
        input = InputIdsNotices(required=True)

    notices = graphene.NonNull(graphene.List(NoticeType, required=True))

    def mutate(root, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.DOCUMENT.value)
        notices = Notice.objects.filter(id__in=input.ids)
        notices.update(is_sent=True)
        return SendNotice(notices=notices)


class ArchiveNotice(graphene.Mutation):
    class Arguments:
        input = InputIdsNotices(required=True)

    notices = graphene.NonNull(graphene.List(NoticeType, required=True))

    def mutate(root, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.DOCUMENT.value)
        notices = Notice.objects.filter(id__in=input.ids)
        notices.update(is_archive=True)
        return ArchiveNotice(notices=notices)


class ActivateNotice(graphene.Mutation):
    class Arguments:
        input = InputIdsNotices(required=True)

    notices = graphene.NonNull(graphene.List(NoticeType, required=True))

    def mutate(root, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.DOCUMENT.value)
        notices = Notice.objects.filter(id__in=input.ids)
        notices.update(is_archive=False)
        return ActivateNotice(notices=notices)



class MutationNotice(graphene.ObjectType):
    admin_create_notice_by_id_hotel = CreateNotice.Field(required=True)
    admin_archive_notice = ArchiveNotice.Field(required=True)
    admin_activate_notice = ActivateNotice.Field(required=True)
    admin_send_notice = SendNotice.Field(required=True)
