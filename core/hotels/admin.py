import dateutil.relativedelta
from django import forms
from django.contrib import admin, messages
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ngettext
from passports.models import PassportData

from .models import (
    Address,
    Admin,
    AdminJournal,
    Agreement,
    Coordinates,
    Executer,
    ExecuterFiles,
    ExecuterNotice,
    ExecuterStatDoc,
    ExecuterState,
    ExecutorJumpFinance,
    FCMToken,
    FeedbackExecuter,
    FeedbackManager,
    FileInfo,
    Hotel,
    InfoBlock,
    Logo,
    Manager,
    Notification,
    Payment,
    PaymentJumpFinance,
    PaymentWithCard,
    PersonalProfession,
    Profession,
    Requisites,
    SimpleRequisite,
    StatDoc,
    Task,
    TempString,
)
from .signals import save_task_in_admin_panel

admin.site.register(Notification)
admin.site.register(Address)
admin.site.register(FileInfo)
admin.site.register(ExecuterFiles)
admin.site.register(StatDoc)
admin.site.register(TempString)
admin.site.register(ExecuterStatDoc)
admin.site.register(FCMToken)
admin.site.register(Payment)
admin.site.register(Agreement)
admin.site.register(InfoBlock)
admin.site.register(Logo)


class ChangeManagerForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    managers = forms.ModelChoiceField(queryset=Manager.objects.all().order_by("middle_name"), label="Менеджер")


def move_to_manager(modeladmin, request, queryset):
    form = None

    if "apply" in request.POST:
        form = ChangeManagerForm(request.POST)

        if form.is_valid():
            manager = form.cleaned_data["managers"]
            queryset.update(manager=manager)
            modeladmin.message_user(request, "Менеджер %s применен к %d заявкам." % (manager, queryset.count()))
            return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = ChangeManagerForm(initial={"_selected_action": request.POST.getlist(ACTION_CHECKBOX_NAME)})

    return render(request, "move_to_manager.html", {"items": queryset, "form": form, "title": "Изменение менеджера"})


move_to_manager.short_description = "Изменить менеджера"


class BarInline(admin.TabularInline):
    model = ExecuterState.task_set.through
    extra = 0  # This will get error
    autocomplete_fields = [
        "task",
    ]


@admin.register(ExecuterState)
class ExecuterStateAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = [
        "id",
        "task_info",
        "executer",
        "start_at",
        "stop_at",
        "volume_of_the_work",
        "payment_status",
        "correction_comment",
    ]
    list_editable = ["start_at", "stop_at", "volume_of_the_work"]
    search_fields = (
        "=id",
        "executer__first_name",
        "executer__second_name",
        "executer__middle_name",
        "task__id",
        "task__start_at",
    )
    list_filter = [
        "status",
    ]
    list_select_related = ("executer",)
    autocomplete_fields = [
        "executer",
    ]
    inlines = (BarInline,)
    actions = ["flush_executer_state", "flush_executer_state_payment"]

    @admin.action(description="Перевести статусы Исполнителей в состояние ОТКЛИКНУЛСЯ")
    def flush_executer_state(self, request, queryset):
        queryset.update(
            start_at=None,
            stop_at=None,
            correction_comment=None,
            volume_of_the_work=None,
            status=ExecuterState.STATE[0][0],
            payment_status=None,
            payment=None,
        )
        self.message_user(
            request,
            ngettext(
                "%d отклик Исполнителя переведен в статус ОТКЛИКНУЛСЯ.",
                "%d откликов Исполнителя переведены в статус ОТКЛИКНУЛСЯ.",
                len(queryset),
            )
            % len(queryset),
            messages.SUCCESS,
        )

    @admin.action(description="Снять отметку о выплатах")
    def flush_executer_state_payment(self, request, queryset):
        for executer_state in queryset:
            executer_state.payment_status = None
            executer_state.payment = None
            executer_state.save()
        # queryset.update(
        #                 payment_status=None,
        #                 payment=None
        #                 )
        self.message_user(
            request,
            ngettext(
                "%d очищен от отметок о выплатах.",
                "%d очищены от отметок о выплатах",
                len(queryset),
            )
            % len(queryset),
            messages.SUCCESS,
        )

    def task_info(self, instance):
        return instance.task_info

    task_info.verbose_name = "Заявка"


@admin.register(AdminJournal)
class AdminJournalAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ["id", "admin", "text", "type", "create_at"]
    search_fields = ("=id", "admin__name", "text")
    list_filter = ["type", "admin"]
    date_hierarchy = "create_at"
    empty_value_display = "---"
    list_select_related = ("admin",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    actions = ["transfer_tasks", "clear_tasks", move_to_manager]

    @admin.action(description="Переместить заявки на 1 месяц назад")
    def transfer_tasks(self, request, queryset):
        for task in queryset:
            task.start_at -= dateutil.relativedelta.relativedelta(months=1)
            task.save()
        self.message_user(
            request,
            ngettext(
                "%d заявка переместилась на 1 месяц назад.",
                "%d заявок переместились на 1 месяц назад.",
                len(queryset),
            )
            % len(queryset),
            messages.SUCCESS,
        )

    @admin.action(description="Очистить старты и стопы в заявках")
    def clear_tasks(self, request, queryset):
        for task in queryset:
            executers = task.executers.all()
            executers.update(start_at=None, stop_at=None, payment_status=None, status="REPLY", correction_comment=None)
        self.message_user(
            request,
            ngettext(
                "%d заявка очищена от старта и стопа.",
                "%d заявок очищены от стартов и стопов.",
                len(queryset),
            )
            % len(queryset),
            messages.SUCCESS,
        )

    list_per_page = 20
    list_editable = ["start_at", "rent", "count_executers", "duration"]
    list_display = [
        "id",
        "rent",
        "count_executers",
        "start_at",
        "duration",
        "profession",
        "manager",
        "is_approved",
        "is_closed",
    ]
    search_fields = ("=id", "manager__first_name", "manager__second_name", "manager__middle_name")
    list_filter = ["is_approved", "profession"]
    date_hierarchy = "start_at"
    empty_value_display = "---"
    list_select_related = ("profession", "personal_profession")
    autocomplete_fields = ["executers", "profession", "personal_profession", "manager"]

    def is_closed(self, instance):
        return instance.is_closed

    is_closed.boolean = True

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        form.base_fields["personal_profession_name"].required = False
        form.base_fields["comment"].required = False
        form.base_fields["executers"].required = False
        form.base_fields["payment_status"].required = False
        return form

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        save_task_in_admin_panel.send(sender=self, instance=form.instance)


@admin.register(PaymentJumpFinance)
class PaymentJumpFinanceAdmin(admin.ModelAdmin):
    list_display = ["id", "contractor", "payment", "amount"]
    search_fields = (
        "=id",
        "=contractor__executer__id",
        "contractor__executer__first_name",
        "contractor__executer__second_name",
        "contractor__executer__middle_name",
        "contractor__executer__phone_number",
    )


#
@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "numerate"]
    search_fields = (
        "=id",
        "name",
    )
    list_filter = [
        "numerate",
    ]


@admin.register(PersonalProfession)
class PersonalProfessionAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "owner", "analog", "rent", "active"]
    search_fields = (
        "=id",
        "owner__nameLegalEntity",
        "owner__nameHotel",
        "name",
    )

    autocomplete_fields = [
        "owner",
        "analog",
    ]


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    exclude = ("Executers",)
    list_display = [
        "id",
        "nameLegalEntity",
        "nameHotel",
        "is_active",
        "is_verify",
        "is_test",
        "max_count_of_personal_profession",
    ]
    search_fields = ("=id", "nameLegalEntity", "nameHotel")
    list_filter = ["is_active", "is_verify", "is_test"]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["phone_number"].required = False
        form.base_fields["undergroundStation"].required = False

        return form


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    exclude = ("password",)
    list_display = ["id", "fullname", "hotel", "email", "is_admin", "is_active", "status"]
    search_fields = ("=id", "first_name", "second_name", "middle_name", "email")
    list_filter = ["is_admin", "is_active", "status", "hotel"]


@admin.register(Executer)
class ExecuterAdmin(admin.ModelAdmin):
    """
    Модель Исполнителя в администрировании БД
    """

    exclude = ("password",)
    list_display = [
        "id",
        "middle_name",
        "first_name",
        "second_name",
        "is_test_short",
        "phone_number",
        "email",
        "citizenship",
        "professions_comma",
        "status",
        "is_active",
        "work_expiration",
        "medical_book_expiration",
    ]
    search_fields = ("=id", "first_name", "second_name", "middle_name", "phone_number")
    list_filter = ["is_active", "status", "is_test"]
    date_hierarchy = "created_at"
    empty_value_display = "---"

    def citizenship(self, obj):
        pp = PassportData.objects.filter(executer=obj.id).last()
        return pp.citizenship if pp else "---"

    citizenship.short_description = "Гражданство"

    def professions_comma(self, obj):
        return ", ".join([p.name for p in obj.professions.all()])

    professions_comma.short_description = "Профессии"

    def is_test_short(self, obj):
        return obj.is_test

    is_test_short.short_description = "Т"
    is_test_short.boolean = True


@admin.register(ExecutorJumpFinance)
class ExecutorJumpFinanceAdmin(admin.ModelAdmin):
    list_display = ["id_contractor", "executer"]
    search_fields = (
        "=id",
        "id_contractor",
        "=executer__id",
        "executer__first_name",
        "executer__second_name",
        "executer__middle_name",
        "executer__phone_number",
    )
    list_select_related = ("executer",)
    autocomplete_fields = ["executer"]


class TaskInline(admin.StackedInline):
    model = Task.executers.through
    extra = 0


@admin.register(Requisites)
class RequisitesAdmin(admin.ModelAdmin):
    pass


@admin.register(Coordinates)
class CoordinatesAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        print(form.base_fields)
        form.base_fields["label"].required = False

        return form


@admin.register(Admin)
class AdminsAdmin(admin.ModelAdmin):
    exclude = ("password",)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # form.base_fields["label"].required = False

        return form


@admin.register(FeedbackExecuter)
class FeedbackExecuterAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        print(form.base_fields)
        # form.base_fields["label"].required = False

        return form


@admin.register(FeedbackManager)
class FeedbackManagerAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        print(form.base_fields)
        # form.base_fields["label"].required = False

        return form


@admin.register(SimpleRequisite)
class SimpleRequisiteAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "executer",
        "inn",
        "card_number",
    ]
    search_fields = ("=id", "executer__first_name", "executer__second_name", "executer__middle_name")

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        print(form.base_fields)
        # form.base_fields["label"].required = False

        return form


@admin.register(PaymentWithCard)
class PaymentWithCardAdmin(admin.ModelAdmin):
    list_display = ["id", "executer", "create_at", "payment_id"]
    search_fields = ("=id", "executer__first_name", "executer__second_name", "executer__middle_name", "=executer__id")

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        print(form.base_fields)
        # form.base_fields["label"].required = False

        return form


@admin.register(ExecuterNotice)
class ExecuterNoticeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "executer",
        "is_auto_generate",
        "create_at",
    ]
    search_fields = ("=id", "executer__first_name", "executer__second_name", "executer__middle_name", "=executer__id")
