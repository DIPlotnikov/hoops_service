import logging
from datetime import datetime


logging.basicConfig(filename=f"/logs/{datetime.now().timestamp()}_midd_log.log", level=logging.DEBUG)


def do_log(root, token, pk, role, cookies, files, post, meta, body, values, parent, path, type, root_type, var_values):
    try:

        logging.info(
            f"\rTIME:{datetime.now()}"
            f"\rtoken:{token}"
            f"\r\tid:{pk}"
            f"\r\trole:{role}"
            f"\r\tCOOKIES:{cookies}"
            f"\r\tFILES:{files}"
            f"\r\tPOST:{post}"
            f"\r\tMETA:{meta}"
            f"\r\tinfo:{body}"
            f"\r\tvariable_values:{values}"
            f"\r\tparent_type:{parent}"
            f"\r\tpath:{path}"
            f"\r\treturn_type:{type}"
            f"\r\troot_value:{root_type}"
            f"\r\tvariable_values:{var_values}"
            f"\r\troot:{root}"
        )

    except Exception as e:
        print(e)


class LogAllRequests(object):
    def resolve(self, next, root, info, **args):
        return next(root, info, **args)
