import typing as t

from apscheduler.schedulers.background import BackgroundScheduler

from internal.modules.utils import Singleton


class APScheduler(BackgroundScheduler, Singleton):
    pass


def new_scheduler(scheduler=BackgroundScheduler(timezone='Asia/Shanghai')) -> APScheduler:
    return APScheduler(scheduler=scheduler)


cli: t.Optional[APScheduler] = None
