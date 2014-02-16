# -*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

from datetime import timedelta

from celery import Celery


celery = Celery('weather', broker='redis://localhost:6379/2')

celery.conf.update(
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERY_IMPORTS=('weather.monitor.periodic', ),
    CELERY_IGNORE_RESULT=True,
    CELERY_ACCEPT_CONTENT=['pickle', ],
    CELERY_TASK_SERIALIZER='pickle',
    CELERYD_MAX_TASKS_PER_CHILD=100,
    CELERYBEAT_SCHEDULE={
        'sampling-010': {
            'task': 'weather.monitor.periodic.sampling',
            'schedule': timedelta(minutes=20),
            'args': ('Z9010', '北京地区降雨预警 [下雨][下雨]'),
        },
        'sampling-200': {
            'task': 'weather.monitor.periodic.sampling',
            'schedule': timedelta(minutes=20),
            'args': ('Z9200', '广州地区降雨预警 [下雨][下雨]'),
        },
        'sampling-210': {
            'task': 'weather.monitor.periodic.sampling',
            'schedule': timedelta(minutes=20),
            'args': ('Z9210', '上海地区降雨预警 [下雨][下雨]'),
        },
    },
    ADMINS=(('Codeb Fan', 'codeb2cc@163.com'), ),
    CELERY_SEND_TASK_ERROR_EMAILS = False,
)


if __name__ == '__main__':
    celery.start()

