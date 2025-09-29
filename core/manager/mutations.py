import graphene

from hotels.schemas.input import InputID
from hotels.schemas.schema_handler import is_manager
from .models import BlackList


class ManagerAddExecutorInBlackList(graphene.Mutation):
    """
    Добавить Исполнителя в Черный список
    """

    class Arguments:
        input = InputID(required=True)

    class Meta:
        output = graphene.Boolean

    @staticmethod
    def mutate(root, info, input):
        manager = is_manager(info=info)
        BlackList.objects.get_or_create(manager_id=manager.id, executor_id=input.id)
        return True


class ManagerRemoveExecutorFromBlackList(graphene.Mutation):
    """
    Убрать Исполнителя из Черного списка
    """

    class Arguments:
        input = InputID(required=True)

    class Meta:
        output = graphene.Boolean

    @staticmethod
    def mutate(root, info, input):
        manager = is_manager(info=info)
        BlackList.objects.filter(manager_id=manager.id, executor_id=input.id).delete()
        return True


class ManagerFlushAllBlackList(graphene.Mutation):
    """
    Удалить все записи из Черного списка
    """

    class Meta:
        output = graphene.Boolean

    @staticmethod
    def mutate(root, info):
        manager = is_manager(info=info)
        BlackList.objects.filter(manager_id=manager.id).delete()
        return True


class ManagerMutation(graphene.ObjectType):
    """
    Менеджерские мутации
    """

    manager_executor_add_in_black_list_by_id = ManagerAddExecutorInBlackList.Field(required=True)
    manager_executor_remove_from_black_list_by_id = ManagerRemoveExecutorFromBlackList.Field(required=True)
    manager_executor_flush_all_black_list = ManagerFlushAllBlackList.Field(required=True)
