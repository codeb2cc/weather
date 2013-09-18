# -*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

import datetime
import tempfile
import cStringIO
import traceback

import requests
import Image, ImageDraw, ImageFont

from .celery import celery
from .utils import merge_gif

from .. import conf


logger = celery.log.get_default_logger()


@celery.task(ignore_result=True)
def boardcast(code, message):
    try:
        logger.info('Monitor Start Boardcast: %s - %s' % (code, message))
        _radar_frame = 10
        _radar_interval = 5     # 雷达数据采样频率
        _radar_defer = 5        # 监测数据有延迟

        t_now = datetime.datetime.now()
        t_utcnow = datetime.datetime.utcnow()

        logger.info('  Construct radar images urls')
        radar_urls = []
        for i in xrange(_radar_frame + _radar_defer):
            if i < _radar_defer: continue
            t = t_utcnow - datetime.timedelta(minutes=(_radar_interval * (i + 1)))
            r = 'mocimg/radar/image/%(code)s/QREF/%(date)s/%(code)s.QREF000.%(datetime)s.GIF' % {
                    'code': code,
                    'date': t.strftime('%Y/%m/%d'),
                    'datetime': t.strftime('%Y%m%d.%H') + '%02d' % (t.minute - t.minute % _radar_interval) + '00',
                }
            radar_urls.append(r)
        radar_urls.reverse()

        logger.info('  Fetch radar images')
        radar_images = []
        for url in radar_urls:
            try:
                r = requests.get('http://weather.codeb2cc.com/' + url)

                if not r.status_code == requests.codes.ok:
                    continue

                image = Image.open(cStringIO.StringIO(r.content))
                radar_images.append(image)
            except Exception as e:
                logger.error(e)
                traceback.print_exc()
                continue

        if not radar_images:
            logger.warn('!! No radar image found.')
            return

        logger.info('  Generate radar GIF')
        radar_cropped = []
        for image in radar_images:
            # 新浪微博GIF图片大小限制为450x450, 超出限制的图片将不能播放
            im = image.crop((20, 20, 460, 460))
            radar_cropped.append(im)

        temp_file = tempfile.TemporaryFile()
        merge_gif(temp_file, radar_cropped, 100)
        temp_file.seek(0)

        logger.info('  Update weibo status')
        _api = 'https://upload.api.weibo.com/2/statuses/upload.json'
        _param = {
            'access_token': conf.WEIBO_TOKEN,
            'status': '%s - %s http://weather.codeb2cc.com/' % (t_now.strftime('%Y/%m/%d %H:%M'), message),
        }
        _file = { 'pic': temp_file }

        r = requests.post(_api, data=_param, files=_file)
        r = r.json()
        if r.get('error_code'):
            logger.warn('!! Update weibo failed: %s' % r)
    except Exception as e:
        logger.error(e)
        traceback.print_exc()

