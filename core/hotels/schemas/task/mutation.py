from .mutations.executer import MutationTaskForExecuter
from .mutations.manager import MutationTaskForManager


class MutationTask(MutationTaskForManager, MutationTaskForExecuter):
    """
    Мутации Заявок
    """

    pass
