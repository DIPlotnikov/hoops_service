def calc_tax(price, nds):
    """
    Расчет НДС в стоимости
    @param price: Стоимость
    @param nds: Ставка НДС
    @return: Сколько НДС заложено в стоимость
    """
    if nds is None:
        return None
    return round(price / (100 + nds) * nds, 2)


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
