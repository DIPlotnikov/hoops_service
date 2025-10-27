import math


def round_value_for_hoops(num):
    return math.ceil(num * 100) / 100


import math
from decimal import ROUND_DOWN, Decimal, ROUND_UP, ROUND_HALF_UP


def round_volume_by_spec(value) -> Decimal:
    """
    Округление объёмов услуг до 2 знаков по правилу:
    1) Отбросить всё после 3-го знака.
    2) Если 3-й знак > 0 — округлить 2-й знак вверх, иначе оставить.
    Возвращает Decimal с двумя знаками.
    """
    d = Decimal(str(value))
    # Отсечь до 3 знаков
    d3 = d.quantize(Decimal('0.000'), rounding=ROUND_DOWN)
    third_digit = int((d3 * 1000) % 10)
    # Базовые 2 знака (без учёта третьего)
    d2 = d3.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
    if third_digit > 0:
        d2 += Decimal('0.01')
    return d2


def round_money_4_5(value: float) -> Decimal:
    """
    Округляет денежные значения по правилу 4/5 до 2 знаков после запятой.
    
    Правила:
    - Если после запятой больше 2 знаков, учитываем только 3-й знак
    - 3-й знак >= 5 → второй знак округляем вверх
    - 3-й знак <= 4 → второй знак без изменений  
    - 4-й и последующие знаки игнорируются
    
    Применяется для всех денежных значений: тарифы, суммы, НДС, итоги.
    
    @param value: денежное значение для округления
    @return: округлённое значение с 2 знаками после запятой
    """
    d = Decimal(str(value))
    # Отрезаем всё после 3-го знака
    d_truncated = d.quantize(Decimal('0.000'), rounding='ROUND_DOWN')
    
    frac = str(d_truncated).split('.')[-1] if '.' in str(d_truncated) else ''
    third_digit = int(frac[2]) if len(frac) > 2 else 0
    
    if third_digit >= 5:
        d_result = d_truncated.quantize(Decimal('0.01'), rounding=ROUND_UP)
    else:
        d_result = d_truncated.quantize(Decimal('0.01'), rounding='ROUND_DOWN')
    
    return d_result
