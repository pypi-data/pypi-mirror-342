from __future__ import annotations

import os
import sys
from contextlib import contextmanager
from datetime import datetime, tzinfo
from decimal import Decimal
from ipaddress import IPv4Address, IPv6Address
from sqlite3 import Connection, Cursor, connect
from typing import Any, Iterable
from urllib.parse import ParseResult, unquote, urlparse

from zut import build_url
from zut.db import Db, DbObj


class SqliteDb(Db[Connection, Cursor]):
    """
    Database adapter for SQLite 3 (using driver included in python3).
    """
    scheme = 'sqlite'
    default_schema = None
    split_multi_statement_files = True
    table_in_path = False # URL may be a path
    sql_placeholder = '?'
    sql_named_placeholder = ':%s'
    bool_sql_basetype = 'integer'
    int_sql_basetype = 'integer'
    float_sql_basetype = 'real'
    decimal_sql_basetype = 'text'
    datetime_sql_basetype = 'real'
    date_sql_basetype = 'text'
    uuid_sql_basetype = 'text'
    accept_aware_datetime = False
    identity_definition_sql = 'AUTOINCREMENT'
    truncate_with_delete = True
    can_cascade_truncate = False
    temp_schema = 'temp'

    # Configurable globally
    mkdir = False
    

    def __init__(self, origin: Connection|str|os.PathLike|ParseResult|dict|None = None, *, mkdir: bool = None, name: str = None, user: str = None, password: str = None, host: str = None, port: str = None, password_required: bool = False, autocommit: bool = None, tz: tzinfo|str|None = None, migrations_dir: str|os.PathLike = None, table: str|tuple|DbObj|None = None):
        if origin is None:
            origin = getattr(self.__class__, 'origin', None)

        if isinstance(origin, str) and not origin.startswith(('sqlite:', 'sqlite3:')) and origin.endswith(('.db','.sqlite','.sqlite3')):
            self._file = origin.replace('\\', '/')
            origin = build_url(scheme='sqlite', path=self._file)
        elif isinstance(origin, os.PathLike):
            self._file = origin.as_posix()
            origin = build_url(scheme='sqlite', path=self._file)
        else:
            self._file = None

        super().__init__(origin, name=name, user=user, password=password, host=host, port=port, password_required=password_required, autocommit=autocommit, tz=tz, migrations_dir=migrations_dir, table=table)

        self.mkdir = mkdir if mkdir is not None else self.__class__.mkdir


    @contextmanager
    def _create_transaction(self):
        self.connection.execute("BEGIN")
        try:
            yield None
            self.connection.execute("COMMIT")
        except:
            self.connection.execute("ROLLBACK")
            raise


    def _get_cursor_lastrowid(self, cursor: Cursor):
        return cursor.lastrowid
    

    @property
    def file(self):
        if self._file is None:
            url = self.get_url(hide_password=True)
            self._file = unquote(urlparse(url).path)
        return self._file

    
    @property
    def is_port_opened(self):
        from zut import files
        return files.exists(self._file)
   

    def _create_connection(self):
        if self.mkdir:
            from zut import files
            dir_path = files.dirname(self.file)
            if dir_path:
                files.makedirs(dir_path, exist_ok=True)

        if sys.version_info < (3, 12): # Sqlite connect()'s autocommit parameter introduced in Python 3.12
            return connect(self.file, isolation_level=None if self._autocommit else 'DEFERRED')
        else:
            return connect(self.file, autocommit=self._autocommit)
        

    def get_autocommit(self):
        if sys.version_info < (3, 12): # Sqlite connect()'s autocommit parameter introduced in Python 3.12
            return self._autocommit
        else:
            return super().get_autocommit()
    

    def _get_cursor_lastrowid(self, cursor: Cursor):
        return cursor.lastrowid
    

    def _get_url_from_connection(self):
        seq, name, file = self.get_tuple("PRAGMA database_list")
        return build_url(scheme=self.scheme, path=file)


    def table_exists(self, table: str|tuple|DbObj = None) -> bool:
        table = self.parse_obj(table)
        
        if table.schema == 'temp':
            query = "SELECT COUNT(*) FROM sqlite_temp_master WHERE type = 'table' AND name = ?"
        elif not table.schema:
            query = "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table' AND name = ?"
        else:
            raise ValueError(f'Cannot use schema "{table.schema}"')
        
        return self.get_val(query, [table.name]) > 0
        

    def _get_headers_data_from_table(self, table: DbObj, *, minimal: bool) -> Iterable[dict[str,Any]]:
        # Build main query
        sql = f"""
SELECT
    c.cid AS "ordinal"
	,c.name
	,CASE WHEN c."notnull" = 1 THEN 1 ELSE 0 END AS not_null
	,lower(c."type") AS sql_type
	,null AS "precision"
	,null AS "scale"
	,c.pk AS primary_key	
	,CASE WHEN lower(c."type") = 'integer' AND c.pk = 1 AND lower(t."sql") LIKE '%autoincrement%' THEN 1 ELSE 0 END AS "identity" -- For sqlite, AUTOINCREMENT columns are necessarily INTEGER PRIMARY KEY columns
	,c.dflt_value AS "default"
FROM {'temp' if table.schema == 'temp' else 'main'}.pragma_table_info(?) c
LEFT OUTER JOIN sqlite{'_temp' if table.schema == 'temp' else ''}_master t ON t.name = ?
ORDER BY c.cid
"""
        
        columns_by_name: dict[str,dict[str,Any]] = {}
        if not minimal:
            pk: list[str] = []
        for data in self.get_dicts(sql, [table.name, table.name]):
            if not minimal and data['primary_key'] == 1:
                pk.append(data['name'])
            columns_by_name[data['name']] = data

        if not minimal:
            unique_keys_by_column: dict[str, list[list[str]]] = {}

            for column in pk:
                unique_keys_by_column[column] = [pk]

            for index_name in self.get_vals(f'SELECT name FROM {"temp" if table.schema == "temp" else "main"}.pragma_index_list(?) WHERE "unique" = 1', [table.name]):
                index_columns = self.get_vals(f'SELECT name FROM {"temp" if table.schema == "temp" else "main"}.pragma_index_info(?) ORDER BY seqno', [index_name])
                for column in index_columns:
                    if not column in unique_keys_by_column:
                        unique_keys_by_column[column] = [index_columns]
                    else:
                        unique_keys_by_column[column].append(index_columns)
            
            for data in columns_by_name.values():
                if data['name'] in unique_keys_by_column:
                    unique_keys = unique_keys_by_column[data['name']]
                    if any(unique_key == [data['name']] for unique_key in unique_keys):
                        data['unique'] = True
                    else:
                        data['unique'] = sorted(unique_keys, key=lambda unique_key: [columns_by_name[name]['ordinal'] for name in unique_key])
                else:
                    data['unique'] = False

        for data in columns_by_name.values():
            yield data


    def to_supported_value(self, value: Any):
        if isinstance(value, (IPv4Address,IPv6Address)):
            return value.compressed
        elif isinstance(value, Decimal):
            return str(value)
        elif isinstance(value, datetime):
            datetime_sql_basetype = self.datetime_sql_basetype.lower()
            if 'int' in datetime_sql_basetype:
                return int(value.timestamp())
            elif 'real' in datetime_sql_basetype or 'float' in datetime_sql_basetype or 'double' in datetime_sql_basetype or 'decimal' in datetime_sql_basetype:
                return value.timestamp()
            else:
                return value.isoformat()
        else:
            return super().to_supported_value(value)
