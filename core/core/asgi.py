import os

import graphql
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django_asgi_app = get_asgi_application()
from core.schema import schema
from hotels.schemas.schema_handler import getIDRole
import channels_graphql_ws

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


async def demo_middleware(next_middleware, root, info, *args, **kwds):
    result = next_middleware(root, info, *args, **kwds)
    if graphql.pyutils.is_awaitable(result):
        result = await result
    return result


class MyGraphqlWsConsumer(channels_graphql_ws.GraphqlWsConsumer):
    schema = schema
    send_ping_every = 5  # seconds
    middleware = [demo_middleware]
    # confirm_subscriptions = True

    async def _on_gql_connection_init(self, payload):
        await super()._on_gql_connection_init(payload)
        authorization_header = payload["headers"].get("authorization").split()[1]
        id_user, role_user = getIDRole(authorization_header)
        self.scope["id_user"] = id_user
        self.scope["role_user"] = role_user


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": URLRouter(
            [
                path("graphql/", MyGraphqlWsConsumer.as_asgi()),
            ]
        ),
    }
)
