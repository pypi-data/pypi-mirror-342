# -*- coding: utf-8 -*-
import os
from pymongo import MongoClient, ReadPreference
from flask import g
import ssl
try:
    from ssl import CERT_NONE
    ssl_available = True
except ImportError:  # pragma: no cover
    CERT_NONE = None
    ssl_available = False

# MONGODB_HOST = os.environ.get('MONGO_HOST', 'ds147118.mlab.com')
# MONGODB_PORT = os.environ.get('MONGO_PORT', 47118)
# MONGO_USERNAME = os.environ.get('MONGO_USERNAME', 'root')
# MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD', 'root12')
# MONGODB_NAME = os.environ.get('MONGO_DBNAME', 'selfship')

# mongodb+srv://root:root12@mum-01.sr4se.mongodb.net/selfship?retryWrites=true&w=majority
MONGO_CONNECTION_STRING = os.environ.get('MONGO_CONNECTION_STRING') or 'mongodb+srv://root:root12@mum-01.sr4se.mongodb.net/selfship?retryWrites=true&w=majority'

MONGODB_HOST = os.environ.get('MONGO_HOST', 'localhost')
MONGODB_PORT = os.environ.get('MONGO_PORT', 27017)
MONGO_USERNAME = os.environ.get('MONGO_USERNAME', '')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD', '')
MONGODB_NAME = os.environ.get('MONGO_DBNAME', 'selfship')

MONGO_MAP = {}


def fetch_g_host():
    try:
        from flask import g
        return g.host
    except Exception as e:
        return None


class Conn(MongoClient):
    '''A singleton Wrapper over pymongo connection.
    We have this abstraction to avoid instantiating a mongo db connection on module import,
     as well as avoid instantiating too many connections in a single application.

    The underlying connection object is thread-safe as well as implements thread pooling.
    It also re-connects to database if the connection fails. That makes using a single connection
    throughout the application life possible.
    '''

    _instance = None

    def __new__(cls, *args, **kwargs):
        __hostname = None
        __conn_string = None
        __ssl_mode = False
        try:
            try:
                __hostname = g.host
            except Exception as e:
                __hostname = None

            # Parent connection relies on eShipz control DB
            if kwargs and kwargs.get('parent_db'):
                return cls._get_connection()
            # Provision to override hostname and connection string - esp for celery usecases as we were unable to extract the request context under celery
            if kwargs and kwargs.get('hostname') and kwargs.get('connection_string'):
                __hostname = kwargs.get('hostname')
                __conn_string = kwargs.get('connection_string')
            if kwargs and kwargs.get('ssl_mode'):
                __ssl_mode = kwargs.get('ssl_mode')

            if MONGO_MAP.get(__hostname) is None:
                MONGO_MAP.update({__hostname: cls._get_connection(hostname=__hostname, connection_string=__conn_string, ssl_mode=__ssl_mode)})
            return MONGO_MAP.get(__hostname)
        except Exception as e:
            return cls._get_connection(hostname=__hostname, connection_string=__conn_string)

    @classmethod
    def _get_connection(self, connection_string=None, hostname=None, ssl_mode=False):
        ''' Creates a new Mongo DB connection object'''
        # TODO: Reach from settings file
        # mongodb: // root: root12 @ ds147118.mlab.com:47118 / selfship
        conn_string = ''
        if connection_string is None:
            __host = None
            tenant_details = None
            try:
                __host = hostname
                tenant_details = g.tenant_details
            except Exception as e:
                __host = hostname
            print(__host)
            if tenant_details and tenant_details.get('ssl_mode'):
                ssl_mode = tenant_details.get('ssl_mode')
            if __host and tenant_details and tenant_details.get('db_uri'):
                conn_string = tenant_details.get('db_uri')
            elif MONGO_CONNECTION_STRING:
                conn_string = MONGO_CONNECTION_STRING
            elif MONGO_USERNAME and MONGO_PASSWORD:
                conn_string = 'mongodb://%s:%s@%s:%s/%s' % (MONGO_USERNAME, MONGO_PASSWORD, MONGODB_HOST, MONGODB_PORT, MONGODB_NAME)
            else:
                conn_string = 'mongodb://%s:%s/%s' % (MONGODB_HOST, MONGODB_PORT, MONGODB_NAME)
        else:
            conn_string = connection_string

        # print(conn_string)
        if ssl_mode:
            if ssl_available:
                c = MongoClient(conn_string, ssl=ssl_mode, ssl_cert_reqs=ssl.CERT_NONE).get_database(MONGODB_NAME, read_preference=ReadPreference.SECONDARY_PREFERRED)
            else:
                c = MongoClient(conn_string, ssl=ssl_mode).get_database(MONGODB_NAME, read_preference=ReadPreference.SECONDARY_PREFERRED)
        else:
            c = MongoClient(conn_string).get_database(MONGODB_NAME, read_preference=ReadPreference.SECONDARY_PREFERRED)

        return c
