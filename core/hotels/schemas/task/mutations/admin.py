import dateutil.relativedelta
import graphene

from ....models import AdminJournal, Executer, ExecuterState, Notification, RoleAdmin, Task
from ...input import InputIdTaskIdExecuter
from ...schema_handler import is_admin
from ..input import inputIDs
from ..type import TaskForAdminType


class DeleteExecuterStates(graphene.Mutation):
    """
    Удаление откликов Администратором
    """

    class Arguments:
        input = inputIDs(required=True)

    class Meta:
        output = graphene.Boolean

    @staticmethod
    def mutate(root, info, input):
        admin = is_admin(info=info, permission=RoleAdmin.Roles.TASK.value, model=True)
        executer_states = ExecuterState.objects.prefetch_related("task_set", "task_set__manager").filter(
            id__in=input.ids
        )
        for executer_state in executer_states:
            executer_state.task.is_block_to_modify
        for executer_state in executer_states:
            message = f"{admin} удалил отклик Исполнителя {executer_state.executer.full_name} на {executer_state.task}"

            AdminJournal.objects.create(admin=admin, text=message)

            notify = Notification(
                type=Notification.TypeNotification.TASK,
                id_instance=executer_state.task.manager.pk,
                role="manager",
                read=False,
                text=f"Один из исполнителей отказался от заявки #{executer_state.task.id}",
            )
            notify.save(task_id=executer_state.task.pk)

            notify = Notification(
                type=Notification.TypeNotification.TASK,
                id_instance=executer_state.executer.pk,
                role="executer",
                read=False,
                text=f"Вы исключены из выполнения  заявки #{executer_state.task.pk} на {str(executer_state.task.start_at)[:11]}.",
            )
            notify.save(notification=True)

            executer_states.delete()

        return True


class CreateExecuterStateByTaskIDAndExecuterID(graphene.Mutation):
    """
    Создание отклика Администратором
    """

    class Arguments:
        input = InputIdTaskIdExecuter(required=True)

    task = graphene.NonNull(TaskForAdminType)

    @staticmethod
    def mutate(root, info, input):
        admin = is_admin(info=info, permission=RoleAdmin.Roles.TASK.value, model=True)
        # logger.info(f'{admin} начал создание отклика на заявку {input.id_task} исполнителя {input.id_executer}')

        task = (
            Task.objects.prefetch_related("executers")
            .filter(id=input.id_task)
            .exclude(executers__executer__id__in=[input.id_executer])
            .first()
        )
        assert task, "Заявка не найдена или Исполнитель на нее уже откликнулся"
        task.is_block_to_modify

        executer = Executer.objects.filter(id=input.id_executer).first()
        assert executer is not None, "Исполнитель не найден"
        assert executer.status == "STEP_3_VERIFIED", "Аккаунт Исполнителя не подтвержден"
        assert executer.is_test is False, "Аккаунт Исполнителя тестовый"
        assert executer.check_tasks_by_task(task), "Данная дата занята другой заявкой"

        executer_state = ExecuterState(executer=executer)
        executer_state.save()

        task.executers.add(executer_state)
        task.save()

        if task.count_executers < task.executers.all().count():
            task.count_executers = task.executers.all().count()
            task.save()
            message = f"{admin} изменилось количество исполнителей у заявки {task.id} из-за добавления"
            AdminJournal.objects.create(admin=admin, text=message)
        message = f"{admin} закончил создание отклика на заявку {input.id_task} исполнителя {executer.full_name}"
        AdminJournal.objects.create(admin=admin, text=message)

        notify = Notification(
            type=Notification.TypeNotification.TASK,
            id_instance=task.manager.pk,
            role="manager",
            read=False,
            text=f"На Вашу заявку #{task.id} появился отклик!",
        )
        notify.save(task_id=task.pk)

        return CreateExecuterStateByTaskIDAndExecuterID(task=task)


class MoveTasksToOneMonthAhead(graphene.Mutation):
    """
    Перемещение откликов на 1 месяц назад
    """

    class Arguments:
        input = inputIDs(required=True)

    tasks = graphene.List(graphene.NonNull(TaskForAdminType), required=True)

    @staticmethod
    def mutate(root, info, input):
        admin = is_admin(info=info, permission=RoleAdmin.Roles.TASK.value, model=True)
        tasks = Task.objects.filter(id__in=input.ids)
        for task in tasks:
            task.to_transfer(task.start_at - dateutil.relativedelta.relativedelta(months=1))
            message = f"{admin} переместил заявку {task.id} на 1 месяц назад"
            AdminJournal.objects.create(admin=admin, text=message)
        return MoveTasksToOneMonthAhead(tasks=tasks)


class TaskArchiveForAdmin(graphene.Mutation):
    """
    Переместить в Архив Администратора заявки
    """

    class Arguments:
        input = inputIDs(required=True)

    tasks = graphene.List(graphene.NonNull(TaskForAdminType), required=True)

    @staticmethod
    def mutate(root, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.TASK_ARCHIVE.value)
        tasks = Task.objects.filter(id__in=input.ids)
        tasks.update(is_archived_for_admin=True)
        return TaskArchiveForAdmin(tasks=tasks)


class TaskUnarchiveForAdmin(graphene.Mutation):
    """
    Переместить из Архива Администратора заявки
    """

    class Arguments:
        input = inputIDs(required=True)

    tasks = graphene.List(graphene.NonNull(TaskForAdminType), required=True)

    @staticmethod
    def mutate(root, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.TASK_ARCHIVE.value)
        tasks = Task.objects.filter(id__in=input.ids)
        tasks.update(is_archived_for_admin=False)
        return TaskUnarchiveForAdmin(tasks=tasks)


class MutationTaskForAdmin(graphene.ObjectType):
    """
    Мутации Заявок
    """

    admin_create_executer_state_by_task_id_and_executer_id = CreateExecuterStateByTaskIDAndExecuterID.Field(
        required=True, description="Создание отклика Администратором"
    )
    admin_delete_executer_states_by_id = DeleteExecuterStates.Field(
        required=True, description="Удаление откликов Администратором по их идентификаторам"
    )
    admin_move_tasks_to_one_month_ahead = MoveTasksToOneMonthAhead.Field(
        required=True, description="Перемещение заявок на один месяц назад"
    )
    admin_archive_tasks_by_ids = TaskArchiveForAdmin.Field(required=True, description="Перемещение заявок в архив")
    admin_unarchive_tasks_by_ids = TaskUnarchiveForAdmin.Field(
        required=True, description="Перемещение заявок из архива"
    )
