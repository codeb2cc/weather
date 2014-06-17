#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

import sys
import traceback
import SimpleHTTPServer
import SocketServer

PORT = 8000
PATH = '.'


class DocumantRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/console.html'

        self.path = PATH + self.path.split('?', 1)[0]
        if not self.path.endswith(('.html', '.js', '.css', 'jpeg', 'gif', )):
            self.send_error(404, "Not Found")
        else:
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def list_directory(self, path):
        self.send_error(404, "Not Found")
        return None


if __name__ == '__main__':
    httpd = SocketServer.TCPServer(("", PORT), DocumantRequestHandler)
    try:
        sys.stdout.write('Experiment Console on {0:d} ...\n'.format(PORT))
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    except Exception:
        traceback.print_exc()
    finally:
        httpd.shutdown()

