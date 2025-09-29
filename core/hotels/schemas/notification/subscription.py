import logging

import channels_graphql_ws
import graphene

logger = logging.getLogger(__name__)


class MySubscription(channels_graphql_ws.Subscription):
    notification_queue_limit = 64
    text = graphene.String()

    def subscribe(self, info, *args, **kwargs):
        assert info.context.channels_scope.get("role_user", "") == 1, "NO!"
        assert info.context.channels_scope.get("id_user"), "Where you id?!"
        logger.info(f"New subscription {info.context.channels_scope}")
        return [str(info.context.channels_scope.get("id_user"))]

    def publish(self, *args, **kwargs):
        new_msg_text = self["text"]
        return MySubscription(text=new_msg_text)

    @classmethod
    def new_message(cls, id_instance, text):
        cls.broadcast(
            group=str(id_instance),
            payload={"text": text},
        )


class SubscriptionNotification(graphene.ObjectType):
    """Root GraphQL subscription."""

    manager_notification_create = MySubscription.Field()
