# -*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

import math
import time
import datetime
import subprocess
import traceback

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy import stats


COLOR_MAP = {
    (173, 144, 240): 75,
    (120, 0, 132): 70,
    (255, 0, 240): 65,
    (192, 0, 0): 60,
    (214, 0, 0): 55,
    (255, 0, 0): 50,
    (255, 144, 0): 45,
    (231, 192, 0): 40,
    (255, 255, 0): 35,
    (1, 144, 0): 30,
    (0, 200, 0): 25,
    (1, 255, 0): 20,
    (0, 236, 236): 15,
    (1, 160, 246): 10,
    (0, 0, 246): 5,
}


def binarize(image, thread=0):
    bi_image = Image.new('1', image.size)

    _width, _height = image.size
    _im_pixels = image.load()
    _bi_pixels = bi_image.load()

    for y in xrange(_height):
        for x in xrange(_width):
            _bi_pixels[x, y] = 1 if COLOR_MAP.get(_im_pixels[x, y], -1) > thread else 0

    # Blur
    bi_image = bi_image.filter(ImageFilter.MinFilter(size=3))

    return bi_image


def extract(image, mask):
    assert image.size == mask.size

    image = image.copy()

    _width, _height = image.size
    _fill = (255, 255, 255)
    _im_pixels = image.load()
    _mask_pixels = mask.load()

    for y in xrange(_height):
        for x in xrange(_width):
            if not _mask_pixels[x, y]:
                _im_pixels[x, y] = _fill

    return image


def calculate_centroid(image, factor):
    image = image.copy()

    _width, _height = image.size
    _pixels = image.load()

    _P = [0, 0, 0, 0]

    pixel_count = 0
    weight_count = 0
    for y in xrange(_height):
        for x in xrange(_width):
            l = 5
            w = COLOR_MAP.get(_pixels[x, y], 0)
            if w:
                e = pow(w // l, factor)
                _P[0] += x * e
                _P[1] += e
                _P[2] += y * e
                _P[3] += e

                pixel_count += 1
                weight_count += w

    center = (_P[0] // _P[1], _P[2] // _P[3])

    color = (255, 0, 0)
    font = ImageFont.truetype('font.ttf', 22)
    draw = ImageDraw.Draw(image)
    size = 10
    offset = 10

    draw.line((center[0] - size, center[1], center[0] + size, center[1]), fill=color, width=3)
    draw.line((center[0], center[1] - size, center[0], center[1] + size), fill=color, width=3)
    draw.text((10, 10), 'PC: %d' % pixel_count, fill=color, font=font)
    draw.text((10, 32), 'WC: %d' % weight_count, fill=color, font=font)
    draw.text((10, 54), 'E:  %d' % (weight_count // pixel_count), fill=color, font=font)
    draw.text((center[0] + offset, center[1] + offset), '%s, %s' % center, fill=color, font=font)

    del draw

    return image, center, pixel_count, weight_count


def regress(images, data, size_thread=0, level_thread=20):
    if not size_thread:
        size_thread = images[0].size[0] * images[0].size[1] // 100

    _xi, _yi = [], []
    for point, pixels, weight in data:
        print(pixels, size_thread, weight / pixels, level_thread)
        if pixels < size_thread:
            continue
        if weight / pixels < level_thread:
            continue
        _xi.append(point[0])
        _yi.append(point[1])

    if len(_xi) < 2:
        raise Exception('Not enough valid data!')

    slope, intercep, r_value, p_value, std_err = stats.linregress(_xi, _yi)

    color_red = (255, 0, 0)
    color_purple = (255, 0, 255)
    font = ImageFont.truetype('font.ttf', 22)

    for idx, image in enumerate(images):
        path_image = image.copy()
        path_draw = ImageDraw.Draw(path_image)

        path_draw.text((10, 10), 'P: %d' % len(_xi), fill=color_red, font=font)
        path_draw.text((10, 32), 'S: %.2f' % slope, fill=color_red, font=font)
        path_draw.text((10, 54), 'I: %.2f' % intercep, fill=color_red, font=font)

        # Direction
        _direction = '%s%s' % (
                'E' if _xi[0] < _xi[-1] else 'W',
                'S' if _yi[0] < _yi[-1] else 'N',
            )
        path_draw.text((10, 76), 'D: %s' % _direction, fill=color_red, font=font)

        # Path line
        point_a = (0, int(slope * 0 + intercep))
        point_b = (image.size[0], int(slope * image.size[0] + intercep))
        path_draw.line(point_a + point_b, fill=color_purple, width=3)

        # Cross marks
        for i, x in enumerate(_xi):
            y = _yi[i]
            path_draw.line((x - 10, y, x + 10, y), fill=color_red, width=2)
            path_draw.line((x, y - 10, x, y + 10), fill=color_red, width=2)

        del path_draw
        path_image.save('out/path-%d.jpeg' % idx)

    return slope, intercep


def calculate_area(images, slope, intercep, thread=0):
    color_red = (255, 0, 0)
    color_purple = (255, 0, 255)
    font = ImageFont.truetype('font.ttf', 22)

    def _dist(point):
        return (slope * point[0] - point[1] + intercep) / math.sqrt(slope * slope + 1)

    for idx, image in enumerate(images):
        _width, _height = image.size

        mask_image = binarize(image, thread)

        # Further filter
        mask_image = mask_image.filter(ImageFilter.MinFilter(size=5))

        mask_pixels = mask_image.load()

        # Boundry point
        bp_a = (0, 0, 0)
        bp_b = (0, 0, 0)

        for y in xrange(_height):
            for x in xrange(_width):
                if mask_pixels[x, y]:
                    d = _dist((x, y))
                    if d > 0 and d > bp_a[2]:
                        bp_a = (x, y, d)
                    elif d < 0 and d < bp_b[2]:
                        bp_b = (x, y, d)

        # Boundry interception
        bi_a = bp_a[1] - slope * bp_a[0]
        bi_b = bp_b[1] - slope * bp_b[0]

        # Boundry line
        bl_a = (0, int(bi_a), _width, int(slope * _width + bi_a))
        bl_b = (0, int(bi_b), _width, int(slope * _width + bi_b))

        # Visualize
        area_image = image.copy()
        area_draw = ImageDraw.Draw(area_image)

        area_draw.line(bl_a, fill=color_purple, width=3)
        area_draw.line(bl_b, fill=color_purple, width=3)

        area_draw.line((bp_a[0] - 10, bp_a[1], bp_a[0] + 10, bp_a[1]), fill=color_red, width=2)
        area_draw.line((bp_a[0], bp_a[1] - 10, bp_a[0], bp_a[1] + 10), fill=color_red, width=2)
        area_draw.text((bp_a[0] + 10, bp_a[1] + 10), '%s, %s' % bp_a[:2], fill=color_red, font=font)

        area_draw.line((bp_b[0] - 10, bp_b[1], bp_b[0] + 10, bp_b[1]), fill=color_red, width=2)
        area_draw.line((bp_b[0], bp_b[1] - 10, bp_b[0], bp_b[1] + 10), fill=color_red, width=2)
        area_draw.text((bp_b[0] + 10, bp_b[1] + 10), '%s, %s' % bp_b[:2], fill=color_red, font=font)

        del area_draw
        area_image.save('out/area-%d.jpeg' % idx)

    return bi_a, bi_b


def process(factor=1, thread=0):
    sample_images = []
    for i in xrange(9):
        sample = Image.open('samples/origin-%d.gif' % i)
        sample_images.append(sample.crop((0, 0, 480, 480)).convert('RGB'))

    bi_images = []
    for idx, im in enumerate(sample_images):
        bi_image = binarize(im, thread)
        bi_image.save('out/bi-%d.jpeg' % idx)
        bi_images.append(bi_image)

    extract_images = []
    extract_data = []
    for idx, im in enumerate(sample_images):
        extract_image = extract(im, bi_images[idx])
        extract_image, center, pixels, weight = calculate_centroid(extract_image, factor)
        extract_image.save('out/extract-%d.jpeg' % idx)

        extract_images.append(extract_image)
        extract_data.append((center, pixels, weight))

        print(center, pixels, weight)

    slope, intercep = regress(sample_images, extract_data)
    print(slope, intercep)

    intercep_a, intercep_b = calculate_area(sample_images, slope, intercep, thread)
    print(slope, intercep_a)
    print(slope, intercep_b)


def fetch(code='Z9010', dt=None, rate=15):
    _interval = 5
    _rate = rate
    _num = 9

    if not dt:
        dt = datetime.datetime.utcnow() - datetime.timedelta(minutes=20)
    else:
        dt = dt + datetime.timedelta(seconds=time.timezone)

    _count = 0
    while True:
        _host = 'http://weather.codeb2cc.com'
        _path = '/mocimg/radar/image/%(code)s/QREF/%(date)s/%(code)s.QREF000.%(datetime)s.GIF' % {
                'code': code,
                'date': dt.strftime('%Y/%m/%d'),
                'datetime': dt.strftime('%Y%m%d.%H') + '%02d' % (dt.minute - dt.minute % _interval) + '00',
            }
        _dest = 'samples/origin-%d.gif' % (_num - _count - 1)

        try:
            subprocess.check_call(['wget', _host + _path, '-O', _dest])
            dt = dt - datetime.timedelta(minutes=(_rate))

            _count += 1
            if _count >= _num: break
        except subprocess.CalledProcessError:
            # 404?
            dt = dt - datetime.timedelta(minutes=(_interval))
        except KeyboardInterrupt:
            break

