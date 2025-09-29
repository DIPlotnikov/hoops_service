import graphene

from hotels.models import FileInfo
from hotels.schemas.enums import EnumCitizenShip
from hotels.schemas.schema_handler import is_executer
from hotels.utils.date_time import date_normalize
from passports.input import InputPassportData
from passports.models import PassportData
from passports.type import PassportDataType


class ExecuterUpsertPassport(graphene.Mutation):
    class Arguments:
        input = InputPassportData(required=True)

    passportData = graphene.NonNull(PassportDataType)

    @staticmethod
    def mutate(root, info, input):
        executer = is_executer(info=info)

        assert len(input.passportFileInfo) > 0, "Не правильный формат, количество страниц должно быть более 1"
        passport = PassportData.objects.filter(executer=executer.id).first()
        if passport:
            # TODO: вычищать сами файлы тоже надо!!!
            passport.firstPage.delete()
            if passport.secondPage:
                passport.secondPage.delete()
            passport.delete()

        first_page = FileInfo.objects.create(**input.passportFileInfo[0])
        second_page = None
        if len(input.passportFileInfo) > 1:
            second_page = FileInfo.objects.create(**input.passportFileInfo[1])
        input.pop("passportFileInfo")
        date_of_issue = date_normalize(input.pop("date_of_issue"))
        new_object = PassportData(
            executer=executer.pk, firstPage=first_page, secondPage=second_page, date_of_issue=date_of_issue, **input
        )
        new_object.save()
        executer.break_status()
        if input.citizenship == EnumCitizenShip.RUSSIA:
            executer.work_expiration = None
            executer.save()

        return ExecuterUpsertPassport(passportData=new_object)


class ExecuterDeletePassport(graphene.Mutation):

    ok = graphene.Boolean(required=True)

    @staticmethod
    def mutate(root, info):
        passport = PassportData.objects.filter(executer=str(is_executer(info=info).id)).first()
        assert passport, "Паспорт не найден"
        passport.firstPage.delete()
        passport.secondPage.delete()
        passport.delete()
        return ExecuterDeletePassport(ok=True)


class MutationPassportData(graphene.ObjectType):
    executer_upsert_passport = ExecuterUpsertPassport.Field(required=True)
    executer_delete_passport = ExecuterDeletePassport.Field(required=True)
