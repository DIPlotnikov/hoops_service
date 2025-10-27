from hotels.utils.invoice import round_money_4_5


def calc_tax(price, nds):
    """
    Расчет НДС в стоимости
    @param price: Стоимость
    @param nds: Ставка НДС
    @return: Сколько НДС заложено в стоимость
    """
    if nds is None:
        return None
    return round_money_4_5(price / (100 + nds) * nds)


def calc_cost_without_tax(price, nds):
    """
    Расчет стоимости без НДС
    @param price: Стоимость
    @param nds: Ставка НДС
    @return: Стоимость без НДС
    """
    if nds is None:
        return None
    return round(price / (100 + nds) * 100, 2)
