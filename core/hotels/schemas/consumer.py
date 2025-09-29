import channels_graphql_ws

from .schema import schema


class MyGraphqlWsConsumer(channels_graphql_ws.GraphqlWsConsumer):
    """Channels WebSocket consumer which provides GraphQL API."""

    schema = schema

    # Uncomment to send ping message every 42 seconds.
    # send_ping_every = 42

    # Uncomment to process requests sequentially (useful for tests).
    # strict_ordering = True
