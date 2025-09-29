import graphene
from admin.queries import AdminQueries
from closing_documents.mutation import MutationClosingDocument
from closing_documents.query import QueryClosingDocument
from django.conf import settings
from executor.queries import ExecutorQueries, ExecutorQueriesForAdmin
from hotels.schemas.admin.mutation import MutationAdmin
from hotels.schemas.admin.mutations.manager import MutationAdminManager
from hotels.schemas.admin.query import QueryAdmin
from hotels.schemas.agreement.mutation import MutationAgreement
from hotels.schemas.agreement.query import QueryAgreement
from hotels.schemas.executer.mutation import MutationExecuter
from hotels.schemas.executer.query import QueryExecuter
from hotels.schemas.feedback.mutation import MutationFeedback
from hotels.schemas.feedback.query import QueryFeedback
from hotels.schemas.hotel.mutation import MutationHotel
from hotels.schemas.hotel.query import QueryHotel
from hotels.schemas.infoblock.mutation import MutationInfoBlock
from hotels.schemas.infoblock.query import QueryInfoBlock
from hotels.schemas.landing_post.mutation import MutationPostLanding
from hotels.schemas.landing_post.query import QueryPostLanding
from hotels.schemas.logo.mutation import MutationLogo
from hotels.schemas.logo.query import QueryLogo
from hotels.schemas.manager.mutation import MutationManager
from hotels.schemas.manager.query import QueryManager
from hotels.schemas.notice.mutation import MutationNotice
from hotels.schemas.notice.query import QueryNotice
from hotels.schemas.notice_executer.mutation import MutationExecuterNotice
from hotels.schemas.notice_executer.query import QueryExecuterNotice
from hotels.schemas.notification.mutation import MutationNotify
from hotels.schemas.notification.query import QueryNotification
from hotels.schemas.post.mutation import MutationPost
from hotels.schemas.post.query import QueryPost
from hotels.schemas.profession.mutation import MutationProfession
from hotels.schemas.profession.query import QueryProfession
from hotels.schemas.schema_address import MutationAddress, QueryAddress
from hotels.schemas.schema_info import QueryStatistic
from hotels.schemas.schema_personal_profession import MutationPersonalProfession, QueryPersonalProfession
from hotels.schemas.schema_validate import QueryValidateToken
from hotels.schemas.scheme_requisites import Mutationrequisites, QueryRequisites
from hotels.schemas.stat_doc.mutation import MutationStatDocs
from hotels.schemas.stat_doc.query import QueryStatDocs
from hotels.schemas.task.mutation import MutationTask
from hotels.schemas.task.mutations.admin import MutationTaskForAdmin
from hotels.schemas.task.query import QueryTask
from manager.mutations import ManagerMutation
from manager.queries import ManagerQueries
from passports.mutation import MutationPassportData
from passports.query import QueryPassportData
from payment.queries import PaymentQueries


class Query(
    AdminQueries,
    QueryAdmin,
    QueryHotel,
    QueryManager,
    QueryRequisites,
    QueryExecuterNotice,
    QueryProfession,
    QueryExecuter,
    QueryValidateToken,
    QueryInfoBlock,
    QueryPersonalProfession,
    QueryAgreement,
    QueryClosingDocument,
    QueryNotice,
    QueryPost,
    QueryLogo,
    QueryPostLanding,
    QueryNotification,
    QueryPassportData,
    QueryAddress,
    QueryStatistic,
    QueryFeedback,
    QueryStatDocs,
    QueryTask,
    ManagerQueries,
    PaymentQueries,
    ExecutorQueries,
    ExecutorQueriesForAdmin,
):
    pass


class Mutation(
    MutationPersonalProfession,
    MutationNotify,
    MutationProfession,
    MutationExecuter,
    MutationNotice,
    MutationPost,
    MutationExecuterNotice,
    MutationAdminManager,
    MutationLogo,
    MutationTaskForAdmin,
    MutationHotel,
    MutationManager,
    MutationAdmin,
    MutationPassportData,
    Mutationrequisites,
    MutationAddress,
    MutationInfoBlock,
    MutationPostLanding,
    MutationStatDocs,
    MutationTask,
    MutationFeedback,
    MutationAgreement,
    MutationClosingDocument,
    ManagerMutation,
):
    pass


if settings.DEV:
    from hotels.schemas.notification.subscription import SubscriptionNotification

    class Subscription(SubscriptionNotification):
        pass

    schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)
else:
    schema = graphene.Schema(query=Query, mutation=Mutation)
