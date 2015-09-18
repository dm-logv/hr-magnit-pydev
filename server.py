#!/bin/env python
# -*- coding: utf-8 -*-

from wsgiref.simple_server import make_server
import logging
import os
import wsgi

log = logging.getLogger('wsgi-test')
log.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(os.path.join(os.path.dirname(__file__), 'wsgi-test.log'))
file_handler.setFormatter(logging.Formatter('%(asctime)s: %(name)s: %(levelname)s: %(message)s'))
log.addHandler(file_handler)
log.info('Started')


httpd = make_server(
    'localhost',
    8080,
    wsgi.application
)

httpd.serve_forever()

