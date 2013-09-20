# -*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

from datetime import timedelta

from celery import Celery
from celery.schedules import crontab


celery = Celery('weather', broker='beanstalk://localhost:11300')

celery.conf.update(
    CELERY_TIMEZONE = 'Asia/Shanghai',
    CELERY_IMPORTS = ('weather.monitor.periodic', ),
    CELERY_IGNORE_RESULT = True,
    CELERYD_MAX_TASKS_PER_CHILD = 100,
    CELERYBEAT_SCHEDULE = {
        'boardcast-010-am': {
            'task': 'weather.monitor.periodic.boardcast',
            'schedule': crontab(hour=8, minute=0, day_of_week=[1,2,3,4,5]),
            'args': ('Z9010', '北京地区当前气象状况 - 基本反射率（降水）'),
        },
        'boardcast-010-pm': {
            'task': 'weather.monitor.periodic.boardcast',
            'schedule': crontab(hour=18, minute=0, day_of_week=[1,2,3,4,5]),
            'args': ('Z9010', '北京地区当前气象状况 - 基本反射率（降水）'),
        },
        'boardcast-200-am': {
            'task': 'weather.monitor.periodic.boardcast',
            'schedule': crontab(hour=7, minute=30, day_of_week=[1,2,3,4,5]),
            'args': ('Z9200', '广州地区当前气象状况 - 基本反射率（降水）'),
        },
        'boardcast-200-pm': {
            'task': 'weather.monitor.periodic.boardcast',
            'schedule': crontab(hour=17, minute=30, day_of_week=[1,2,3,4,5]),
            'args': ('Z9200', '广州地区当前气象状况 - 基本反射率（降水）'),
        },
        'sampling-010': {
            'task': 'weather.monitor.periodic.sampling',
            'schedule': timedelta(minutes=30),
            'args': ('Z9010', '北京地区降雨预警 [下雨][下雨]'),
        },
        'sampling-200': {
            'task': 'weather.monitor.periodic.sampling',
            'schedule': timedelta(minutes=30),
            'args': ('Z9200', '广州地区降雨预警 [下雨][下雨]'),
        },
    },
    ADMINS = (('Codeb Fan', 'codeb2cc@163.com'), ),
    CELERY_SEND_TASK_ERROR_EMAILS = False,
)


if __name__ == '__main__':
    celery.start()

