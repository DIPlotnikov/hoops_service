import graphene


class InputFeedback(graphene.InputObjectType):
    feedback_id = graphene.ID(required=False, desc='Идентификатор отзыва опциональный')
    task_id = graphene.ID(required=True, desc='Идентификатор работы')
    rating = graphene.Int(required=True, desc='Оценка по пятибальной шкале')
    comment = graphene.String(required=True, desc='Текст отзыва')


class InputFeedbackManager(InputFeedback):
    executer_id = graphene.ID(required=True, desc='Идентификатор исполнителя')


class InputFeedbackAbout(graphene.InputObjectType):
    id = graphene.ID(required=True, desc='Идентификатор сущности')

