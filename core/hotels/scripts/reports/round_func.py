from decimal import Decimal, ROUND_UP

def round_volume(value: float) -> float:
    """
    Округляет объём услуги по правилам:
    - Смотрим 3-й знак после запятой
    - Если он > 0, второй знак округляем вверх
    - Отбрасываем все знаки после 3-го
    - Итог: два знака после запятой
    """

    # Преобразуем в Decimal для точного округления
    d = Decimal(str(value))

    # Отбрасываем всё после 3-го знака
    d_truncated = d.quantize(Decimal('0.000'), rounding='ROUND_DOWN')

    # Проверяем 3-й знак после запятой
    third_digit = int(str(d_truncated).split('.')[-1][2]) if '.' in str(d_truncated) and len(
        str(d_truncated).split('.')[-1]) > 2 else 0

    # Если 3-й знак > 0, округляем вверх второй знак
    if third_digit > 0:
        d_result = d_truncated.quantize(Decimal('0.01'), rounding=ROUND_UP)
    else:
        d_result = d_truncated.quantize(Decimal('0.01'), rounding='ROUND_DOWN')

    return float(d_result)


from decimal import Decimal, ROUND_DOWN, ROUND_UP

def round_service_rate(value: float) -> float:
    """
    Правила:
    - Если после запятой > 2 знаков, учитываем только 3-й знак.
    - 3-й знак >= 5 → второй знак округляем вверх.
    - 3-й знак <= 4 → второй знак без изменений.
    - 4-й и последующие знаки игнорируем.
    """

    d = Decimal(str(value))
    # Отрезаем всё после 3-го знака
    d_truncated = d.quantize(Decimal('0.000'), rounding=ROUND_DOWN)

    frac = str(d_truncated).split('.')[-1] if '.' in str(d_truncated) else ''
    third_digit = int(frac[2]) if len(frac) > 2 else 0

    if third_digit >= 5:
        d_result = d_truncated.quantize(Decimal('0.01'), rounding=ROUND_UP)
    else:
        d_result = d_truncated.quantize(Decimal('0.01'), rounding=ROUND_DOWN)

    return float(d_result)



# @pytest.mark.parametrize("input_val, expected", [
#     (12.3456, 12.35),
#     (12.3401, 12.34),
#     (12.3009, 12.30),
#     (5.999,   6.00),
#     (5.991,   6.00),
#     (0.331,   0.34),
#     (0.5555,  0.56),
#     (1.2345,  1.24),
# ])
# def test_round_up(input_val, expected):
#     result = round_volume(input_val)
#     assert result == expected, f"Ожидали {expected}, получили {result}"
#
#
#
# @pytest.mark.parametrize("input_val, expected", [
#     (12.3456, 12.35),   # 3-й знак=5 → округляем вверх
#     (12.3449, 12.34),   # 3-й знак=4 → не округляем
#     (12.3009, 12.30),   # 3-й знак=0 → не округляем
#     (5.999,   6.00),    # 3-й знак=9 → округляем вверх
#     (5.991,   5.99),    # 3-й знак=1 → не округляем
#     (0.331,   0.33),    # 3-й знак=1 → не округляем
#     (0.335,   0.34),    # 3-й знак=5 → округляем вверх
#     (1.2345,  1.23),    # 3-й знак=4 → не округляем
#     (1.2351,  1.24),    # 3-й знак=5 → округляем вверх
# ])
# def test_round_service_rate(input_val, expected):
#     result = round_service_rate(input_val)
#     assert result == expected, f"Ожидали {expected}, получили {result}"