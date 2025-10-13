"""Утилиты для сравнения реквизитов организаций в сгруппированных закрывающих документах.

Функции выносят логику сравнения из `core/closing_documents/mutation.py`,
чтобы сделать код чище и переиспользуемым.
"""
from __future__ import annotations

from typing import Dict, Iterable, List, Tuple


def _collect_base(orgs_data: List[dict]) -> dict:
    """Возвращает базовые реквизиты (из первой записи) либо пустой словарь.

    orgs_data: список словарей вида {
      'hotel_id': int,
      'hotel_name': str,
      'requisites': {'inn': str, 'kpp': str, 'legal_address': str, 'signer': str},
      ...
    }
    """
    return orgs_data[0].get("requisites", {}) if orgs_data else {}


def diff_requisites_against_base(
    orgs_data: List[dict],
    keys: Tuple[str, ...] = ("inn", "kpp", "legal_address", "signer"),
) -> List[Tuple[int, str, Dict[str, Dict[str, str]]]]:
    """Сравнивает реквизиты каждой организации с первой (базовой).

    Возвращает список кортежей: (hotel_id, hotel_name, diffs), где diffs — словарь
    отличий по ключам: { key: { 'base': <значение у базовой>, 'current': <текущее> } }
    Только организации с отличиями попадают в результат.
    """
    base_req = _collect_base(orgs_data)
    result: List[Tuple[int, str, Dict[str, Dict[str, str]]]] = []

    for org in orgs_data[1:]:
        current_req = org.get("requisites", {})
        diffs: Dict[str, Dict[str, str]] = {}
        for k in keys:
            if base_req.get(k) != current_req.get(k):
                diffs[k] = {"base": base_req.get(k), "current": current_req.get(k)}
        if diffs:
            result.append((org.get("hotel_id"), org.get("hotel_name"), diffs))

    return result


def group_requisites_differences(
    orgs_data: List[dict],
    keys: Tuple[str, ...] = ("inn", "kpp", "legal_address", "signer"),
) -> Dict[str, Dict[str, List[int]]]:
    """Строит группировку отличий по каждому полю реквизитов.

    Возвращает словарь: key -> { value -> [hotel_id, ...] }
    где value — конкретное значение реквизита, а список — id организаций с таким значением.
    """
    groups: Dict[str, Dict[str, List[int]]] = {}
    for k in keys:
        by_value: Dict[str, List[int]] = {}
        for org in orgs_data:
            v = (org.get("requisites", {})).get(k)
            by_value.setdefault(str(v), []).append(org.get("hotel_id"))
        groups[k] = by_value
    return groups


def check_and_log_requisites_differences(orgs_data: List[dict]) -> None:
    """Печатает различия реквизитов (как раньше в мутации), если они есть.

    - По-организационно: отличия относительно первой записи.
    - По-полям: групповой срез значений и состав групп по значениям.
    """
    try:
        # По-организационно: вывод различий относительно первой записи
        per_org_diffs = diff_requisites_against_base(orgs_data)
        for hotel_id, hotel_name, diffs in per_org_diffs:
            print(
                f"[CreateGroupedClosingDocuments][ALARM] Реквизиты отличаются у hotel_id={hotel_id} (\"{hotel_name}\"). "
                f"Отличия: {diffs}"
            )

        # По-полям: групповой срез различий
        groups = group_requisites_differences(orgs_data)
        for k, by_value in groups.items():
            if len(by_value.keys()) > 1:
                print(
                    f"[CreateGroupedClosingDocuments] Поле реквизитов '{k}' различается между организациями: {by_value}"
                )
    except Exception as e:
        print(f"[CreateGroupedClosingDocuments] Ошибка при сравнении реквизитов: {e}")
