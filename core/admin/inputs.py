import graphene


class FilterAdminInput(graphene.InputObjectType):
    """
    Инпут для фильтрации админов
    """

    name = graphene.String(required=False, description="Имя админа")
    id = graphene.ID(required=False, description="ID админа")
