import os
import psycopg2  # pylint:disable=import-error

from urllib.parse import urlparse

DB_URL = os.getenv('EMOJI_ESSAY_BOT_DB_URL')


def connect_to_db():
    conn_creds = parse_db_url()

    conn = psycopg2.connect(
        dbname=conn_creds['database'],
        user=conn_creds['username'],
        password=conn_creds['password'],
        host=conn_creds['hostname']
    )
    c = conn.cursor()
    return conn, c


def disconnect_from_db(conn, c):
    conn.close()
    c.close()

    return


def parse_db_url():
    result = urlparse(DB_URL)

    conn_creds = {}
    conn_creds['username'] = result.username
    conn_creds['password'] = result.password
    conn_creds['database'] = result.path[1:]
    conn_creds['hostname'] = result.hostname

    return conn_creds
