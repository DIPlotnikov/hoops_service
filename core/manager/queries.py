import graphene
from graphene_django import DjangoConnectionField

from hotels.schemas.executer.type import ExecuterType
from hotels.schemas.schema_handler import is_manager
from .models import BlackList


class ManagerQueries(graphene.ObjectType):
    """
    Запросы Менеджера
    """

    manager_get_all_black_list = DjangoConnectionField(
        ExecuterType,
        required=True,
        description="Черный список Исполнителей у Менеджера",
    )

    def resolve_manager_get_all_black_list(self, info, **kwargs):
        manager = is_manager(info=info)
        return [x.executor for x in BlackList.objects.filter(manager=manager).all()]
