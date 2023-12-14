import sqlite3


def get_db_connection():
    return sqlite3.connect('library.sqlite')


def join_string(some_list):
    return ', '.join(['"{}"'.format(some_list) for some_list in some_list])
