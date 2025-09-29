from datetime import timedelta


def date_normalize(datetime, offset: int = None):
    """
    Нормализатор даты относительно смещения
    @param datetime: время дата для преобразования
    @param offset: смещение от фронта - если None то + 1 день к дате
    @return: измененная дата и время
    """
    if offset is not None:
        datetime -= timedelta(minutes=offset)
    else:
        datetime += timedelta(hours=12)
    return datetime
