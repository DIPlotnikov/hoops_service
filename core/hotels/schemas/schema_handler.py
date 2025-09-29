import logging
from typing import Union

import jwt
from django.conf import settings

from ..models import Admin, Executer, FCMToken, Manager, RoleAdmin
from ..scripts import exception_handler as EH

logger = logging.getLogger(__name__)


def set_session(info, object):

    info.context.session.create()
    info.context.session["role"] = type(object).__name__
    info.context.session["id"] = object.id
    if hasattr(object, "permissions"):
        info.context.session["permissions"] = object.permissions
    info.context.session["user_agent"] = info.context.META["HTTP_USER_AGENT"]
    info.context.session.set_expiry(60 * 60 * 24 * 30 * 2)
    logger.info(f"Присвоение сессии {object} {info.context.META['HTTP_USER_AGENT']}")


def isAuth(info, temp=""):
    """
    Проверка, что пользлватель авторизован
    """

    try:
        token = info.context.headers.get("authorization")
        if not token:
            token = info.context.headers.get(b"authorization").decode("utf-8")
        token = token.split(" ")[1]
    except Exception:
        if temp != "":
            raise EH.customError(temp)
        raise EH.customError("Ошибка", "пользователь не авторизован")
    if token is None:
        if temp != "":
            raise EH.customError(temp)
        raise EH.customError("Ошибка", "пользователь не авторизован")
    token_d = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    if token_d.get("role") == 1:
        manager = Manager.objects.get(id=token_d.get("id"))
        if manager.is_active is False or manager.status == 1 or manager.status == 0:
            raise EH.customError("Ошибка", "пользователь не авторизован")
    if token_d.get("role") == 2:
        if token_d.get("id") == Executer.get_technical_account() and info.operation.operation == "mutation":
            raise ValueError("Технический аккаунт может только смотреть!")
        executer = Executer.objects.get(id=token_d.get("id"))
        if executer.is_active is False:
            raise EH.customError("Ошибка", "пользователь не авторизован")

    return token


def is_manager_admin(info):
    id_o, role, admin = getIDRoleAdmin(isAuth(info))
    assert role == 1, "Нет прав доступа"
    manager = Manager.objects.select_related("hotel").filter(id=id_o, is_admin=True).first()
    assert manager, "Неизвестный пользователь"
    return manager


def isValidate(token, info, fcm_token=None):
    """
    Проверка токена
    :param token: токен jwt
    :param fcm_token: токен fcm для Исполнителя
    :return: объект пользователя
    """
    # пробуем
    try:
        # декодирование токена
        token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])  # ,  options={'verify_exp': False})
        # получение типа пользователя
        type_object = token.get("type")
        # получение его идентификатора в системе
        id_object = token.get("id")

        # если типа нет
        if not type_object:
            # из словаря типов
            types_objects = {-1: "Admin", 1: "Manager", 2: "Executer"}
            # получаем тип обьекта
            type_object = types_objects.get(token.get("role"), -9)
            token["type"] = type_object

        # получаем объект
        object_user = globals()[type_object].objects.get(id=id_object, is_active=True)
        # проверка валидации (у всех сущностей есть свойство валидации)
        object_user.validate
        # fcm токен для пушей только у Исполнителей
        if type(object_user) is Executer and fcm_token:
            fcm_token_object, created = FCMToken.objects.get_or_create(token=fcm_token, executer=object_user)
        return token
    # в случае ошибки
    except Exception as e:
        # делаем ошибку - она улетит на фронтенд
        logger.error(e)
        raise ValueError("Неизвестный пользователь")


def get_token(info):
    try:
        token = info.context.headers.get("authorization")
        token = token.split(" ")[1]
        token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except Exception:
        raise EH.customError("Ошибка", "пользователь не авторизован")
    if token is None:
        raise EH.customError("Ошибка", "пользователь не авторизован")
    return token


def is_admin(*, info, permission, model=False) -> Union[str, Admin]:
    """
    Проверка на Администратора
    :param info: Информация о запросе
    :param permission: Тип прав, которые проверяются
    :param model: Флаг на возврат сущности админа
    :return: Идентификатор админа
    """
    token = get_token(info)
    if token.get("role") != -1:
        logger.critical(f"Неизвестный пользователь попытался пройти администратором {info}")

    id_admin = token.get("id")
    current_roles = RoleAdmin.objects.filter(admin__id=id_admin).values_list("role", flat=True)

    if type(permission) is not list:
        permission = [permission]
    for per in permission:
        if per in current_roles:
            break
    else:
        logger.critical(f"Неуспешная проверка Администратора: id:{id_admin}  permissions:{permission}")
        raise PermissionError(
            f"Нарушение прав доступа - обратитесь к техническому специалисту {permission} {current_roles}"
        )

    # пишем лог
    logger.info(f"Успешная проверка Администратора: id:{id_admin} permissions:{permission}")
    return id_admin if not model else Admin.objects.get(id=id_admin)


def getIDRole(token):
    token_d = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    return token_d.get("id"), token_d.get("role")


def isExecuter(token):
    token_d = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    assert token_d.get("role") == 2, "Нет прав доступа"
    return token_d.get("id")


def getID(token):
    id, role = getIDRole(token)
    return id


def getIDRoleAdmin(token):
    token_d = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    return token_d.get("id"), token_d.get("role"), token_d.get("admin")


def is_manager(*, info, permission=None, model=False, is_admin=False) -> Union[str, Manager]:
    """
    Проверка на Менеджера
    @param info: Информация о запросе
    @param permission: Тип прав, которые проверяются
    @param model: Флаг на возврат сущности админа
    @param is_admin: Признак главного
    :return: Идентификатор менеджера или его инстанс
    """

    token = get_token(info)

    assert token.get("role") == 1, "Нет прав доступа"

    manager = Manager.objects.prefetch_related("roles").filter(id=token.get("id", -1)).first()
    assert manager, "Пользователь не найден"
    if is_admin:
        assert manager.is_admin, "Не достаточно прав"
    if permission:
        assert set(permission) & set(manager.roles.values_list("role", flat=True)), "Не достаточно прав"

    return manager


def is_executer(*, info) -> Union[str, Executer]:
    """
    Проверка на Исполнителя
    @param info: Информация о запросе
    :return: Идентификатор исполнителя или его инстанс
    """

    token = get_token(info)

    assert token.get("role") == 2, "Нет прав доступа"

    executer = Executer.objects.filter(id=token.get("id", -1)).first()
    assert executer, "Пользователь не найден"

    return executer
