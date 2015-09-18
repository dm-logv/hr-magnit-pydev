#!/bin/env python
# -*- coding: utf-8 -*-


import codecs
import json
import logging
import re
import string
import wsgi
import modules.crud as crud

log = logging.getLogger('wsgi-test')

# Service functions


def load_file(file_path):
    """Load all string of the file"""
    log.debug('load_file(): %s' % file_path)
    file_ = ''
    try:
        file_ = ''.join(codecs.open(file_path, 'r', encoding='utf_8').readlines())
    except IOError, e:
        log.error('Error when loading file: %s' % e)
        file_ = -1
    log.debug('File: %s' % file_)

    return file_


def load_template(template_file):
    """Load a template file to string.Template processing"""
    log.debug('load_template() %s' % template_file)
    template = ''
    try:
        template = string.Template(load_file(template_file))
    except IOError, e:
        log.error('Error when loading template: %s' % e)
    log.debug('Template: %s' % template)

    return template


# Load main template
_main_template = load_template('assets/templates/page.tpl')
log.debug('_main_template: %s' % _main_template)


def render_service(pattern, environ, status):
    """Render when service call occurs"""
    log.debug('render_service()')
    template_filled = _main_template.safe_substitute({
        'base_url': wsgi.config['variables']['base_url'],
        'title': u'%s — %s' % (wsgi.config['app']['name'], wsgi.config['app']['version']),
        'main_header': u'%s: Main Page' % wsgi.config['app']['name'],
        'main_section':
            u'<table>%s</table>' %
            '\n'.join([u'<tr><td>%s</td><td>%s</td></tr>'
                       % (k, v) for k, v in environ.items()])
    })
    log.debug('template_filled: %s' % template_filled)

    return template_filled


# Pages

def render_main(pattern, environ, status):
    log.debug('render_main()')
    template_filled = _main_template.safe_substitute({
        'base_url': wsgi.config['variables']['base_url'],
        'title': u'%s — %s' % (wsgi.config['app']['name'], wsgi.config['app']['version']),
        'main_header': u'%s: Main Page' % wsgi.config['app']['name'],
        'main_section': load_file('assets/templates/snippets/main.snippet')
    })
    log.debug('template_filled: %s' % template_filled)

    return template_filled


def render_comment(pattern, environ, status):
    log.debug('render_comment()')

    chunk = load_template('assets/templates/chunks/select-item.chunk')
    chunks_filled = '\n'.join([
        chunk.safe_substitute({
            'item_id': db_row[0],
            'item_text': db_row[1]
        })
        for db_row in crud.get_regions()
    ])
    log.debug('chunks_filled: %s' % chunks_filled)

    snippet = load_template('assets/templates/snippets/comment.snippet')
    snippet_filled = snippet.safe_substitute({
        'regions_list': chunks_filled
    })
    log.debug('snippet_filled: %s' % snippet_filled)

    template_filled = _main_template.safe_substitute({
        'base_url': wsgi.config['variables']['base_url'],
        'title': u'%s — %s' % (wsgi.config['app']['name'], wsgi.config['app']['version']),
        'main_header': u'%s: Comment adding' % wsgi.config['app']['name'],
        'main_section': snippet_filled
    })
    log.debug('template_filled: %s' % template_filled)

    return template_filled


def render_view(pattern, environ, status):
    log.debug('render_view')
    chunk = load_template('assets/templates/chunks/view-table-row.chunk')
    chunks_filled = '\n'.join([
        chunk.safe_substitute(
            dict([(key, db_row[key]) for key in db_row.keys()])
        )
        for db_row in crud.get_comments()
    ])
    log.debug('chunks_filled: %s' % chunks_filled)

    snippet = load_template('assets/templates/snippets/view.snippet')
    snippet_filled = snippet.safe_substitute({
        'view_table_row': chunks_filled
    })
    log.debug('snippet_filled: %s' % snippet_filled)

    template_filled = _main_template.safe_substitute({
        'base_url': wsgi.config['variables']['base_url'],
        'title': u'%s — %s' % (wsgi.config['app']['name'], wsgi.config['app']['version']),
        'main_header': u'%s: View comments' % wsgi.config['app']['name'],
        'main_section': snippet_filled
    })
    log.debug('template_filled: %s' % template_filled)

    return template_filled


def render_stat_regions(pattern, environ, status):
    log.debug('render_stat')
    chunk = load_template('assets/templates/chunks/stat-region-table-row.chunk')

    chunks_filled_max = '\n'.join([
        chunk.safe_substitute({
            'object_id': db_row['region_id'],
            'object_name': db_row['region_name'],
            'object_count': db_row['count']
        })
        for db_row in crud.get_stat_regions_max()
    ])
    log.debug('chunks_filled: %s' % chunks_filled_max)

    chunks_filled = '\n'.join([
        chunk.safe_substitute({
            'object_id': db_row['region_id'],
            'object_name': db_row['region_name'],
            'object_count': db_row['count']
        })
        for db_row in crud.get_stat_regions()
    ])
    log.debug('chunks_filled: %s' % chunks_filled)

    snippet = load_template('assets/templates/snippets/stat-region.snippet')
    snippet_filled = snippet.safe_substitute({
        'stat_table_row_max': chunks_filled_max,
        'stat_table_row': chunks_filled
    })
    log.debug('snippet_filled: %s' % snippet_filled)

    template_filled = _main_template.safe_substitute({
        'base_url': wsgi.config['variables']['base_url'],
        'title': u'%s — %s' % (wsgi.config['app']['name'], wsgi.config['app']['version']),
        'main_header': u'%s: View comments' % wsgi.config['app']['name'],
        'main_section': snippet_filled
    })
    log.debug('template_filled: %s' % template_filled)

    return template_filled


def render_stat_cities(pattern, environ, status):
    region_id = int(re.match(pattern, environ['PATH_INFO']).group(1))
    log.debug('render_stat')
    chunk = load_template('assets/templates/chunks/stat-city-table-row.chunk')

    chunks_filled = '\n'.join([
        chunk.safe_substitute({
            'object_id': db_row['city_id'],
            'object_name': db_row['city_name'],
            'object_count': db_row['count']
        })
        for db_row in crud.get_stat_cities((region_id,))
    ])
    log.debug('chunks_filled: %s' % chunks_filled)

    snippet = load_template('assets/templates/snippets/stat-city.snippet')
    snippet_filled = snippet.safe_substitute({
        'stat_table_row': chunks_filled
    })
    log.debug('snippet_filled: %s' % snippet_filled)

    template_filled = _main_template.safe_substitute({
        'base_url': wsgi.config['variables']['base_url'],
        'title': u'%s — %s' % (wsgi.config['app']['name'], wsgi.config['app']['version']),
        'main_header': u'%s: View comments' % wsgi.config['app']['name'],
        'main_section': snippet_filled
    })
    log.debug('template_filled: %s' % template_filled)

    return template_filled


# POST Section


def post_cities(pattern, environ, status):
    region_id = int(re.match(pattern, environ['PATH_INFO']).group(1))
    chunk = load_template('assets/templates/chunks/select-item.chunk')
    chunks_filled = '\n'.join([
        chunk.safe_substitute({
            'item_id': db_row[0],
            'item_text': db_row[2]
        })
        for db_row in crud.get_cities((region_id,))
    ])
    log.debug(chunks_filled)
    return chunks_filled


def add_comment(pattern, environ, status):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        request_body_size = 0

    request_body = environ['wsgi.input'].read(request_body_size)
    data = json.loads(request_body)

    try:
        crud.put_comment((
            data['last-name'],
            data['first-name'],
            data['patronymic'],
            data['region'],
            data['city'],
            data['phone'],
            data['email'],
            data['comment']
        ))
    except Exception, e:
        log.error('Exception when comment adding: {0!r}'.format(e))
        return json.dumps({
            'type': 'fail',
            'text': '{0!r}'.format(e)
        })

    return json.dumps({
        'type': 'success',
        'text': 'Comment added successfully'
    })


def remove_comment(pattern, environ, status):
    comment_id = int(re.match(pattern, environ['PATH_INFO']).group(1))
    return crud.remove_comment((comment_id,))