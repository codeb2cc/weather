# -*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

import math
import logging
import traceback

from scipy import stats
from PIL import Image, ImageDraw, ImageFilter


logger = logging.getLogger('weather.monitor')
logger.addHandler(logging.StreamHandler())


LEVEL_COLORS = {
    (173, 144, 240) : 75,
    (120, 0, 132)   : 70,
    (255, 0, 240)   : 65,
    (192, 0, 0)     : 60,
    (214, 0, 0)     : 55,
    (255, 0, 0)     : 50,
    (255, 144, 0)   : 45,
    (231, 192, 0)   : 40,
    (255, 255, 0)   : 35,
    (1, 144, 0)     : 30,
    (0, 200, 0)     : 25,
    (1, 255, 0)     : 20,
    (0, 236, 236)   : 15,
    (1, 160, 246)   : 10,
    (0, 0, 246)     : 5,
}


def o16(i):
    return chr(i&255) + chr(i>>8&255)


def merge_gif(fp, images, durations, loops=0):
    _im = images[0]
    _durations = [durations for im in images] if isinstance(durations, int) else durations

    _bits = 8
    _size = _im.size
    try:
        assert len(_durations) == len(images)
        for im in images:
            im.load()
            assert _size == im.size
    except AssertionError:
        raise

    # Header
    _h = [
        'GIF89a',
        o16(_size[0]),              # width
        o16(_size[1]),              # height
        chr(128 + (_bits - 1)),     # flags: palette + bits
        chr(0),                     # background
        chr(0),                     # reserved/aspect
    ]
    fp.write(''.join(_h))

    # Palette
    _mode = 'P'     # palette/grayscale (P/L)
    _colors = 256
    _palette = _im.im.getpalette('RGB')[:_colors * 3]
    fp.write(_palette)

    # Ext: application extension
    _loop = loops
    _ext = [
        '\x21\xFF\x0B',
        'NETSCAPE2.0',
        '\x03\x01',
        o16(_loop),
        '\x00',
    ]
    fp.write(''.join(_ext))

    # Images
    for idx, im in enumerate(images):
        # Ext: graphics control extension
        _cext = [
            '\x21\xF9\x04',
            '\x08',                 # flag: transparency: \x08 | \x09
            o16(_durations[idx]),   # druation
            '\x00',                 # transparency
            '\x00',
        ]
        fp.write(''.join(_cext))

        # Image
        _h = [
            '\x2C',                             # ',' sperator
            o16(0), o16(0),                     # offset
            o16(im.size[0]), o16(im.size[1]),   # size
            chr(0),                             # flag: no local palette
            chr(_bits),                         # color bits
        ]
        fp.write(''.join(_h))

        _encoder = Image._getencoder(im.mode, "gif", im.mode)
        _encoder.setimage(im.im, (0, 0) + im.size)
        _bufsize = 4096
        while True:
            l, s, d = _encoder.encode(_bufsize)
            fp.write(d)
            if s: break
        if s < 0:
            raise IOError("encoder error %d when writing image file" % s)
        fp.write('\x00')

    # End
    fp.write('\x3b')    # ';' trailer
    fp.flush()


def binarize(image, threshold=0):
    bi_image = Image.new('1', image.size)

    im_pixels = image.load()
    bi_pixels = bi_image.load()

    for y in xrange(image.size[1]):
        for x in xrange(image.size[0]):
            bi_pixels[x, y] = 1 if LEVEL_COLORS.get(im_pixels[x, y], -1) > threshold else 0

    return bi_image


def denoise(image, level=2):
    for i in xrange(level):
        image = image.filter(ImageFilter.MinFilter(size=3))
        image = image.filter(ImageFilter.MinFilter(size=3))

    return image


def calculate_centroid(image, mask):
    assert image.size == mask.size

    im_pixels = image.load()
    mask_pixels = mask.load()

    e_l, e_p = 5, 10

    accumulator = [0, 1, 0, 1]      # 1 for safe division
    counter = [1, 0]
    for y in xrange(image.size[1]):
        for x in xrange(image.size[0]):
            if not mask_pixels[x, y]: continue

            w = LEVEL_COLORS.get(im_pixels[x, y], 0)
            if w:
                e = pow(w // e_l, e_p)
                accumulator[0] += x * e
                accumulator[1] += e
                accumulator[2] += y * e
                accumulator[3] += e

                counter[0] += 1
                counter[1] += w

    centroid = (accumulator[0] // accumulator[1], accumulator[2] // accumulator[3])
    area = counter[0]
    density = counter[1] // area

    logger.debug('Centroid: (%d, %d) %d %d' % (centroid[0], centroid[1], area, density))

    return centroid, area, density


def calculate_path(points):
    assert len(points) >= 2

    xi = [ p[0] for p in points ]
    yi = [ p[1] for p in points ]
    slope, intercep, r_value, p_value, std_err = stats.linregress(xi, yi)

    logger.debug('Path: Y = %fX + %f' % (slope, intercep))
    logger.debug('Linear Regress Info: %f, %f, %f' % (r_value, p_value, std_err))

    return slope, intercep


def calculate_zone(points, slope, intercep):
    def signed_dist(point):
        return (slope * point[0] - point[1] + intercep) / math.sqrt(slope * slope + 1)

    # Boundry points
    bp_a = ((0, 0), 0)
    bp_b = ((0, 0), 0)

    for point in points:
        d = signed_dist(point)
        if d > 0 and d >= bp_a[1]:
            bp_a = (point, d)
        elif d <= 0 and d <= bp_b[1]:
            bp_b = (point, d)

    logger.debug('Boundry Points: A(%d, %d) B(%d, %d)' % (
            bp_a[0][0], bp_a[0][1], bp_b[0][0], bp_b[0][1]))

    # Boundry lines
    line_a = (slope, bp_a[0][1] - slope * bp_a[0][0])
    line_b = (slope, bp_b[0][1] - slope * bp_b[0][0])

    logger.debug('Boundry Lines: \nA: Y = %fX + %f\nB: Y = %fX + %f' % (
            line_a[0], line_a[1], line_b[0], line_b[1]))

    return line_a, line_b


def debug_mode():
    logger.setLevel(logging.DEBUG)

