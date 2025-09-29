import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from ..models import Executer, Hotel, Task, ExecuterState
from .schema_handler import isAuth, getIDRole
from ..scripts import exception_handler as EH
from datetime import datetime
from functools import lru_cache


class StatisticType(ObjectType):

    executers = graphene.Int(required=True, description='Исполнителей')
    customers = graphene.Int(required=True, description='Заказчиков')
    tasks = graphene.Int(required=True, description='Активных заявок')
    executers_in_work = graphene.Int(required=True, description='Оказывают услуги')

    def resolve_executers(self, info):
        return Executer.objects.filter(is_active=True).count()

    def resolve_customers(self, info):
        return Hotel.objects.all().count()

    def resolve_tasks(self, info):

        return Task.objects.filter(start_at__date=datetime.now().date()).exclude(status='DELETED').count()

    def resolve_executers_in_work(self, info):
        return ExecuterState.objects.filter(task__start_at__date=datetime.now().date()).count()


class QueryStatistic(graphene.ObjectType):
    statistics = graphene.Field(StatisticType)

    def resolve_statistics(self, info):
        return StatisticType()