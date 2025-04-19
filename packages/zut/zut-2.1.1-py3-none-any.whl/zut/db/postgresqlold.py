from __future__ import annotations

import logging
import re
from contextlib import nullcontext
from typing import TYPE_CHECKING, TextIO
from urllib.parse import unquote, urlparse

from zut import build_url, get_logger
from zut.db.postgresql import PostgreSqlDb

if TYPE_CHECKING:
    from psycopg2.extensions import connection, cursor

try:
    from psycopg2 import connect
    _missing_dependency = None
except ModuleNotFoundError:
    _missing_dependency = "psycopg2"


class PostgreSqlOldDb(PostgreSqlDb[connection, cursor] if TYPE_CHECKING else PostgreSqlDb):
    """
    Database adapter for PostgreSQL (using `psycopg2` driver).
    """
    missing_dependency = _missing_dependency

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._in_transaction = None

    def _create_connection(self):
        r = urlparse(self._connection_url)

        kwargs = {}
        if r.hostname:
            kwargs['host'] = unquote(r.hostname)
        if r.port:
            kwargs['port'] = r.port

        path = r.path.lstrip('/')
        if path:
            kwargs['dbname'] = unquote(path)

        if r.username:
            kwargs['user'] = unquote(r.username)
        if r.password:
            kwargs['password'] = unquote(r.password)

        conn = connect(**kwargs)
        conn.autocommit = self._autocommit
        return conn

    def _create_transaction(self):
        if self._in_transaction:
            return nullcontext()
        
        class CM:
            def __init__(self, db: PostgreSqlOldDb):
                self.db = db

            def __enter__(self):
                self.db._in_transaction = self.db.connection.__enter__()
                return self
            
            def __exit__(self, *args):
                self.db._in_transaction.__exit__(*args)
                self.db._in_transaction = None
                
        return CM(self)

    def _get_url_from_connection(self):    
        params = self.connection.get_dsn_parameters()
        return build_url(
            scheme=self.scheme,
            path='/' + params.get('dbname', None),
            hostname=params.get('host', None),
            port=params.get('port', None),
            username=params.get('user', None),
            password=params.get('password', None),
        )
    

    def _register_cursor_messages_handler(self, cursor, messages_source: str|None):
        logger = get_logger(f'{self._logger.name}:{messages_source}') if messages_source else self._logger
        return PostgreSqlOldNoticeHandler(cursor.connection, logger)


    def _actual_copy_from_csv(self, cursor: cursor, sql: str, fp: TextIO, buffer_size: int):
        cursor.copy_expert(sql, fp, buffer_size)


class PostgreSqlOldNoticeHandler:
    """
    This class is the actual handler required by psycopg 2 `connection.notices`.
    
    It can also be used as a context manager that remove the handler on exit.
    """
    _notice_re = re.compile(r"^(?P<severity>[A-Z]+)\:\s(?P<message>.*)$", re.DOTALL)

    def __init__(self, connection, logger: logging):
        self.connection = connection
        self.logger = logger
        self.connection.notices = self

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type = None, exc_value = None, exc_traceback = None):
        self.connection.notices = []

    def append(self, fullmsg: str):
        fullmsg = fullmsg.strip()
        m = self._notice_re.match(fullmsg)
        if not m:
            self.logger.error(fullmsg)
            return

        severity = m.group("severity")
        message = m.group("message").lstrip()
        level, message = PostgreSqlDb.parse_message(severity, message)

        self.logger.log(level, message)
