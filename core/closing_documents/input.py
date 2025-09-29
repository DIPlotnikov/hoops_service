import graphene


class InputForCreateClosingDocuments(graphene.InputObjectType):
    """Создание закрывающих документов"""

    id = graphene.ID(required=True, description="ID Гостиницы")
    start_date = graphene.DateTime(required=True, description="Начало периода")
    end_date = graphene.DateTime(required=True, description="Конец периода")
    closing_date = graphene.DateTime(required=False, description="Дата закрытия")
    join_payment_docs = graphene.Boolean(required=False, description="Объединить платежку")


class InputIdsClosingDocuments(graphene.InputObjectType):
    ids = graphene.List(graphene.NonNull(graphene.ID), required=True)


class InputForQueryClosingDocument(graphene.InputObjectType):
    id = graphene.ID(required=True)


class InputForQueryClosingDocuments(graphene.InputObjectType):
    """Параметры запроса таблицы закрывающих документов для Гостиниц"""

    id_hotel = graphene.ID(required=False, description="Фильтр по ID гостиницы")
    is_archive = graphene.Boolean(required=False, description="Фильтр по флагу is_archive")
    is_sent = graphene.Boolean(required=False, description="Фильтр по флагу is_sent")
    start_date = graphene.DateTime(required=False, description="Фильтр по дате отправки - начало периода")
    end_date = graphene.DateTime(required=False, description="Фильтр по дате отправки - конец периода")
    is_paid = graphene.Boolean(required=False, description="Фильтр по флагу оплат")


class InputForManagerQueryClosingDocuments(graphene.InputObjectType):
    """Параметры запроса закрывающих документов для Менеджера"""

    start_date = graphene.DateTime(required=False)
    end_date = graphene.DateTime(required=False)
