import graphene
from .type import FeedbackAboutExecuterByManagerType, FeedbackAboutTaskByExecuterType
from .input import InputFeedback, InputFeedbackManager
from ...models import FeedbackExecuter, Task, Executer, FeedbackManager, Notification
from ..schema_handler import isAuth, getIDRole
from ...scripts import exception_handler as EH
from datetime import datetime, timedelta


class UpsertFeedbackExecuter(graphene.Mutation):
    class Arguments:
        input = InputFeedback(required=True)

    feedback_executer = graphene.NonNull(FeedbackAboutTaskByExecuterType)

    @staticmethod
    def mutate(root, info, input):
        # TODO: проверить что отзыв 1
        id_o, role = getIDRole(isAuth(info))

        if role != 2:
            raise EH.customError("Ошибка", 'отзыв может оставлять только исполнитель')


        if input.feedback_id is not None:
            feedback = FeedbackExecuter.objects.filter(id=input.feedback_id,
                                                     task_id=input.task_id, executer_id=id_o)
            if len(feedback) == 0:
                raise EH.customError("Ошибка", 'что то не так с идентификаторами отзыва')

            executer_state = feedback[0].task.executers.filter(executer_id=id_o).first()
            if executer_state.stop_at.timestamp() < (datetime.now() - timedelta(hours=24)).timestamp():
                raise EH.customError("Ошибка", 'на создание отзыва дается 24 часа')
            feedback.update(rating=input.rating, comment=input.comment)

        task = Task.objects.filter(id=input.task_id, executers__executer__id=id_o).first()

        if task is None:
            raise EH.customError("Ошибка", 'нельзя оставлять отзыв о данной работе')
        executer_status = task.executers.filter(executer_id=id_o).first()

        if executer_status.status != "STOP":
            raise EH.customError("Ошибка", 'задача не закрыта заказчиком, необходимо его подтверждение о завершении')
        if executer_status.stop_at.timestamp() < (datetime.now() - timedelta(hours=24)).timestamp():
            raise EH.customError("Ошибка", 'на создание отзыва дается 24 часа')

        feedback = FeedbackExecuter(task=task, executer=executer_status.executer,
                                    rating=input.rating, comment=input.comment)
        feedback.save()
        return UpsertFeedbackExecuter(feedback_executer=feedback)


class UpsertFeedbackManager(graphene.Mutation):
    class Arguments:
        input = InputFeedbackManager(required=True)

    feedback_manager = graphene.NonNull(FeedbackAboutExecuterByManagerType)

    @staticmethod
    def mutate(root, info, input):
        #TODO: проверить что отзыв 1
        id_o, role = getIDRole(isAuth(info))
        if role != 1:
            raise EH.customError("Ошибка", 'нет прав доступа')
        if input.feedback_id is not None:
            feedback = FeedbackManager.objects.filter(id=input.feedback_id, task_id=input.task_id,
                                                      manager_id=id_o, executer_id=input.executer_id)
            if len(feedback) == 0:
                raise EH.customError("Ошибка", 'что то не так с идентификаторами отзыва')

            executer_state = feedback[0].task.executers.filter(executer=feedback[0].executer).first()
            # if executer_state.stop_at.timestamp() < (datetime.now() - timedelta(hours=24)).timestamp():
            #     raise EH.customError("Ошибка", 'на создание отзыва дается 24 часа')
            executer = feedback[0].executer
            executer.score += input.rating
            executer.score -= feedback[0].rating
            executer.save()
            feedback.update(rating=input.rating, comment=input.comment)
            return UpsertFeedbackManager(feedback_manager=feedback[0])

        task = Task.objects.filter(id=input.task_id, manager_id=id_o).first()
        if task is None:
            raise EH.customError("Ошибка", 'нельзя оставлять отзыв о данной работе')

        executer_state = task.executers.filter(executer_id=input.executer_id).first()
        if executer_state is None:
            raise EH.customError("Ошибка", 'отсутствует такой исполнитель')
        if executer_state.status != "STOP":
            raise EH.customError("Ошибка", 'работа исполнителя не завершена')
        # if executer_state.stop_at.timestamp() < (datetime.now() - timedelta(hours=24)).timestamp():
        #     raise EH.customError("Ошибка", 'на создание отзыва дается 24 часа')

        feedback = FeedbackManager(task=task, executer=executer_state.executer,
                                   manager=task.manager,
                                   rating=input.rating, comment=input.comment)
        feedback.save()
        executer = executer_state.executer
        executer.score += input.rating
        executer.count_work_with_rating += 1
        executer.save()
        notify = Notification(type=Notification.TypeNotification.ACCOUNT,
                              id_instance=executer.pk, role='executer', read=False,
                              text=f'У Вас новый отзыв!')
        notify.save(notification=True)

        return UpsertFeedbackManager(feedback_manager=feedback)





class MutationFeedback(graphene.ObjectType):

    executer_upsert_feedback_about_task = UpsertFeedbackExecuter.Field(required=True)

    manager_upsert_feedback_about_executer_in_task = UpsertFeedbackManager.Field(required=True)
