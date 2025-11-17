import pandas as pd
from django.db.models import Case, CharField, DateTimeField, ExpressionWrapper, F, FloatField, Func, Value, When
from django.db.models.functions import Coalesce, Concat, TruncMinute

from hotels.utils.invoice import round_money_4_5, round_volume_by_spec
from settings.models import get_remuneration
from hotels.scripts.nds_handler import calc_tax

from .utils import create_footer_and_stamp_signature


def prepare_queryset_data(queryset, remuneration=10):
    """
    Подготавливает данные из БД для стандартного отчета.
    
    Выполняет все ORM-аннотации для расчета производных полей и извлекает необходимые данные.
    
    @param queryset: QuerySet состояний исполнителей
    @param remuneration: Процент вознаграждения от доли HOOPS (не используется в ORM, но оставлен для совместимости)
    @return: Список словарей с данными для построения DataFrame
    """
    # ФИО Исполнителя -> столбец "ФИО Исполнителя"
    queryset = queryset.annotate(
        executer_full_name=Concat(
            "executer__middle_name", Value(" "), "executer__first_name", Value(" "), "executer__second_name"
        )
    )
    # Наименование профессии -> столбец "Наименование профессии"
    queryset = queryset.annotate(profession_name=Coalesce("task__personal_profession__name", "task__profession__name"))

    class MinuteInterval(Func):
        template = "INTERVAL %(expressions)s HOUR"

    _end_date = F("task__start_at") + MinuteInterval(F("task__duration"))

    # старт задачи с предположениями -> столбец "Время начала"
    queryset = queryset.annotate(start_teor=Coalesce("start_at", "task__start_at"))
    # стоп задачи с предположениями
    # queryset = queryset.annotate(
    #     stop_task=ExpressionWrapper(F("task__start_at") + timedelta(hours=F("task__duration")), output_field=DateTimeField())
    # )
    queryset = queryset.annotate(
        stop_task=ExpressionWrapper(_end_date, output_field=DateTimeField()),
    )
    queryset = queryset.annotate(stop_teor=Coalesce("stop_at", "stop_task"))  # -> столбец "Время окончания"

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

    # Пересчитываем volume_time_f и volume_time_t на базе duration_f и duration_t
    # БЕЗ округления - округление будет применено в pandas через round_volume_by_spec
    queryset = queryset.annotate(
        volume_time_f=ExpressionWrapper(F("duration_f") / 3600000000, output_field=FloatField())
    )
    queryset = queryset.annotate(
        volume_time_t=ExpressionWrapper(F("duration_t") / 3600000000, output_field=FloatField())
    )

    # Объем услуг -> столбец "Объем услуг"
    # Базовые объемы (БЕЗ округления) - округление будет применено в pandas через round_volume_by_spec
    # volume_f_base — фактический объем: Coalesce(ручной, расчетный факт)
    queryset = queryset.annotate(volume_f_base=Coalesce("volume_of_the_work", "volume_time_f"))
    # volume_t_base — теоретический объем: Coalesce(ручной, расчетный теоретический)
    queryset = queryset.annotate(volume_t_base=Coalesce("volume_of_the_work", "volume_time_t"))

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

    # Статус заявки -> столбец "Статус заявки"
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

    # Менеджер Заказчика -> столбец "Менеджер Заказчика"
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

    # Вознаграждение для HOOPS -> одинаковое значение для всех записей
    # Получаем значение из настроек и добавляем как константу
    remuneration_value = get_remuneration()
    queryset = queryset.annotate(remuneration=Value(remuneration_value, output_field=FloatField()))

    # Формируем плоский набор значений для построения DataFrame — выбираем только те поля, которые нужны для отчета
    # ВАЖНО: Берем базовые значения БЕЗ округления для последующего пересчета в pandas с правильным округлением
    newarr = queryset.values(
        "executer_full_name",  # -> столбец "ФИО Исполнителя"
        "profession_name",  # -> столбец "Наименование профессии"
        "task__profession__description",  # -> столбец "Наименование услуги"
        "task__rent",  # -> столбец "Ставка, руб." (базовое значение, будет округлено в pandas)
        "task__profession__percent",  # Процент HOOPS (нужен для расчетов)
        "task__profession__numerate",  # Тип профессии (HOUR/SUIT) для группировки в закрывающих документах
        "start_teor",  # -> столбец "Время начала"
        "stop_teor",  # -> столбец "Время окончания"
        "volume_t_base",  # -> столбец "Объем услуг" (БЕЗ округления, будет округлен в pandas)
        "volume_f_base",  # Базовый фактический объем (БЕЗ округления, будет округлен в pandas)
        "task__id",  # -> столбец "Номер заявки"
        "manager_full_name",  # -> столбец "Менеджер Заказчика"
        "task__start_at",  # -> столбец "Дата"
        "problem",  # -> столбец "Статус заявки"
        "additional_date",
        "additional_description",
        "remuneration",  # Вознаграждение для HOOPS (одинаковое для всех записей)
    )
    
    return list(newarr)


def calculate_financial_data(data, remuneration=10, nds=20.0):
    """
    Выполняет финансовые расчеты в pandas с применением округлений из invoice.
    
    Применяет округления и рассчитывает все финансовые поля согласно логике invoice:
    сначала цены за единицу, затем умножение на объем, затем округление итогов.
    Также рассчитывает НДС и стоимости без НДС для закрывающих документов.
    
    @param data: Список словарей с базовыми данными из prepare_queryset_data
    @param remuneration: Процент вознаграждения от доли HOOPS
    @param nds: Ставка НДС (по умолчанию 20.0%)
    @return: Кортеж (DataFrame с рассчитанными финансовыми полями, итоговые суммы)
             Итоговые суммы: (itog_sum_fact, hs_sum_fact, executor_sum_fact, volume_sum_fact, hoops_remuneration_fact,
                              itog_sum_teor, hs_sum_teor, executor_sum_teor, volume_sum_teor, hoops_remuneration_teor,
                              total_price_invoice, total_sum_for_executer_invoice, total_tax_invoice)
    """

    # --- КОНВЕРТИРУЕМ В DataFrame ---
    df = pd.DataFrame(data)
    df = df.reset_index(drop=True)
    df.index += 1

    # --- ПРИМЕНЯЕМ ОКРУГЛЕНИЯ ИЗ INVOICE ПЕРЕД МАТЕМАТИЧЕСКИМИ ОПЕРАЦИЯМИ ---
    # ВАЖНО: Приводим к логике invoice: сначала рассчитываем цены за единицу, затем умножаем на объем
    
    # 1. Округляем объем услуг (теоретический) через round_volume_by_spec
    df["volume_t"] = df["volume_t_base"].apply(
        lambda x: float(round_volume_by_spec(x)) if pd.notnull(x) else x
    )
    
    # 2. Округляем фактический объем через round_volume_by_spec
    df["volume_f"] = df["volume_f_base"].apply(
        lambda x: float(round_volume_by_spec(x)) if pd.notnull(x) else x
    )
    
    # 3. Рассчитываем цены за единицу (как в invoice)
    # Цены за единицу одинаковы для теоретического и фактического расчета (не зависят от объема)
    # ВАЖНО: Округляем каждую цену ДО использования в следующих расчетах для обеспечения баланса
    
    # Цена услуг исполнителей за единицу: rent - (rent * prof_percent / 100)
    df["rent_for_executer_raw"] = df["task__rent"] - (df["task__rent"] * df["task__profession__percent"] / 100)
    df["rent_for_executer"] = df["rent_for_executer_raw"].apply(
        lambda x: float(round_money_4_5(x)) if pd.notnull(x) else x
    )
    
    # Стоимость услуги HOOPS за единицу: (rent - rent_for_executer) * remuneration_percent / 100
    # Используем округленное значение rent_for_executer для расчета
    df["rent_for_hoops_raw"] = (df["task__rent"] - df["rent_for_executer"]) * remuneration / 100
    df["rent_for_hoops"] = df["rent_for_hoops_raw"].apply(
        lambda x: float(round_money_4_5(x)) if pd.notnull(x) else x
    )
    
    # Вознаграждение за единицу: rent - rent_for_hoops - rent_for_executer (через вычитание УЖЕ ОКРУГЛЕННЫХ значений)
    # ВАЖНО: используем округленные значения для расчета, чтобы обеспечить баланс: rent = rent_for_executer + rent_for_hoops + remuneration_for_executer
    df["remuneration_for_executer"] = df["task__rent"] - df["rent_for_hoops"] - df["rent_for_executer"]
    # Округляем вознаграждение для консистентности (как в invoice)
    df["remuneration_for_executer"] = df["remuneration_for_executer"].apply(
        lambda x: float(round_money_4_5(x)) if pd.notnull(x) else x
    )
    
    # 5. Умножаем округленные цены за единицу на округленный теоретический объем (как в invoice)
    df["salary_executer_t_raw"] = df["rent_for_executer"] * df["volume_t"]
    # cost_of_the_service_t = стоимость услуг HOOPS Service (основная услуга, как hoops_cost в invoice)
    # В invoice: hoops_cost = rent_for_hoops * worktime
    df["cost_of_the_service_t_raw"] = df["rent_for_hoops"] * df["volume_t"]
    # remuneration_of_the_service_t = вознаграждение за исполнение поручения (как hoops_remuneration в invoice)
    # В invoice: hoops_remuneration = remuneration_for_executer * worktime
    df["remuneration_of_the_service_t_raw"] = df["remuneration_for_executer"] * df["volume_t"]

    # print('salary_executer_t_raw: ', df["salary_executer_t_raw"].iloc[0])
    # print('cost_of_the_service_t_raw: ', df["cost_of_the_service_t_raw"].iloc[0])
    # print('remuneration_of_the_service_t_raw: ', df["remuneration_of_the_service_t_raw"].iloc[0])
    # print("--------------------------------")
    
    # 6. Округляем итоговые суммы (как в invoice)
    df["salary_executer_t"] = df["salary_executer_t_raw"].apply(
        lambda x: float(round_money_4_5(x)) if pd.notnull(x) else x
    )
    df["cost_of_the_service_t"] = df["cost_of_the_service_t_raw"].apply(
        lambda x: float(round_money_4_5(x)) if pd.notnull(x) else x
    )
    df["remuneration_of_the_service_t"] = df["remuneration_of_the_service_t_raw"].apply(
        lambda x: float(round_money_4_5(x)) if pd.notnull(x) else x
    )
    
    # 7. Рассчитываем итоговую оплату (теоретическая): сумма всех компонентов
    df["salary_t"] = df["cost_of_the_service_t"] + df["remuneration_of_the_service_t"] + df["salary_executer_t"]
    
    # 8. Умножаем округленные цены за единицу на округленный фактический объем (как в invoice)
    # Используем те же цены за единицу, что и для теоретического расчета
    df["salary_executer_f_raw"] = df["rent_for_executer"] * df["volume_f"]
    # cost_of_the_service_f = стоимость услуг HOOPS Service (основная услуга, как hoops_cost в invoice)
    # В invoice: hoops_cost = rent_for_hoops * worktime
    df["cost_of_the_service_f_raw"] = df["rent_for_hoops"] * df["volume_f"]
    # remuneration_of_the_service_f = вознаграждение за исполнение поручения (как hoops_remuneration в invoice)
    # В invoice: hoops_remuneration = remuneration_for_executer * worktime
    df["remuneration_of_the_service_f_raw"] = df["remuneration_for_executer"] * df["volume_f"]

    # print('salary_executer_f_raw: ', df["salary_executer_f_raw"].iloc[0])
    # print('cost_of_the_service_f_raw: ', df["cost_of_the_service_f_raw"].iloc[0])
    # print('remuneration_of_the_service_f_raw: ', df["remuneration_of_the_service_f_raw"].iloc[0])
    # print("--------------------------------")
    
    # 9. Округляем фактические итоговые суммы (как в invoice)
    df["salary_executer_f"] = df["salary_executer_f_raw"].apply(
        lambda x: float(round_money_4_5(x)) if pd.notnull(x) else x
    )
    df["cost_of_the_service_f"] = df["cost_of_the_service_f_raw"].apply(
        lambda x: float(round_money_4_5(x)) if pd.notnull(x) else x
    )
    df["remuneration_of_the_service_f"] = df["remuneration_of_the_service_f_raw"].apply(
        lambda x: float(round_money_4_5(x)) if pd.notnull(x) else x
    )

    # 12. Рассчитываем итоговую фактическую оплату: сумма всех компонентов
    df["salary_f"] = df["cost_of_the_service_f"] + df["remuneration_of_the_service_f"] + df["salary_executer_f"]

    # 13. Расчет НДС для фактических сумм (для закрывающих документов)
    # НДС для основной услуги HOOPS Service
    df["nds_cost_of_the_service_f"] = df["cost_of_the_service_f"].apply(
        lambda x: float(calc_tax(x, nds)) if pd.notnull(x) else x
    )
    # НДС для вознаграждения
    df["nds_remuneration_of_the_service_f"] = df["remuneration_of_the_service_f"].apply(
        lambda x: float(calc_tax(x, nds)) if pd.notnull(x) else x
    )
    # Услуги исполнителей не облагаются НДС
    df["nds_salary_executer_f"] = 0.0

    # 14. Расчет стоимости без НДС для фактических сумм (для закрывающих документов)
    df["cost_of_the_service_f_without_tax"] = df["cost_of_the_service_f"] - df["nds_cost_of_the_service_f"]
    df["remuneration_of_the_service_f_without_tax"] = df["remuneration_of_the_service_f"] - df["nds_remuneration_of_the_service_f"]
    df["salary_executer_f_without_tax"] = df["salary_executer_f"] - df["nds_salary_executer_f"]

    # Округляем стоимости без НДС
    df["cost_of_the_service_f_without_tax"] = df["cost_of_the_service_f_without_tax"].apply(
        lambda x: float(round_money_4_5(x)) if pd.notnull(x) else x
    )
    df["remuneration_of_the_service_f_without_tax"] = df["remuneration_of_the_service_f_without_tax"].apply(
        lambda x: float(round_money_4_5(x)) if pd.notnull(x) else x
    )
    df["salary_executer_f_without_tax"] = df["salary_executer_f_without_tax"].apply(
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
        # Фильтруем только валидные строки (не NaN)
        valid_mask = (
            df["cost_of_the_service_t"].notna()
            & df["remuneration_of_the_service_t"].notna()
            & df["salary_executer_t"].notna()
            & df["salary_t"].notna()
        )
        
        if valid_mask.any():
            left_sum = (
                df.loc[valid_mask, "cost_of_the_service_t"].astype(float)
                + df.loc[valid_mask, "remuneration_of_the_service_t"].astype(float)
                + df.loc[valid_mask, "salary_executer_t"].astype(float)
            )
            right_sum = df.loc[valid_mask, "salary_t"].astype(float)
            mism = (left_sum.round(2) != right_sum.round(2))
            
            if mism.any():
                cnt = int(mism.sum())
                print(f"[StandardReport] Rounding mismatch rows (theory): {cnt}")
                # Вывести детальную информацию для диагностики
                mism_rows = df.loc[valid_mask].loc[mism]
                for idx, row in mism_rows.head(10).iterrows():
                    left = (
                        float(row["cost_of_the_service_t"])
                        + float(row["remuneration_of_the_service_t"])
                        + float(row["salary_executer_t"])
                    )
                    right = float(row["salary_t"])
                    diff = abs(left - right)
                    task_id = row.get("task__id", "N/A")
                    print(
                        f"  Row {idx} (task_id={task_id}): "
                        f"left={left:.2f}, right={right:.2f}, diff={diff:.4f} | "
                        f"cost={row['cost_of_the_service_t']:.2f}, "
                        f"rem={row['remuneration_of_the_service_t']:.2f}, "
                        f"exec={row['salary_executer_t']:.2f}"
                    )
    except Exception as e:
        print(f"[StandardReport] Rounding check failed: {e}")

    # Проверка равенства (факт): cost_of_the_service_f + remuneration_of_the_service_f + salary_executer_f == salary_f
    try:
        # Фильтруем только валидные строки (не NaN)
        valid_mask_f = (
            df["cost_of_the_service_f"].notna()
            & df["remuneration_of_the_service_f"].notna()
            & df["salary_executer_f"].notna()
            & df["salary_f"].notna()
        )
        
        if valid_mask_f.any():
            left_sum_f = (
                df.loc[valid_mask_f, "cost_of_the_service_f"].astype(float)
                + df.loc[valid_mask_f, "remuneration_of_the_service_f"].astype(float)
                + df.loc[valid_mask_f, "salary_executer_f"].astype(float)
            )
            right_sum_f = df.loc[valid_mask_f, "salary_f"].astype(float)
            mism_f = (left_sum_f.round(2) != right_sum_f.round(2))
            
            if mism_f.any():
                cnt = int(mism_f.sum())
                print(f"[StandardReport] Rounding mismatch rows (fact): {cnt}")
                # Вывести детальную информацию для диагностики
                mism_rows_f = df.loc[valid_mask_f].loc[mism_f]
                for idx, row in mism_rows_f.head(10).iterrows():
                    left = (
                        float(row["cost_of_the_service_f"])
                        + float(row["remuneration_of_the_service_f"])
                        + float(row["salary_executer_f"])
                    )
                    right = float(row["salary_f"])
                    diff = abs(left - right)
                    task_id = row.get("task__id", "N/A")
                    print(
                        f"  Row {idx} (task_id={task_id}): "
                        f"left={left:.2f}, right={right:.2f}, diff={diff:.4f} | "
                        f"cost={row['cost_of_the_service_f']:.2f}, "
                        f"rem={row['remuneration_of_the_service_f']:.2f}, "
                        f"exec={row['salary_executer_f']:.2f}"
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
    
    # Итоговые суммы для закрывающих документов (invoice)
    # total_price = общая сумма HOOPS (основная услуга + вознаграждение)
    total_price_invoice = round((df["cost_of_the_service_f"].sum() + df["remuneration_of_the_service_f"].sum()), 2)
    # total_sum_for_executer = сумма услуг исполнителей
    total_sum_for_executer_invoice = round(df["salary_executer_f"].sum(), 2)
    # total_tax = общий НДС (НДС основной услуги + НДС вознаграждения)
    total_tax_invoice = round((df["nds_cost_of_the_service_f"].sum() + df["nds_remuneration_of_the_service_f"].sum()), 2)
    
    totals = (
        itog_sum_fact, hs_sum_fact, executor_sum_fact, volume_sum_fact, hoops_remuneration_fact,
        itog_sum_teor, hs_sum_teor, executor_sum_teor, volume_sum_teor, hoops_remuneration_teor,
        total_price_invoice, total_sum_for_executer_invoice, total_tax_invoice
    )
    
    return df, totals


def create_excel_document(
    df, path="hotels/scripts/reports/result.xlsx", period="test period", hotel_name="test name", totals=None
):
    """
    Формирует Excel-документ стандартного отчета из подготовленного DataFrame.
    
    Выполняет форматирование, добавляет шапку, итоговые строки, футер и сохраняет файл.
    
    @param df: DataFrame с рассчитанными данными из calculate_financial_data
    @param path: Путь для сохранения Excel-файла
    @param period: Период отчета для отображения в шапке
    @param hotel_name: Название гостиницы для отображения в шапке
    @param totals: Кортеж с итоговыми суммами из calculate_financial_data
                   (itog_sum_fact, hs_sum_fact, executor_sum_fact, volume_sum_fact, hoops_remuneration_fact,
                    itog_sum_teor, hs_sum_teor, executor_sum_teor, volume_sum_teor, hoops_remuneration_teor,
                    total_price_invoice, total_sum_for_executer_invoice, total_tax_invoice)
                   Последние 3 значения используются только для закрывающих документов и игнорируются в стандартном отчете
    """
    # Распаковываем итоговые суммы (рассчитаны в calculate_financial_data)
    if totals is None:
        # Fallback: рассчитываем на месте, если totals не передан (для обратной совместимости)
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
    else:
        # Распаковываем только первые 10 значений (для стандартного отчета)
        # Последние 3 значения (total_price_invoice, total_sum_for_executer_invoice, total_tax_invoice) используются только для закрывающих документов
        itog_sum_fact, hs_sum_fact, executor_sum_fact, volume_sum_fact, hoops_remuneration_fact, \
        itog_sum_teor, hs_sum_teor, executor_sum_teor, volume_sum_teor, hoops_remuneration_teor, \
        *_ = totals  # Игнорируем последние 3 значения для invoice


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


# pip install xlsxwriter
def create_standart_report(
    queryset, path="hotels/scripts/reports/result.xlsx", period="test period", hotel_name="test name", remuneration=10
):
    """
    Формирует Excel-файл «Стандартный отчет» на основе выборки состояний исполнителей (queryset).
    
    ВЫХОД:
    - Сохраняет Excel в указанный путь (path), использует движок xlsxwriter для форматирования.
    - Возвращаемого значения нет — файл закрывается writer.close().
    
    ОСНОВНАЯ ЛОГИКА:
    1) prepare_queryset_data: На уровне ORM-выражений (annotate) рассчитываются и добавляются к queryset все необходимые
       производные поля: ФИО, профессия, "теоретические" и "фактические" времена/объемы/стоимости,
       доля HOOPS, вознаграждение сервиса, выплаты исполнителю, статусы/проблемы и т.д.
       Через .values(...) извлекаются выбранные поля в плоский набор словарей.
    2) calculate_financial_data: В pandas обогащаем данными для отображения (локализация времени в Europe/Moscow, 
       форматирование дат/времени), применяем округления и рассчитываем финансовые поля согласно логике invoice.
    3) create_excel_document: Суммируем значения для итоговых строк (теория/факт) и записываем их в конец листа.
       Записываем DataFrame на лист «Стандартный отчет» с оформлением: шапка, логотип, автофильтр,
       выравнивания, рамки, форматы валют, итоговые строки и футер с печатью/подписью.
    
    ОБРАТИТЕ ВНИМАНИЕ:
    - В текущей реализации часть расчетов выполнена на уровне ORM (через annotate), а часть — в pandas/Excel.
    - Округление объемов (как фактического, так и теоретического) выполняется в pandas через round_volume_by_spec.
      Базовые объемы (volume_f_base и volume_t_base) возвращаются БЕЗ округления для последующей обработки в pandas.
    - Параметр remuneration (процент от доли HOOPS, направляемый на вознаграждение сервиса) задается аргументом
      функции и влияет на соответствующие поля с суффиксами *_t и *_f.
    """
    # 1. Получаем данные из БД
    data = prepare_queryset_data(queryset, remuneration)
    
    # 2. Выполняем финансовые расчеты в pandas
    df, totals = calculate_financial_data(data, remuneration)
    
    # 3. Формируем Excel-документ
    create_excel_document(df, path, period, hotel_name, totals)

