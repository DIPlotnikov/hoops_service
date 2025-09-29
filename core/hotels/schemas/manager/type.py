import graphene
from graphene_django.types import DjangoObjectType

from manager.models import BlackList
from ..hotel.types import HotelType
from ...models import Manager, RoleManager, Task


class ManagerBaseType(DjangoObjectType):
    class Meta:
        model = Manager
        exclude = ("password", "task_set", "feedbackmanager_set", "favourite_executers")

    status = graphene.NonNull(Manager.StatusEnum)
    count_tasks = graphene.Int(required=True)
    favorite_executers = graphene.List(graphene.NonNull(graphene.ID), required=True)
    blacklist_executers = graphene.List(graphene.NonNull(graphene.ID), required=True)

    def resolve_status(self, info):
        if self.status == 0:
            return Manager.Status.SEND_INVITE.value
        if self.status == 1:
            return Manager.Status.CANCEL_INVITE.value
        if self.status == 2:
            return Manager.Status.INVITED.value
        return Manager.Status.ADMIN.value

    def resolve_favorite_executers(self, info):
        return self.favourite_executers.all().values_list("id", flat=True)

    def resolve_blacklist_executers(self, info):
        return BlackList.objects.filter(manager=self).values_list("executor_id", flat=True)

    def resolve_count_tasks(self, info):
        if self.is_admin == False:
            return (
                Task.objects.filter(manager_id=self.pk)
                .exclude(status="DELETED")
                .exclude(status="ARCHIVED")
                .exclude(is_archived=True)
                .count()
            )
        else:
            return (
                Task.objects.filter(manager__hotel=self.hotel)
                .exclude(status="DELETED")
                .exclude(status="ARCHIVED")
                .exclude(is_archived=True)
                .count()
            )

    def resolve_hotel(self, info):
        return self.hotel


class ManagerAuthType(DjangoObjectType):
    class Meta:
        model = Manager
        exclude = exclude = ("password", "task_set", "feedbackmanager_set", "favourite_executers")

    token = graphene.String()

    def resolve_token(self, info):
        return Manager.objects.get(id=self.pk).token


class ManagerType(ManagerBaseType):
    class Meta:
        model = Manager
        exclude = ("password", "task_set", "feedbackmanager_set", "favourite_executers")

    hotel = graphene.NonNull(HotelType)

    def resolve_hotel(self, info):
        return self.hotel

    roles = graphene.List(graphene.NonNull(RoleManager.RolesManagerEnum), required=True, description="Роли Менеджера")

    def resolve_roles(self, info):
        return self.roles.all().values_list("role", flat=True)
