from __future__ import absolute_import, division, print_function, with_statement

import Image


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


