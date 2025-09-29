from datetime import datetime, timedelta

import graphene
from django.db.models import Q
from django.utils import timezone
from graphene import ObjectType

from ..input import (
    InputForForbidTasks,
    InputForSetVolumeOfWorkInTask,
    inputForStartTask,
    inputForStopTask,
    inputForTaskUpsert,
    inputIDs,
    inputTaskIdExecuterID,
    inputTaskIdExecuterIDCorrection,
)
from ..type import TaskType
from ...schema_handler import getIDRoleAdmin, is_manager, isAuth
from ....models import (
    AdditionalTask,
    CommentOfTask,
    ExecuterState,
    Manager,
    Notification,
    PersonalProfession,
    Profession,
    Task,
)
from ....scripts import exception_handler as EH


def get_task(info, id, role="TASK_EDIT"):
    manager = is_manager(info=info)
    filters = [Q(id=id), manager.filter_for_mutation_task(role)]
    task = Task.objects.filter(*filters).exclude(status="DELETED").first()
    assert task, "у Вас нет полномочий на эту заявку"
    return task


def get_tasks(info, ids, check_admin=False, role="TASK_EDIT"):
    manager = is_manager(info=info)
    filters = [Q(id__in=ids), manager.filter_for_mutation_task(role)]
    if check_admin:
        if not manager.is_admin:
            raise PermissionError("Доступно только главным менеджерам")
    tasks = Task.objects.filter(*filters).exclude(status="DELETED")
    assert tasks, "у Вас нет полномочий на эту заявку"
    return tasks


class UpsertTask(graphene.Mutation):

    class Arguments:
        input = inputForTaskUpsert(required=True)

    task = graphene.Field(graphene.NonNull(TaskType))

    @staticmethod
    def mutate(root, info, input):
        id_o, role, admin = getIDRoleAdmin(isAuth(info))
        if role != 1:
            raise EH.customError("Ошибка", "нет прав создания заявки")

        manager = Manager.objects.filter(id=id_o).first()
        if manager is None:
            raise EH.customError("Ошибка", "менеджер не менеджер")
        if manager.hotel.status != "STEP_3_VERIFIED":
            raise EH.customError("Ошибка", "необходимо подтвердить аккаунт.")

        if manager.hotel.is_allow_to_use_basic_profession is False:
            assert bool(input.personal_profession), "Нельзя создать заявку без эксклюзивной профессии"

        if input.id_task:
            task = get_tasks(info, [input.id_task])
            if task[0].start_at < (timezone.now() + timedelta(hours=8)):
                raise EH.customError("Ошибка", "изменение заявки за менее чем 8 часов до старта невозможно!")
        else:
            task = Task()

        input = input.copy()
        input["profession"] = Profession.objects.get(id=input["profession"])
        if "personal_profession" in input:
            pp = PersonalProfession.objects.filter(id=input["personal_profession"], owner__manager__id=id_o).first()
            if pp:
                input["personal_profession"] = pp
                input["personal_profession_name"] = pp.name
                # if int(input["rent"]) != pp.rent:
                #     raise EH.customError(
                #         "Ошибка", f"cтавка указанная не совпадает со ставкой эксклюзивной профессии ({pp.rent})"
                #     )
            else:
                if input["rent"] < input["profession"].rate_min or input["rent"] > input["profession"].rate_max:
                    raise EH.customError(
                        "Ошибка",
                        f"Ставка указанная не в диапазоне ставок профессии: "
                        f"от {input['profession'].rate_min} до {input['profession'].rate_max}",
                    )
        else:
            input["personal_profession_name"] = None

        if input["count_executers"] < 1:
            raise EH.customError("Ошибка", "должен быть хотя бы 1 исполнитель")
        if input["count_executers"] > 999:
            raise EH.customError("Ошибка", "слишком много исполнителей, максимально 999, хотя и это много...")
        if (
            input["duration"] < 1
            or input["duration"] > 24
            and input["profession"].numerate == Profession.Numerates.HOUR
        ):
            raise EH.customError("Ошибка", "длительность заявки от 1 до 24 часов")
        start_at_mass = input.pop("start_at")
        assert len(start_at_mass) > 0, "Неверная дата старта заявки"
        for start_at in start_at_mass:
            assert start_at > (timezone.now()), "Заявку в прошлое создать нельзя"
        additional = input.pop("additional", None)
        additional_dict = None
        if additional:
            if all((additional.datetime, additional.description)):
                additional_dict = {"datetime": additional.datetime, "description": additional.description}

        if "id_task" in input:
            input.pop("id_task")
            input["start_at"] = start_at_mass[0]
            # откликов больше чем размер заявки
            diff = task[0].executers.all().count() - input["count_executers"]
            if diff > 0:
                executers_to_delete = task[0].executers.all().order_by("-id")[:diff]

                for executer_to_delete in executers_to_delete:
                    notify = Notification(
                        type=Notification.TypeNotification.TASK,
                        id_instance=executer_to_delete.executer.pk,
                        role="executer",
                        read=False,
                        text=f"Вы исключены из выполнения  заявки #{task[0].pk} на {str(task[0].start_at)[:11]}.",
                    )
                    notify.save(notification=True)
                    executer_to_delete.delete()

            task.update(**input, is_approved=manager.hotel.auto_approve_tasks)

            task = task[0]

            if additional_dict:
                if task.additional:
                    AdditionalTask.objects.filter(id=task.additional.pk).update(**additional_dict)
                else:
                    task.additional = AdditionalTask.objects.create(**additional_dict)
                    task.save()
            else:
                if task.additional:
                    task.additional.delete()

            for executerStatus in task.executers.all():
                notify = Notification(
                    type=Notification.TypeNotification.TASK,
                    id_instance=executerStatus.executer.pk,
                    role="executer",
                    read=False,
                    text=f'В заявке #{task.pk}  на {task.start_at.strftime("%d.%m.%Y")} произошли изменения. '
                    f"Проверьте, пожалуйста, и если Вас не устраивают новые условия - откажитесь от заявки.",
                )
                notify.save(notification=True, url="personal")
        else:
            input["manager"] = manager

            for start_at in start_at_mass:
                task = Task(
                    **input,
                    start_at=start_at,
                    is_approved=manager.hotel.auto_approve_tasks,
                    additional=AdditionalTask.objects.create(**additional_dict) if additional_dict else None,
                )
                task.save()
            for executer in manager.favourite_executers.all():
                notify = Notification(
                    type=Notification.TypeNotification.TASK,
                    id_instance=executer.pk,
                    role="executer",
                    read=False,
                    text=f"У заказчика {manager.hotel.nameHotel} на "
                    f'{task.start_at.strftime("%d.%m.%Y")} появилась заявка'
                    f" для избранных исполнителей.",
                )
                notify.save(notification=True, url="tasks")
        return UpsertTask(task=task)


class deleteTask(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    task = graphene.NonNull(TaskType)

    def mutate(root, info, id):

        task = get_task(info, id)
        if task.start_at.timestamp() < (datetime.now() + timedelta(hours=8)).timestamp():
            raise EH.customError("Ошибка", "удалять менее чем за 8 часов запрещено")
        task.status = "DELETED"

        if task.executers.count() != 0:
            for executerStatus in task.executers.all():
                notify = Notification(
                    type=Notification.TypeNotification.TASK,
                    id_instance=executerStatus.executer.pk,
                    role="executer",
                    read=False,
                    text=f"Заявка #{task.pk}  на {str(task.start_at)[:11]} удалена,"
                    f" свяжитесь с менеджером гостиницы, если у Вас не разрешенные вопросы.",
                )
                notify.save(notification=True, url="personal")
            task.executers.clear()
        task.save()

        return deleteTask(task=task)


class startTask(graphene.Mutation):
    """
    Мутация старта Заявки
    """

    class Arguments:
        input = inputForStartTask(required=True, description="input for startTask")

    task = graphene.Field(TaskType, required=True)

    def mutate(root, info, input):

        task = get_task(info, input.id_task)

        if input.id_executer is None:
            executersState = ExecuterState.objects.filter(task=task).exclude(status="STOP").exclude(status="START")
        else:
            executersState = ExecuterState.objects.filter(executer__id=input.id_executer, task=task)
            if len(executersState) == 0:
                raise EH.customError("Ошибка", "отсутствует исполнитель")
            if executersState[0].status == "START":
                raise EH.customError("Ошибка", "исполнитель начал работу")
        executersState.update(status="START")
        executersState.update(start_at=input.start_at)
        for executerState in executersState:
            notify = Notification(
                type=Notification.TypeNotification.TASK,
                id_instance=executerState.executer.pk,
                role="executer",
                read=False,
                text=f"Заявка #{task.pk} начата!",
            )
            notify.save(notification=True, url="personal", task_id=task.pk)
        return startTask(task=task)


class stopTask(graphene.Mutation):
    """
    Мутация стопа Заявки
    """

    class Arguments:
        input = inputForStopTask(required=True, description="input for stopTask")

    task = graphene.Field(TaskType, required=True)

    def mutate(root, info, input):
        task = get_task(info, input.id_task)
        executerState = ExecuterState.objects.filter(executer__id=input.id_executer, task=task).first()
        if executerState is None:
            raise EH.customError("Executer not found")
        assert executerState.status == "START", "Исполнитель не начал еще работу"
        assert executerState.start_at < input.stop_at, "Время окончания не может быть меньше времени начала работ"
        executerState.status = "STOP"
        executerState.stop_at = input.stop_at
        executerState.save()
        Notification(
            type=Notification.TypeNotification.TASK,
            id_instance=executerState.executer.pk,
            role="executer",
            read=False,
            text=f"Заявка #{task.id} выполнена!",
        ).save(notification=True, url="personal", task_id=task.pk)

        return startTask(task=task)


class SetVolumeOfWorkByExecuterState(graphene.Mutation):
    """
    Установка объема выполненных работ по id Отклика Исполнителя
    """

    class Arguments:
        input = InputForSetVolumeOfWorkInTask(required=True, description="Объем и id Отклика Исполнителя")

    task = graphene.Field(TaskType, required=True)

    def mutate(root, info, input):
        manager = is_manager(info=info)
        executer_state = (
            ExecuterState.objects.prefetch_related("task_set")
            .filter(id=input.id_executer_state, task__manager=manager)
            .first()
        )
        assert executer_state is not None, "Не найден отклик"
        executer_state.set_volume(input.volume_of_the_work)
        Notification(
            type=Notification.TypeNotification.TASK,
            id_instance=executer_state.executer.pk,
            role="executer",
            read=False,
            text=f"Заявка #{executer_state.task.id} выполнена!",
        ).save(notification=True, url="personal", task_id=executer_state.task.pk)
        return SetVolumeOfWorkByExecuterState(task=executer_state.task)


class archiveTask(graphene.Mutation):
    class Arguments:
        input = inputIDs(required=True)

    tasks = graphene.List(graphene.NonNull(TaskType), required=True)

    def mutate(root, info, input):
        tasks = get_tasks(info, input.ids, role="TASK_ARCHIVE")
        tasks.update(is_archived=True)
        return unarchiveTask(tasks=tasks)


class ApproveTask(graphene.Mutation):
    class Arguments:
        input = inputIDs(required=True)

    tasks = graphene.List(graphene.NonNull(TaskType), required=True)

    def mutate(root, info, input):
        tasks = get_tasks(info, input.ids, check_admin=True)
        tasks.update(is_approved=True)
        return ApproveTask(tasks=tasks)


class ForbidTask(graphene.Mutation):
    class Arguments:
        input = InputForForbidTasks(required=True)

    tasks = graphene.List(graphene.NonNull(TaskType), required=True)

    def mutate(root, info, input):
        tasks = get_tasks(info, input.ids, check_admin=True)
        tasks.update(is_approved=False)
        comment = CommentOfTask()
        comment.save()

        comment.tasks.add(*tasks)
        comment.text = input.text
        comment.save()
        return ForbidTask(tasks=tasks)


class unarchiveTask(graphene.Mutation):
    class Arguments:
        input = inputIDs(required=True)

    tasks = graphene.List(graphene.NonNull(TaskType), required=True)

    def mutate(root, info, input):
        tasks = get_tasks(info, input.ids)
        tasks.update(is_archived=False)
        return unarchiveTask(tasks=tasks)


class setCorrectionCommentToExecuterInTask(graphene.Mutation):
    class Arguments:
        input = inputTaskIdExecuterIDCorrection(required=True)

    task = graphene.Field(TaskType, required=True)

    def mutate(root, info, input):

        task = get_task(info, input.id_task)
        executerState = ExecuterState.objects.filter(executer__id=input.id_executer, task=task).first()

        if executerState is None:
            raise EH.customError("Ошибка", "пользователь не найден")
        assert executerState.stop_at is None, "У Исполнителя стоит отметка о том, что заявка выполнена"
        executerState.correction_comment = input.correction_comment
        executerState.save()
        task.save()
        return setCorrectionCommentToExecuterInTask(task=task)


class setExecuterAsViolator(graphene.Mutation):
    class Arguments:
        input = inputTaskIdExecuterID(required=True)

    task = graphene.Field(TaskType, required=True)

    def mutate(root, info, input):

        task = get_task(info, input.id_task)
        executer_state = ExecuterState.objects.filter(executer__id=input.id_executer, task=task).first()

        if executer_state is None:
            raise EH.customError("Ошибка", "пользователь не найден")
        assert executer_state.stop_at is None, "У Исполнителя стоит отметка о том, что заявка выполнена"
        # executerState.start_at = datetime(2000, 1, 1, 0, 0, 0, 0)
        # executerState.stop_at = datetime(2000, 1, 1, 0, 0, 0, 0)
        now = datetime.now().replace(hour=3, minute=0, second=0, microsecond=0)
        now = executer_state.task.start_at.replace(hour=0, minute=0, second=0, microsecond=0)
        executer_state.start_at = now
        executer_state.stop_at = now
        executer_state.correction_comment = "Исполнитель не явился"
        executer_state.status = "STOP"
        executer_state.save()
        task.save()
        return setExecuterAsViolator(task=task)


class TestWork(graphene.Mutation):
    """
    Мутация отметки тестовой работы в Заявке
    """

    class Arguments:
        input = inputTaskIdExecuterID(required=True)

    task = graphene.Field(TaskType, required=True)

    def mutate(root, info, input):

        task = get_task(info, input.id_task)
        executer_state = ExecuterState.objects.filter(executer__id=input.id_executer, task=task).first()

        if executer_state is None:
            raise EH.customError("Ошибка", "пользователь не найден")
        assert executer_state.stop_at is None, "У Исполнителя стоит отметка о том, что заявка выполнена"
        executer_state.start_at = datetime(2000, 1, 1, 0, 0, 0, 0)
        executer_state.stop_at = datetime(2000, 1, 1, 0, 0, 0, 0)
        executer_state.correction_comment = "Тестовая услуга"
        executer_state.status = "STOP"
        executer_state.save()
        task.save()
        return TestWork(task=task)


class MutationTaskForManager(ObjectType):
    """
    Мутации Заявок
    """

    manager_task_upsert = UpsertTask.Field(required=True)
    manager_task_delete = deleteTask.Field(required=True)

    manager_set_correction_comment_to_executer_in_task = setCorrectionCommentToExecuterInTask.Field(required=True)
    manager_start_task = startTask.Field(required=True)
    manager_stop_task = stopTask.Field(required=True)
    manager_set_volume_of_work_by_executer_state = SetVolumeOfWorkByExecuterState.Field(required=True)
    manager_task_archive = archiveTask.Field(required=True)
    manager_task_unarchive = unarchiveTask.Field(required=True)
    manager_set_executer_as_violator_in_task_by_id = setExecuterAsViolator.Field(required=True)
    manager_set_executer_as_tester = TestWork.Field(required=True)

    manager_approve_tasks = ApproveTask.Field(required=True)
    manager_forbid_tasks_with_comment = ForbidTask.Field(required=True)
