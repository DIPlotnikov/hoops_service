"""Утилиты для форматирования дат и периодов для документов.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional, Union


def to_datetime(value: Union[str, datetime, None]) -> Optional[datetime]:
    """Приводит значение к datetime.
    Если строка — пробует распарсить несколько форматов, без таймзоны.
    Возвращает None, если распарсить не удалось.
    """
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        # Отбрасываем возможную таймзону вида "+03:00"
        value_ = value.split("+")[0]
        for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                return datetime.strptime(value_, fmt)
            except Exception:
                continue
    return None


def format_date_ru(dt: datetime) -> str:
    """Форматирует дату как '10 сентября 2025 года'."""
    months = {
        1: "января", 2: "февраля", 3: "марта", 4: "апреля", 5: "мая", 6: "июня",
        7: "июля", 8: "августа", 9: "сентября", 10: "октября", 11: "ноября", 12: "декабря",
    }
    return f"{dt.day} {months.get(dt.month, '')} {dt.year} года"


def format_period_ru(start_dt: Union[str, datetime, None], end_dt: Union[str, datetime, None]) -> str:
    """Возвращает строку вида: 'с 10 сентября 2025 года по 13 сентября 2025 года'.
    Если даты отсутствуют или не распарсены — вернёт пустую строку.
    """
    sd = to_datetime(start_dt)
    ed = to_datetime(end_dt)
    if not sd or not ed:
        return ""
    return f"с {format_date_ru(sd)} по {format_date_ru(ed)}"
