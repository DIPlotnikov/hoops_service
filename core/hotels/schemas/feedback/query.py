import graphene
from .type import FeedbackAboutExecuterByManagerType, FeedbackAboutTaskByExecuterType
from .input import InputFeedbackAbout
from ...models import FeedbackExecuter, FeedbackManager
from ..schema_handler import isAuth, getIDRole
from ...scripts import exception_handler as EH


class QueryFeedback(graphene.ObjectType):

    manager_get_my_feedback = graphene.List(graphene.NonNull(FeedbackAboutExecuterByManagerType), required=True)

    executer_get_my_feedback = graphene.List(graphene.NonNull(FeedbackAboutTaskByExecuterType), required=True)

    feedback_get_about_executer = graphene.List(graphene.NonNull(FeedbackAboutExecuterByManagerType),
                                                required=True, input=InputFeedbackAbout(required=True))
    feedback_get_about_customer = graphene.List(graphene.NonNull(FeedbackAboutTaskByExecuterType),
                                                required=True, input=InputFeedbackAbout(required=True))

   #обработчик managers
    def resolve_manager_get_my_feedback(self, info):
        id_o, role = getIDRole(isAuth(info))

        if role == 1:
            return FeedbackManager.objects.filter(manager_id=id_o)
        raise EH.customError("Ошибка",'нет доступа к данному разделу')


    def resolve_executer_get_my_feedback(self, info):
        id_o, role = getIDRole(isAuth(info))

        if role == 2:
            return FeedbackExecuter.objects.filter(executer_id=id_o)
        raise EH.customError("Ошибка", 'нет доступа к данному разделу')

    def resolve_feedback_get_about_executer(self, info, input):
        id_o, role = getIDRole(isAuth(info))
        return FeedbackManager.objects.filter(executer_id=input.id)


    def resolve_feedback_get_about_customer(self, info, input):
        id_o, role = getIDRole(isAuth(info))
        if role == 2:
            return FeedbackExecuter.objects.filter(task__manager__hotel__id=input.id)
        raise EH.customError("Ошибка", 'нет доступа к данному разделу')