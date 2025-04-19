"""
Common operations on databases.
"""
from __future__ import annotations

import logging
import os
import re
import socket
import sys
from configparser import _UNSET
from collections import abc
from dataclasses import dataclass
from datetime import date, datetime, time, tzinfo
from decimal import Decimal
from enum import Enum, Flag
from io import IOBase
from pathlib import Path
from secrets import token_hex
from threading import current_thread
from time import time_ns
from typing import (Any, Generator, Generic, Iterable, Mapping, NamedTuple, Sequence, TextIO,
                    TypeVar, overload, TYPE_CHECKING)
from urllib.parse import ParseResult, parse_qs, quote, unquote, urlparse
from uuid import UUID

from zut import (Header, Literal, Protocol, Secret, TabularDumper, TupleRow, cached_property, make_naive,
                 build_url, convert, files, get_logger, get_secret,
                 hide_url_password, now_naive_utc, parse_tz, slugify,
                 tabular_dumper)

try:
    from django.http import Http404 as _BaseNotFoundError
except ModuleNotFoundError:
    _BaseNotFoundError = Exception

try:
    from tabulate import tabulate
except ModuleNotFoundError:
    tabulate = None

if TYPE_CHECKING:
    from zut.db.load import LoadForeignKey, LoadResult


#region Protocol objects (for type generics)

class Connection(Protocol):
    def close(self) -> None:
        ...

    def commit(self) -> None:
        ...

    def cursor(self) -> Cursor:
        ...


class Cursor(Protocol):
    def __enter__(self) -> Cursor:
        ...

    def __exit__(self, exc_type = None, exc_value = None, exc_traceback = None) -> None:
        ...

    def close(self) -> None:
        ...
    
    def execute(self, sql: str, params: Sequence[Any]|Mapping[str,Any]|None = None) -> None:
        ...

    def nextset(self) -> bool:
        ...

    @property
    def connection(self) -> Connection:
        ...

    @property
    def rowcount(self) -> int:
        ...

    @property
    def description(self) -> tuple[tuple[str, Any, int, int, int, int, bool]]:
        ...

#endregion

if sys.version_info < (3, 13): # TypeVar's default argument introduced in Python 3.13
    T_Connection = TypeVar('T_Connection', bound=Connection)
    T_Cursor = TypeVar('T_Cursor', bound=Cursor)
else:
    T_Connection = TypeVar('T_Connection', bound=Connection, default=Connection)
    T_Cursor = TypeVar('T_Cursor', bound=Cursor, default=Cursor)


class Db(Generic[T_Connection, T_Cursor]):
    """
    Base class for database adapters.
    """

    #region Init

    # DB engine specifics
    scheme: str
    default_port: int
    default_schema: str|None = 'public'
    only_positional_params = False
    split_multi_statement_files = False
    table_in_path = True
    identifier_quotechar_begin = '"'
    identifier_quotechar_end = '"'
    sql_placeholder = '%s'
    sql_named_placeholder = '%%(%s)s'
    bool_sql_basetype = 'boolean'
    int_sql_basetype = 'bigint'
    float_sql_basetype = 'double precision'
    decimal_sql_basetype = 'numeric'
    datetime_sql_basetype = 'timestamp with time zone'
    date_sql_basetype = 'date'
    str_sql_basetype = 'text'
    str_precised_sql_basetype = 'character varying'
    uuid_sql_basetype = 'uuid'
    accept_aware_datetime = True
    truncate_with_delete = False
    can_cascade_truncate = True
    identity_definition_sql = 'GENERATED ALWAYS AS IDENTITY'
    procedure_caller = 'CALL'
    procedure_params_parenthesis = True
    function_requires_schema = False
    can_add_several_columns = False
    temp_schema = 'pg_temp'
    missing_dependency: str = None
    
    # Global configurable
    autocommit = True
    use_http404 = False
    """ Use Django's HTTP 404 exception instead of NotFoundError (if Django is available). """

    def __init__(self, origin: T_Connection|str|ParseResult|dict|None = None, *, name: str = None, user: str = None, password: str|Secret = None, host: str = None, port: str = None, encrypt: bool|None = None, password_required: bool = False, autocommit: bool = None, tz: tzinfo|str|None = None, migrations_dir: str|os.PathLike = None, table: str|tuple|DbObj|None = None):
        """
        Create a new Db instance.
        - `origin`: an existing connection object (or Django wrapper), the URL for the new connection to be created by the Db instance, or the key to build a connection object (name of DB, or prefix of environment variable names).
        - `autocommit`: commit transactions automatically (applies only for connections created by the Db instance).
        - `tz`: naive datetimes in results are made aware in the given timezone.
        """
        if self.missing_dependency:
            raise ValueError(f"Cannot use {type(self).__name__} (missing {self.missing_dependency} dependency)")
                
        self.table = DbObj.parse(table, db=type(self)) if table else None
        """ A specific table associated to this instance. Used for example as default table for `dumper`. """

        logger_name = f"{__name__}.{self.__class__.__qualname__}"
        
        if origin is None:
            origin = getattr(self.__class__, 'origin', None)

        if origin is None:
            origin = {
                'name': name or getattr(self.__class__, 'name', None),
                'user': user or getattr(self.__class__, 'user', None),
                'password': password or getattr(self.__class__, 'password', None),
                'host': host or getattr(self.__class__, 'host', None),
                'port': port or getattr(self.__class__, 'port', None),
                'encrypt': encrypt if encrypt is not None else getattr(self.__class__, 'encrypt', None),
            }
            if not origin['name']:
                raise TypeError(f"Argument 'name' must be given when 'origin' is none.")
        
        elif (isinstance(origin, str) and not ':' in origin): # origin is a key: either the name of the DB, or the prefix of environment variable names
            logger_name += f'.{origin}'
            env_prefix = slugify(origin, separator='_').upper()     
            origin = {
                'name': os.environ.get(f'{env_prefix}_DB_NAME') or name or getattr(self.__class__, 'name', None) or origin,
                'user': os.environ.get(f'{env_prefix}_DB_USER') or user or getattr(self.__class__, 'user', None),
                'password': get_secret(f'{env_prefix}_DB_PASSWORD') or password or getattr(self.__class__, 'password', None),
                'host': os.environ.get(f'{env_prefix}_DB_HOST') or host or getattr(self.__class__, 'host', None),
                'port': os.environ.get(f'{env_prefix}_DB_PORT') or port or getattr(self.__class__, 'port', None),
                'encrypt': os.environ.get(f'{env_prefix}_DB_ENCRYPT') if os.environ.get(f'{env_prefix}_DB_ENCRYPT') is not None else (encrypt if encrypt is not None else getattr(self.__class__, 'encrypt', None)),
            }
        
        else:            
            if name is not None:
                raise TypeError(f"Argument 'name' cannot be set when 'origin' is not a string.")
            if user is not None:
                raise TypeError(f"Argument 'user' cannot be set when 'origin' is not a string.")
            if password is not None:
                raise TypeError(f"Argument 'password' cannot be set when 'origin' is not a string.")
            if host is not None:
                raise TypeError(f"Argument 'host' cannot be set when 'origin' is not a string.")
            if port is not None:
                raise TypeError(f"Argument 'port' cannot be set when 'origin' is not a string.")
            if encrypt is not None:
                raise TypeError(f"Argument 'encrypt' cannot be set when 'origin' is not a string.")
        
        # Actual interpretation of 'origin'
        self._connection_url: str
        self._connection_encrypt: bool|None = None
        self._connection_url_secret: Secret|None = None
        if isinstance(origin, dict):
            self._owns_connection = True
            self._connection: T_Connection = None

            if 'NAME' in origin: # uppercase (as used by django)
                password = origin.get('PASSWORD', None)
                if isinstance(password, Secret):
                    self._connection_url_secret = password
                    password = None
                self._connection_encrypt = origin.get('ENCRYPT')
                
                self._connection_url = build_url(
                    scheme = self.scheme,
                    hostname = origin.get('HOST', None),
                    port = origin.get('PORT', None),
                    username = origin.get('USER', None),
                    password = password,
                    path = origin.get('NAME', None),
                )
                if not self.table:
                    table = origin.get('TABLE', None)
                    if table:
                        self.table = DbObj(table, origin.get('SCHEMA', None), type(self))

            else: # lowercase (as used by some drivers' connection kwargs)                
                password = origin.get('password', None)
                if isinstance(password, Secret):
                    self._connection_url_secret = password
                    password = None
                self._connection_encrypt = origin.get('encrypt')

                self._connection_url = build_url(
                    scheme = self.scheme,
                    hostname = origin.get('host', None),
                    port = origin.get('port', None),
                    username = origin.get('user', None),
                    password = password,
                    path = origin.get('name', origin.get('dbname', None)),
                )
                if not self.table:
                    table = origin.get('table', None)
                    if table:
                        self.table = DbObj(table, origin.get('schema', None), type(self))

        elif (isinstance(origin, str) and ':' in origin) or isinstance(origin, ParseResult): # URL
            self._owns_connection = True
            self._connection: T_Connection = None

            r = origin if isinstance(origin, ParseResult) else urlparse(origin)
            if r.fragment:
                raise ValueError(f"Invalid {self.__class__.__name__}: unexpected fragment: {r.fragment}")
            if r.params:
                raise ValueError(f"Invalid {self.__class__.__name__}: unexpected params: {r.params}")
            
            query = parse_qs(r.query)
            query_schema = query.pop('schema', [None])[-1]
            query_table = query.pop('table', [None])[-1]
            if not self.table:          
                if query_table:
                    self.table = DbObj(query_table, query_schema, type(self))
            if query:
                raise ValueError(f"Invalid {self.__class__.__name__}: unexpected query data: {query}")
            
            scheme = r.scheme
            r = self._verify_scheme(r)
            if not r:
                raise ValueError(f"Invalid {self.__class__.__name__}: invalid scheme: {scheme}")

            if not self.table and self.table_in_path:
                table_match = re.match(r'^/?(?P<name>[^/@\:]+)/((?P<schema>[^/@\:\.]+)\.)?(?P<table>[^/@\:\.]+)$', r.path)
                if table_match:
                    self.table = DbObj(table_match['table'], table_match['schema'] if table_match['schema'] else None, type(self))            
                    r = r._replace(path=table_match['name'])
                self._connection_url = r.geturl()
            else:
                self._connection_url = r.geturl()
            self._connection_url_secret = None

        elif type(origin).__name__ in {'Connection', 'ConnectionProxy'} or hasattr(origin, 'cursor'):
            self._connection = origin
            self._connection_url: str = None
            self._owns_connection = False

            if password_required:
                raise TypeError(f"Argument 'password_required' cannot be set when 'origin' is connection object.")
            if autocommit is not None:
                raise TypeError(f"Argument 'autocommit' cannot be set when 'origin' is connection object.")
            if migrations_dir is not None:
                raise TypeError(f"Argument 'migrations_dir' cannot be set when 'origin' is connection object.")        
        else:
            raise TypeError(f"Invalid type for argument 'origin': {type(origin).__name__}")


        self.password_required = password_required
        if not tz:
            tz = getattr(self.__class__, 'tz', None)
        if isinstance(tz, str):
            tz = tz if tz == 'localtime' else parse_tz(tz)
        self.tz = tz
        
        self._autocommit = autocommit or getattr(self.__class__, 'autocommit', None)
        self._migrations_dir = migrations_dir or getattr(self.__class__, 'migrations_dir', None)
        self._is_port_opened = None
        
        self._logger = get_logger(logger_name)
    

    @classmethod
    def get_sqlutils_path(cls):
        path = Path(__file__).resolve().parent.joinpath('sqlutils', f"{cls.scheme}.sql")
        if not path.exists():
            return None
        return path
    
    
    def _verify_scheme(self, r: ParseResult) -> ParseResult|None:
        if r.scheme == self.scheme:
            return r
        else:
            return None


    def get_url(self, *, hide_password = False):
        if self._connection_url:
            url = self._connection_url
        else:
            url = self._get_url_from_connection()

        if hide_password:
            url = hide_url_password(url, always_password=self._connection_url_secret)
        elif self._connection_url_secret:
            r = urlparse(url)
            password = self._connection_url_secret.value
            url = build_url(r, password=password)
            self._connection_url_secret = None
            self._connection_url = url

        if self.table:
            if self.table_in_path:
                url += f"/"
                if self.table.schema:
                    url += quote(self.table.schema)
                    url += '.'
                url += quote(self.table.name)
            else:
                url += f"?table={quote(self.table.name)}"
                if self.table.schema:
                    url += f"&schema={quote(self.table.schema)}"

        return url


    def _get_url_from_connection(self):
        raise NotImplementedError()
    

    def get_db_name(self):
        url = self.get_url(hide_password=True)
        r = urlparse(url)
        return unquote(r.path).lstrip('/')


    @property
    def is_port_opened(self):
        if self._is_port_opened is None:
            r = urlparse(self.get_url(hide_password=True))
            host = r.hostname or '127.0.0.1'
            port = r.port if r.port is not None else self.default_port
        
            if self._logger.isEnabledFor(logging.DEBUG):
                self._logger.debug("Check host %s, port %s (from thread %s)", host, port, current_thread().name)

            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((host, port))
                if result == 0:
                    self._logger.debug("Host %s, port %s: connected", host, port)
                    self._is_port_opened = True
                else:
                    self._logger.debug("Host %s, port %s: NOT connected", host, port)
                    self._is_port_opened = False
                sock.close()
            except Exception as err:
                raise ValueError(f"Cannot check host {host}, port {port}: {err}")
        
        return self._is_port_opened
    
    #endregion
    

    #region Connections, cursors and transactions

    def __enter__(self):
        return self


    def __exit__(self, exc_type = None, exc_value = None, exc_traceback = None):
        self.close()


    def close(self):
        if self._connection is None or not self._owns_connection:
            return
        
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug("Close %s (%s) connection to %s", type(self).__name__, type(self._connection).__module__ + '.' + type(self._connection).__qualname__, hide_url_password(self._connection_url, always_password=self._connection_url_secret))
        self._connection.close()
        self._connection = None


    @property
    def connection(self) -> T_Connection:
        if self._connection is None:
            if self._connection_url_secret:
                r = urlparse(self._connection_url)
                password = self._connection_url_secret.value
                self._connection_url_secret = None
                
                self._connection_url = build_url(r, password=password)

            elif self.password_required:
                password = urlparse(self._connection_url).password
                if not password:
                    raise ValueError("Cannot create %s connection to %s: password not provided" % (type(self).__name__, hide_url_password(self._connection_url)))
                
            if self._logger.isEnabledFor(logging.DEBUG):
                self._logger.debug(f"Create %s connection to %s", type(self).__name__, hide_url_password(self._connection_url))
            self._connection = self._create_connection()

            if self._migrations_dir:
                self.migrate(self._migrations_dir)
        return self._connection
    

    def get_autocommit(self):
        if not self._connection:
            return self._autocommit
        else:
            return self._connection.autocommit


    def _create_connection(self) -> T_Connection:
        raise NotImplementedError()
    
        
    def transaction(self):    
        try:
            from django.db import transaction
            from django.utils.connection import ConnectionProxy
            if isinstance(self._connection, ConnectionProxy):
                return transaction.atomic()
        except ModuleNotFoundError:
            pass
        return self._create_transaction()
        

    def _create_transaction(self):
        raise NotImplementedError()

    
    @overload
    def cursor(self, query: str|None = None, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int|None = None, offset: int|None = None, warn_results: int|bool = False, messages_source: str|None = None, result: Literal[False] = ...) -> CursorContext[T_Connection, T_Cursor]:
        """ Create a cursor, execute the given SQL statement if any, and return a context manager that gives the cursor object when entered (must be entered and exited properly using `with`). """
        ...

    @overload
    def cursor(self, query: str|None = None, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int|None = None, offset: int|None = None, warn_results: int|bool = False, messages_source: str|None = None, result: Literal[True]) -> ResultContext[T_Connection, T_Cursor]:
        """ Create a cursor, execute the given SQL statement if any, and return a result context manager (must be entered and exited properly using `with`). """
        ...
    
    def cursor(self, query: str|None = None, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int|None = None, offset: int|None = None, warn_results: int|bool = False, messages_source: str|None = None, result = False):
        if query:
            if limit is not None or offset is not None:
                query, _ = self.get_paginated_and_total_query(query, limit=limit, offset=offset)
            if isinstance(params, abc.Mapping) and self.only_positional_params:
                query, params = self.to_positional_params(query, params)
        return (ResultContext if result else CursorContext)(self, query, params, warn_results=warn_results, messages_source=messages_source)
    

    def _register_cursor_messages_handler(self, cursor: T_Cursor, messages_source: str|None):
        """
        Register a messages handler for the cursor. Must be a context manager.
        """
        pass
    
    
    def _log_cursor_messages(self, cursor: T_Cursor, messages_source: str|None):
        """
        Log messages produced during execution of a cursor. Use this if messages cannot be handled through `_register_cursor_messages_handler`.
        """
        pass

    _log_cursor_messages._do_nothing = True


    def _get_cursor_lastrowid(self, cursor: T_Cursor):
        raise NotImplementedError()

    #endregion


    #region Execute
    
    @overload
    def execute(self, query: str, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int|None = None, offset: int|None = None, warn_results: int|bool = False, messages_source = None, result: Literal[False] = ...) -> int:
        """ Execute a SQL statement, return the number of affected rows or -1 if none (cursor is entered and exited automatically). """
        ...

    @overload
    def execute(self, query: str, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int|None = None, offset: int|None = None, warn_results: int|bool = False, messages_source = None, result: Literal[True]) -> ResultContext[T_Connection, T_Cursor]:
        """ Execute a SQL statement, return the result context (must be entered and exited properly using `with`). """
        ...
    
    def execute(self, query: str, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int|None = None, offset: int|None = None, warn_results: int|bool = False, messages_source = None, result = False):
        the_result = self.cursor(query, params, limit=limit, offset=offset, warn_results=warn_results, messages_source=messages_source, result=True)
        if result:
            return the_result
        else:
            with the_result:
                return the_result.cursor.rowcount


    @overload
    def execute_file(self, file: str|os.PathLike, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int|None = None, offset: int|None = None, warn_results: int|bool = False, messages_source = None, encoding = 'utf-8', result: Literal[False] = ...) -> int:
        """ Execute a SQL file (possibly multi statement), return the total number of affected rows or -1 if none (cursor is entered and exited automatically). """
        ...

    @overload
    def execute_file(self, file: str|os.PathLike, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int|None = None, offset: int|None = None, warn_results: int|bool = False, messages_source = None, encoding = 'utf-8', result: Literal[True]) -> ResultContext[T_Connection, T_Cursor]:
        """ Execute a SQL file (possibly multi statement), return the result context (must be entered and exited properly using `with`). """
        ...
    
    def execute_file(self, file: str|os.PathLike, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int|None = None, offset: int|None = None, warn_results: int|bool = False, messages_source = None, encoding = 'utf-8', result = False, **file_kwargs):
        file_content = files.read_text(file, encoding=encoding)
        if file_kwargs:
            file_content = file_content.format(**{key: '' if value is None else value for key, value in file_kwargs.items()})
        
        a_result = None
        previous_rowcount = 0
        if self.split_multi_statement_files and ';' in file_content:
            # Split queries
            import sqlparse  # not at the top because the enduser might not need this feature
            queries = sqlparse.split(file_content, encoding)
            
            # Execute all queries
            query_count = len(queries)
    
            for index, query in enumerate(queries):
                if a_result is not None:
                    with a_result:
                        if not result:
                            rowcount = a_result.rowcount
                            if rowcount != -1:
                                previous_rowcount += rowcount
                
                query_num = index + 1
                if self._logger.isEnabledFor(logging.DEBUG):
                    query_start = re.sub(r"\s+", " ", query).strip()[0:100] + "…"
                    self._logger.debug("Execute query %d/%d: %s ...", query_num, query_count, query_start)
                if not messages_source:
                    messages_source = os.path.basename(file) + f' (query {query_num}/{query_count})'

                a_result = self.execute(query, params, limit=limit, offset=offset, warn_results=True if query_num < query_count else warn_results, messages_source=messages_source, result=True)
        else:
            if not messages_source:
                messages_source = os.path.basename(file)
            a_result = self.execute(file_content, params, limit=limit, offset=offset, warn_results=warn_results, messages_source=messages_source, result=True)
            
        # Handle last result
        if result:
            return a_result
        else:
            with a_result:
                rowcount = a_result.rowcount
                return previous_rowcount + (rowcount if rowcount != -1 else 0)
    

    def execute_function(self, obj: str|tuple|DbObj, params: list|tuple|dict = None, *, limit: int|None = None, offset: int|None = None, warn_results: int|bool = False, messages_source = None, result = False, caller='SELECT', params_parenthesis=True):
        obj = self.parse_obj(obj)
        
        query = f"{caller} {obj.full_escaped if self.function_requires_schema else obj.escaped}"
        if params_parenthesis:
            query += "("
                
        if isinstance(params, abc.Mapping):
            list_params = []
            first = True
            for key, value in enumerate(params):
                if not key:
                    raise ValueError(f"Parameter cannot be empty")
                elif not re.match(r'^[\w\d0-9_]+$', key): # for safety
                    raise ValueError(f"Parameter contains invalid characters: {key}")
                
                if first:
                    first = False
                else:
                    query += ','

                query += f'{key}={self.sql_placeholder}'
                list_params.append(value)
            params = list_params
        elif params:
            query += ','.join([self.sql_placeholder] * len(params))
    
        if params_parenthesis:
            query += ")"

        if not messages_source:
            messages_source = obj.unsafe

        return self.execute(query, params, limit=limit, offset=offset, warn_results=warn_results, messages_source=messages_source, result=result)
    

    def execute_procedure(self, obj: str|tuple|DbObj, params: list|tuple|dict = None, *, limit: int|None = None, offset: int|None = None, warn_results: int|bool = 10, messages_source = None, result = False):
        return self.execute_function(obj, params, limit=limit, offset=offset, warn_results=warn_results, messages_source=messages_source, result=result, caller=self.procedure_caller, params_parenthesis=self.procedure_params_parenthesis)


    #endregion


    #region Query helpers

    @classmethod
    def escape_identifier(cls, value: str|Header) -> str:
        if isinstance(value, Header):
            value = value.name
        elif not isinstance(value, str):
            raise TypeError(f"Invalid identifier: {value} ({type(value)})")
        return f"{cls.identifier_quotechar_begin}{value.replace(cls.identifier_quotechar_end, cls.identifier_quotechar_end+cls.identifier_quotechar_end)}{cls.identifier_quotechar_end}"
    

    @classmethod
    def escape_literal(cls, value) -> str:
        if value is None:
            return "null"
        else:
            return f"'" + str(value).replace("'", "''") + "'"
    
    
    def parse_obj(self, input: str|tuple|type|DbObj|None = None, *, schema: str|None = _UNSET) -> DbObj:
        if isinstance(input, DbObj) and schema is _UNSET and input.db:
            return input
        return DbObj.parse(input, self, schema=schema)


    def to_supported_value(self, value: Any):
        """ Convert a value to types supported by the underlying connection. """        
        if isinstance(value, (Enum,Flag)):
            return value.value
        elif isinstance(value, (datetime,time)):
            if value.tzinfo:
                if self.accept_aware_datetime:
                    return value
                elif self.tz:
                    value = make_naive(value, self.tz)
                else:
                    raise ValueError(f"Cannot store tz-aware datetimes with {type(self).__name__} without providing `tz` argument")
            return value
        else:
            return value
    
    def to_positional_params(self, query: str, params: Mapping[str,Any]) -> tuple[str, Sequence[Any]]:
        from sqlparams import SQLParams  # not at the top because the enduser might not need this feature

        if not hasattr(self.__class__, '_params_formatter'):
            self.__class__._params_formatter = SQLParams('named', 'qmark') # type: ignore
        query, params = self.__class__._params_formatter.format(query, params) # type: ignore

        return query, params # type: ignore
    

    def get_paginated_and_total_query(self, query: str, *, limit: int|None, offset: int|None) -> tuple[str,str]:        
        if limit is not None:
            if isinstance(limit, str) and re.match(r"^[0-9]+$", limit):
                limit = int(limit)
            elif not isinstance(limit, int):
                raise TypeError(f"Invalid type for limit: {type(limit).__name__} (expected int)")
            
        if offset is not None:
            if isinstance(offset, str) and re.match(r"^[0-9]+$", offset):
                offset = int(offset)
            elif not isinstance(offset, int):
                raise TypeError(f"Invalid type for offset: {type(limit).__name__} (expected int)")
        
        beforepart, selectpart, orderpart = self._split_select_query(query)

        paginated_query = beforepart
        total_query = beforepart
        
        paginated_query += self._paginate_splited_select_query(selectpart, orderpart, limit=limit, offset=offset)
        total_query += f"SELECT COUNT(*) FROM ({selectpart}) s"

        return paginated_query, total_query
    

    def _split_select_query(self, query: str):
        import sqlparse  # not at the top because the enduser might not need this feature

        # Parse SQL to remove token before the SELECT keyword
        # example: WITH (CTE) tokens
        statements = sqlparse.parse(query)
        if len(statements) != 1:
            raise sqlparse.exceptions.SQLParseError(f"Query contains {len(statements)} statements")

        # Get first DML keyword
        dml_keyword = None
        dml_keyword_index = None
        order_by_index = None
        for i, token in enumerate(statements[0].tokens):
            if token.ttype == sqlparse.tokens.DML:
                if dml_keyword is None:
                    dml_keyword = str(token).upper()
                    dml_keyword_index = i
            elif token.ttype == sqlparse.tokens.Keyword:
                if order_by_index is None:
                    keyword = str(token).upper()
                    if keyword == "ORDER BY":
                        order_by_index = i

        # Check if the DML keyword is SELECT
        if not dml_keyword:
            raise sqlparse.exceptions.SQLParseError(f"Not a SELECT query (no DML keyword found)")
        if dml_keyword != 'SELECT':
            raise sqlparse.exceptions.SQLParseError(f"Not a SELECT query (first DML keyword is {dml_keyword})")

        # Get part before SELECT (example: WITH)
        if dml_keyword_index > 0:
            tokens = statements[0].tokens[:dml_keyword_index]
            beforepart = ''.join(str(token) for token in tokens)
        else:
            beforepart = ''
    
        # Determine actual SELECT query
        if order_by_index is not None:
            tokens = statements[0].tokens[dml_keyword_index:order_by_index]
            selectpart = ''.join(str(token) for token in tokens)
            tokens = statements[0].tokens[order_by_index:]
            orderpart = ''.join(str(token) for token in tokens)
        else:
            tokens = statements[0].tokens[dml_keyword_index:]
            selectpart = ''.join(str(token) for token in tokens)
            orderpart = ''

        return beforepart, selectpart, orderpart
    

    def _paginate_splited_select_query(self, selectpart: str, orderpart: str, *, limit: int|None, offset: int|None) -> str:
        result = f"{selectpart} {orderpart}"
        if limit is not None:
            result += f" LIMIT {limit}"
        if offset is not None:
            result += f" OFFSET {offset}"
        return result
    

    def _get_select_table_query(self, table: str|tuple|DbObj = None, *, schema_only = False) -> str:
        """
        Build a query on the given table.

        If `schema_only` is given, no row will be returned (this is used to get information on the table).
        Otherwise, all rows will be returned.

        The return type of this function depends on the database engine.
        It is passed directly to the cursor's execute function for this engine.
        """
        table = self.parse_obj(table)
        
        query = f'SELECT * FROM {table.escaped}'
        if schema_only:
            query += ' WHERE 1 = 0'

        return query   
    
    #endregion
    

    #region Result shortcuts
   
    def iter_rows(self, sql: str, params: Sequence[Any]|Mapping[str,Any]|None = None, limit: int|None = None, offset: int|None = None):
        with self.cursor(sql, params, limit=limit, offset=offset, result=True) as result:
            yield from iter(result)


    def get_row(self, sql: str, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int|None = None, offset: int|None = None) -> TupleRow:        
        """Retrieve the first row from the query. Raise NotFoundError if there is no row."""
        with self.cursor(sql, params, limit=limit, offset=offset, result=True) as result:
            return result.get_row()


    def get_rows(self, sql: str, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int|None = None, offset: int|None = None) -> TupleRow:        
        """Retrieve the first row from the query. Raise NotFoundError if there is no row."""
        with self.cursor(sql, params, limit=limit, offset=offset, result=True) as result:
            return result.get_rows()
        

    def single_row(self, sql: str, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int|None = None, offset: int|None = None) -> TupleRow:        
        """Retrieve the result row from the query. Raise NotFoundError if there is no row or SeveralFound if there are more than one row."""
        with self.cursor(sql, params, limit=limit, offset=offset, result=True) as result:
            return result.single_row()
        
    
    def first_row(self, sql: str, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int|None = None, offset: int|None = None) -> TupleRow|None:
        """Retrieve the first row from the query. Return None if there is no row."""
        with self.cursor(sql, params, limit=limit, offset=offset, result=True) as result:
            return result.first_row()


    def get_vals(self, sql: str, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int|None = None, offset: int|None = None):
        """A convenience function for returning the first column of the first row from the query. Raise NotFoundError if there is no row."""
        with self.cursor(sql, params, limit=limit, offset=offset, result=True) as result:
            return result.get_vals()


    def get_val(self, sql: str, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int|None = None, offset: int|None = None):
        """A convenience function for returning the first column of the first row from the query. Raise NotFoundError if there is no row."""
        with self.cursor(sql, params, limit=limit, offset=offset, result=True) as result:
            return result.get_val()


    def single_val(self, sql: str, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int|None = None, offset: int|None = None):
        """A convenience function for returning the first column of the first row from the query. Raise NotFoundError if there is no row or SeveralFound if there are more than one row."""
        with self.cursor(sql, params, limit=limit, offset=offset, result=True) as result:
            return result.single_val()


    def first_val(self, sql: str, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int|None = None, offset: int|None = None):
        """A convenience function for returning the first column of the first row from the query. Raise None if there is no row."""
        with self.cursor(sql, params, limit=limit, offset=offset, result=True) as result:
            return result.first_val()
   

    def iter_dicts(self, sql: str, params: Sequence[Any]|Mapping[str,Any]|None = None, limit: int|None = None, offset: int|None = None):
        with self.cursor(sql, params, limit=limit, offset=offset, result=True) as result:
            yield from result.iter_dicts()
   

    def get_dicts(self, sql: str, params: Sequence[Any]|Mapping[str,Any]|None = None, limit: int|None = None, offset: int|None = None):
        with self.cursor(sql, params, limit=limit, offset=offset, result=True) as result:
            return result.get_dicts()
   

    def paginate_dicts(self, sql: str, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int, offset: int = 0):
        paginated_sql, total_query = self.get_paginated_and_total_query(sql, limit=limit, offset=offset)
        rows = self.get_dicts(paginated_sql, params)
        total = self.get_val(total_query, params)
        return {"rows": rows, "total": total}
    

    def get_dict(self, sql: str, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int|None = None, offset: int|None = None):
        with self.cursor(sql, params, limit=limit, offset=offset, result=True) as result:
            return result.get_dict()
    

    def single_dict(self, sql: str, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int|None = None, offset: int|None = None):
        with self.cursor(sql, params, limit=limit, offset=offset, result=True) as result:
            return result.single_dict()
    

    def first_dict(self, sql: str, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int|None = None, offset: int|None = None):
        with self.cursor(sql, params, limit=limit, offset=offset, result=True) as result:
            return result.first_dict()

    #endregion


    #region Inspect

    def schema_exists(self, schema: str = None) -> bool:        
        if self.default_schema is None:
            raise ValueError("This Db does not support schemas")
        raise NotImplementedError()


    def table_exists(self, table: str|tuple|DbObj = None) -> bool:
        raise NotImplementedError()
    

    def get_columns(self, table_or_cursor: str|tuple|DbObj|T_Cursor = None) -> tuple[str]:
        if table_or_cursor is None or isinstance(table_or_cursor, (str,tuple,DbObj)):
            # table_or_cursor is assumed to be a table name (use self.table if None) 
            query = self._get_select_table_query(table_or_cursor, schema_only=True)
            with self.cursor() as cursor:
                cursor.execute(query)
                return self.get_columns(cursor)
        else:
            # table_or_cursor is assumed to be a cursor
            if not table_or_cursor.description:
                raise ValueError("No results in last executed query (no cursor description available)")
            return tuple(info[0] for info in table_or_cursor.description)


    def get_headers(self, object: str|tuple|DbObj|T_Cursor = None, minimal = False) -> list[Header]:
        """
        Get the headers for the given table, cursor, or Django model.

        The following Header attributes are set (when possible):
        - `name`: set to the name of the table or cursor columns, or of the Django model columns.
        - `not_null`: indicate whether the column has a 'not null' constraint.
        
        If `minimal`, perform minimal queries, to get at least the type.
        """
        if object is None or isinstance(object, (str,tuple,DbObj)): # `object` is assumed to be a table name (use `self.table` if `object` is `None`)
            return self._get_headers_from_table(object, minimal=minimal)

        elif isinstance(object, type): # `object` is assumed to be a Django model
            from zut.db.django import get_headers_from_django_model
            return get_headers_from_django_model(object, minimal=minimal)

        else: # `object` is assumed to be a cursor
            if not object.description:
                raise ValueError("No results in last executed query (no cursor description available)")
            return self._get_headers_from_cursor_description(object.description)
        

    def _get_headers_from_table(self, table: str|tuple|DbObj|None = None, *, minimal = False):
        table = self.parse_obj(table)

        headers: list[Header] = []
        for data in self._get_headers_data_from_table(table, minimal=minimal):
            data.pop('ordinal', None)
            
            _type = None
            if 'type_info' in data:
                type_info = data.pop('type_info')
                _type = self.get_type(type_info)
                data['type'] = _type

            if 'default' in data:
                default = data['default']
                if isinstance(default, str):
                    if default == '(getdate())' or default == 'statement_timestamp()' or default == 'now()':
                        default = Header.DEFAULT_NOW
                    else:
                        m = re.match(r"^\((.+)\)$", default) # sqlserver-specific
                        if m:
                            default = m[1]
                            m = re.match(r"^\((.+)\)$", default) # second level (e.g. for integer value)
                            if m:
                                default = m[1]
                        m = re.match(r"^'(.+)'(?:::[a-z0-9 ]+)?$", default) # note: `::type` is postgresql-specific
                        if m:
                            default = re.sub(r"''", "'", m[1]) # remove quotes

                if default != Header.DEFAULT_NOW and _type is not None:
                    default = convert(default, _type)
                
                data['default'] = default

            for key in ['not_null', 'primary_key', 'unique', 'identity']:
                if key in data and isinstance(data[key], int):
                    if data[key] == 0:
                        data[key] = False
                    elif data[key] == 1:
                        data[key] = True
                    else:
                        raise ValueError(f"Invalid integer value for \"{key}\": \"{data[key]}\" in {data}")
            
            header = Header(**data)
            headers.append(header)
        
        return headers
    

    def _get_headers_data_from_table(self, table: DbObj, *, minimal: bool) -> Iterable[dict[str,Any]]:
        raise NotImplementedError()
    

    def _get_headers_from_cursor_description(self, cursor_description) -> list[Header]:
        headers = []

        for name, type_info, display_size, internal_size, precision, scale, nullable in cursor_description:
            actual_type = self.get_type(type_info)
            if actual_type == str and precision is None and display_size is not None: # for postgresql
                precision = display_size

            if isinstance(nullable, int):
                if nullable == 1:
                    nullable = True
                elif nullable == 0:
                    nullable = False
               
            header = Header(name, type=actual_type, precision=precision, scale=scale, not_null=not nullable if isinstance(nullable, bool) else None)
            headers.append(header)
        
        return headers
    

    def get_type(self, type_info: type|int|str) -> type|None:
        if isinstance(type_info, type):
            return type_info
        
        if not type_info:
            return None
        
        # Simple heuristic, compatible with sqlite, see 3.1 ("Determination Of Column Affinity") in https://www.sqlite.org/datatype3.html
        if isinstance(type_info, str):
            if 'int' in type_info:
                return int
            elif 'char' in type_info or 'clob' in type_info or 'text' in type_info:
                return str
            elif 'real' in type_info or 'floa' in type_info or 'doub' in type_info:
                return float
            elif type_info == 'uuid': # postgresql
                return UUID
            else:
                return None
        elif isinstance(type_info, int):
            raise NotImplementedError(f"Cannot use integer type_info. Method missing in the subclass?")
        else:
            raise TypeError(f"type_info: {type(type_info).__name__}")
    

    def get_sql_type(self, _type: type|Header, precision: int|None = None, scale: int|None = None, *, key: bool|None = None) -> str:
        if isinstance(_type, Header):
            header = _type
            if header.sql_type:
                return header.sql_type
            
            _type = header.type
            if precision is None:
                precision = header.precision
            if scale is None:
                scale = header.scale
            if key is None:
                key = True if header.unique else False
            if _type is None:
                if header.default is not None:
                    if header.default == header.DEFAULT_NOW:
                        _type = datetime
                    else:
                        _type = type(header.default)
                else:
                    _type = str
        elif not isinstance(_type, type):
            raise TypeError(f"_type: {type(_type)}")
        
        if issubclass(_type, bool):
            sql_basetype = self.bool_sql_basetype
        elif issubclass(_type, int):
            sql_basetype = self.int_sql_basetype
        elif issubclass(_type, UUID):
            sql_basetype = self.uuid_sql_basetype
        elif issubclass(_type, float):
            sql_basetype = self.float_sql_basetype
        elif issubclass(_type, Decimal):
            if self.decimal_sql_basetype == 'text':
                sql_basetype = self.decimal_sql_basetype
            else:
                if precision is None:
                    raise ValueError("Precision must be set for decimal values")
                if scale is None:
                    raise ValueError("Scale must be set for decimal values")
                sql_basetype = self.decimal_sql_basetype
        elif issubclass(_type, datetime):
            sql_basetype = self.datetime_sql_basetype
        elif issubclass(_type, date):
            sql_basetype = self.date_sql_basetype
        else: # use str
            if precision is not None:
                sql_basetype = self.str_precised_sql_basetype
            elif key:
                sql_basetype = self.str_precised_sql_basetype
                precision = 255 # type for key limited to 255 characters (max length for a 1-bit length VARCHAR on MariaDB)
            else:
                sql_basetype = self.str_sql_basetype

        sql_type = sql_basetype
        if precision is not None or scale is not None:
            sql_type += '('
            if precision is not None:
                sql_type += str(precision)                
            if scale is not None:
                if precision is not None:
                    sql_type += ','
                sql_type += str(scale)
            sql_type += ')'

        return sql_type


    def get_sql_column_definition(self, column: Header|str, *, ignore_decimal = False, ignore_not_null = False):
        if not isinstance(column, Header):
            column = Header(column)

        if ignore_decimal and column.type and issubclass(column.type, (float,Decimal)):
            sql_type = 'varchar(100)'
        else:
            sql_type = self.get_sql_type(column)
            
        if column.primary_key or column.identity:
            not_null = True
        elif ignore_not_null:
            not_null = False
        else:
            not_null = column.not_null
        
        sql = f"{self.escape_identifier(column.name)} {sql_type} {'NOT NULL' if not_null else 'NULL'}"

        if column.default is not None:
            sql += f" DEFAULT {self.get_sql_escaped_default(column.default)}"

        return sql
    

    def get_sql_escaped_default(self, default):
        if default is None:
            return 'null'
        elif default == Header.DEFAULT_NOW:
            return 'CURRENT_TIMESTAMP'
        elif isinstance(default, str) and default.startswith('sql:'):
            return default[len('sql:'):]
        else:
            return self.escape_literal(default)
    
    #endregion


    #region DDL
    
    def drop_table(self, table: str|tuple|type|DbObj = None, *, if_exists = False, loglevel = logging.DEBUG):
        table = self.parse_obj(table)
        
        query = "DROP TABLE "
        if if_exists:
            query += "IF EXISTS "
        query += table.escaped

        self._logger.log(loglevel, "Drop table %s", table.unsafe)
        self.execute(query)


    def clear_table(self, table: str|tuple|type|DbObj = None, *, scope: str|None = None, truncate: bool|Literal['cascade'] = False, if_exists = False, loglevel = logging.DEBUG):
        table = self.parse_obj(table)

        if if_exists:
            if not self.table_exists(table):
                return
        
        if scope or not truncate or self.truncate_with_delete:
            query = "DELETE FROM "
        else:
            query = "TRUNCATE "
        
        query += table.escaped

        if scope:
            query += " WHERE scope = %s"
            params = [scope]
        else:
            if truncate == 'cascade':
                if self.truncate_with_delete:
                    raise ValueError("Cannot clear with truncate")
                query += " CASCADE"
            params = []
        
        self._logger.log(loglevel, "Clear table %s", table.unsafe)
        self.execute(query, params)


    def get_create_table_query(self, table: str|tuple|DbObj, columns: Iterable[str|Header], *, ignore_decimal = False, ignore_not_null = False, if_not_exists = False):
        table = self.parse_obj(table)
        
        columns = [Header(column) if not isinstance(column, Header) else column for column in columns]

        sql = "CREATE "
        if table.schema in {self.temp_schema, 'temp'}:
            sql += "TEMPORARY "
        sql += "TABLE "
        if if_not_exists:
            sql += "IF NOT EXISTS "
        sql += f"{table.escaped}("

        primary_key: tuple[str] = tuple(sorted(column.name for column in columns if column.primary_key))

        unique_keys: list[tuple[str]] = []    
        for column in columns:
            if column.unique:
                if column.unique is True:
                    key = (column.name,)
                    if not key in unique_keys and key != primary_key:
                        unique_keys.append(key)
                else:
                    for key in column.unique:
                        if not key in unique_keys and key != primary_key:
                            unique_keys.append(key)

        for i, column in enumerate(columns):
            sql += (',' if i > 0 else '') + self.get_sql_column_definition(column, ignore_decimal=ignore_decimal, ignore_not_null=ignore_not_null)
            if len(primary_key) == 1 and primary_key[0] == column.name:
                sql += " PRIMARY KEY"
            if column.identity:
                sql += f" {self.identity_definition_sql}"

        # Multi primary keys ?
        if len(primary_key) > 1:
            sql += ",PRIMARY KEY("
            for i, column in enumerate(primary_key):
                sql += ("," if i > 0 else "") + f"{self.escape_identifier(column)}"
            sql += ")" # end PRIMARY KEY

        # Unique together ?
        for unique_key in unique_keys:
            sql += ",UNIQUE("
            for i, key in enumerate(unique_key):
                sql += ("," if i > 0 else "") + f"{self.escape_identifier(key)}"
            sql += ")" # end UNIQUE
        
        sql += ")" # end CREATE TABLE
        return sql


    def create_table(self, table: str|tuple|DbObj, columns: Iterable[str|Header], *, ignore_decimal = False, ignore_not_null = False, if_not_exists = False, loglevel = logging.DEBUG):
        """
        Create a table from a list of columns.

        NOTE: This method does not intend to manage all cases, but only those usefull for zut library internals.
        """
        table = self.parse_obj(table)
        sql = self.get_create_table_query(table, columns, ignore_decimal=ignore_decimal, ignore_not_null=ignore_not_null, if_not_exists=if_not_exists)
        self._logger.log(loglevel, "Create table %s", table.unsafe)
        self.execute(sql)


    def append_column(self, table: str|tuple|DbObj, columns: list[str|Header], *, ignore_decimal = False, ignore_not_null = False, loglevel = logging.DEBUG):
        """
        Add column(s) to a table.

        NOTE: This method does not intend to manage all cases, but only those usefull for zut library internals.
        """
        table = self.parse_obj(table)

        if len(columns) > 1 and not self.can_add_several_columns:
            for column in columns:
                self.append_column(table, [column], ignore_decimal=ignore_decimal, ignore_not_null=ignore_not_null, loglevel=loglevel)
            return

        sql = f"ALTER TABLE {table.escaped}"
        sql += f" ADD "
        for i, column in enumerate(columns):
            if isinstance(column, Header):
                if column.primary_key:
                    raise NotImplementedError(f"Cannot append primary key column: {column.name}")
                if column.unique:
                    raise NotImplementedError(f"Cannot append unique column: {column.name}")
                if column.identity:
                    raise NotImplementedError(f"Cannot append identity column: {column.name}")
            sql += (',' if i > 0 else '') + self.get_sql_column_definition(column, ignore_decimal=ignore_decimal, ignore_not_null=ignore_not_null)

        self._logger.log(loglevel, "Append column%s %s to table %s", ('s' if len(columns) > 1 else '', ', '.join(str(column) for column in columns)), table.unsafe)        
        self.execute(sql)


    def alter_column_default(self, table: tuple|str|type|DbObj, columns: Header|Iterable[Header]|dict[str,Any], *, loglevel = logging.DEBUG):
        table = self.parse_obj(table)

        if isinstance(columns, Header):
            columns = [columns]
        elif isinstance(columns, dict):
            columns = [Header(name, default=value) for name, value in columns.items()]

        columns_sql = ''
        columns_names: list[str] = []
        only_reset = True
        for column in columns:
            columns_sql = (", " if columns_sql else "") + f"ALTER COLUMN {self.escape_identifier(column.name)} "
            if column.default is None:
                columns_sql += "DROP DEFAULT"
            else:
                columns_sql += f"SET DEFAULT {self.get_sql_escaped_default(column.default)}"
                only_reset = False
            columns_names.append(f'"{column.name}"')

        if not columns_sql:
            return
    
        sql = f"ALTER TABLE {table.escaped} {columns_sql}"

        self._logger.log(loglevel, "%s default for column%s %s of table %s", 'Reset' if only_reset else 'Alter', 's' if len(columns_names) > 1 else '', ', '.join(columns_names), table.unsafe)
        self.execute(sql)


    def drop_column_default(self, table: tuple|str|type, columns: Iterable[Header|str]|Header|str, *, loglevel = logging.DEBUG):
        if isinstance(columns, (Header,str)):
            columns = [columns]
        
        columns_dict = {}
        for column in columns:
            columns_dict[column.name if isinstance(column, Header) else column] = None

        return self.alter_column_default(table, columns_dict, loglevel=loglevel)
    

    def get_new_rand_table_obj(self, basename: str|None = None, *, schema = None, temp = None):
        if not basename:
            basename = '_'
        else:
            basename = slugify(basename, separator='_')[:40]
        
        if schema is None:
            if temp:
                schema = self.temp_schema

        while True:
            name = f"{basename}_{token_hex(4)}"
            obj = DbObj.parse(name, schema=schema, db=self)
            if not self.table_exists(obj):
                return obj
   

    def drop_schema(self, schema: str = None, *, if_exists = False, loglevel = logging.DEBUG):
        if self.default_schema is None:
            raise ValueError("This Db does not support schemas")
        
        if not schema:
            if self.table and self.table.schema:
                schema = self.table.schema
            else:
                schema = self.default_schema
            if not schema:
                raise ValueError("No schema defined for this Db")
        
        query = "DROP SCHEMA "
        if if_exists:
            query += "IF EXISTS "
        query += f"{self.escape_identifier(schema)}"
        
        self._logger.log(loglevel, "Drop schema %s", schema)
        self.execute(query)
    

    def create_schema(self, schema: str = None, *, if_not_exists = False, loglevel = logging.DEBUG):
        if self.default_schema is None:
            raise ValueError("This Db does not support schemas")

        if not schema:
            if self.table and self.table.schema:
                schema = self.table.schema
            else:
                schema = self.default_schema
            if not schema:
                raise ValueError("No schema defined for this Db")
        
        query = "CREATE SCHEMA "
        if if_not_exists:
            if self.scheme == 'sqlserver':
                if self.schema_exists(schema):
                    return
            else:
                query += "IF NOT EXISTS "
        query += f"{self.escape_identifier(schema)}"
        
        self._logger.log(loglevel, "Create schema %s", schema)
        self.execute(query)

    # endregion


    #region Non-Django migrations

    def migrate(self, dir: str|os.PathLike, **file_kwargs):        
        last_name = self.get_last_migration_name()

        if last_name is None:
            sql_utils = self.get_sqlutils_path()
            if sql_utils:
                self._logger.info("Deploy SQL utils ...")
                self.execute_file(sql_utils)

            self._logger.info("Create migration table ...")
            self.execute(f"CREATE TABLE _migration(id {self.int_sql_basetype} NOT NULL PRIMARY KEY {self.identity_definition_sql}, name {self.get_sql_type(str, key=True)} NOT NULL UNIQUE, deployed_utc {self.datetime_sql_basetype} NOT NULL)")
            last_name = ''
        
        for path in sorted((dir if isinstance(dir, Path) else Path(dir)).glob('*.sql')):
            if path.stem == '' or path.stem.startswith('~') or path.stem.endswith('~'):
                continue # skip
            if path.stem > last_name:
                self._apply_migration(path, **file_kwargs)

        self.connection.commit()


    def _apply_migration(self, path: Path, **file_kwargs):
        self._logger.info("Apply migration %s ...", path.stem)

        self.execute_file(path, **file_kwargs)
        self.execute(f"INSERT INTO _migration (name, deployed_utc) VALUES({self.sql_placeholder}, {self.sql_placeholder})", [path.stem, self.to_supported_value(now_naive_utc())])


    def get_last_migration_name(self) -> str|None:
        if not self.table_exists("_migration"):
            return None
        
        try:
            return self.get_val("SELECT name FROM _migration ORDER BY name DESC", limit=1)
        except NotFoundError:
            return ''

    #endregion


    #region Check if available
                
    def is_available(self, *, migration: tuple[str,str]|str = None):
        if migration:
            if isinstance(migration, tuple):
                migration_app, migration_name = migration
            else:
                pos = migration.index(':')
                migration_app = migration[:pos]
                migration_name = migration[pos+1:]
        
        try:
            with self.cursor():
                if migration:
                    from django.db.migrations.recorder import MigrationRecorder
                    recorder = MigrationRecorder(self.connection)
                    recorded_migrations = recorder.applied_migrations()
                    for an_app, a_name in recorded_migrations.keys():
                        if an_app == migration_app and a_name == migration_name:
                            return True
                    return False
                else:
                    return True
        except:
            return False
        
    #endregion


    #region Load (copy and merge)

    # ROADMAP: add option to only update selected fields
    def load_from_csv(self,
            # Main parameters
            csv_files: str|os.PathLike|TextIO|list[str|os.PathLike|TextIO],
            table: str|tuple|type|DbObj = None,
            headers: list[Header|str]|None = None,
            *,
            # Column options
            optional: str|Sequence[str]|Literal['*',True]|None = None,
            columns: dict[str,str|None]|Literal['snake']|None = None,
            # Merge options
            merge: Literal['append','truncate','recreate','auto','auto|append','auto|truncate','auto|recreate']|tuple[Header|str]|list[Header|str] = 'auto',
            scope: dict[str|Any]|None = None,
            consts: dict[str|Any] = None,
            insert_consts: dict[str|Any] = None,
            inserted_at_column: bool|str|None = None,
            updated_at_column: bool|str|None = None,
            missing_at_column: bool|str|None = None,
            foreign_keys: list[LoadForeignKey] = None,
            # Creation options
            create = False,
            create_model: str|tuple|type|list[Header] = None,
            create_pk: bool|str = False,
            create_additional: dict[str|Any]|list[Header] = None,
            # CSV format
            encoding = 'utf-8',
            delimiter: str = None,
            decimal_separator: str = None,
            quotechar = '"',
            nullval: str = None,
            no_headers: bool = None,
            # Title
            title: str|bool = None,
            interval: float|int|bool|None = None,
            src_name: str|bool|None = None,
            # Debugging
            debug = False,
            # File options
            dir: str|os.PathLike|Literal[False]|None = None,
            **kwargs) -> LoadResult:
        """
        Load CSV file(s) to a table.
        
        - `headers`: list of CSV headers to use. If not provided, headers will be determined from the first line of the first input CSV file.
        
        - `optional`: optional headers will be discared if they do not exist in the destination.

        - `merge`:
            - If `append`, data will simply be appended.
            - If `truncate`, destination table will be truncated if it already exists.
            - If a tuple (or list), reconciliate using the given header names as keys.
            - If `auto` or `auto|append` (default):
                - [`id`] if header `id` is present in the CSV headers;
                - or the first unique key found in `create_model` if given;
                - or the first unique key in the destination table;
                - or (if there is no unique key): `append`.
            - If `auto|truncate`, same as `auto` but if no key is found, truncate destination table before.

        - `create`:
            - If `True`, destination table will be created if it does not already exist.
            - If `recreate`, destination table will be droped if exist, and (re)created.

        - `create_pk`: if a non-empty string or True (means `id`), destination table will be created (if necessary) with
        an auto-generated primary key named as the value of `create_pk`, if it is not already in CSV headers.

        - `create_model`: can be a Django model, the name (or tuple) of a table, or a list of columns. If set, destination
        table will be created (if necessaray) with SQL types and unique keys matching `create_model` columns.

        - `create_additional`: can be a dictionnary (column name: default value) or a list of columns. If set, destination
        table will be created (if necessary) with these columns (in addition to those provided by `create_model` if any).

        - `consts`: set constant values when a row is inserted or updated (during a merge). If the colunm name (key of the
        dictionnary) ends with '?', there will first be a check that the column exist and the constant will be ignored
        if the column does not exist.

        - `insert_consts`: same as `consts` but only set when a row is inserted.
        """        

        from zut.db.load import Load
        return Load(self,
            csv_files = csv_files,
            table = table,
            headers = headers,
            # Column options
            optional = optional,
            columns = columns,
            # Merge options
            merge = merge,
            consts = consts,
            insert_consts = insert_consts,
            scope = scope,
            inserted_at_column = inserted_at_column,
            updated_at_column = updated_at_column,
            missing_at_column = missing_at_column,
            foreign_keys = foreign_keys,
            # Creation options
            create = create,
            create_model = create_model,
            create_pk = create_pk,
            create_additional = create_additional,
            # CSV format
            encoding = encoding,
            delimiter = delimiter,
            decimal_separator = decimal_separator,
            quotechar = quotechar,
            nullval = nullval,
            no_headers = no_headers,
            # Title and file helpers (similar to zut.load_tabular())                            
            title = title,
            interval = interval,
            src_name = src_name,
            # Debugging
            debug = debug,
            # File options
            dir = dir,
            **kwargs).execute()


    def copy_from_csv(self,
                    csv_file: Path|str|TextIO,
                    table: str|tuple|DbObj = None,
                    headers: list[Header|str] = None,
                    *,
                    buffer_size = 65536,
                    # CSV format
                    encoding = 'utf-8',
                    delimiter: str = None,
                    quotechar = '"',
                    nullval: str = None,
                    no_headers: bool = None) -> int:
        
        raise NotImplementedError() # Must be implemented by concrete Db subclasses


    def merge_table(self,
            # Main parameters
            src_table: str|tuple,
            dst_table: str|tuple|DbObj|None = None,
            *,
            # Column options
            columns: Sequence[Header|str]|Mapping[Header|str,Header|str] = None,
            # Merge options
            key: str|tuple[str]|None = None,
            scope: dict[str|Any]|None = None,
            consts: dict[str|Any]|None = None,
            insert_consts: dict[str|Any]|None = None,
            inserted_at_column: bool|str = False,
            updated_at_column: bool|str = False,
            missing_at_column: bool|str = False,
            foreign_keys: list[LoadForeignKey]|None = None,
            conversions: dict[str,str|type|Header] = {},
            # Debugging
            debug = False) -> LoadResult:

        from zut.db.load import Merge
        return Merge(self,
            # Main parameters
            src_table = src_table,
            dst_table = dst_table,
            # Column options
            columns = columns,
            key = key,
            # Merge options
            scope = scope,
            consts = consts,
            insert_consts = insert_consts,
            inserted_at_column = inserted_at_column,
            updated_at_column = updated_at_column,
            missing_at_column = missing_at_column,
            foreign_keys = foreign_keys,
            conversions = conversions,
            # Debugging
            debug = debug).execute()
        

    def get_load_auto_key(self,
            target: str|tuple|type|DbObj|list[Header],
            *,
            headers: list[str|Header]|str|os.PathLike|TextIO = None, # headers or CSV file
            columns: dict[str,str|None]|Literal['snake']|None = None, # translation of headers into column names
            # For determining headers from `headers` argument if this is actually a file
            encoding = 'utf-8',
            delimiter: str = None,
            quotechar = '"') -> tuple[str]:

        from zut.db.load import get_auto_key              
        return get_auto_key(self,
            target,
            headers=headers,
            columns=columns,
            encoding=encoding,
            delimiter=delimiter,
            quotechar=quotechar)

    #endregion


    #region Dump

    def dumper(self,               
               # DB-specific options
               table: str|tuple = None, *,
               add_autoincrement_pk: bool|str = False,
               batch: int|None = None,
               # Common TabularDumper options
               headers: Iterable[Header|Any]|None = None,
               append = False,
               archivate: bool|str|Path|None = None,
               title: str|bool|None = None,
               dst_name: str|bool = True,
               dir: str|Path|Literal[False]|None = None,
               delay: bool = False,
               defaults: dict[str,Any] = None,
               optional: str|Sequence[str]|Literal['*',True]|None = None,
               add_columns: bool|Literal['warn'] = False,
               no_tz: tzinfo|str|bool|None = None,
               # Destination mask values
               **kwargs) -> DbDumper[T_Connection, T_Cursor]:
        
        if no_tz is None:
            no_tz = self.tz

        extended_kwargs = {
                'headers': headers,
                'append': append,
                'archivate': archivate,
                'title': title,
                'dst_name': dst_name,
                'dir': dir,
                'delay': delay,
                'defaults': defaults,
                'optional': optional,
                'add_columns': add_columns,
                'no_tz': no_tz,
                **kwargs
            }

        return DbDumper(self,
                        table=table,
                        add_autoincrement_pk=add_autoincrement_pk,
                        batch_size=batch,
                        **extended_kwargs)
    
    #endregion


@dataclass(frozen=True)
class DbObj:
    name: str
    schema: str|None = None
    db: type[Db]|None = None

    def __str__(self):
        return self.escaped
    
    @cached_property
    def escaped(self):
        if not self.db:
            raise ValueError(f"Cannot use `escaped`: DbObj for \"{self.name}\" was not built with a db object")
        return f"{f'{self.db.escape_identifier(self.schema)}.' if self.schema else ''}{self.db.escape_identifier(self.name)}"
    
    @cached_property
    def full_escaped(self):
        """ Include the db default schema if none is given. """
        if not self.db:
            raise ValueError(f"Cannot use `full_escaped`: DbObj for \"{self.name}\" was not built with a db object")
        if self.schema:
            schema = self.schema
        else:
            schema = self.db.default_schema            
        return f"{f'{self.db.escape_identifier(schema)}.' if schema else ''}{self.db.escape_identifier(self.name)}"
    
    @cached_property
    def unsafe(self):
        return f"{f'{self.schema}.' if self.schema else ''}{self.name}"
    
    @classmethod
    def parse(cls, input: str|tuple|type|DbObj|None, db: Db|type[Db]|None = None, *, schema: str|None = _UNSET):
        if input is None:
            if not isinstance(db, Db):
                raise ValueError("No db given")
            if not db.table:
                raise ValueError("No table given")
            if schema is _UNSET:
                schema = db.table.schema
            name = db.table.name
        elif isinstance(input, DbObj):
            if schema is _UNSET:
                schema = input.schema
            name = input.name
        elif isinstance(input, tuple):
            if schema is _UNSET:
                schema = input[0]
            name = input[1]
        elif isinstance(input, str):
            if schema is _UNSET:
                try:
                    pos = input.index('.')
                    schema = input[0:pos]
                    name = input[pos+1:]
                except ValueError:
                    schema = None
                    name = input
            else:
                name = input
        else:
            meta = getattr(input, '_meta', None) # Django model
            if meta:
                if schema is _UNSET:
                    schema = None
                name: str = meta.db_table
            else:
                raise TypeError(f'input: {type(input).__name__}')
            
        if schema == '#': # sqlserver (temp table)
            schema = None
            name = f'#{name}'
        
        if db:
            if schema == 'temp':
                if db.temp_schema == '#':
                    schema = None
                    name = f'#{name}'
                else:
                    schema = db.temp_schema

        return DbObj(name, schema, db=type(db) if isinstance(db, Db) else db)


class CursorContext(Generic[T_Connection, T_Cursor]):
    def __init__(self, db: Db[T_Connection, T_Cursor], sql: str|None = None, params: Sequence[Any]|Mapping[str,Any]|None = None, *, warn_results: int|bool = False, messages_source: str|None = None):
        self.db = db
        self._warn_results = warn_results
        self._messages_source = messages_source
        self._messages_handler = None
        
        cursor = db.connection.cursor()
        self.cursor = cursor if self.db.scheme == 'sqlite' else cursor.__enter__() # sqlite cursors are not context managers

        self._messages_handler = self.db._register_cursor_messages_handler(cursor, self._messages_source)
        if self._messages_handler:
            self._messages_handler.__enter__()

        if sql:
            if params is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, params)

    def __enter__(self) -> T_Cursor:
        return self.cursor
    
    def __exit__(self, exc_type = None, exc_value = None, exc_traceback = None):
        if self._messages_handler:
            self._messages_handler.__exit__(exc_type, exc_value, exc_traceback)

        no_cursor_messages = getattr(self.db._log_cursor_messages, '_do_nothing', None)
        if no_cursor_messages and not self._warn_results:
            self.cursor.close()
            return

        while True: # traverse all result sets
            self.db._log_cursor_messages(self.cursor, self._messages_source)

            if self._warn_results:
                if self.cursor.description:
                    rows = []
                    there_are_more = False
                    for i, row in enumerate(iter(self.cursor)):
                        if self._warn_results is True or i < self._warn_results:
                            rows.append(row)
                        else:
                            there_are_more = True
                            break

                    if rows:
                        columns = [c[0] for c in self.cursor.description]
                        warn_text = "Unexpected result set:\n" 
                        
                        if tabulate:
                            warn_text += tabulate(rows, columns)
                        else:
                            warn_text += '\t'.join(columns)
                            for row in rows:
                                warn_text += '\n' + '\t'.join(str(val) for val in row)
                        
                        if there_are_more:
                            warn_text += "\n…"
                        logger = logging.getLogger(f"{self.db._logger.name}:{self._messages_source}") if self._messages_source else self.db._logger
                        logger.warning(warn_text)

            if self.db.scheme == 'sqlite' or not self.cursor.nextset():
                break

        self.cursor.close()


class ResultContext(CursorContext[T_Connection, T_Cursor]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._row_iterator = None
        self._row_iteration_stopped = False
        self._iterated_rows: list[TupleRow] = []

    def __enter__(self):
        return self

    @cached_property
    def headers(self):
        return self.db._get_headers_from_cursor_description(self.cursor.description)

    @cached_property
    def columns(self) -> tuple[str]:
        return tuple(c[0] for c in self.cursor.description)

    def __iter__(self):       
        return ResultIterator(self)
        
    def __bool__(self):
        try:
            next(iter(self))
            return True
        except StopIteration:
            return False

    def _next_row_values(self):
        if self._row_iterator is None:
            self._row_iterator = iter(self.cursor)
        
        if self._row_iteration_stopped:
            raise StopIteration()
    
        try:
            values = next(self._row_iterator)
        except StopIteration:
            self._input_rows_iterator_stopped = True
            raise

        return values

    def _format_row(self, values) -> TupleRow:
        transformed = None

        if self.db.tz:
            for i, value in enumerate(values):
                if isinstance(value, (datetime,time)):
                    if not value.tzinfo:
                        if transformed is None:
                            transformed = [value for value in values] if isinstance(values, tuple) else values
                        transformed[i] = value.replace(tzinfo=self.db.tz)

        row = TupleRow(transformed if transformed is not None else values)
        row.provider = ResultRowProvider(self)
        return row
    
    @property
    def rowcount(self) -> int:
        """
        Return the number of affected rows (or -1 if none).
        
        BEWARE: To get the number of rows in the result set, use `len(result)` (or `result.length`) instead.

        NOTE: Return value in case of DDL (e.g. CREATE queries) varies depending on the database: -1 for PostgreSql, Sql Server, Sqlite; 0 for MariaDB.
        """
        return self.cursor.rowcount
    
    @property
    def length(self) -> int:
        """
        Return the number of rows in the result set.
        
        To get the number of affected rows by the query, use `result.affected_rowcount` instead. 
        """
        return len(self)
    
    def __len__(self):
        """
        Return the number of rows in the result set.
        
        To get the number of affected rows by the query, use `result.affected_rowcount` instead. 
        """
        return sum(1 for _ in iter(self))
    
    @property
    def lastrowid(self):
        return self.db._get_cursor_lastrowid(self.cursor)
    
    def iter_rows(self) -> Generator[TupleRow,Any,None]:
        for row in iter(self):
            yield row
    
    def get_rows(self):
        return [row for row in self.iter_rows()]

    def get_row(self):
        iterator = iter(self)
        try:
            return next(iterator)
        except StopIteration:
            raise NotFoundError()

    def single_row(self):
        iterator = iter(self)
        try:
            result = next(iterator)
        except StopIteration:
            raise NotFoundError()
        
        try:
            next(iterator)
        except StopIteration:
            return result
        
        raise SeveralFoundError()

    def first_row(self):
        try:
            return self.get_row()
        except NotFoundError:
            return None
    
    def iter_dicts(self) -> Generator[dict[str,Any],Any,None]:
        for row in iter(self):
            yield {column: row[i] for i, column in enumerate(self.columns)}
    
    def get_dicts(self):
        return [data for data in self.iter_dicts()]

    def get_dict(self):
        iterator = self.iter_dicts()
        try:
            return next(iterator)
        except StopIteration:
            raise NotFoundError()

    def single_dict(self):
        iterator = self.iter_dicts()
        try:
            result = next(iterator)
        except StopIteration:
            raise NotFoundError()
        
        try:
            next(iterator)
        except StopIteration:
            return result
        
        raise SeveralFoundError()

    def first_dict(self):
        try:
            return self.first_dict()
        except NotFoundError:
            return None

    def get_vals(self):
        """A convenience function for returning the first column of each row from the query."""
        return [row[0] for row in iter(self)]

    def get_val(self):
        """A convenience function for returning the first column of the first row from the query. Raise NotFoundError if there is no row."""
        return self.get_row()[0]

    def single_val(self):
        """A convenience function for returning the first column of the first row from the query. Raise NotFoundError if there is no row or SeveralFound if there are more than one row."""
        return self.single_row()[0]

    def first_val(self):
        """A convenience function for returning the first column of the first row from the query. Raise None if there is no row."""
        row = self.get_row()
        if row is None:
            return None
        return row[0]
    
    def tabulate(self):
        if not self.cursor.description:
            return "No result"
        
        rows = self.get_rows()
        if tabulate:
            return tabulate(rows, self.columns)
        else:
            text = '\t'.join(self.columns)
            for row in rows:
                text += '\n' + '\t'.join(str(val) for val in row)
            return text
    
    def print_tabulate(self, *, file = sys.stdout, max_length: int|None = None):
        text = self.tabulate()
        if max_length is not None and len(text) > max_length:
            text = text[0:max_length-1] + '…'
        file.write(text)

    #ROADMAP pipe: rename as 'pipe' and make 'ResultContext' a Loader object
    def to_dumper(self, dumper: TabularDumper|TextIO|str|os.PathLike, close=True, **kwargs):
        """
        Send results to the given tabular dumper.
        
        If dumper is `tab`, `csv`, a stream or a str/path, create the appropriate Tab/CSV/Excel dumper.
        
        Return a tuple containing the list of columns and the number of exported rows.
        """
        if isinstance(dumper, TabularDumper):
            if dumper.headers is not None:
                if [header.name for header in dumper.headers] != self.columns:
                    raise ValueError("Invalid headers in given dumper")
            else:
                dumper.headers = self.headers
        else:
            dumper = tabular_dumper(dumper, headers=self.headers, **kwargs)

        try:
            for row in iter(self):
                dumper.dump(row)        
            return self.columns, dumper.count
        finally:
            if close:
                dumper.close()


class ResultRowProvider:
    def __init__(self, context: ResultContext):
        self._db = context.db
        self._cursor_description = context.cursor.description

    @cached_property
    def headers(self):
        return self._db._get_headers_from_cursor_description(self._cursor_description)

    @cached_property
    def columns(self) -> tuple[str]:
        return tuple(c[0] for c in self._cursor_description)
    

class ResultIterator(Generic[T_Connection, T_Cursor]):
    def __init__(self, context: ResultContext[T_Connection, T_Cursor]):
        self.context = context
        self.next_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.next_index < len(self.context._iterated_rows):
            row = self.context._iterated_rows[self.next_index]
        else:
            values = self.context._next_row_values()
            row = self.context._format_row(values)
            self.context._iterated_rows.append(row)
        
        self.next_index += 1
        return row


class DbDumper(TabularDumper[Db[T_Connection, T_Cursor]]):
    """ 
    Line-per-line INSERT commands (to be used when `InsertSqlDumper` is not available).
    """
    def __init__(self, origin: Db[T_Connection, T_Cursor]|T_Connection|ParseResult|dict,
                 table: str|tuple|DbObj|None = None,
                 *,
                 add_autoincrement_pk: bool|str = False,
                 batch_size: int|None = None,
                 **kwargs):
        
        if isinstance(origin, Db):
            dst = origin
            self._close_dst = False
        else:
            dst = get_db(origin, autocommit=False)
            self._close_dst = True
        
        if table:
            self._table = dst.parse_obj(table)
        elif dst.table:
            self._table = dst.table
        else:
            raise ValueError("Table name not provided")

        dst_name = kwargs.pop('dst_name', None)
        if not dst_name:
            dst_name = self._table.unsafe

        super().__init__(dst, dst_name=dst_name, **kwargs)

        self._add_autoincrement_pk = 'id' if add_autoincrement_pk is True else add_autoincrement_pk
        self._insert_sql_headers: list[Header] = []
        self._insert_sql_single: str = None
        self._insert_sql_batch: str = None
        if self.dst.scheme == 'sqlite':
            self._max_params = 999
        elif self.dst.scheme == 'sqlserver':
            self._max_params = 2100
        else:
            self._max_params = 65535 # postgresql limit
        self.batch_size = batch_size

        self._cursor = None
        self._batch_rows = []
        self._executed_batch_count = 0

        self._insert_table = self._table

    @property
    def cursor(self):
        """
        Reused cursor (only for inserting data).
        """
        if self._cursor is None:
            self._cursor = self.dst.connection.cursor()
        return self._cursor

    def close(self, *final_queries):
        """
        Export remaining rows, execute optional final SQL queries, and then close the dumper.
        """
        super().close()

        self.flush(*final_queries)

        if self._cursor is not None:
            self._cursor.close()
            self._cursor = None       

        if not self.dst.get_autocommit():
            self.dst.connection.commit()

        if self._close_dst:
            self.dst.close()

    def _build_insert_sqls(self, additional_headers: list[Header]):
        self._insert_sql_headers += additional_headers

        into_sql = self._insert_table.escaped

        into_sql += "("
        values_sql = "("
        need_comma = False
        for header in self._insert_sql_headers:
            if need_comma:
                into_sql += ","
                values_sql += ","
            else:
                need_comma = True
            into_sql += f"{self.dst.escape_identifier(header.name)}"
            values_sql += self.dst.sql_placeholder
        into_sql += ")"
        values_sql += ")"

        max_batch = int(self._max_params / len(self._insert_sql_headers))
        if self.batch_size is None or max_batch < self.batch_size:
            self.batch_size = max_batch

        self._insert_sql_single = f"INSERT INTO {into_sql} VALUES {values_sql}"
        self._insert_sql_batch = f"INSERT INTO {into_sql} VALUES "
        for i in range(self.batch_size):
            self._insert_sql_batch += (',' if i > 0 else '') + values_sql

    def open(self) -> list[Header]|None:
        # Called at first exported row, before headers are analyzed.
        # Return list of existing headers if table exists, None if not.
        if self.dst.table_exists(self._table):
            if not self.append:
                self.dst.clear_table(self._table)
            
            headers = [header for header in self.dst.get_headers(self._table) if not header.identity]
            self._build_insert_sqls(headers)
            return headers
        else:
            return None
    
    def export_headers(self, headers: list[Header]):
        # Called at first exported row, if there are no pre-existing headers (= table does not exist) => create table
        columns = [header for header in headers]
        
        if self._add_autoincrement_pk and not any(header.name == self._add_autoincrement_pk for header in headers):
            columns.insert(0, Header(name=self._add_autoincrement_pk, type=int, primary_key=True, identity=True))

        self.dst.create_table(self._table, columns)

        self._build_insert_sqls(headers)

    def new_headers(self, headers: list[Header]) -> bool|None:
        self.dst.append_column(self._table, headers, ignore_not_null=True)
        self._build_insert_sqls(headers)
        return True

    def _ensure_opened(self):
        if not self.headers:
            raise ValueError(f"Cannot dump to db without headers")
        super()._ensure_opened()

    def _convert_value(self, value: Any):
        value = super()._convert_value(value)
        value = self.dst.to_supported_value(value)
        return value

    def export(self, row: list):
        self._batch_rows.append(row)
        if len(self._batch_rows) >= self.batch_size:
            self._export_batch()

    def _export_batch(self):
        kwargs = {}
        if self.dst.scheme == 'postgresql':
            kwargs['prepare'] = True
            
        inlined_row = []
        while len(self._batch_rows) / self.batch_size >= 1:
            for row in self._batch_rows[:self.batch_size]:
                inlined_row += row
                
            if self._logger.isEnabledFor(logging.DEBUG):
                t0 = time_ns()
                if self._executed_batch_count == 0:
                    self._d_total = 0
            
            self.cursor.execute(self._insert_sql_batch, inlined_row, **kwargs)
            self._executed_batch_count += 1

            if self._logger.isEnabledFor(logging.DEBUG):
                t = time_ns()
                d = t - t0
                self._d_total += d
                self._logger.debug(f"Batch {self._executed_batch_count}: {self.batch_size:,} rows inserted in {d/1e6:,.1f} ms (avg: {self._d_total/1e3/(self._executed_batch_count * self.batch_size):,.1f} ms/krow, inst: {d/1e3/self.batch_size:,.1f} ms/krow)")
            
            self._batch_rows = self._batch_rows[self.batch_size:]

    def flush(self, *final_queries):
        """
        Export remaining rows, and then execute optional final SQL queries.
        """
        super().flush()

        kwargs = {}
        if self.dst.scheme == 'postgresql':
            kwargs['prepare'] = True
        
        self._ensure_opened()
        self._export_batch()

        if self._batch_rows:
            if self._logger.isEnabledFor(logging.DEBUG):
                t0 = time_ns()

            for row in self._batch_rows:
                while len(row) < len(self._insert_sql_headers):
                    row.append(None)
                self.cursor.execute(self._insert_sql_single, row, **kwargs)
                            
            if self._logger.isEnabledFor(logging.DEBUG):
                d = time_ns() - t0
                self._logger.debug(f"Remaining: {len(self._batch_rows):,} rows inserted one by one in {d/1e6:,.1f} ms ({d/1e3/(len(self._batch_rows)):,.1f} ms/krow)")

            self._batch_rows.clear()

        for final_query in final_queries:
            self.dst.execute(final_query)


class NotFoundError(_BaseNotFoundError): # Status code 404
    def __init__(self, message: str = None):
        super().__init__(message if message else "Not found")


class SeveralFoundError(Exception): # Status code 409 ("Conflict")
    def __init__(self, message: str = None):
        super().__init__(message if message else "Several found")


def _get_connection_from_wrapper(db):    
    if type(db).__module__.startswith(('django.db.backends.', 'django.utils.connection')):
        return db.connection
    elif type(db).__module__.startswith(('psycopg_pool.pool',)):
        return db.connection()
    elif type(db).__module__.startswith(('psycopg2.pool',)):
        return db.getconn()
    else:
        return db


def get_db(origin, *, autocommit=True) -> Db:
    """
    Create a new Db instance (if origin is not already one).
    - `autocommit`: commit transactions automatically (applies only for connections created by the Db instance).
    """
    from zut.db.mariadb import MariaDb
    from zut.db.postgresql import PostgreSqlDb
    from zut.db.postgresqlold import PostgreSqlOldDb
    from zut.db.sqlite import SqliteDb
    from zut.db.sqlserver import SqlServerDb

    if isinstance(origin, str):
        db_cls = get_db_class(origin)
        if db_cls is None:
            raise ValueError(f"Invalid db url: {origin}")
        return db_cls(origin, autocommit=autocommit)
    
    elif isinstance(origin, dict) and 'ENGINE' in origin: # Django
        engine = origin['ENGINE']
        if engine in {"django.db.backends.postgresql", "django.contrib.gis.db.backends.postgis"}:
            if not PostgreSqlDb.missing_dependency:
                return PostgreSqlDb(origin, autocommit=autocommit)
            elif not PostgreSqlOldDb.missing_dependency:
                return PostgreSqlOldDb(origin, autocommit=autocommit)
            else:
                raise ValueError(f"PostgreSql and PostgreSqlOld not available (psycopg missing)")
        elif engine in {"django.db.backends.mysql", "django.contrib.gis.db.backends.mysql"}:
            return MariaDb(origin, autocommit=autocommit)
        elif engine in {"django.db.backends.sqlite3", "django.db.backends.spatialite"}:
            return SqliteDb(origin, autocommit=autocommit)
        elif engine in {"mssql"}:
            return SqlServerDb(origin, autocommit=autocommit)
        else:
            raise ValueError(f"Invalid db: unsupported django db engine: {engine}")
        
    elif isinstance(origin, Db):
        return origin
    
    else:
        db_cls = get_db_class(origin)
        if db_cls is None:
            raise ValueError(f"Invalid db: unsupported origin type: {type(origin)}")
        return db_cls(origin)
    

def get_db_class(origin: Connection|ParseResult|str) -> type[Db]|None:
    from zut.db.mariadb import MariaDb
    from zut.db.postgresql import PostgreSqlDb
    from zut.db.postgresqlold import PostgreSqlOldDb
    from zut.db.sqlite import SqliteDb
    from zut.db.sqlserver import SqlServerDb

    if isinstance(origin, str):
        origin = urlparse(origin)

    if isinstance(origin, ParseResult):
        if origin.scheme in {'postgresql', 'postgres', 'pg'}:
            if not PostgreSqlDb.missing_dependency:
                db_cls = PostgreSqlDb
            elif not PostgreSqlOldDb.missing_dependency:
                db_cls = PostgreSqlOldDb
            else:
                raise ValueError(f"PostgreSql and PostgreSqlOld not available (psycopg missing)")
        elif origin.scheme in {'mariadb', 'mysql'}:
            db_cls = MariaDb
        elif origin.scheme in {'sqlite', 'sqlite3'}:
            db_cls = SqliteDb
        elif origin.scheme in {'sqlserver', 'sqlservers', 'mssql', 'mssqls'}:
            db_cls = SqlServerDb
        else:
            return None
    else: # origin is assumed to be a connection object
        origin = _get_connection_from_wrapper(origin)

        type_fullname: str = type(origin).__module__ + '.' + type(origin).__qualname__
        if type_fullname == 'psycopg2.extension.connection':
            db_cls = PostgreSqlOldDb
        elif type_fullname == 'psycopg.Connection':
            db_cls = PostgreSqlDb
        elif type_fullname == 'MySQLdb.connections.Connection':
            db_cls = MariaDb
        elif type_fullname == 'sqlite3.Connection':
            db_cls = SqliteDb
        elif type_fullname == 'pyodbc.Connection':
            db_cls = SqlServerDb
        else:
            return None
    
    if db_cls.missing_dependency:
        raise ValueError(f"Cannot use db {db_cls} (missing {db_cls.missing_dependency} dependency)")
    
    return db_cls
