import graphene


class InputForLogout(graphene.InputObjectType):
    """
    Параметры для выхода из системы
    """

    fcm_token = graphene.String(required=False, description="FCM токен с мобильного приложения")
