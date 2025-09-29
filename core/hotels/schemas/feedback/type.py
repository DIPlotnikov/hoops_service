from ...models import FeedbackExecuter, FeedbackManager
from graphene_django.types import DjangoObjectType


class FeedbackAboutTaskByExecuterType(DjangoObjectType):
    class Meta:
        model = FeedbackExecuter


class FeedbackAboutExecuterByManagerType(DjangoObjectType):
    class Meta:
        model = FeedbackManager
