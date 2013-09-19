# -*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

import datetime
import tempfile
import cStringIO
import logging
import traceback

import requests
import Image, ImageDraw, ImageFont

from .celery import celery
from .utils import merge_gif
from .utils import binarize, denoise
from .utils import calculate_centroid, calculate_path, calculate_zone

from .. import conf


logger = celery.log.get_default_logger()


@celery.task(ignore_result=True)
def boardcast(code, message):
    try:
        logger.info('Monitor Start Boardcast: %s' % code, message)
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


@celery.task(ignore_result=True)
def sampling(code, message):
    try:
        logger.info('Monitor Start Sampling: %s' % code)
        _radar_interval = 5
        _radar_defer = 5
        _sample_frame = 8
        _sample_rate = 15
        _sample_level_threshold = 20
        _sample_denoise_level = 2
        _sample_area_threshold = 480 * 480 / 100
        _sample_warn_threshold = 4

        _lock_file = '/tmp/weather.lock'
        _lock_minutes = 60 * 2

        # Check task lock
        try:
            lock_file = open(_lock_file)
            lock_timestamp = int(lock_file.read())
            lock_datetime = datetime.datetime.fromtimestamp(lock_timestamp)

            if datetime.datetime.now() < lock_datetime:
                logger.warn('!! Task is locked until %s' % lock_datetime)
                return False
        except:
            traceback.print_exc()

        dt = datetime.datetime.utcnow()
        dt = dt - datetime.timedelta(minutes=(_radar_interval * _radar_defer))
        dt = dt - datetime.timedelta(minutes=(dt.minute % _radar_interval))

        count = 30
        raw_images = []
        while count > 0:
            try:
                url = '/mocimg/radar/image/%(code)s/QREF/%(date)s/%(code)s.QREF000.%(datetime)s.GIF' % {
                        'code': code,
                        'date': dt.strftime('%Y/%m/%d'),
                        'datetime': dt.strftime('%Y%m%d.%H') + '%02d' % dt.minute + '00',
                    }

                r = requests.get('http://weather.codeb2cc.com/' + url)

                if r.status_code == requests.codes.ok:
                    im = Image.open(cStringIO.StringIO(r.content))
                    raw_images.append(im)
                    if len(raw_images) >= _sample_frame: break
                else:
                    count -= 1

                dt = dt - datetime.timedelta(minutes=_sample_rate)
            except Exception as e:
                logger.error(e)
                traceback.print_exc()
                break

        if len(raw_images) < _sample_frame:
            logger.warn('!! Not enough available radar data')
            return False

        logger.info('  Processing %d sample images' % len(raw_images))

        raw_images.reverse()
        sample_images = [ im.crop((0, 0, 480, 480)).convert('RGB') for im in raw_images ]

        centroids = []
        for im in sample_images:
            mask = binarize(im, _sample_level_threshold)
            mask = denoise(mask, _sample_denoise_level)

            centroid, area, density = calculate_centroid(im, mask)

            if area > _sample_area_threshold:
                centroids.append(centroid)

        logger.info('  Find %d nimbus: %s' % (len(centroids), centroids))

        if len(centroids) < _sample_warn_threshold:
            logger.info('  Good weather!')
            return True

        # Nimbus path and affected zone
        slope, intercep = calculate_path(centroids)
        logger.info('  Nimbus path: Y = %d * X + %d' % (slope, intercep))

        sample_points = []
        mask = binarize(sample_images[-1], _sample_level_threshold)
        sample_pixels = mask.load()
        for y in xrange(mask.size[1]):
            for x in xrange(mask.size[0]):
                if sample_pixels[x, y]:
                    sample_points.append((x, y))

        b_a, b_b = calculate_zone(sample_points, slope, intercep)
        logger.info('  Affected zone: %s, %s' % (b_a, b_b))

        # Affected?
        ref_point = (240, 240)
        ref_intercep = ref_point[0] - slope * ref_point[1]
        if ref_intercep > min(b_a[1], b_b[1]) and ref_intercep < max(b_a[1], b_b[1]):
            logger.info('  Going to rain!')
            # Update weibo
            boardcast.apply_async((code, message))

            # Lock periodic task
            lock_datetime = datetime.datetime.now() + datetime.timedelta(minutes=_lock_minutes)
            f = open(_lock_file, 'w')
            f.write(lock_datetime.strftime('%s'))
            f.close()

        return True
    except Exception as e:
        logger.error(e)
        traceback.print_exc()

