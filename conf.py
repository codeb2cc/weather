# -*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

import os

WEIBO_KEY = '2250230588'
WEIBO_SECRET = os.environ['WEIBO_SECRET']

# 未审核应用绑定开发者帐号Token有效期为五年, 无需动态更新
WEIBO_UID = '1652592967'
WEIBO_TOKEN = os.environ['WEIBO_TOKEN']

OAUTH2_URL = 'http://localhost.com/oauth2'

MEMCACHED = ['127.0.0.1:11211', ]
MEMCACHED_PREFIX = '#W#'
