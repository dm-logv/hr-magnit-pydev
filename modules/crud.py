#!/bin/env python
# -*- coding: utf-8 -*-

import logging
import json
import wsgi

log = logging.getLogger('wsgi-test')


def get_connection():
    """Returns DB connection of followed type by URI"""
    db_type = wsgi.config['db']['type']
    db_uri = wsgi.config['db']['uri']
    log.info('Try to get DB connection: {0!r}: {1!r}'.format(db_type, db_uri))

    # Import DB module
    try:
        db_module = __import__(db_type)
    except ImportError, e:
        log.error('DB module import error: {0!r}'.format(e))
        return None
    else:
        log.debug('DB module imported')

    # Create connection
    try:
        db_conn = db_module.connect(db_uri)
    except db_module.Error, e:
        log.error('DB connection error: {0!r}'.format(e))
    else:
        log.debug('DB connection established')

    # Try to set row_factory = row
    try:
        db_conn.row_factory = db_module.Row
    except AttributeError, e:
        log.warning('Row factory set error: {0!r}'.format(e))

    return db_conn


def put_query(query, parameters=()):
    """Execute a query to put data into DB and returns additional information"""
    db_conn = get_connection()
    cursor = db_conn.cursor()

    try:
        cursor.execute(query, parameters)
    except (db_conn.OperationalError, db_conn.ProgrammingError), e:
        log.error('Error when data put: {0!r}. Rollback'.format(e))
        db_conn.rollback()
        return json.dumps({
            'type': 'fail',
            'text': 'Error when put/removing data: {0!r}'.format(e)
        })
    else:
        log.debug('Data put/removing successfully done')
        db_conn.commit()
    finally:
        db_conn.close()

    return json.dumps({
        'type': 'success',
        'text': 'Data put/removing successfully done'
    })


def get_query(query, parameters=()):
    """Returns query result set and/or additional information"""
    db_conn = get_connection()
    cursor = db_conn.cursor()
    result = []

    try:
        cursor.execute(query, parameters)
    except (db_conn.OperationalError, db_conn.ProgrammingError), e:
        log.error('Error when getting data: {0!r}'.format(e))
        db_conn.close()
        return []
    else:
        log.debug('Data got successfully')

    try:
        result = cursor.fetchall()
    except db_conn.Error, e:
        log.error('Error when rows fetching: {0!r}'.format(e))
    else:
        log.debug('Rows fetched successfully')
    finally:
        db_conn.close()

    return result


def get_comments():
    """Returns set of comments"""
    query = """
        SELECT
            comment_id  ,
            last_name   ,
            first_name  ,
            patronymic  ,
            region_name ,
            city_name   ,
            phone       ,
            email       ,
            comment
        FROM
            Comments
        LEFT JOIN Regions ON Regions.region_id = Comments.region_id
        LEFT JOIN Cities  ON Cities.city_id = Comments.city_id
    """
    log.debug('get_comments(): "{0!r}"'.format(query))
    return get_query(query)


def put_comment(comment):
    """Insert comment record into DB"""

    query = """
        INSERT INTO Comments(
            last_name  ,
            first_name ,
            patronymic ,
            region_id  ,
            city_id    ,
            phone      ,
            email      ,
            comment
        )
        VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?
        )
    """
    log.debug('put_query(): "{0!r}" % {1!r}'.format(query, comment))
    return put_query(query, comment)


def remove_comment(comment_id):
    """Delete comments with followed id's"""

    query = """
        DELETE FROM Comments
        WHERE comment_id = ?
    """
    log.debug('delete_comment(): "{0!r}" % {1!r}'.format(query, comment_id))
    return put_query(query, comment_id)


def get_regions():
    """ Returns list of regions"""
    query = """
        SELECT
            region_id   ,
            region_name
        FROM
            Regions
    """
    log.debug('get_regions(): "{0!r}"'.format(query))
    return get_query(query)


def get_cities(region):
    """Returns list of cities"""

    query = """
        SELECT
            city_id    ,
            region_id  ,
            city_name
        FROM
            Cities
        WHERE region_id = ?
    """
    log.debug('get_cities(): "{0!r}" % {1!r}'.format(query, region))
    return get_query(query, region)


def get_stat_regions():
    """Returns count of comments for each region"""
    query = """
        SELECT
            Regions.region_id           AS region_id,
            Regions.region_name         AS region_name,
            COUNT(Comments.comment_id)  AS count
        FROM
            Comments
        JOIN
            Regions
            ON Comments.region_id = Regions.region_id
        GROUP BY
            Regions.region_id,
            Regions.region_name
    """
    log.debug('get_stat_regions(): "{0!r}"'.format(query))
    return get_query(query)


def get_stat_regions_max():
    """Return count of comments for each region where count > 5"""
    query = """
        SELECT
            Regions.region_id          AS region_id,
            Regions.region_name        AS region_name,
            COUNT(Comments.comment_id) AS count
        FROM
            Comments
        JOIN
            Regions
            ON Regions.region_id = Comments.region_id
        GROUP BY
            Regions.region_id,
            Regions.region_name
        HAVING
            COUNT(Comments.comment_id) > 5
    """
    log.debug('get_stat_regions_max(): "{0!r}"'.format(query))
    return get_query(query)


def get_stat_cities(region_id):
    """Returns counts of comments from region's list cities"""
    query = """
        SELECT
            Cities.city_id             AS city_id,
            Cities.city_name           AS city_name,
            COUNT(Comments.comment_id) AS count
        FROM
            Comments
        JOIN
            Cities
            ON Cities.city_id = Comments.city_id
        WHERE
            Comments.region_id = ?
        GROUP BY
            Cities.city_id,
            Cities.city_name
    """
    log.debug('get_stat_cities(): "{0!r}" % {1!r}'.format(query, region_id))
    return get_query(query, region_id)