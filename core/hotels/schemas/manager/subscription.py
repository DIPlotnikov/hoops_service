from django.db.models.signals import post_save, post_delete
from graphene_subscriptions.signals import post_save_subscription, post_delete_subscription
import graphene
from ...models import Manager
from .type import ManagerType
post_save.connect(post_save_subscription, sender=Manager, dispatch_uid="Manager_post_save")
post_delete.connect(post_delete_subscription, sender=Manager, dispatch_uid="Manager_post_delete")


class SubscriptionManager(graphene.ObjectType):
    manager_updated = graphene.Field(graphene.NonNull(ManagerType), id=graphene.ID(required=True))

    def resolve_manager_updated(root, info, id):

        return root.filter(
            lambda event:
            event.operation == 'updated' and
            isinstance(event.instance, Manager) and event.instance.pk == int(id)
        ).map(lambda event: event.instance)