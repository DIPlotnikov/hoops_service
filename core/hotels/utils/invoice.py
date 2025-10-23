import math


def round_value_for_hoops(num):
    return math.ceil(num * 100) / 100


import math
from decimal import Decimal, ROUND_UP, ROUND_HALF_UP


def round_volume_ceil(value: float) -> float:
    """
    Округляет объём услуг по правилу "всегда вверх" до 2 знаков после запятой.
    
    Применяется для объёмов услуг (часы, количество) в закрывающих документах.
    
    Примеры:
    - 0.331 → 0.34
    - 0.5555 → 0.56  
    - 1.2345 → 1.24
    
    @param value: объём услуги для округления
    @return: округлённый объём с 2 знаками после запятой
    """
    return math.ceil(value * 100) / 100


def round_money_4_5(value: float) -> float:
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
    
    return float(d_result)
