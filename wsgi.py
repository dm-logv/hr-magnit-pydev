#!/bin/env python
# -*- coding: utf-8 -*-

__version__ = '0.1.1'

import logging
import os
import modules.router as router
from modules.config import config as config

# Service answer
answer = None

# app path
config['app']['path'] = os.path.dirname(__file__)

log = logging.getLogger('wsgi-test')


def application(environ, callback):
    log.info('WSGI Application started')
    log.debug('Environ: %s' % environ)

    status = '200 OK'
    request_method = environ['REQUEST_METHOD']
    response_headers = []

    response_body, mimetype, status = router.route(environ, status)

    response_headers.append(('Content-Length', str(len(response_body.encode('utf-8')))))
    response_headers.append(('Content-Type', mimetype))

    log.debug('Response headers: %s' % response_headers)
    log.debug('Response status: %s' % status)
    log.debug('Response body: %s' % response_body)

    callback(status, response_headers)

    return [response_body.encode('utf-8')]

