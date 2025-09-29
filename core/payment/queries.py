import json

import graphene

from hotels.models import RoleAdmin
from hotels.schemas.schema_handler import is_admin


class PaymentQueries(graphene.ObjectType):
    """
    Запросы Оплат
    """

    admin_payment_ping = graphene.String(
        required=True,
        description="Проверка связи с интеграцией",
    )

    def resolve_admin_payment_ping(self, info, **kwargs):
        is_admin(info=info, permission=RoleAdmin.Roles.SETTINGS.value)
        return json.dumps({"status": "ok", "message": "pong", "version": "0.0.1"})
