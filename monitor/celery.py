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
        'boardcast-morning': {
            'task': 'weather.monitor.periodic.boardcast',
            'schedule': crontab(hour=8, minute=0, day_of_week=[1,2,3,4,5]),
            'args': ('Z9010', '北京当前天气雷达数据'),
        },
        'boardcast-evening': {
            'task': 'weather.monitor.periodic.boardcast',
            'schedule': crontab(hour=18, minute=0, day_of_week=[1,2,3,4,5]),
            'args': ('Z9010', '北京当前天气雷达数据'),
        },
    },
    ADMINS = (('Codeb Fan', 'codeb2cc@163.com'), ),
    CELERY_SEND_TASK_ERROR_EMAILS = False,
)


if __name__ == '__main__':
    celery.start()

