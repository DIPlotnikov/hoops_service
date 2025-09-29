from .mutations.activate_deactivate import MutationManagerActivate
from .mutations.auth import MutationManagerAuth
from .mutations.favorite_executors import MutationManagerFavoriteExecutors
from .mutations.invite import MutationManagerInvite
from .mutations.password import MutationManagerPassword
from .mutations.update import MutationManagerUpdate


class MutationManager(
    MutationManagerAuth,
    MutationManagerPassword,
    MutationManagerActivate,
    MutationManagerFavoriteExecutors,
    MutationManagerInvite,
    MutationManagerUpdate,
):
    pass
