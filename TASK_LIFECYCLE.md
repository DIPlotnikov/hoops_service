# Процесс работы с заявками: создание → отклик → старт/стоп → завершение → (оплата)

Документ описывает сквозной процесс работы с заявками (Task) во фронт/бэкенд взаимодействии: создание заявки менеджером, отклик исполнителя, старт/стоп работ, установка объема (для нечасовых), а также связь с оплатой/закрывающими. Приведены ссылки на соответствующие файлы и готовые примеры GraphQL-запросов.

- Версия: 1.0
- Область: Django + GraphQL (Graphene)
- Ключевые директории:
  - [core/hotels/models.py](./core/hotels/models.py)
  - [core/hotels/schemas/task/](./core/hotels/schemas/task/)
  - [core/hotels/schemas/admin/](./core/hotels/schemas/admin/)
  - [core/closing_documents/](./core/closing_documents/)

---

## 1) Где реализована логика

- Создание/редактирование заявки менеджером:
  - Мутация `UpsertTask` в [core/hotels/schemas/task/mutations/manager.py](./core/hotels/schemas/task/mutations/manager.py).
  - Инпут `inputForTaskUpsert` в [core/hotels/schemas/task/input.py](./core/hotels/schemas/task/input.py).
- Отклик исполнителя на заявку:
  - Мутация `requestTask` в [core/hotels/schemas/task/mutations/executer.py](./core/hotels/schemas/task/mutations/executer.py).
  - Инпут `inputId` в [core/hotels/schemas/task/input.py](./core/hotels/schemas/task/input.py).
- Старт/стоп заявки (по исполнителям):
  - `startTask`, `stopTask` в [core/hotels/schemas/task/mutations/manager.py](./core/hotels/schemas/task/mutations/manager.py).
  - Инпуты: `inputForStartTask`, `inputForStopTask`.
- Объем выполненных работ (для нечасовых профессий):
  - `SetVolumeOfWorkByExecuterState` в [core/hotels/schemas/task/mutations/manager.py](./core/hotels/schemas/task/mutations/manager.py).
  - Инпут: `InputForSetVolumeOfWorkInTask`.
- Отмена отклика исполнителем:
  - `deleteRequestTask` в [core/hotels/schemas/task/mutations/executer.py](./core/hotels/schemas/task/mutations/executer.py).
- Оплата/закрывающие документы (после завершения):
  - Админские мутации оплаты: [core/hotels/schemas/admin/mutations/payment.py](./core/hotels/schemas/admin/mutations/payment.py).
  - Закрывающие документы: [core/closing_documents/mutation.py](./core/closing_documents/mutation.py).

Модельный контекст:
- Заявка `Task` и отклик `ExecuterState` в [core/hotels/models.py](./core/hotels/models.py).

---

## 2) Схема процесса (happy-path)

1. Менеджер создаёт заявку — `manager_task_upsert`.
2. Исполнитель откликается — `executer_task_request`.
3. Менеджер стартует выполнение — `manager_start_task` (всем или конкретному исполнителю).
4. Менеджер завершает выполнение — `manager_stop_task` (по каждому исполнителю).
5. Для профессий с учётом объёма (не «Час») — `manager_set_volume_of_work_by_executer_state`.
6. Далее заявка попадает в цикл оплаты/закрывающих (обычно не дергается фронтом менеджера/исполнителя напрямую).

Дополнительно:
- Исполнитель может отменить свой отклик до T-8 часов — `executer_request_task_delete`.
- Автоподтверждение заявок управляется флагом отеля `Hotel.auto_approve_tasks`.

---

## 3) Готовые GraphQL-запросы для прогонки

Все запросы выполняются с корректным JWT в заголовке `Authorization: Bearer <token>`:
- Токен менеджера — для менеджерских мутаций.
- Токен исполнителя — для исполнительских мутаций.

### 3.1 Создание заявки (менеджер)
Файл: [core/hotels/schemas/task/mutations/manager.py](./core/hotels/schemas/task/mutations/manager.py) → `UpsertTask`
Инпут: `inputForTaskUpsert` ([core/hotels/schemas/task/input.py](./core/hotels/schemas/task/input.py))

```graphql
mutation CreateTask($input: inputForTaskUpsert!) {
  manager_task_upsert(input: $input) {
    task {
      id
      startAt
      duration
      countExecuters
      profession { id name }
      isApproved
      comment
    }
  }
}
```

Пример переменных (почасовая профессия):
```json
{
  "input": {
    "min_rating": 0,
    "for_favorite": false,
    "profession": "PROFESSION_ID",
    "count_executers": 2,
    "rent": 1500.0,
    "start_at": ["2025-09-05T10:00:00+03:00"],
    "duration": 8,
    "comment": "Уборка стандарт, корпус А",
    "additional": {
      "datetime": "2025-09-04T18:00:00+03:00",
      "description": "Забрать ключи на рецепции"
    }
  }
}
```

Ключевые проверки/ограничения:
- Нельзя создавать с прошедшим `start_at`.
- Нельзя изменять заявку за < 8 часов до старта.
- Если у отеля `is_allow_to_use_basic_profession == false`, обязательна `personal_profession`.
- `count_executers` ∈ [1; 999]. Для HOUR `duration` ∈ [1; 24].

---

### 3.2 Отклик исполнителя на заявку
Файл: [core/hotels/schemas/task/mutations/executer.py](./core/hotels/schemas/task/mutations/executer.py) → `requestTask`
Инпут: `inputId`

```graphql
mutation RequestTask($input: inputId!) {
  executer_task_request(input: $input) {
    id
    executers { id status executer { id firstName } }
    isApproved
  }
}
```

Переменные:
```json
{ "input": { "id": "TASK_ID" } }
```

Ограничения/валидации:
- `task.is_approved == true` и `task.is_closed == false`.
- Нет времовых конфликтов с другими принятыми заявками исполнителя.
- Исполнитель имеет указанную `profession` и достаточный рейтинг (`min_rating`).
- Если `for_favorite == true` и прошло < 120 минут с создания заявки — отклик только из избранных менеджера.

---

### 3.3 Старт работ (менеджер)
Файл: [core/hotels/schemas/task/mutations/manager.py](./core/hotels/schemas/task/mutations/manager.py) → `startTask`
Инпут: `inputForStartTask`

```graphql
mutation StartTask($input: inputForStartTask!) {
  manager_start_task(input: $input) {
    task {
      id
      startAt
      executers { id status startAt executer { id firstName } }
    }
  }
}
```

Переменные — старт всем (кроме уже START/STOP):
```json
{
  "input": {
    "id_task": "TASK_ID",
    "start_at": "2025-09-05T10:00:10+03:00"
  }
}
```

Переменные — старт конкретному исполнителю:
```json
{
  "input": {
    "id_task": "TASK_ID",
    "id_executer": "EXECUTER_ID",
    "start_at": "2025-09-05T10:00:10+03:00"
  }
}
```

---

### 3.4 Завершение работ (менеджер, по каждому исполнителю)
Файл: [core/hotels/schemas/task/mutations/manager.py](./core/hotels/schemas/task/mutations/manager.py) → `stopTask`
Инпут: `inputForStopTask`

```graphql
mutation StopTask($input: inputForStopTask!) {
  manager_stop_task(input: $input) {
    task {
      id
      executers { id status startAt stopAt executer { id firstName } }
    }
  }
}
```

Переменные:
```json
{
  "input": {
    "id_task": "TASK_ID",
    "id_executer": "EXECUTER_ID",
    "stop_at": "2025-09-05T18:15:00+03:00"
  }
}
```

Проверки:
- У исполнителя должен быть статус START.
- `stop_at` > `start_at`.

---

### 3.5 Установка объёма работ (для нечасовых профессий)
Файл: [core/hotels/schemas/task/mutations/manager.py](./core/hotels/schemas/task/mutations/manager.py) → `SetVolumeOfWorkByExecuterState`
Инпут: `InputForSetVolumeOfWorkInTask`

```graphql
mutation SetVolume($input: InputForSetVolumeOfWorkInTask!) {
  manager_set_volume_of_work_by_executer_state(input: $input) {
    task { id executers { id volumeOfTheWork executer { id firstName } } }
  }
}
```

Переменные:
```json
{
  "input": {
    "id_executer_state": "EXECUTER_STATE_ID",
    "volume_of_the_work": 12.0
  }
}
```

Где взять `id_executer_state`: из деталей заявки (`Task.executers`).

---

### 3.6 Отмена отклика исполнителем
Файл: [core/hotels/schemas/task/mutations/executer.py](./core/hotels/schemas/task/mutations/executer.py) → `deleteRequestTask`

```graphql
mutation CancelMyRequest($task: ID!) {
  executer_request_task_delete(task: $task) {
    id
    executers { id executer { id } }
  }
}
```

Переменные:
```json
{ "task": "TASK_ID" }
```

Ограничения:
- Нельзя отменить за < 8 часов до старта.
- Нельзя отменить, если статус START/STOP.

---

## 4) Связь с оплатой и закрывающими документами

- После завершения (стоп/объем) задачи учитываются в биллинге/закрывающих.
- Формирование и отправка закрывающих документов реализовано в домене `closing_documents`:
  - Мутации: [core/closing_documents/mutation.py](./core/closing_documents/mutation.py) (например, создание и пометка отправки комплектов документов).
  - Генерация счетов/актов/платёжек, Diadoc XML, загрузка в MinIO — см. соответствующие классы/скрипты в [core/hotels/scripts/](./core/hotels/scripts/) и [core/closing_documents/](./core/closing_documents/).
 - Админские операции оплаты: [core/hotels/schemas/admin/mutations/payment.py](./core/hotels/schemas/admin/mutations/payment.py).
- Как правило, менеджер/исполнитель не дергают админские мутации напрямую.

---

## 5) Полезные замечания и валидации

- `Hotel.auto_approve_tasks` управляет автоапрувом новых заявок.
- Для почасовых профессий (`Profession.Numerates.HOUR`) `duration` ∈ [1; 24]. Для нечасовых — используется `volumeOfTheWork` на `ExecuterState`.
- Ограничения времени:
  - Создание/редактирование: нельзя ближе чем за 8 часов до старта.
  - Отмена отклика исполнителем: нельзя за < 8 часов до старта.
- `requestTask` проверяет:
  - Статус заявки (`is_approved`, `is_closed`).
  - Конфликты по времени с уже принятыми заявками исполнителя.
  - Соответствие профессии и рейтинга.
  - «Для избранных» в течение первых 120 минут.

---

## 6) Вопросы для уточнения (для фронта)

- Нужны ли фронту явные действия по оплате, или завершения достаточно (далее всё делает биллинг/закрывающие)?
- Нужны ли примеры Query для списков/деталей заявок (экраны менеджера/исполнителя)? При необходимости добавить — используйте `inputForGetMyTasks`, типы в [core/hotels/schemas/task/type.py](./core/hotels/schemas/task/type.py).

---

## 7) Быстрый чек-лист прогонки

1. Менеджер: `manager_task_upsert`.
2. (Опционально) Главный менеджер: `manager_approve_tasks` (если автоапрув выключен).
3. Исполнитель: `executer_task_request`.
4. Менеджер: `manager_start_task`.
5. Менеджер: `manager_stop_task`.
6. (Если нечасовая профессия) Менеджер: `manager_set_volume_of_work_by_executer_state`.

---

Ссылки на ключевые файлы для изучения:
 - [core/hotels/models.py](./core/hotels/models.py) — модели `Task`, `ExecuterState`, `Hotel`, `Profession` и др.
 - [core/hotels/schemas/task/mutations/manager.py](./core/hotels/schemas/task/mutations/manager.py) — мутации менеджера.
 - [core/hotels/schemas/task/mutations/executer.py](./core/hotels/schemas/task/mutations/executer.py) — мутации исполнителя.
 - [core/hotels/schemas/task/input.py](./core/hotels/schemas/task/input.py) — инпут-типы для мутаций задач.
 - [core/hotels/schemas/admin/mutations/payment.py](./core/hotels/schemas/admin/mutations/payment.py) — админские платежные мутации.
 - [core/closing_documents/mutation.py](./core/closing_documents/mutation.py) — закрывающие документы (формирование/отправка).


## P.S. Быстрая смена пароля менеджера.
django shell
- from django.utils import timezone
- from core.hotels.models import Manager
- m = Manager.objects.get(email="manager@example.com")
- m.set_password("NewStrongPass123!")
- m.update_password_at = timezone.now()
- m.save()
- print("ok")