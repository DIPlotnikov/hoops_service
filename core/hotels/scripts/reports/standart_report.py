import pandas as pd
from django.db.models import Case, CharField, DateTimeField, ExpressionWrapper, F, FloatField, Func, Value, When
from django.db.models.functions import Coalesce, Concat, Ceil, Floor, TruncMinute

from hotels.utils.invoice import round_money_4_5, round_volume_by_spec

from .utils import create_footer_and_stamp_signature


# pip install xlsxwriter
def create_df(
    queryset, path="hotels/scripts/reports/result.xlsx", period="test period", hotel_name="test name", remuneration=10
):
    """
    Формирует Excel-файл «Стандартный отчет» на основе выборки состояний исполнителей (queryset).

    ВЫХОД:
    - Сохраняет Excel в указанный путь (path), использует движок xlsxwriter для форматирования.
    - Возвращаемого значения нет — файл закрывается writer.close().

    ОСНОВНАЯ ЛОГИКА:
    1) На уровне ORM-выражений (annotate) рассчитываются и добавляются к queryset все необходимые
       производные поля: ФИО, профессия, "теоретические" и "фактические" времена/объемы/стоимости,
       доля HOOPS, вознаграждение сервиса, выплаты исполнителю, статусы/проблемы и т.д.
    2) Через .values(...) извлекаются выбранные поля в плоский набор словарей, из которого строится DataFrame.
    3) В pandas обогащаем данными для отображения (локализация времени в Europe/Moscow, форматирование дат/времени).
    4) Суммируем значения для итоговых строк (теория/факт) и записываем их в конец листа.
    5) Записываем DataFrame на лист «Стандартный отчет» с оформлением: шапка, логотип, автофильтр,
       выравнивания, рамки, форматы валют, итоговые строки и футер с печатью/подписью.

    ОБРАТИТЕ ВНИМАНИЕ:
    - В текущей реализации часть расчетов выполнена на уровне ORM (через annotate), а часть — в pandas/Excel.
    - Округление "фактического" объема выполняется через Ceil на уровне ORM; "теоретический" объем — как деление без
      округления. При необходимости изменить политику округления — корректируется именно здесь.
    - Параметр remuneration (процент от доли HOOPS, направляемый на вознаграждение сервиса) задается аргументом
      функции и влияет на соответствующие поля с суффиксами *_t и *_f.

    ФОРМУЛЫ ФОРМИРОВАНИЯ СТОЛБЦОВ ОТЧЕТА:
    ======================================

    1. ФИО Исполнителя:
       Формула: executer__middle_name + " " + executer__first_name + " " + executer__second_name
       Описание: Конкатенация отчества, имени и фамилии исполнителя через пробелы.

    2. Наименование профессии:
       Формула: COALESCE(task__personal_profession__name, task__profession__name)
       Описание: Приоритет персональной профессии, если задана; иначе — базовая профессия задачи.

    3. Наименование услуги:
       Формула: task__profession__description
       Описание: Прямое поле — описание услуги из базовой профессии задачи.

    4. Дата:
       Формула: FORMAT(tz_convert(COALESCE(start_at, task__start_at), 'Europe/Moscow'), '%d.%m.%Y')
       Описание: Дата начала работы (фактическая или плановая), конвертированная в московское время,
                 обнуление секунд, форматирование в формат ДД.ММ.ГГГГ.

    5. Ставка, руб.:
       Формула: task__rent
       Описание: Прямое поле — ставка оплаты за единицу времени/объема из задачи.

    6. Время начала:
       Формула: FORMAT(tz_convert(TruncMinute(COALESCE(start_at, task__start_at)), 'Europe/Moscow'), '%H:%M')
       Описание: Время начала работы (фактическое или плановое), обнуление секунд, конвертация в МСК,
                 форматирование в формат ЧЧ:ММ.

    7. Время окончания:
       Формула: FORMAT(tz_convert(TruncMinute(COALESCE(stop_at, task__start_at + INTERVAL task__duration HOUR)), 'Europe/Moscow'), '%H:%M')
       Описание: Время окончания работы (фактическое или расчетное: старт + длительность), обнуление секунд,
                 конвертация в МСК, форматирование в формат ЧЧ:ММ.

    8. Объем услуг:
       Формула: CEIL(COALESCE(volume_of_the_work, volume_time_t) * 100) / 100
       где volume_time_t = (stop_teor_min - start_teor_min) / 3600000000
       Описание: Объем работы в часах. Приоритет ручного объема (volume_of_the_work), иначе — расчетный
                 по разнице времени начала и окончания (в наносекундах, деление на 3.6e9 для перевода в часы).
                 Округление вверх до сотых долей часа.

    9. Итого оплат, руб.:
       Формула: FLOOR((volume_t * task__rent) * 100 + 0.5) / 100
       Описание: Общая стоимость услуг = объем * ставка, округление до 2 знаков по правилу 4/5
                 (математическое округление: floor(x*100+0.5)/100).

    10. Стоимость услуг HOOPS Service:
        Формула: round_money_4_5(salary_t - remuneration_of_the_service_t - salary_executer_t)
        где:
          salary_t = round_money_4_5(volume_t * task__rent_rounded)
          remuneration_of_the_service_t = round_money_4_5(full_hoops_t * remuneration / 100)
          salary_executer_t = round_money_4_5(salary_t - full_hoops_t)
        Описание: Стоимость услуг HOOPS рассчитывается через вычитание (как в invoice: rent_for_hoops): 
                  общая сумма минус вознаграждение минус выплата исполнителям. Все вычитаемые значения предварительно округлены.
                  Соответствует формуле invoice: rent_for_hoops = rent - remuneration_for_executer - rent_for_executer.

    11. Вознаграждение за исполнение поручения:
        Формула: round_money_4_5(full_hoops_t * remuneration / 100)
        где full_hoops_t = round_money_4_5(salary_t * task__profession__percent / 100)
        Описание: Вознаграждение (как в invoice: remuneration_for_executer). Рассчитывается как 
                  full_hoops_t * remuneration / 100, затем округляется. Соответствует формуле invoice:
                  remuneration_for_executer = (rent - rent_for_executer) * remuneration_percent / 100.

    12. Выплата исполнителям:
        Формула: round_money_4_5(salary_t - full_hoops_t)
        где full_hoops_t = round_money_4_5(salary_t * task__profession__percent / 100)
        Описание: Общая стоимость услуг минус доля HOOPS (как в invoice: rent_for_executer). 
                  Округление до 2 знаков по правилу 4/5.

    13. Номер заявки:
        Формула: task__id
        Описание: Прямое поле — идентификатор задачи (заявки).

    14. Статус заявки:
        Формула: IF volume_of_the_work IS NOT NULL THEN correction_comment ELSE COALESCE(problem1, problem2, problem3, correction_comment)
        где:
          problem1 = IF task__is_approved = FALSE THEN 'Не согласована' ELSE NULL
          problem2 = IF start_at IS NULL THEN 'Не было старта работы' ELSE NULL
          problem3 = IF stop_at IS NULL THEN 'Не было стопа работы' ELSE NULL
        Описание: При наличии ручного объема (корректировки) — комментарий коррекции; иначе — первая найденная
                  проблема из списка: несогласованность, отсутствие старта, отсутствие стопа, комментарий коррекции.

    15. Менеджер Заказчика:
        Формула: task__manager__first_name + " " + task__manager__middle_name + " " + task__manager__second_name
        Описание: Конкатенация имени, отчества и фамилии менеджера заявки через пробелы.

    ПРИМЕЧАНИЯ:
    - Все денежные расчеты используют теоретические значения (суффикс _t), основанные на плановых временах.
    - Округление денежных сумм выполняется через round_money_4_5() (из hotels.utils.invoice) - учитывает только 3-й знак.
    - Округление объема выполняется через round_volume_by_spec() (из hotels.utils.invoice) - условное округление вверх.
    - ВАЖНО: Округления применяются ДО математических операций:
      * Сначала округляются объем и ставка
      * Затем выполняются расчеты с использованием уже округленных значений
      * Затем округляются итоговые суммы
    - Времена и даты конвертируются в таймзону Europe/Moscow перед форматированием.
    - Секунды обнуляются на уровне ORM через TruncMinute для согласованности расчетов.
    - Все расчеты выполняются в pandas после конвертации DataFrame для применения правильных функций округления.
    """
    # ФИО Исполнителя
    queryset = queryset.annotate(
        executer_full_name=Concat(
            "executer__middle_name", Value(" "), "executer__first_name", Value(" "), "executer__second_name"
        )
    )
    # Наименование профессии
    queryset = queryset.annotate(profession_name=Coalesce("task__personal_profession__name", "task__profession__name"))

    class MinuteInterval(Func):
        template = "INTERVAL %(expressions)s HOUR"

    _end_date = F("task__start_at") + MinuteInterval(F("task__duration"))

    # старт задачи с предположениями
    queryset = queryset.annotate(start_teor=Coalesce("start_at", "task__start_at"))
    # стоп задачи с предположениями
    # queryset = queryset.annotate(
    #     stop_task=ExpressionWrapper(F("task__start_at") + timedelta(hours=F("task__duration")), output_field=DateTimeField())
    # )
    queryset = queryset.annotate(
        stop_task=ExpressionWrapper(_end_date, output_field=DateTimeField()),
    )
    queryset = queryset.annotate(stop_teor=Coalesce("stop_at", "stop_task"))

    # --- ОБНУЛЯЕМ СЕКУНДЫ НА УРОВНЕ ORM ---
    # Все расчеты времени и объема переводим на поля с обнулёнными секундами
    queryset = queryset.annotate(
        start_at_min=TruncMinute('start_at'),
        stop_at_min=TruncMinute('stop_at'),
        start_teor_min=TruncMinute('start_teor'),
        stop_teor_min=TruncMinute('stop_teor'),
    )

    # Используем новые поля для расчёта длительности и объёма
    queryset = queryset.annotate(duration_f=ExpressionWrapper(F("stop_at_min") - F("start_at_min"), output_field=FloatField()))
    queryset = queryset.annotate(duration_t=ExpressionWrapper(F("stop_teor_min") - F("start_teor_min"), output_field=FloatField()))

    # УДАЛЯЕМ старые duration_f и duration_t, чтобы не было двойных расчетов
    # Пересчитываем volume_time_f и volume_time_t на базе новых duration_f и duration_t
    queryset = queryset.annotate(
        volume_time_f=ExpressionWrapper(Ceil((F("duration_f") * 100) / 3600000000), output_field=FloatField()) / 100
    )
    queryset = queryset.annotate(
        volume_time_t=ExpressionWrapper(F("duration_t") / 3600000000, output_field=FloatField())
    )
    # Остальной код расчета объема и денег не меняется, так как volume_f, volume_t используют volume_time_f и volume_time_t

    # объем работы фактический
    # volume_f — фактический объем: Coalesce(ручной, расчетный факт) с округлением «вверх» до двух знаков
    # 1) Базовый объем факта
    queryset = queryset.annotate(volume_f_base=Coalesce("volume_of_the_work", "volume_time_f"))
    # 2) Применяем ceil до сотых: ceil(volume_f_base * 100) / 100
    queryset = queryset.annotate(
        volume_f=ExpressionWrapper(
            Ceil(
                ExpressionWrapper(F("volume_f_base") * Value(100.0), output_field=FloatField())
            ) / Value(100.0),
            output_field=FloatField(),
        )
    )

    # Объем услуг
    # volume_t — теоретический объем: Coalesce(ручной, расчетный теоретический) с округлением «вверх» до двух знаков
    # 1) Базовый объем теории
    queryset = queryset.annotate(volume_t_base=Coalesce("volume_of_the_work", "volume_time_t"))
    # 2) Применяем ceil до сотых: ceil(volume_t_base * 100) / 100
    queryset = queryset.annotate(
        volume_t=ExpressionWrapper(
            Ceil(
                ExpressionWrapper(F("volume_t_base") * Value(100.0), output_field=FloatField())
            ) / Value(100.0),
            output_field=FloatField(),
        )
    )

    # Итого оплат, руб.
    # salary_t_raw — стоимость услуг по теоретическому объему: объем * ставка
    queryset = queryset.annotate(salary_t_raw=F("volume_t") * F("task__rent"))
    # salary_t — округление до 2 знаков по правилу 4/5: floor(x*100+0.5)/100
    queryset = queryset.annotate(
        salary_t=ExpressionWrapper(
            Floor(
                ExpressionWrapper(F("salary_t_raw") * Value(100.0), output_field=FloatField()) + Value(0.5)
            )
            / Value(100.0),
            output_field=FloatField(),
        )
    )

    # общая прибыль hoops теоритическая (без округления — промежуточное)
    # full_hoops_t — доля HOOPS по теоретической стоимости: salary_t * percent профессии / 100
    queryset = queryset.annotate(full_hoops_t=F("salary_t") * F("task__profession__percent") / 100)

    # Вознаграждение за исполнение поручения
    queryset = queryset.annotate(remuneration_of_the_service_t_raw=F("full_hoops_t") / 100 * remuneration)
    queryset = queryset.annotate(
        remuneration_of_the_service_t=ExpressionWrapper(
            Floor(
                ExpressionWrapper(F("remuneration_of_the_service_t_raw") * Value(100.0), output_field=FloatField())
                + Value(0.5)
            )
            / Value(100.0),
            output_field=FloatField(),
        )
    )

    # Стоимость услуг HOOPS Service
    queryset = queryset.annotate(cost_of_the_service_t_raw=F("full_hoops_t") - F("remuneration_of_the_service_t"))
    queryset = queryset.annotate(
        cost_of_the_service_t=ExpressionWrapper(
            Floor(
                ExpressionWrapper(F("cost_of_the_service_t_raw") * Value(100.0), output_field=FloatField())
                + Value(0.5)
            )
            / Value(100.0),
            output_field=FloatField(),
        )
    )

    # Выплата исполнителям
    queryset = queryset.annotate(salary_executer_t_raw=F("salary_t") - F("full_hoops_t"))
    queryset = queryset.annotate(
        salary_executer_t=ExpressionWrapper(
            Floor(
                ExpressionWrapper(F("salary_executer_t_raw") * Value(100.0), output_field=FloatField()) + Value(0.5)
            )
            / Value(100.0),
            output_field=FloatField(),
        )
    )

    # зарплата фактическая
    # salary_f_raw — фактическая стоимость услуг: округленный объем volume_f * ставка
    queryset = queryset.annotate(salary_f_raw=F("volume_f") * F("task__rent"))
    queryset = queryset.annotate(
        salary_f=ExpressionWrapper(
            Floor(
                ExpressionWrapper(F("salary_f_raw") * Value(100.0), output_field=FloatField()) + Value(0.5)
            )
            / Value(100.0),
            output_field=FloatField(),
        )
    )
    # full_hoops_f — фактическая доля HOOPS от фактической стоимости (промежуточное без округления)
    queryset = queryset.annotate(full_hoops_f=F("salary_f") * F("task__profession__percent") / 100)
    # remuneration_of_the_service_f — фактическое вознаграждение сервиса (округление 4/5)
    queryset = queryset.annotate(remuneration_of_the_service_f_raw=F("full_hoops_f") / 100 * remuneration)
    queryset = queryset.annotate(
        remuneration_of_the_service_f=ExpressionWrapper(
            Floor(
                ExpressionWrapper(
                    F("remuneration_of_the_service_f_raw") * Value(100.0), output_field=FloatField()
                )
                + Value(0.5)
            )
            / Value(100.0),
            output_field=FloatField(),
        )
    )
    # cost_of_the_service_f — фактическая стоимость услуг HOOPS (округление 4/5)
    queryset = queryset.annotate(
        cost_of_the_service_f_raw=F("full_hoops_f") - F("remuneration_of_the_service_f")
    )
    queryset = queryset.annotate(
        cost_of_the_service_f=ExpressionWrapper(
            Floor(
                ExpressionWrapper(F("cost_of_the_service_f_raw") * Value(100.0), output_field=FloatField())
                + Value(0.5)
            )
            / Value(100.0),
            output_field=FloatField(),
        )
    )
    # salary_executer_f — фактическая выплата Исполнителю (округление 4/5)
    queryset = queryset.annotate(salary_executer_f_raw=F("salary_f") - F("full_hoops_f"))
    queryset = queryset.annotate(
        salary_executer_f=ExpressionWrapper(
            Floor(
                ExpressionWrapper(F("salary_executer_f_raw") * Value(100.0), output_field=FloatField()) + Value(0.5)
            )
            / Value(100.0),
            output_field=FloatField(),
        )
    )

    # Наименование услуги
    # Текущее описание услуги берется из базовой профессии (без приоритета персональной профессии)
    queryset = queryset.annotate(description=F("task__profession__description"))

    # problem1
    # queryset = queryset.annotate(problem1=Value("Не согласована") if F("task__is_approved") else None)
    # problem1 — флаг несогласованной заявки
    queryset = queryset.annotate(
        problem1=Case(
            When(task__is_approved=False, then=Value("Не согласована")), default=None, output_field=CharField()
        )
    )
    # problem2
    # queryset = queryset.annotate(problem2=Value("Не было старта работы") if F("start_at") else None)
    # problem2 — отсутствие фактического старта работы
    queryset = queryset.annotate(
        problem2=Case(
            When(start_at__isnull=True, then=Value("Не было старта работы")), default=None, output_field=CharField()
        )
    )
    # problem3
    # queryset = queryset.annotate(problem3=Value("Не было стопа работы") if F("stop_at") else None)
    # problem3 — отсутствие фактического стопа работы
    queryset = queryset.annotate(
        problem3=Case(
            When(stop_at__isnull=True, then=Value("Не было стопа работы")),
            default=None,
            output_field=CharField(),
        )
    )

    # Статус заявки
    # problem_res — агрегированное поле проблем: первое непустое из problem1/2/3/correction_comment
    queryset = queryset.annotate(problem_res=Coalesce("problem1", "problem2", "problem3", "correction_comment"))

    # queryset = queryset.annotate(problem=F("correction_comment") if F("volume_of_the_work") else F("problem_res"))
    # problem — если указан ручной объем (корректировка), отображаем комментарий коррекции; иначе — агрегированная проблема
    queryset = queryset.annotate(
        problem=Case(
            When(volume_of_the_work__isnull=False, then=F("correction_comment")),
            default=F("problem_res"),
            output_field=CharField(),
        )
    )

    # queryset = queryset.annotate(problem=F("correction_comment") if F("volume_of_the_work") else F("problem_res"))
    # Дополнительные поля из task.additional — дата и описание, отображаются, если данные вообще присутствуют в выборке
    queryset = queryset.annotate(
        additional_date=Case(
            When(task__additional__isnull=False, then=F("task__additional__datetime")),
            default=None,
            output_field=DateTimeField(),
        )
    )
    queryset = queryset.annotate(
        additional_description=Case(
            When(task__additional__isnull=False, then=F("task__additional__description")),
            default=None,
            output_field=CharField(),
        )
    )

    # Менеджер Заказчика
    # ФИО менеджера заявки (конкатенация ФИО)
    queryset = queryset.annotate(
        manager_full_name=Concat(
            "task__manager__first_name",
            Value(" "),
            "task__manager__middle_name",
            Value(" "),
            "task__manager__second_name",
        )
    )

    # Формируем плоский набор значений для построения DataFrame — выбираем только те поля, которые нужны для отчета
    # ВАЖНО: Берем базовые значения БЕЗ округления для последующего пересчета в pandas с правильным округлением
    newarr = queryset.values(
        "executer_full_name",  # ФИО Исполнителя
        "profession_name",  # Наименование профессии
        "task__profession__description",  # Наименование услуги
        "task__rent",  # Ставка, руб. (базовое значение, будет округлено в pandas)
        "task__profession__percent",  # Процент HOOPS (нужен для расчетов)
        "start_teor",  # используется для формирования "Время начала"
        "stop_teor",  # используется для формирования "Время окончания"
        "volume_t_base",  # Базовый объем услуг (БЕЗ округления, будет округлен в pandas)
        "volume_f_base",  # Базовый фактический объем (БЕЗ округления, будет округлен в pandas)
        "task__id",  # Номер заявки
        "manager_full_name",  # Менеджер Заказчика
        "task__start_at",  # используется для формирования "Дата"
        "problem",  # Статус заявки
        "additional_date",
        "additional_description",
    )

    # --- КОНВЕРТИРУЕМ В DataFrame ---
    df = pd.DataFrame(newarr)
    df = df.reset_index(drop=True)
    df.index += 1

    # --- ПРИМЕНЯЕМ ОКРУГЛЕНИЯ ИЗ INVOICE ПЕРЕД МАТЕМАТИЧЕСКИМИ ОПЕРАЦИЯМИ ---
    # ВАЖНО: Сначала округляем объем и финансовые данные, затем используем их в расчетах
    
    # 1. Округляем объем услуг (теоретический) через round_volume_by_spec
    df["volume_t"] = df["volume_t_base"].apply(
        lambda x: float(round_volume_by_spec(x)) if pd.notnull(x) else x
    )
    
    # 2. Округляем фактический объем через round_volume_by_spec
    df["volume_f"] = df["volume_f_base"].apply(
        lambda x: float(round_volume_by_spec(x)) if pd.notnull(x) else x
    )
    
    # 3. Округляем ставку через round_money_4_5
    df["task__rent_rounded"] = df["task__rent"].apply(
        lambda x: float(round_money_4_5(x)) if pd.notnull(x) else x
    )
    
    # 4. Рассчитываем итоговую оплату (теоретическая): округленный_объем * округленная_ставка, затем округляем результат
    df["salary_t_raw"] = df["volume_t"] * df["task__rent_rounded"]
    df["salary_t"] = df["salary_t_raw"].apply(
        lambda x: float(round_money_4_5(x)) if pd.notnull(x) else x
    )
    
    # 5. Рассчитываем долю HOOPS: salary_t * percent / 100, затем округляем
    df["full_hoops_t_raw"] = df["salary_t"] * df["task__profession__percent"] / 100
    df["full_hoops_t"] = df["full_hoops_t_raw"].apply(
        lambda x: float(round_money_4_5(x)) if pd.notnull(x) else x
    )
    
    # 6. Рассчитываем выплату исполнителям: salary_t - full_hoops_t, затем округляем (как в invoice: rent_for_executer)
    df["salary_executer_t_raw"] = df["salary_t"] - df["full_hoops_t"]
    df["salary_executer_t"] = df["salary_executer_t_raw"].apply(
        lambda x: float(round_money_4_5(x)) if pd.notnull(x) else x
    )
    
    # 7. Рассчитываем вознаграждение: full_hoops_t * remuneration / 100, затем округляем
    # Это соответствует invoice: remuneration_for_executer = (rent - rent_for_executer) * remuneration_percent / 100
    # где (rent - rent_for_executer) = full_hoops_t / volume, но на уровне итоговых сумм: full_hoops_t * remuneration / 100
    df["remuneration_of_the_service_t_raw"] = df["full_hoops_t"] * remuneration / 100
    df["remuneration_of_the_service_t"] = df["remuneration_of_the_service_t_raw"].apply(
        lambda x: float(round_money_4_5(x)) if pd.notnull(x) else x
    )
    
    # 8. Рассчитываем стоимость услуг HOOPS через вычитание (как в invoice): salary_t - remuneration_of_the_service_t - salary_executer_t
    # Все вычитаемые значения уже округлены на предыдущих шагах
    # Это соответствует invoice: rent_for_hoops = rent - remuneration_for_executer - rent_for_executer
    # Или: cost_of_the_service = full_hoops - remuneration
    df["cost_of_the_service_t_raw"] = df["salary_t"] - df["remuneration_of_the_service_t"] - df["salary_executer_t"]
    df["cost_of_the_service_t"] = df["cost_of_the_service_t_raw"].apply(
        lambda x: float(round_money_4_5(x)) if pd.notnull(x) else x
    )
    
    # 9. Рассчитываем фактическую оплату: округленный_фактический_объем * округленная_ставка, затем округляем
    df["salary_f_raw"] = df["volume_f"] * df["task__rent_rounded"]
    df["salary_f"] = df["salary_f_raw"].apply(
        lambda x: float(round_money_4_5(x)) if pd.notnull(x) else x
    )
    
    # 10. Рассчитываем фактическую долю HOOPS: salary_f * percent / 100, затем округляем
    df["full_hoops_f_raw"] = df["salary_f"] * df["task__profession__percent"] / 100
    df["full_hoops_f"] = df["full_hoops_f_raw"].apply(
        lambda x: float(round_money_4_5(x)) if pd.notnull(x) else x
    )
    
    # 11. Рассчитываем фактическую выплату исполнителям: salary_f - full_hoops_f, затем округляем (как в invoice: rent_for_executer)
    df["salary_executer_f_raw"] = df["salary_f"] - df["full_hoops_f"]
    df["salary_executer_f"] = df["salary_executer_f_raw"].apply(
        lambda x: float(round_money_4_5(x)) if pd.notnull(x) else x
    )
    
    # 12. Рассчитываем фактическое вознаграждение: full_hoops_f * remuneration / 100, затем округляем
    # Это соответствует invoice: remuneration_for_executer = (rent - rent_for_executer) * remuneration_percent / 100
    df["remuneration_of_the_service_f_raw"] = df["full_hoops_f"] * remuneration / 100
    df["remuneration_of_the_service_f"] = df["remuneration_of_the_service_f_raw"].apply(
        lambda x: float(round_money_4_5(x)) if pd.notnull(x) else x
    )
    
    # 13. Рассчитываем фактическую стоимость услуг HOOPS через вычитание (как в invoice): salary_f - remuneration_of_the_service_f - salary_executer_f
    # Все вычитаемые значения уже округлены на предыдущих шагах
    # Это соответствует invoice: rent_for_hoops = rent - remuneration_for_executer - rent_for_executer
    df["cost_of_the_service_f_raw"] = df["salary_f"] - df["remuneration_of_the_service_f"] - df["salary_executer_f"]
    df["cost_of_the_service_f"] = df["cost_of_the_service_f_raw"].apply(
        lambda x: float(round_money_4_5(x)) if pd.notnull(x) else x
    )

    # --- ОБНУЛЯЕМ СЕКУНДЫ У ВСЕХ ДАТ/ВРЕМЕНИ, ГДЕ ЭТО ВАЖНО ---
    # Список колонок, где нужно обнулять секунды (start_teor, stop_teor, task__start_at, additional_date)
    for col in ["start_teor", "stop_teor", "task__start_at", "additional_date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
            df[col] = df[col].apply(lambda x: x.replace(second=0, microsecond=0) if pd.notnull(x) else x)

    # Переводим "теоретические" времена в московскую таймзону для корректного отображения и формируем строки времени/даты
    df["start_moscow"] = df["start_teor"].dt.tz_convert("Europe/Moscow")
    df["stop_moscow"] = df["stop_teor"].dt.tz_convert("Europe/Moscow")
    df["start_t"] = df["start_moscow"].dt.strftime("%H:%M")  # Время начала
    df["stop_t"] = df["stop_moscow"].dt.strftime("%H:%M")  # Время окончания

    df["task__start_at"] = df["start_moscow"].dt.strftime("%d.%m.%Y")  # Дата

    # Проверка равенства: cost_of_the_service_t + remuneration_of_the_service_t + salary_executer_t == salary_t
    try:
        left_sum = (
            df["cost_of_the_service_t"].astype(float)
            + df["remuneration_of_the_service_t"].astype(float)
            + df["salary_executer_t"].astype(float)
        )
        right_sum = df["salary_t"].astype(float)
        mism = (left_sum.round(2) != right_sum.round(2))
        if mism.any():
            cnt = int(mism.sum())
            print(f"[StandardReport] Rounding mismatch rows: {cnt}")
            # Вывести первые несколько случаев для диагностики
            print(
                df.loc[mism, [
                    "salary_t",
                    "cost_of_the_service_t",
                    "remuneration_of_the_service_t",
                    "salary_executer_t",
                ]].head(5)
            )
    except Exception as e:
        print(f"[StandardReport] Rounding check failed: {e}")

    # Проверка равенства (факт): cost_of_the_service_f + remuneration_of_the_service_f + salary_executer_f == salary_f
    try:
        left_sum_f = (
            df["cost_of_the_service_f"].astype(float)
            + df["remuneration_of_the_service_f"].astype(float)
            + df["salary_executer_f"].astype(float)
        )
        right_sum_f = df["salary_f"].astype(float)
        mism_f = (left_sum_f.round(2) != right_sum_f.round(2))
        if mism_f.any():
            cnt = int(mism_f.sum())
            print(f"[StandardReport] Rounding mismatch rows (fact): {cnt}")
            print(
                df.loc[mism_f, [
                    "salary_f",
                    "cost_of_the_service_f",
                    "remuneration_of_the_service_f",
                    "salary_executer_f",
                ]].head(5)
            )
    except Exception as e:
        print(f"[StandardReport] Rounding check (fact) failed: {e}")

    # Агрегируем суммы для итоговых строк (факт/теория). Округление до 2 знаков через round для вывода
    itog_sum_fact, hs_sum_fact, executor_sum_fact, volume_sum_fact, hoops_remuneration_fact = (
        round(df["salary_f"].sum(), 2),
        round(df["cost_of_the_service_f"].sum(), 2),
        round(df["salary_executer_f"].sum(), 2),
        round(df["volume_f"].sum(), 2),
        round(df["remuneration_of_the_service_f"].sum(), 2),
    )
    itog_sum_teor, hs_sum_teor, executor_sum_teor, volume_sum_teor, hoops_remuneration_teor = (
        round(df["salary_t"].sum(), 2),
        round(df["cost_of_the_service_t"].sum(), 2),
        round(df["salary_executer_t"].sum(), 2),
        round(df["volume_t"].sum(), 2),
        round(df["remuneration_of_the_service_t"].sum(), 2),
    )
    #
    # df = df.rename(
    #     columns={
    #         "executer_full_name": "ФИО Исполнителя",
    #         "profession_name": "Наименование профессии",
    #         "task__profession__description": "Наименование услуги",
    #         "task__rent": "Ставка, руб.",
    #         "start_t": "Время начала",
    #         "stop_t": "Время окончания",
    #         "volume_t": "Объем услуг",
    #         "task__id": "Номер заявки",
    #         "manager_full_name": "Менеджер Заказчика",
    #         "salary_t": "Итого оплат, руб.",
    #         "cost_of_the_service_t": "Стоимость услуг HOOPS Service",
    #         "remuneration_of_the_service_t": "Вознаграждение за исполнение поручения",
    #         "salary_executer_t": "Выплата исполнителям",
    #         "task__start_at": "Дата",
    #         "problem": "Статус заявки",
    #         "additional_date": "Дата комментария",
    #         "additional_description": "Комментарий",
    #     }
    # )
    #
    # columns = [
    #     "ФИО Исполнителя",
    #     "Наименование профессии",
    #     "Наименование услуги",
    #     "Дата",
    #     "Ставка, руб.",
    #     "Время начала",
    #     "Время окончания",
    #     "Объем услуг",
    #     "Итого оплат, руб.",
    #     "Стоимость услуг HOOPS Service",
    #     "Выплата исполнителям",
    #     "Номер заявки",
    #     "Статус заявки",
    #     "Менеджер Заказчика",
    #     "Дата комментария",
    #     "Комментарий",
    # ]

    # Переименование колонок на человекочитаемые заголовки и формирование перечня финальных колонок
    df = df.rename(
        columns={
            "executer_full_name": "ФИО Исполнителя",  # ФИО Исполнителя
            "profession_name": "Наименование профессии",  # Наименование профессии
            "task__profession__description": "Наименование услуги",  # Наименование услуги
            "task__rent": "Ставка, руб.",  # Ставка, руб.
            "start_t": "Время начала",  # Время начала
            "stop_t": "Время окончания",  # Время окончания
            "volume_t": "Объем услуг",  # Объем услуг
            "task__id": "Номер заявки",  # Номер заявки
            "manager_full_name": "Менеджер Заказчика",  # Менеджер Заказчика
            "salary_t": "Итого оплат, руб.",  # Итого оплат, руб.
            "cost_of_the_service_t": "Стоимость услуг HOOPS Service",  # Стоимость услуг HOOPS Service
            "remuneration_of_the_service_t": "Вознаграждение за исполнение поручения",  # Вознаграждение за исполнение поручения
            "salary_executer_t": "Выплата исполнителям",  # Выплата исполнителям
            "task__start_at": "Дата",  # Дата
            "problem": "Статус заявки",  # Статус заявки
            "additional_date": "Дата комментария",
            "additional_description": "Комментарий",
        }
    )

    columns = [
        "ФИО Исполнителя",
        "Наименование профессии",
        "Наименование услуги",
        "Дата",
        "Ставка, руб.",
        "Время начала",
        "Время окончания",
        "Объем услуг",
        "Итого оплат, руб.",
        "Стоимость услуг HOOPS Service",
        "Вознаграждение за исполнение поручения",
        "Выплата исполнителям",
        "Номер заявки",
        "Статус заявки",
        "Менеджер Заказчика",
        "Дата комментария",
        "Комментарий",
    ]

    # Оставляем в DataFrame только необходимые к выводу колонки в заданном порядке
    df = df[columns]
    # Проверяем, присутствуют ли вообще дополнительные поля (дата/комментарий). Если нет — эти колонки удаляются.
    additional = df["Дата комментария"].notnull().any()
    if not additional:
        del df["Дата комментария"]
        del df["Комментарий"]
    if additional:
        # Локализуем дату комментария в МСК и форматируем для вывода
        df["Дата комментария"] = df["Дата комментария"].dt.tz_convert("Europe/Moscow")
        df["Дата комментария"] = df["Дата комментария"].dt.strftime("%d.%m.%Y")

    # Инициализируем ExcelWriter и выгружаем DataFrame на лист «Стандартный отчет»
    writer = pd.ExcelWriter(path, engine="xlsxwriter")
    df.to_excel(
        writer,
        float_format="%.2f",
        sheet_name="Стандартный отчет",
        startrow=1,
        index=False,
    )
    # Готовим форматы для шапки, заголовков и ячеек
    center_format_with_grey = writer.book.add_format(
        {
            "align": "center",  # Горизонтальное выравнивание
            "valign": "vcenter",  # Вертикальное выравнивание
            "bg_color": "#D3D3D3",
            "border": 1,
            "bold": True,
            "text_wrap": True,
        }
    )
    center_format_with_white = writer.book.add_format(
        {
            "align": "center",  # Горизонтальное выравнивание
            "valign": "vcenter",  # Вертикальное выравнивание
            "border": 1,
            "bold": True,
            "font_size": 12,
        }
    )

    border = writer.book.add_format(
        {
            "border": 1,
        }
    )

    size_align_right = {"font_size": 12, "align": "right"}
    size_align_left = {"font_size": 12, "align": "left"}
    all_format_right_align = writer.book.add_format(size_align_right)
    all_format_left_align = writer.book.add_format(size_align_left)

    rub_format = writer.book.add_format({"num_format": "#,##0.00₽", **size_align_right})

    worksheet = writer.sheets["Стандартный отчет"]
    # Устанавливаем формат по умолчанию для всего рабочего листа
    worksheet.set_default_row(height=15)

    # Настройка шапки: автофильтр на заголовках, высота строк, объединение ячеек под период и название гостиницы,
    # вставка логотипа, auto-fit столбцов
    worksheet.autofilter("A2:N2")
    worksheet.set_row(0, 50)
    worksheet.set_row(1, 30)
    worksheet.merge_range(0, 2, 0, 7, data=period, cell_format=center_format_with_white)
    worksheet.merge_range(0, 8, 0, 10, data="", cell_format=center_format_with_white)
    worksheet.merge_range(0, 11, 0, 13, data=hotel_name, cell_format=center_format_with_white)
    worksheet.merge_range(0, 0, 0, 1, "Стандартный отчет", cell_format=center_format_with_white)
    worksheet.insert_image("J1", "hotels/scripts/sample/hoops.png")
    worksheet.autofit()

    # стиль столбцов
    # Ширины и форматы по диапазонам столбцов: выравнивание, формат валют, ширина
    worksheet.set_column(0, 0, 45, all_format_left_align)
    worksheet.set_column(1, 3, 27, all_format_left_align)
    worksheet.set_column(3, 9, 15, all_format_right_align)
    worksheet.set_column(9, 11, 22, all_format_right_align)
    worksheet.set_column(11, 13, 22, all_format_right_align)
    worksheet.set_column(14, 14, 34, all_format_left_align)
    worksheet.set_column(8, 11, 17, rub_format)
    worksheet.set_column(4, 4, 15, rub_format)
    # worksheet.conditional_format(
    #     1,
    #     10,
    #     10,
    #     10,
    #     {"type": "cell", "criteria": "all", "value": "", "format": border},
    # )
    # Рисуем рамки по всей области данных условным форматированием «no_errors»
    max_row, max_col = df.shape
    max_col -= 1
    max_row += 1
    worksheet.conditional_format(
        2,
        0,
        max_row,
        max_col,
        {"type": "no_errors", "format": border},
    )

    # Вывод итоговых строк: «Сумма услуг ...» (теория) и «Сумма фактически оказанных услуг ...» (факт)
    max_row += 2
    row_for_teor = max_row + 1
    row_for_fact = max_row + 2
    worksheet.write(row_for_teor, 0, "Сумма  услуг по заявкам за период:")
    worksheet.write(row_for_teor, 7, volume_sum_teor)
    worksheet.write(row_for_teor, 8, itog_sum_teor)
    worksheet.write(row_for_teor, 9, hs_sum_teor)
    worksheet.write(row_for_teor, 10, hoops_remuneration_teor)
    worksheet.write(row_for_teor, 11, executor_sum_teor)
    worksheet.write(row_for_fact, 0, "Сумма фактически оказанных услуг за период:")
    worksheet.write(row_for_fact, 7, volume_sum_fact)
    worksheet.write(row_for_fact, 8, itog_sum_fact)
    worksheet.write(row_for_fact, 9, hs_sum_fact)
    worksheet.write(row_for_fact, 10, hoops_remuneration_fact)
    worksheet.write(row_for_fact, 11, executor_sum_fact)

    # Перерисовываем заголовки таблицы с серой заливкой и выравниванием по центру
    for num, value in enumerate(list(df.columns), 0):
        worksheet.write(1, num, value, center_format_with_grey)

    # Добавляем футер и печать/подпись, затем сохраняем/закрываем файл
    create_footer_and_stamp_signature(worksheet, max_row + 4)

    writer.close()
