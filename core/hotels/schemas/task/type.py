import graphene
from graphene import ObjectType, relay
from graphene_django.types import DjangoObjectType

from ..additional_task.type import AdditionalTaskType
from ..admin.type import executerForAdmin
from ..comment_of_task.type import CommentOfTaskType
from ..enums import PaymentStatus
from ..executer.type import ExecuterType
from ..feedback.type import FeedbackAboutExecuterByManagerType, FeedbackAboutTaskByExecuterType
from ..manager.type import ManagerType
from ..pagination import ExtendedConnection
from ..profession.type import ProfessionType
from ...models import ApprovedStatus, ApprovedStatusEnum, ExecuterState, FeedbackExecuter, FeedbackManager, Task


class ExecuterStateType(DjangoObjectType):
    class Meta:
        model = ExecuterState
        exclude = ("task_set",)

    payment_status = PaymentStatus(required=False)

    executer = graphene.NonNull(ExecuterType)
    feedback = graphene.Field(FeedbackAboutExecuterByManagerType, description="Отзыв об исполнителе")
    is_violator = graphene.Boolean(required=True, description="флаг нарушителя")
    is_test = graphene.Boolean(required=True, description="флаг тестера")
    pay_in_rubles = graphene.Float(required=True, description="оплата в рублях")
    volume_of_the_work = graphene.Float(required=True, description="объем работы")

    # feedback_about_task = graphene.Field(FeedbackAboutTaskByExecuterType, description='Отзыв о выполненной задаче')

    def resolve_task(self, info):
        return self.task

    def resolve_feedback(self, info):
        return FeedbackManager.objects.filter(executer=self.executer, task=self.task_set.all().first()).first()

    def resolve_feedback_about_task(self, info):
        return FeedbackExecuter.objects.filter(executer=self.executer, task=self.task_set.all().first()).first()

    def resolve_is_violator(self, info):
        if (
            self.status == "STOP"
            and self.start_at == self.stop_at
            and self.correction_comment == "Исполнитель не явился"
        ):
            return True
        return False

    def resolve_is_test(self, info):
        if self.status == "STOP" and self.start_at == self.stop_at and self.correction_comment == "Тестовая услуга":
            return True
        return False

    def resolve_pay_in_rubles(self, info):
        return self.get_sum_full

    def resolve_volume_of_the_work(self, info):
        return float(self.get_work_time_in_hours or 0.0)


class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection
        exclude = (
            "feedbackexecuter_set",
            "feedbackmanager_set",
            "payment_status",
            "is_archived_for_admin",
            "personal_profession_name",
            "payment_set",
            "closingdocument_set",
            "commentoftask_set",
        )

    id = graphene.ID(required=True)
    profession = graphene.NonNull(ProfessionType, description="Профессия")
    start_at_date = graphene.Date(required=True, description="Дата старта заявки")
    start_at_time = graphene.Time(required=True, description="Время старта заявки")
    manager = graphene.NonNull(ManagerType, description="Менеджер")
    is_closed = graphene.Boolean(required=True, description="Флаг, что заявка либо набралась либо началась")
    rent = graphene.Float(required=True, description="Часовая ставка с условием")
    executers = graphene.List(graphene.NonNull(ExecuterStateType), required=True, description="Список Исполнителей")
    comment_of_task = graphene.List(
        graphene.NonNull(CommentOfTaskType), required=True, description="Комментарии о Заявке"
    )
    approved_status = graphene.NonNull(ApprovedStatusEnum, description="Статус подтверждения")
    count_executors_with_start = graphene.Int(
        required=True, description="Количество Исполнителей, которые приступили к работе"
    )
    count_executors_with_stop = graphene.Int(
        required=True, description="Количество Исполнителей, которые завершили работу"
    )
    count_executors_violators = graphene.Int(required=True, description="Количество Исполнителей, которые не явились")
    additional = graphene.Field(AdditionalTaskType, description="Доп комментарий")

    def resolve_is_closed(self, info):
        return self.is_closed

    def resolve_id(self, info):
        return self.pk

    def resolve_start_at_date(self, info):
        return self.start_at

    def resolve_start_at_time(self, info):
        return self.start_at.time()

    def resolve_rent(self, info):
        if info.context.user.id == 2:
            return round(self.rent * self.profession.multiplier / 100, 2)
        else:
            return self.rent

    def resolve_executers(self, info):
        if info.context.user.id == 2:
            return []
        return self.executers.all()

    def resolve_comment_of_task(self, info):
        if info.context.user.id == 2:
            return []
        return self.commentoftask_set.all()

    def resolve_approved_status(self, info):
        if self.is_approved:
            return ApprovedStatus.APPROVED
        if len(self.commentoftask_set.all()) > 0:
            if self.updated_at < self.commentoftask_set.last().created_at:
                return ApprovedStatus.FORBIDDEN
        return ApprovedStatus.WAITING

    def resolve_count_executors_with_start(self, info):
        return self.executers.filter(status__in=["START", "STOP"]).count()

    def resolve_count_executors_with_stop(self, info):
        return self.executers.filter(status="STOP").count()

    def resolve_count_executors_violators(self, info):
        return self.executers.filter(correction_comment="Исполнитель не явился на заявку").count()


class ExecuterStateTypeForExecuter(ExecuterStateType):
    """
    Статус отклика исполнителя для Исполнителя
    """

    class Meta:
        model = ExecuterState
        exclude = ("task_set",)

    task = graphene.NonNull(TaskType)

    def resolve_task(self, info):
        return self.task


class ExecuterStateTypeForAdmin(ExecuterStateType):
    """Статус отклика исполнителя для Админа"""

    class Meta:
        model = ExecuterState
        exclude = ("task_set",)

    task = graphene.NonNull(TaskType)
    executer = graphene.NonNull(executerForAdmin)

    def resolve_task(self, info):
        return self.task


class DateTasksType(ObjectType):
    date = graphene.Date(required=True)
    tasks = graphene.List(graphene.NonNull(TaskType), required=True)

    def resolve_date(self, info):
        return self.tasks[0].start_at


class TaskForAdminType(DjangoObjectType):
    class Meta:
        model = Task
        interfaces = (relay.Node,)
        connection_class = ExtendedConnection
        exclude = ("feedbackexecuter_set", "feedbackmanager_set")

    id = graphene.ID(required=True)
    is_archived = graphene.Boolean(required=True)
    profession = graphene.NonNull(ProfessionType)
    manager = graphene.NonNull(ManagerType)
    payment_status = PaymentStatus(required=False)
    payment_status_for_executer = PaymentStatus(required=False)

    def resolve_id(self, info):
        return self.pk

    def resolve_id(self, info):
        return self.pk

    def resolve_payment_status_for_executer(self):
        if self.executers.all().filter(payment_status="create_payment").first():
            return PaymentStatus.create_payment
        if self.executers.all().filter(payment_status="paid_payment").first():
            return PaymentStatus.paid_payment
        return None

    def resolve_is_archived(self, info):
        return self.is_archived_for_admin


class TaskPagination(relay.Connection):
    class Meta:
        node = graphene.NonNull(TaskType)


class ExecuterTaskType(ObjectType):
    class Meta:
        description = "Task for executer"

    # implicitly mounted as Field
    task = graphene.NonNull(TaskType)
    # explicitly mounted as Field
    feedback = graphene.Field(FeedbackAboutTaskByExecuterType)
    id = graphene.ID(required=True)
    status = graphene.Field(ExecuterStateType, required=True)

    def resolve_id(self, info):
        return self.id

    def resolve_task(self, info):
        return self.task

    def resolve_feedback(self, info):
        return self.feedback

    def resolve_status(self, info):
        return self.status


class ExecuterStateIDAndTAskStartAt(ObjectType):
    id = graphene.ID(required=True, description="ID отклика Исполнителя")
    start_at = graphene.DateTime(required=True, description="Старт заявки")

    def resolve_id(self, info):
        return self.id

    def resolve_start_at(self, info):
        return self.task.start_at
