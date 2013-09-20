# -*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

from functools import wraps

import pylibmc

from . import conf


def prefixed(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if len(args):
            args = (self.prefix + args[0], ) + args[1:]
        if 'key' in kwargs:
            kwargs['key'] = self.prefix + self.prefix
        return func(self, *args, **kwargs)
    return wrapper


class MCClient(pylibmc.Client):
    def __init__(self, servers, prefix='', **kwargs):
        self.prefix = prefix
        super(MCClient, self).__init__(servers, **kwargs)

    @prefixed
    def get(self, *args, **kwargs):
        return super(MCClient, self).get(*args, **kwargs)

    def get_multi(self, *args, **kwargs):
        kwargs['key_prefix'] = self.prefix
        return super(MCClient, self).get_multi(*args, **kwargs)

    @prefixed
    def set(self, *args, **kwargs):
        return super(MCClient, self).set(*args, **kwargs)

    def set_multi(self, *args, **kwargs):
        kwargs['key_prefix'] = self.prefix
        return super(MCClient, self).set_multi(*args, **kwargs)

    @prefixed
    def add(self, *args, **kwargs):
        return super(MCClient, self).add(*args, **kwargs)

    @prefixed
    def replace(self, *args, **kwargs):
        return super(MCClient, self).replace(*args, **kwargs)

    @prefixed
    def prepend(self, *args, **kwargs):
        return super(MCClient, self).prepend(*args, **kwargs)

    @prefixed
    def incr(self, *args, **kwargs):
        return super(MCClient, self).incr(*args, **kwargs)

    @prefixed
    def decr(self, *args, **kwargs):
        return super(MCClient, self).decr(*args, **kwargs)

    @prefixed
    def delete(self, *args, **kwargs):
        return super(MCClient, self).delete(*args, **kwargs)

    @prefixed
    def delete_multi(self, *args, **kwargs):
        kwargs['key_prefix'] = self.prefix
        return super(MCClient, self).delete_multi(*args, **kwargs)


memcache = MCClient(conf.MEMCACHED, prefix=conf.MEMCACHED_PREFIX)

