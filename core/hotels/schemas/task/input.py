import graphene

from ..additional_task.input import InputForAdditionalTask
from ..enums import Sort, SortFields


class inputForGetTasks(graphene.InputObjectType):
    id = graphene.ID(required=False)
    sort = Sort(required=True)
    fields = SortFields(required=True)
    id_hotel = graphene.ID(desc="ID hotels")


class inputForGetMyTasks(graphene.InputObjectType):
    """
    Инпут для получения совиз Заявок
    """

    id = graphene.ID(required=False, description="")
    id_profession = graphene.ID(description="ID профессии")
    date = graphene.DateTime(description="Дата")
    is_approved = graphene.Boolean(description="Подтвержденная")
    from_archive = graphene.Boolean(required=False, description="Из архива")


class inputId(graphene.InputObjectType):
    id = graphene.ID(required=True)


class inputIDs(graphene.InputObjectType):
    ids = graphene.List(graphene.NonNull(graphene.ID), required=True)


class InputForForbidTasks(inputIDs):
    text = graphene.String(required=True)


class inputForCreateTask(graphene.InputObjectType):
    min_rating = graphene.Int(required=False, default=0)
    for_favorite = graphene.Boolean(required=False, default=False)
    profession = graphene.ID(required=True)
    personal_profession = graphene.ID()
    count_executers = graphene.Int(required=True)
    rent = graphene.Float(required=True)
    start_at = graphene.DateTime(required=True)
    duration = graphene.Int(required=True)
    comment = graphene.String(required=True)


class inputForTaskUpsert(graphene.InputObjectType):
    """
    Параметры создания и обновления Заявки
    """

    min_rating = graphene.Int(required=False, default=0, description="Минимальный рейтинг Исполнителя")
    for_favorite = graphene.Boolean(required=False, default=False, description="Признак для избранных Исполнителей")
    id_task = graphene.ID(required=False, description="ID задачи")
    profession = graphene.ID(required=True, description="ID профессии")
    personal_profession = graphene.ID(description="Указатель эксклюзивной профессии")
    count_executers = graphene.Int(required=True, description="Количество исполнителей")
    rent = graphene.Float(required=True, description="Стоимость заявки")
    start_at = graphene.List(
        graphene.NonNull(graphene.DateTime), required=True, description="Список дат начала Заявок"
    )
    duration = graphene.Int(required=True, description="Объем Заявки")
    comment = graphene.String(required=True, description="Комментарий к Заявке")
    additional = graphene.Field(
        InputForAdditionalTask, required=False, description="Дополнительная информация к Заявке"
    )


class inputForTaskUpdate(graphene.InputObjectType):
    min_rating = graphene.Int(required=False, default=0)
    for_favorite = graphene.Boolean(required=False, default=False)
    id_task = graphene.ID(required=True, description="ID задачи")
    profession = graphene.ID(required=True, description="ID профессии")
    personal_profession = graphene.ID()
    count_executers = graphene.Int(required=True)
    rent = graphene.Float(required=True)
    start_at = graphene.DateTime(required=True)
    duration = graphene.Int(required=True)
    comment = graphene.String(required=True)


class inputForStartTask(graphene.InputObjectType):
    id_task = graphene.ID(required=True, desc="ID заявки")
    id_executer = graphene.ID(required=False, desc="ID исполнителя")
    start_at = graphene.DateTime(required=True, desc="Время нажатия на кнопку START")


class inputForStopTask(graphene.InputObjectType):
    id_task = graphene.ID(required=True, desc="ID заявки")
    id_executer = graphene.ID(required=True, desc="ID исполнителя")
    stop_at = graphene.DateTime(required=True, desc="Время нажатия на кнопку STOP")


class InputForSetVolumeOfWorkInTask(graphene.InputObjectType):
    """
    Установка выполненного объема работ по Отклику Исполнителя
    """

    id_executer_state = graphene.ID(required=True, desc="ID Отклика Исполнителя")
    volume_of_the_work = graphene.Float(required=True, description="Объем выполненных работ")


class inputTaskIdExecuterID(graphene.InputObjectType):
    id_task = graphene.ID(required=True, desc="ID заявки")
    id_executer = graphene.ID(required=True, desc="ID исполнителя")


class inputTaskIdExecuterIDCorrection(inputTaskIdExecuterID):
    correction_comment = graphene.String(required=False, desc="Комментарий корректировки")


class InputForAllTaskForAdmin(graphene.InputObjectType):
    """
    Фильтры заявок для таблицы Администратора
    """

    task_id = graphene.ID(required=False, description="Идентификатор заявки")
    start_at = graphene.DateTime(required=False, description="Фильтр на дату старта заявки")
    profession_id = graphene.List(graphene.NonNull(graphene.ID), required=False)
    is_archived_for_admin = graphene.Boolean(required=False, description="Фильтр на архив у Админа")
