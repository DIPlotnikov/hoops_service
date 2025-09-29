from .mutations.acess import MutationAdminAccess
from .mutations.admin import MutationAdminMain
from .mutations.executer import MutationAdminExecuters
from .mutations.hotel import MutationAdminHotel
from .mutations.payment import MutationAdminPayment
from .mutations.media import MutationAdminMedia


class MutationAdmin(MutationAdminAccess, MutationAdminMain,
                    MutationAdminExecuters, MutationAdminHotel, MutationAdminPayment,MutationAdminMedia):
    pass
