# Hoops Service — Документация проекта

Этот документ описывает архитектуру, стек, структуру каталогов, поток данных (HTTP и WebSocket), GraphQL-реализацию, авторизацию/аутентификацию, интеграции и модель данных (связи между сущностями) в проекте `hoops_service-new-ci-cd/core`.

Все нестандартные термины и ссылки сопровождаются указанием соответствующих файлов и путей в репозитории, чтобы упростить навигацию по коду.


## 1. Обзор и стек

- Бэкенд: Django 4.2
- API: GraphQL (graphene, graphene-django)
- Реальное время: Django Channels + channels-graphql-ws (подписки включаются в DEV-режиме)
- Очереди/фоновые задачи: Celery + django_celery_results; брокер — Redis (URL через env)
- БД: по умолчанию MySQL (чтение конфига из файла в переменной MYSQL_CONFIG), для тестов SQLite; ранее присутствовала конфигурация PostgreSQL (закомментирована)
- Файловое хранилище и интеграции: MinIO, Firebase (пуш), Tinkoff (оплаты) — ключи/настройки через env
- Контейнеризация: Docker/Docker Compose
- CI/CD: GitLab CI (`.gitlab-ci.yml` в корне проекта)

Ключевые зависимости — `core/requirements.txt`.


## 2. Структура проекта (внутри `core/`)

— Ниже приложения объединены по категориям для удобства навигации.

### 2.1. Ядро платформы
* __`core/core/`__ — настройки и инфраструктура GraphQL/Channels
  - `settings.py` — конфигурация Django/Channels/GraphQL
  - `urls.py` — HTTP-маршрутизация (`/graphql/`)
  - `asgi.py`/`wsgi.py` — точки входа ASGI/WSGI
  - `schema.py` — агрегатор Query/Mutation/Subscription
  - `middlewares.py`, `mid_logger.py` — GraphQL middleware и логирование
  - `celery.py` — инициализация Celery
  - `mp.py` — monkey-patch Enum для GraphQL (см. раздел 6)

### 2.2. Доменные модули (бизнес-логика)
* __`hotels/`__ — ядро домена: заказчики (Hotel), исполнители (Executer), менеджеры (Manager), профессии (Profession), файлы (FileInfo), заявки (Task), уведомления (Notification) и др. Содержит GraphQL-схемы (`schemas/*`).
* __`admin/`__ — административные GraphQL-запросы/интерфейсы (например, агрегирующие выборки, сервисные операции для администраторов проекта).
* __`manager/`__ — функционал менеджеров гостиниц (избранные исполнители, фильтры доступа, ЧС и пр.).
* __`executor/`__ — метрики исполнителей (`Metrics`) и связанные утилиты.
* __`closing_documents/`__ — закрывающие документы за периоды: агрегируют заявки и файлы.
* __`payment/`__ — платежные операции/запросы (GraphQL, интеграции; модели не обнаружены в просмотренных файлах).
* __`passports/`__ — паспортные данные исполнителей (`PassportData`, связь с `FileInfo`).

### 2.3. Аутентификация и пользователи
* __`otp/`__ — одноразовые коды для входа/подтверждения (модель `OTP`, отправка через Telegram).
* __`users/`__ — модуль пользователей/аккаунтов (структура присутствует; детали зависят от реализации в проекте).

### 2.4. Конфигурация и настройки бизнес-логики
* __`settings/`__ — переменные доменной логики (`Variable`) и утилиты доступа (`get_nds()`, `get_remuneration()` и др.).
* __`configs/`__ — служебные конфигурационные файлы/шаблоны (например, окружение, lint, пр.).

### 2.5. Планирование задач и вспомогательные скрипты
* __`tasks.py`__ — Celery-задачи верхнего уровня проекта.
* __`cron.py`__ — периодические задания/триггеры.

### 2.6. Представление/шаблоны
* __`templates/`__ — HTML/текстовые шаблоны (письма, страницы и пр.).

### 2.7. Корень проекта и мета-файлы
* __`manage.py`__, `pyproject.toml`, `requirements.txt`, `Dockerfile`, `.gitlab-ci.yml`, `.pre-commit-config.yaml`, `README.md` — стандартные служебные файлы проекта и сборки.


## 3. Конфигурация и включение GraphQL/Channels

Файл: `core/core/settings.py`

- Включение GraphQL:
  - `GRAPHENE = {"SCHEMA": "core.schema.schema"}` — путь до схемы
  - `INSTALLED_APPS` включает `graphene_django`
- Включение Channels:
  - `ASGI_APPLICATION = "core.asgi.application"`
  - `INSTALLED_APPS` включает `channels`
  - `CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}` — in-memory слой (для продакшена обычно Redis)
- Переключатели окружения:
  - `DEV = os.environ.get("DEV", "not") == "true"` — включает подписки GraphQL (см. `core/core/schema.py`)
  - `DEBUG` — стандартный флаг Django
- БД:
  - По умолчанию MySQL через `read_default_file` (см. `DATABASES["default"]["OPTIONS"]["read_default_file"]`)
  - Для тестов — SQLite in-memory
- Монки-патч GraphQL Enum:
  - `GraphQLEnumValue.__init__ = MonkeyPathingGraphQLEnumValue.__init__` (см. `core/core/mp.py`)


## 4. HTTP-поток (GraphQL через GraphQLView)

Файл: `core/core/urls.py`

- Точка входа: `POST /graphql/` (также доступен GraphiQL при `GET`, потому что `graphiql=True`)
- Обработчик: `graphene_django.views.GraphQLView`
- Отключение CSRF: `csrf_exempt(GraphQLView.as_view(...))`
- Подключенные GraphQL middleware (списком на уровне вьюхи):
  - `AuthMiddleWare()` — извлекает JWT из заголовка `Authorization` и:
    - декодирует `jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])`
    - записывает данные в `info.context.user.pk` и `info.context.user.id` (id и роль из payload)
    - если в токене `read=True` и выполняется Mutation — бросает ошибку (блокировка мутаций в read-only)
    - при просрочке токена — ошибка "Сессия завершена"
  - `LogAllRequests()` — сейчас прозрачный pass-through; в `mid_logger.py` есть `do_log(...)`, который можно подключить при необходимости

Путь выполнения запроса:
1) Django URLConf → `GraphQLView`
2) Цепочка Graphene middleware (`AuthMiddleWare`, затем `LogAllRequests`)
3) Исполнение резолверов схемы (Query/Mutation)
4) Результат сериализуется в JSON


## 5. WebSocket-поток (подписки GraphQL)

Файл: `core/core/asgi.py`

- Роутинг ASGI:
  - HTTP: `"http": get_asgi_application()`
  - WS: `"websocket": URLRouter([ path("graphql/", MyGraphqlWsConsumer.as_asgi()) ])`
- `MyGraphqlWsConsumer` (наследует `channels_graphql_ws.GraphqlWsConsumer`):
  - `schema = schema` — использует ту же схему GraphQL
  - `send_ping_every = 5`
  - `middleware = [demo_middleware]` — пример async-middleware
  - `_on_gql_connection_init`: извлекает `authorization` из payload, вызывает `hotels.schemas.schema_handler.getIDRole(...)`, пишет `id_user` и `role_user` в `self.scope`

Протокол клиента:
1) Открыть `ws(s)://<host>/graphql/`
2) Отправить `connection_init` с `payload.headers.authorization = "Bearer <jwt>"`
3) Запуск подписок (`start`); события будут доставляться по реализованным типам Subscription (см. `hotels.schemas.notification.subscription`), если `settings.DEV == True`


## 6. Схема GraphQL

Файл: `core/core/schema.py`

- Агрегация Query:
  - Класс `Query` наследует множество `Query*` из доменных модулей: `QueryHotel`, `QueryTask`, `QueryAdmin`, `QueryExecuter`, `QueryPassportData`, `QueryNotification`, и др.
- Агрегация Mutation:
  - Класс `Mutation` аналогично собирает множество `Mutation*`: `MutationHotel`, `MutationTaskForAdmin`, `MutationExecuter`, `MutationAdmin`, `MutationClosingDocument`, и др.
- Подписки:
  - При `settings.DEV`: `Subscription` включает `SubscriptionNotification` и пробрасывается в схему
- Инициализация схемы:
  - `schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)` (в DEV)
  - иначе без `subscription`

Примечание: доступ и фильтрация на уровне резолверов опираются на поля токена, которые миддлвара `AuthMiddleWare` прокидывает в `info.context.user` (id/role и флаг read-only через проверку Mutation).


## 7. Модели данных и связи (ER-обзор)

Ниже перечислены модели и их ключевые поля/связи на основании просмотренных файлов. Для краткости опускаются auto-поля `id`, `created_at/updated_at` и тривиальные `__str__`.

### 7.1. `hotels/models.py` (ядро)

- `Token` — маркер с `expired_at` (UUID PK)
- `PhoneCode` — подтверждение телефона (код, попытки, валидность; метод `new_code()`)
- `FileInfo` — сведения о загруженном файле (имя, размер, MIME, URL)
- `Coordinates` — координаты (широта/долгота/адрес/label)
- `Address` — адрес исполнителя (широта/долгота/адрес/label)
- `Profession` — профессия/услуга
  - тарифы (min/max/step), `percent` (комиссия), `numerate` (единица учета: час/номер)
  - свойства и методы для расчётов (`volume`, `multiplier`, `calculate_rate`)
- `Hotel` — гостиница
  - статусы (зарегистрирован/подтвержден и т.п.)
  - контактные поля, `inn`, связи 1–1 с `FileInfo` (логотип/аватар), 1–1 с `Coordinates`
  - флаги (автоподтверждение, активность, верификация, тестовый аккаунт)
  - настройки периодичности выплат гостиницей/исполнителям
- `Executer` — исполнитель (профиль исполнителя)
  - персональные данные: ФИО, день рождения, пол, контакты
  - статусы верификации, правовой тип (ИП/самозанятый)
  - `ManyToMany` к `Profession` (навыки) и к `Hotel` (избранные гостиницы)
  - документы: сроки действия разрешений/медкнижки
  - токены/авторизация: генерация JWT, токен для админа (методы `token()`, `token_for_admin()` и др.)
- `ExecuterFiles` — связка `Executer` ↔ `FileInfo` с типом файла (медкнижка/регистрация)
- `Requisites` — банковские реквизиты (1–1 c `Hotel` или 1–1 с `Executer`)
- `SimpleRequisite` — упрощённые реквизиты исполнителя (ИНН, карта, банк)
- `Manager` — менеджер гостиницы
  - связь `ForeignKey` к `Hotel` и `ForeignKey` к `Admin` (ответственный координатор)
  - `ManyToMany` к `Executer` (избранные исполнители)
  - статусы приглашения/админ-флаг; авторизация через JWT (методы `token()`, `token_for_admin()`, и т.д.)

Примечания:
- В `closing_documents.models.ClosingDocument` присутствует `ManyToMany` к `"hotels.Task"` (см. раздел 7.2); модель `Task` упоминается, но её тело не показано в просмотренном фрагменте `hotels/models.py`.
- В коде встречаются ссылки на `hotels.Admin` (для закрывающих документов) — модель `Admin` реализована в `hotels` и участвует в связях (не была раскрыта полностью в просмотренных строках, но используется в связях `ClosingDocument.admin` и `Manager.admin`).

### 7.2. `closing_documents/models.py`

- `ClosingDocumentFile` — имя/путь/номер/сумма (таблица `hotels_closingdocumentfile`)
- `ClosingDocument` — объединяет:
  - `ForeignKey` на `hotels.Admin`
  - `ManyToMany` на `hotels.Task` (таблица `hotels_closingdocument_tasks`)
  - `ManyToMany` на `ClosingDocumentFile` (таблица `hotels_closingdocument_files`)
  - Периоды (start/end/closing), флаги (архив/оплачен/отправлен/блок)

### 7.3. `executor/models.py`

- `Metrics` — метрики по исполнителю: `ForeignKey` на `hotels.Executer`, `last_request_task`

### 7.4. `manager/models.py`

- `BlackList` — связь `Manager` ↔ `Executer` (черный список)

### 7.5. `passports/models.py`

- `PassportData` — паспортные данные исполнителя
  - `executer` (строковый идентификатор), страницы паспорта — `OneToOne` на `hotels.FileInfo`
  - серия/номер/кем выдан/когда/код подразделения/место рождения

### 7.6. `otp/models.py`

- `OTP` — одноразовый код для `django.contrib.auth.models.User`
  - `save()` генерирует новый код, отправляет его через Telegram (используется `settings.TG_KEY`)
  - `verify(code)` — валидация кода, ограничение по попыткам

### 7.7. `settings/models.py`

- `Variable` — переменные бизнес-логики (NDS, REMUNERATION и т.п.)
  - вспомогательные функции `get_nds()`, `get_remuneration()` возвращают значения с приведением типа


## 8. Потоки данных (сквозные сценарии)

Ниже — редуцированные сценарии прохождения данных с указанием ключевых элементов.

### 8.1. Авторизованный GraphQL-запрос (HTTP)

1) Клиент отправляет POST `/graphql/` с JSON `{ query, variables }` и заголовком `Authorization: Bearer <jwt>`
2) `core/core/urls.py` → `GraphQLView`
3) `AuthMiddleWare.resolve(...)`:
   - извлекает и валидирует JWT, записывает `user.pk`, `user.id (role)` в `info.context.user`
   - если токен read-only и операция `Mutation` → ошибка "Не достаточно прав"
4) Резолверы графа (см. `core/core/schema.py` + доменные `schemas/*` модулей) обращаются к ORM-моделям
5) Ответ сериализуется в JSON

### 8.2. Подписка (WS, DEV-режим)

1) Клиент открывает WS на `/graphql/`, посылает `connection_init` с `payload.headers.authorization`
2) `MyGraphqlWsConsumer._on_gql_connection_init(...)` сохраняет `id_user/role_user` в `scope`
3) Подписки из `hotels.schemas.notification.subscription` фильтруют/публикуют события клиенту

### 8.3. Закрывающие документы (пример агрегации)

- Админ формирует закрывающий документ `ClosingDocument` за период, связывая его с набором заявок (`hotels.Task`) и файлами `ClosingDocumentFile`.
- Сервис хранит флаги `is_paid`, `is_sent`, `is_block` для контроля жизненного цикла.

### 8.4. Реквизиты и выплаты

- Реквизиты `Requisites` и/или `SimpleRequisite` связываются 1–1 с `Hotel` или `Executer`.
- Расчёты по ставкам опираются на `Profession.calculate_rate()` с учётом комиссий (`percent`) и типа учёта (`numerate`).


## 9. Авторизация и безопасность

- JWT-токен обязателен для защищённых операций; валидация происходит в `AuthMiddleWare`
- Реальный `request.user` не используется стандартным способом: в контекст прописываются атрибуты `pk` и `id (role)` из токена; резолверам следует опираться на эти данные или валидировать самостоятельно
- Read-only режим: флаг `read=True` в токене глобально запрещает любые `Mutation`
- CSRF отключён для GraphQL эндпоинта (используется токенная авторизация)


## 10. Интеграции и окружение

- MinIO: `MINIO_*` переменные, используется как S3-совместимое хранилище
- Firebase: `FIREBASE_*` — отправка push-уведомлений (см. `hotels.tasks.send_push` и GraphQL-слой уведомлений)
- Tinkoff: `TINKOFF_*` — параметры терминала/URL для платежей
- Celery: `CELERY_*` + `REDIS_URL`


## 11. Логирование

- Подготовлен `mid_logger.do_log(...)` для записи расширенных логов запроса в файл `/logs/<ts>_midd_log.log`
- По умолчанию `LogAllRequests.resolve(...)` лог не пишет; при необходимости можно добавить вызов `do_log(...)` для трассировки GraphQL-запросов/переменных


## 12. Развёртывание и локальный запуск

- Docker Compose поднимает необходимые сервисы (БД, Redis и пр.) — см. `docker-compose.yml` в корне репозитория
- Важные переменные окружения: `SECRET_KEY`, `DEV`, `DEBUG`, `REDIS_URL`, `MINIO_*`, `FIREBASE_*`, `TINKOFF_*`, `MYSQL_CONFIG`, `TG_KEY`, `CSRF_TRUSTED_ORIGINS_KEY`


## 13. Расширение и лучшие практики в проекте

- Проверки прав: централизовать через декораторы/утилиты, опираясь на поля токена из контекста
- GraphQL-ошибки: использовать `GraphQLError` с расширениями (коды/поля), чтобы фронт мог корректно обрабатывать ошибки
- Channels: для продакшена перейти на Redis Channel Layer
- Subscriptions: при необходимости включить в продакшене, убрав условие DEV в `schema.py`
- Логирование GraphQL: включить `do_log(...)` в `LogAllRequests.resolve(...)` (с маскированием чувствительных данных)


## 14. Быстрые ссылки на файлы

- Настройки: `core/core/settings.py`
- URL/HTTP GraphQL: `core/core/urls.py`
- Схема GraphQL (аггрегатор): `core/core/schema.py`
- ASGI/WS: `core/core/asgi.py`
- Celery: `core/core/celery.py`
- Логгирование middleware: `core/core/mid_logger.py`
- Модели (ядро): `core/hotels/models.py`
- Закрывающие документы (модели): `core/closing_documents/models.py`
- Метрики исполнителей: `core/executor/models.py`
- Менеджер/ЧС: `core/manager/models.py`
- Паспортные данные: `core/passports/models.py`
- Доменные переменные: `core/settings/models.py`


## 15. Словарь (основные сущности)

- Hotel — организация-заказчик услуг (гостиница)
- Executer — исполнитель работ/услуг
- Manager — представитель гостиницы, управляющий задачами, имеет выделенные права
- Profession — тип услуги/работ, влияет на тарифы и расчёты
- ClosingDocument — агрегат заявок/сумм за период
- OTP — одноразовый код для входа (админка)
- Variable — переменная доменной логики (например, НДС)


## 16. Примечания по совместимости и Monkey Patch

- Файл `core/core/mp.py` переопределяет конструктор `GraphQLEnumValue`, что влияет на поведение Enum’ов в GraphQL-схеме. Это обычно применяют для устранения несовместимостей между версиями GraphQL-core/graphene и кастомными Enum/описаниями. При обновлении зависимостей необходимо проверить актуальность этого патча.


---
## 17. GraphQL: Hotel (тип/запросы/мутации)

Файлы:
- Типы: `core/hotels/schemas/hotel/types.py` (`HotelType`)
- Запросы: `core/hotels/schemas/hotel/query.py` (`QueryHotel`)
- Мутации: `core/hotels/schemas/hotel/mutation.py` (`MutationHotel`)

### 17.1. Тип `HotelType`

- База: `graphene_django.DjangoObjectType` по модели `hotels.Hotel`.
- Интерфейсы: `relay.Node` + пагинация `ExtendedConnection`.
- Исключены поля: `manager_set`, `requisites`.
- Доп. поля и резолверы:
  - `inn: String!` — форматирует ИНН (пустая строка, если в БД "0", иначе zfill(10)).
  - `profile_pic: [FileInfoType!]!` — список из одного `FileInfo`, если аватар есть, иначе `[]`.
  - `count_tasks: Int!` — число заявок гостиницы (`Task` по `manager__hotel`).
  - `coordinates: CoordinatesType!` — координаты/адрес.
  - `rating: Float!` — сейчас заглушка `4.99`.
  - `personalprofession_set: [PersonalProfessionType!]!` — только активные.
  - `id: ID!` — возвращает `pk`.

### 17.2. Запросы (`QueryHotel`)

- `hotel_by_id(input: { id: ID! }): HotelType!` — по идентификатору. Требует авторизации.
- `executer_get_customer_location_list: [HotelType!]!` — список верифицированных (`status = STEP_3_VERIFIED`).
- `executer_get_customer_by_id(input: { id: ID! }): HotelType!` — данные гостиницы. Требует авторизации.

Примеры:
```graphql
query HotelById($id: ID!) {
  hotel_by_id(input: { id: $id }) {
    id
    nameHotel
    inn
    coordinates { address lat lng }
    count_tasks
    profile_pic { url width height mimeType }
  }
}
```

```graphql
query VerifiedHotels {
  executer_get_customer_location_list {
    id
    nameHotel
  }
}
```

### 17.3. Мутации (`MutationHotel`)

- `manager_create_hotel(input: inputForCreateHotel!): { token: String! }`
- `manager_update_hotel(input: inputForUpdateHotel!): { hotel: HotelType! }`
- `manager_upload_media(input: inputForUploadFile!): { url: String!, path: String! }`
- `manager_create_payment: { hotel: HotelType! }`
- `manager_validate_requisites: { hotel: HotelType! }` — статус → `STEP_2_WAITING_FOR_VERIFICATION`.
- `manager_change_auto_approve_tasks: { hotel: HotelType! }` — переключает автоподтверждение заявок; при включении массово `is_approved=true` для всех неутверждённых.
- `manager_change_allow_to_use_basic_professions: { hotel: HotelType! }` — переключает флаг использования базовых профессий в заявках.

Пример — загрузка аватара (получение URL для PUT в MinIO):
```graphql
mutation UploadHotelAvatar($fileName: String!) {
  manager_upload_media(input: { fileName: $fileName }) {
    url
    path
  }
}
```

## 18. GraphQL: Task (тип/запросы/мутации)

Файлы:
- Типы: `core/hotels/schemas/task/type.py` (`TaskType` и вспомогательные типы)
- Запросы: `core/hotels/schemas/task/query.py` (`QueryTask` + `QueryAllTask`)
- Мутации: `core/hotels/schemas/task/mutations/manager.py` (`MutationTaskForManager`),
  а также `admin.py`, `executer.py` — дополнительные роли

### 18.1. Запросы

- `tasks_hotel_by_id(id: ID!): TaskTypeConnection!` — все активные и одобренные заявки гостиницы, отсортированы по `start_at`, исключены `status = DELETED` и `is_archived=true`. Также исключаются спец-заявки `for_favorite=true` для не-избранных исполнителей в течение 120 минут от создания.

Пример:
```graphql
query TasksOfHotel($id: ID!) {
  tasks_hotel_by_id(id: $id) {
    edges {
      node {
        id
        start_at
        is_approved
        manager { id }
      }
    }
  }
}
```

### 18.2. Мутации менеджера (`MutationTaskForManager`)

См. `core/hotels/schemas/task/mutations/manager.py`:
- `manager_task_upsert(input: inputForTaskUpsert!): { task: TaskType! }` — создание/обновление заявки. Поддерживает множественные даты `start_at` при создании; валидации по ставке/диапазонам, эксклюзивным профессиям.
- `manager_task_delete(id: ID!): { task: TaskType! }` — удаление (запрет менее чем за 8 часов до старта).
- `manager_start_task(input: inputForStartTask!): { task: TaskType! }` — старт выполнения.
- `manager_stop_task(input: inputForStopTask!): { task: TaskType! }` — остановка выполнения.
- `manager_set_volume_of_work_by_executer_state(input: InputForSetVolumeOfWorkInTask!): { task: TaskType! }` — установка объёма работ по отклику.
- `manager_task_archive(input: inputIDs!): { tasks: [TaskType!]! }` — архивировать несколько задач.
- `manager_task_unarchive(input: inputIDs!): { tasks: [TaskType!]! }` — разархивировать.
- `manager_set_executer_as_violator_in_task_by_id(input: inputTaskIdExecuterID!): { task: TaskType! }` — отметить исполнителя нарушителем.
- `manager_set_executer_as_tester(input: inputTaskIdExecuterIDCorrection!): { task: TaskType! }` — отметить как тестовую работу.
- `manager_approve_tasks(input: inputIDs!): { tasks: [TaskType!]! }` — одобрить задачи.
- `manager_forbid_tasks_with_comment(input: InputForForbidTasks!): { tasks: [TaskType!]! }` — запретить с комментарием.

Пример — upsert заявки:
```graphql
mutation UpsertTask($input: inputForTaskUpsert!) {
  manager_task_upsert(input: $input) {
    task { id start_at is_approved }
  }
}
```

Где переменная `$input` может включать (согласно `inputForTaskUpsert`):
- `profession: ID!`
- `personal_profession: ID` (если разрешено, должна принадлежать менеджеру)
- `rent: Int!`, `count_executers: Int!`, `duration: Int!`, `start_at: [DateTime!]!`
- `additional: { datetime: DateTime, description: String }`
- `id_task: ID` (для обновления существующей)

## 19. GraphQL: Notification (тип/запросы/подписки)

Файлы:
- Типы: `core/hotels/schemas/notification/type.py` (`NotifyType`, `MetaType`)
- Запросы: `core/hotels/schemas/notification/query.py` (`QueryNotification`)
- Подписки: `core/hotels/schemas/notification/subscription.py` (`SubscriptionNotification`)

### 19.1. Типы

- `NotifyType` (модель `Notification`):
  - интерфейсы: `relay.Node`, пагинация `ExtendedConnection`.
  - исключено поле `role`.
  - поля: `category: String!` (alias для `type`, помечено как deprecated), `meta: MetaType`.
- `MetaType` (модель `MetaInformationNotification`):
  - исключено поле `notification` (обратная связь).

### 19.2. Запросы (`QueryNotification`)

- `get_read_notifications(input: InputForQueryNotification!): NotifyTypeConnection!`
- `get_unread_notifications(input: InputForQueryNotification!): [NotifyType!]!`
- `get_count_unread_notifications: Int!`
- `get_all_notifications(input: InputForQueryNotification!): NotifyTypeConnection!`

Где `InputForQueryNotification` содержит опциональный фильтр `type` (категория уведомления).

Пример — непрочитанные уведомления с фильтром по типу:
```graphql
query UnreadNotifications($type: String) {
  get_unread_notifications(input: { type: $type }) {
    id
    category
    text
    createdAt
  }
}
```

### 19.3. Подписки (`SubscriptionNotification`)

- `manager_notification_create: { text: String }` — события доставляются по WS-группе с ключом `id_user` из контекста соединения (см. `MySubscription.subscribe`). Доступ — только для роли `role_user == 1` (менеджер).

Пример клиентского сообщения (после `connection_init`):
```graphql
subscription OnManagerNotification {
  manager_notification_create { text }
}
```

## 20. Модель Task и жизненный цикл

Файл: `core/hotels/models.py` (секция модели `Task`).

Ключевые поля и связи (по использованию в схемах/мутациях):
- `manager: ForeignKey -> Manager` — владелец заявки (косвенно связан с `Hotel`).
- `start_at: DateTime` — время начала.
- `is_approved: Boolean` — признак одобрения (влияет на видимость/редактирование).
- `is_archived: Boolean` — архивность.
- `status: String/Enum` — в коде встречаются проверки на `"DELETED"`.
- `executers` — связь с откликами/исполнителями через `ExecuterState`.
- `additional: AdditionalTask?` — доп. сведения (дата/описание).

Связанные операции (менеджер):
- Создание/обновление (`manager_task_upsert`).
- Старт/стоп (`manager_start_task`, `manager_stop_task`).
- Архив/разархив (`manager_task_archive`, `manager_task_unarchive`).
- Удаление (`manager_task_delete`).
- Одобрение/запрет (`manager_approve_tasks`, `manager_forbid_tasks_with_comment`).
- Проставление объёма работ по отклику, отметка тестовой работы, пометка нарушителя.

Жизненный цикл (обобщённо):
- Draft/New → Approved/Forbidden → InProgress (после `start`) → Stopped (после `stop`) → Archived/Unarchived. Удалённые помечаются статусом `DELETED` и исключаются из выборок.

Примечание: точные константы статусов и их описания см. в `hotels/models.py` (модель `Task`). В коде GraphQL учитываются ограничения по времени (нельзя удалять/обновлять ближе 8 часов до старта).

## 21. Примеры типовых GraphQL-операций

- Получить счётчик непрочитанных уведомлений:
```graphql
query {
  get_count_unread_notifications
}
```

- Получить гостиницу и последние 5 заявок:
```graphql
query HotelWithTasks($id: ID!) {
  hotel_by_id(input: { id: $id }) {
    id
    nameHotel
    count_tasks
  }
  tasks_hotel_by_id(id: $id, first: 5) {
    edges { node { id start_at is_approved } }
  }
}
```

- Архивировать задачи:
```graphql
mutation ArchiveTasks($ids: [ID!]!) {
  manager_task_archive(input: { ids: $ids }) {
    tasks { id }
  }
}
```

## 22. ER-диаграмма (ключевые сущности)

Ниже представлена укрупнённая диаграмма связей. Точные поля — см. соответствующие модели.

```mermaid
erDiagram
  HOTEL ||--o{ MANAGER : has
  MANAGER ||--o{ TASK : creates
  TASK }o--o{ EXECUTER : via EXECUTER_STATE
  HOTEL ||--|| REQUISITES : owns
  HOTEL ||--|| COORDINATES : has
  HOTEL ||--o| FILEINFO : avatar
  EXECUTER ||--o{ FILEINFO : docs
  CLOSING_DOCUMENT ||--o{ TASK : aggregates
  CLOSING_DOCUMENT ||--o{ CLOSING_DOCUMENT_FILE : has
  NOTIFICATION ||..|| META_INFORMATION_NOTIFICATION : has
  NOTIFICATION }o..|| USER_CONTEXT : (id_instance, role)
```

Пояснения:
- `TASK` ↔ `EXECUTER` связаны через сущность отклика/состояния исполнения (`ExecuterState`).
- `NOTIFICATION` связано с пользователем по паре `(id_instance, role)` (полиморфная связь).
- `FILEINFO` используется как для аватаров, так и для документов.
