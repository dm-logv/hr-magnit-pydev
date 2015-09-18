#!/bin/env python
# -*- coding: utf-8 -*-

import logging
import mimetypes
import os
import re
import modules.rendering as rendering
import wsgi

log = logging.getLogger('wsgi-test')

ROUTES = {
    'GET': {
        r'^/?$': rendering.render_main,
        r'^/comment/?$': rendering.render_comment,
        r'^/view/?$': rendering.render_view,
        r'^/stat/?$': rendering.render_stat_regions,
        r'^/stat/(\d+)/?$': rendering.render_stat_cities
    },
    'POST': {
        r'^/comment/getCities/(\d+)/?$': rendering.post_cities,
        r'^/comment/addComment/?$': rendering.add_comment,
        r'^/view/removeComment/(\d+)/?$': rendering.remove_comment
    },
    'file': rendering.load_file,
    'service': {
        # Bad request
        400: rendering.render_service,
        # Payment Required
        402: rendering.render_service,
        # Not Found
        404: rendering.render_service
    }
}


def route(environ, status):
    log.info('router.route() is started')
    # Process known methods
    try:
        routes = ROUTES[environ['REQUEST_METHOD']]
        log.debug('Routes: %s' % routes)
    except KeyError:
        status = '400 Bad Request'
        log.warning('Bad request while parsing method: %s' % environ['REQUEST_METHOD'])
        return ROUTES['service'][400]('service', environ, 400), '', status

    # Call rendering method for matched path
    path = environ['PATH_INFO']
    log.info('Requested path: %s' % path)
    for key in routes.keys():
        log.debug('Current key: %s' % key)
        if re.match(key, path) is not None:
            log.debug('Matched key: %s' % key)
            response = routes[key](key, environ, status)

            log.debug('Response: %s' % key)
            return response, 'text/html', status

    # If ROUTES contains no matches, try to return file
    file_path = os.path.normpath(wsgi.config['app']['path'] + '/' + environ['PATH_INFO'])
    file_ = ROUTES['file'](file_path)
    log.debug(file_path)
    if file_ != -1:
        return file_, mimetypes.guess_type(file_path)[0], status

    # If file not found, then :(
    status = '404 Not Found'
    log.debug('Page not found: %s' % status)
    return ROUTES['service'][404]('service', environ, 404), '', status
