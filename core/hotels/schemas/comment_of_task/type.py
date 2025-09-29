from ...models import CommentOfTask
from graphene_django.types import DjangoObjectType


class CommentOfTaskType(DjangoObjectType):
    class Meta:
        model = CommentOfTask
        exclude = ('tasks',)
