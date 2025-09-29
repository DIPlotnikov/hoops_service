import graphene
from ...models import Task
from ..schema_handler import isAuth, getIDRole
from graphene_django.fields import DjangoConnectionField
from .type import TaskType
from django.db.models import Count, F, Q
from .queries.admin import QueryTaskAdmin
from .queries.executer import QueryTaskExecuter
from .queries.manager import QueryTaskManager
from django.utils import timezone
from datetime import timedelta

class QueryAllTask(graphene.ObjectType):
    tasks_hotel_by_id = DjangoConnectionField(TaskType, required=True, id=graphene.ID(required=True))

    def resolve_tasks_hotel_by_id(self, info, id, **kwargs):
        id_o, role = getIDRole(isAuth(info))
        tasks = Task.objects.filter(manager__hotel__id=id, is_approved=True).order_by('start_at').exclude(status="DELETED").exclude(is_archived=True)
        tasks = tasks.exclude(~Q(manager__favourite_executers__id=id_o), for_favorite=True, created_at__gte=(timezone.now() - timedelta(minutes=120)))
        return tasks


class QueryTask(QueryAllTask, QueryTaskAdmin, QueryTaskExecuter, QueryTaskManager):
    pass
