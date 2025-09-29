import graphene

from ....models import Executer, Notification
from ...schema_handler import is_manager
from ..input import inputExecuterID
from ..type import ManagerType


class AddFavoriteExecuter(graphene.Mutation):

    class Arguments:
        input = inputExecuterID(required=True)

    manager = graphene.Field(ManagerType, required=True)

    @staticmethod
    def mutate(root, info, input):
        manager = is_manager(info=info, permission=["FAVORITE_EDIT"])
        executer = Executer.objects.get(id=input.id)
        manager.favourite_executers.add(executer)
        manager.save()
        notify = Notification(
            type=Notification.TypeNotification.ACCOUNT,
            id_instance=executer.pk,
            role="executer",
            read=False,
            text=f"Вас добавили в избранные гостиница {manager.hotel.nameLegalEntity}",
        )
        notify.save(notification=True)

        return AddFavoriteExecuter(manager=manager)


class RemoveFavoriteExecuter(graphene.Mutation):

    class Arguments:
        input = inputExecuterID(required=True)

    manager = graphene.Field(ManagerType, required=True)

    @staticmethod
    def mutate(root, info, input):
        manager = is_manager(info=info, permission=["FAVORITE_EDIT"])
        executer = Executer.objects.get(id=input.id)
        manager.favourite_executers.remove(executer)
        manager.save()
        return RemoveFavoriteExecuter(manager=manager)


class ClearFavoriteExecuter(graphene.Mutation):

    manager = graphene.Field(ManagerType, required=True)

    @staticmethod
    def mutate(root, info):
        manager = is_manager(info=info, permission=["FAVORITE_EDIT"])
        manager.favourite_executers.clear()
        manager.save()
        return ClearFavoriteExecuter(manager=manager)


class MutationManagerFavoriteExecutors(graphene.ObjectType):
    manager_add_favorite_executer = AddFavoriteExecuter.Field(required=True)
    manager_remove_favorite_executer = RemoveFavoriteExecuter.Field(required=True)
    manager_clear_favorite_executer = ClearFavoriteExecuter.Field(required=True)
