from datetime import timedelta
from ..scripts import bill_ver_create

def createPaymentForCustomer(tasks):
    total_rub = 0

    for task in tasks:
        total_sec = 0.0
        for executerState in task.executers.all():
            if executerState.status != 'STOP':
                raise ValueError(f"В заявке {task.id} у {task.manager.hotel} исполнитель #{executerState.executer.id} "
                                 f"{executerState.executer.middle_name} {executerState.executer.first_name} "
                                 f"{executerState.executer.second_name} не закончил работать!")
            start_time = executerState.start_at if executerState.start_at is not None else task.start_at
            end_time = executerState.stop_at if executerState.stop_at is not None else \
                (task.start_at + timedelta(hours=task.duration))
            total_sec += (total_sec - end_time).total_seconds()
        total_rub += task.rent * (total_sec/3600.0)


