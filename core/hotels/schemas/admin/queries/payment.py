from datetime import timedelta

import graphene
from django.db.models import Q
from graphene_django.fields import DjangoConnectionField

from ..input import InputArchive, InputId, InputIdAndArchive
from ..type import PaymentType
from ...payment.input import InputPaymentForAdmin
from ...schema_handler import is_admin
from ....models import Payment, RoleAdmin


class QueryPaymentAdmin(graphene.ObjectType):
    admin_payment_get_all = DjangoConnectionField(PaymentType, input=InputArchive(required=True), required=True)
    admin_payment_get_by_hotel_id = DjangoConnectionField(
        PaymentType, input=InputIdAndArchive(required=True), required=True
    )
    admin_payment_get_by_id = graphene.NonNull(PaymentType, input=InputId(required=True))
    admin_payment_get_all_individual = DjangoConnectionField(
        PaymentType, input=InputPaymentForAdmin(required=True), required=True
    )

    def resolve_admin_payment_get_all(self, info, input, **kwargs):
        is_admin(info=info, permission=RoleAdmin.Roles.PAYMENTS.value)
        return Payment.objects.filter(is_archive=input.is_archive, is_individual=False)

    def resolve_admin_payment_get_by_hotel_id(self, info, input, **kwargs):
        is_admin(info=info, permission=RoleAdmin.Roles.PAYMENTS.value)
        payments = Payment.objects.filter(is_individual=False)
        if input.id:
            # payments_ids = list(set(list(payments.filter(tasks__manager__hotel__id=input.id).values_list('id', flat=True))))
            payments = payments.filter(tasks__manager__hotel__id=input.id).order_by("id").distinct()
            # payments = payments.filter(id__in=payments_ids)

        if input.is_archive is not None:
            payments = payments.filter(is_archive=input.is_archive)
        if input.start_date and input.end_date:
            start_date = input.start_date.replace(hour=0, minute=0, second=0, microsecond=0)
            payments = payments.filter(start_date__gte=start_date).filter(end_date__lte=input.end_date)
        if input.status_executer:
            payments = payments.filter(status_executers=input.status_executer)
        if input.status_hotel:
            payments = payments.filter(status_hotel=input.status_hotel)
        return payments

    def resolve_admin_payment_get_by_id(self, info, input):
        is_admin(info=info, permission=RoleAdmin.Roles.PAYMENTS.value)
        return Payment.objects.get(id=input.id)

    def resolve_admin_payment_get_all_individual(self, info, input, **kwargs):
        is_admin(info=info, permission=RoleAdmin.Roles.PAYMENTS.value)
        filters = [Q(is_individual=True)]
        if input.is_archive is not None:
            filters.append(Q(is_archive=input.is_archive))
        # if input.hotel_name is not None:
        #     filters.append(Q(tasks__manager__hotel__name__icontains=input.hotel_name))
        if input.hotel_id:
            filters.append(Q(tasks__manager__hotel_id=input.hotel_id))
        if input.task_id:
            filters.append(Q(tasks__id=input.task_id))
        if input.date:
            input_date = input.date - timedelta(minutes=int(info.context.headers.get("time-zone-offset", -180)))
            filters.append(Q(create_at__date=input_date.date()))
        return Payment.objects.filter(*filters).order_by("-create_at").distinct()
