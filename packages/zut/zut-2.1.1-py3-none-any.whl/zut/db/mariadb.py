from __future__ import annotations

from contextlib import contextmanager
from datetime import date, datetime, time
from decimal import Decimal
from typing import TYPE_CHECKING, Any, Generator, Iterable
from urllib.parse import unquote, urlparse

from zut import Header
from zut.db import Db, DbObj

if TYPE_CHECKING:
    from MySQLdb import Connection
    from MySQLdb.cursors import Cursor

try:
    from MySQLdb import connect
    _missing_dependency = None
except ModuleNotFoundError:
    _missing_dependency = "mysqlclient"


class MariaDb(Db[Connection, Cursor] if TYPE_CHECKING else Db):
    """
    Database adapter for MariaDB and Mysql.
    """
    scheme = 'mariadb'
    default_port = 3306
    default_schema = None
    identifier_quotechar_begin = '`'
    identifier_quotechar_end = '`'
    identity_definition_sql = 'AUTO_INCREMENT'
    float_sql_basetype = 'double'
    decimal_sql_basetype = 'decimal'
    datetime_sql_basetype = 'datetime(6)'
    str_precised_sql_basetype = 'varchar'
    accept_aware_datetime = False        
    can_cascade_truncate = False
    temp_schema = 'temp'
    missing_dependency = _missing_dependency
    
    def _create_connection(self):        
        r = urlparse(self._connection_url)
        
        kwargs = {}
        if r.hostname:
            kwargs['host'] = unquote(r.hostname)
        if r.port:
            kwargs['port'] = r.port
        
        path = r.path.lstrip('/')
        if path:
            kwargs['database'] = unquote(path)

        if r.username:
            kwargs['user'] = unquote(r.username)
        if r.password:
            kwargs['password'] = unquote(r.password)
        
        return connect(**kwargs, sql_mode='STRICT_ALL_TABLES', autocommit=self._autocommit)

    
    def get_autocommit(self):
        if not self._connection:
            return self._autocommit
        else:
            return self._connection.get_autocommit()


    @contextmanager
    def _create_transaction(self):
        with self.connection.cursor() as cursor:
            cursor.execute("START TRANSACTION")
        try:
            yield None
            with self.connection.cursor() as cursor:
                cursor.execute("COMMIT")
        except:
            with self.connection.cursor() as cursor:
                cursor.execute("ROLLBACK")
            raise


    def _get_cursor_lastrowid(self, cursor: Cursor):
        return cursor.lastrowid
    

    def table_exists(self, table: str|tuple|DbObj = None) -> bool:        
        table = self.parse_obj(table)

        query = "SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = %s)"
        params = [table.name]

        return self.get_val(query, params) == 1
    

    def get_type(self, type_info: type|int|str) -> type|None:
        if isinstance(type_info, int):
            element = self.type_catalog.get(type_info)
            return element[1] if element else None
        else:
            return super().get_type(type_info)
        

    def _get_headers_data_from_table(self, table: DbObj, *, minimal: bool) -> Iterable[dict[str,Any]]:
        sql = f"SHOW COLUMNS FROM {table.escaped}"

        columns: list[dict[str,Any]] = []
        any_multi = False
        pk: list[dict[str,Any]] = []
        for data in self.get_dicts(sql):
            name = data['Field']

            column_data = {
                'name': name,
                'sql_type': data['Type'].lower(),
                'not_null': data['Null'] == 'NO',
                'primary_key': data['Key'] == 'PRI',
                'identity': 'auto' in data['Extra'],
            }

            if not minimal:
                if data['Key'] == 'PRI':
                    pk.append(column_data)
                elif data['Key'] == 'UNI':
                    column_data['unique'] = True
                elif data['Key'] == 'MUL':
                    any_multi = True
                    column_data['unique'] = [(name, '?')]
                else:
                    column_data['unique'] = False

            columns.append(column_data)

        if not any_multi:
            if pk:
                if len(pk) == 1:
                    pk[0]['unique'] = True
                else:
                    any_multi = True
            if not any_multi:                    
                return columns

        # Find multi-column unique keys
        sql = f"SHOW INDEX FROM {table.escaped} WHERE Non_unique = 0"

        columns_by_name: dict[str,dict[str,Any]] = {}
        for column in columns:
            columns_by_name[column['name']] = column
            #Reset unique
            column['unique'] = False

        columns_by_index: dict[str,list[str]] = {}
        for data in self.get_dicts(sql):
            if data['Key_name'] in columns_by_index:
                names = columns_by_index[data['Key_name']]
            else:
                names = []
                columns_by_index[data['Key_name']] = names                
            names.append(data['Column_name'])

        for names in columns_by_index.values():
            for name in names:
                column = columns_by_name[name]
                if len(names) == 1:
                    column['unique'] = True
                elif not column['unique']:
                    column['unique'] = [names]
                else:
                    column['unique'].append(tuple(names))

        return columns


    # See: MySQLdb.constants.FIELD_TYPE
    type_catalog = {
        0: ('decimal', Decimal),
        1: ('tiny', int),
        2: ('short', int),
        3: ('long', int),
        4: ('float', float),
        5: ('double', float),
        6: ('null', None),
        7: ('timestamp', None),
        8: ('longlong', int), # bigint
        9: ('int24', None),
        10: ('date', date),
        11: ('time', time),
        12: ('datetime', datetime),
        13: ('year', None),
        14: ('newdate', None),
        15: ('varchar', str),
        16: ('bit', None),
        246: ('newdecimal', Decimal),
        247: ('interval', None),
        248: ('set', None),
        249: ('tiny_blob', None),
        250: ('medium_blob', None),
        251: ('long_blob', None),
        252: ('blob', None),
        253: ('var_string', str),
        254: ('string', str),
        255: ('geometry', None),
    }
