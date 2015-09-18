#!/bin/env python
# -*- coding: utf-8 -*-

import os


config = {
    'app': {
        'name': 'magnit.python-dev.test',
        'path': os.path.dirname(__file__),
        'version': '0.8.2'
    },
    'db': {
        'type': 'sqlite3',
        'uri': 'db/db.sqlite'
    },
    'logging': {
        'file': os.path.join(os.path.dirname(__file__), 'wsgi.log')
    },
    'variables': {
        'base_url': 'http://localhost:8080/'
    }
}