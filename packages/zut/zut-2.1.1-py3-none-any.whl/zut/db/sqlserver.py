from __future__ import annotations

from datetime import date, datetime, time
from decimal import Decimal
import logging
import re
from typing import Any, TYPE_CHECKING, Iterable
from urllib.parse import unquote, urlparse
from uuid import UUID

from zut import build_url
from zut.db import Db, DbObj

if TYPE_CHECKING:
    from pyodbc import Connection, Cursor

try:
    from pyodbc import connect, drivers
    _missing_dependency = None
except ModuleNotFoundError:
    _missing_dependency = "pyodbc"


class SqlServerDb(Db[Connection, Cursor] if TYPE_CHECKING else Db):
    """
    Database adapter for Microsoft SQL Server (using `pyodbc` driver).
    """
    scheme = 'sqlserver' # or sqlservers (if encrypted)
    default_port = 1433
    default_schema = 'dbo'
    identifier_quotechar_begin = '['
    identifier_quotechar_end = ']'
    sql_placeholder = '?'
    sql_named_placeholder = ':%s'
    only_positional_params = True
    split_multi_statement_files = True
    identity_definition_sql = 'IDENTITY'
    bool_sql_basetype = 'bit'
    datetime_sql_basetype = 'datetime'
    str_precised_sql_basetype = 'varchar'
    uuid_sql_basetype = 'uniqueidentifier'
    accept_aware_datetime = False
    procedure_caller = 'EXEC'
    procedure_params_parenthesis = False
    can_cascade_truncate = False
    can_add_several_columns = True
    function_requires_schema = True
    temp_schema = '#'
    missing_dependency = _missing_dependency

    def _create_connection(self):
        def escape(s):
            if ';' in s or '{' in s or '}' in s or '=' in s:
                return "{" + s.replace('}', '}}') + "}"
            else:
                return s
        
        r = urlparse(self._connection_url)
        
        server = unquote(r.hostname) or '(local)'
        if r.port:
            server += f',{r.port}'

        # Use "ODBC Driver XX for SQL Server" if available ("SQL Server" seems not to work with LocalDB, and takes several seconds to establish connection on my standard Windows machine with SQL Server Developer).
        driver = "SQL Server"
        for a_driver in sorted(drivers(), reverse=True):
            if re.match(r'^ODBC Driver \d+ for SQL Server$', a_driver):
                driver = a_driver
                break

        connection_string = 'Driver={%s};Server=%s;Database=%s;' % (escape(driver), escape(server), escape(r.path.lstrip('/')))

        if r.username:
            connection_string += 'UID=%s;' % escape(unquote(r.username))
            if r.password:
                connection_string += 'PWD=%s;' % escape(unquote(r.password))
        else:
            connection_string += 'Trusted_Connection=yes;'
            
        encrypt = self._connection_encrypt if self._connection_encrypt is not None else r.scheme in {'mssqls', 'sqlservers'}
        connection_string += f"Encrypt={'yes' if encrypt else 'no'};"
        return connect(connection_string, autocommit=self._autocommit)


    def _get_url_from_connection(self):
        with self.cursor() as cursor:
            cursor.execute("SELECT @@SERVERNAME, local_tcp_port, SUSER_NAME(), DB_NAME() FROM sys.dm_exec_connections WHERE session_id = @@spid")
            host, port, user, dbname = next(iter(cursor))
        return build_url(scheme=self.scheme, username=user, hostname=host, port=port, path='/'+dbname)


    def _get_cursor_lastrowid(self, cursor: Cursor):
        cursor.execute("SELECT @@IDENTITY")
        return next(iter(cursor))[0]


    def _paginate_splited_select_query(self, selectpart: str, orderpart: str, *, limit: int|None, offset: int|None) -> str:
        if orderpart:
            result = f"{selectpart} {orderpart} OFFSET {offset or 0} ROWS"
            if limit is not None:
                result += f" FETCH NEXT {limit} ROWS ONLY"
            return result
        elif limit is not None:
            if offset is not None:
                raise ValueError("an ORDER BY clause is required for OFFSET")
            return f"SELECT TOP {limit} * FROM ({selectpart}) s"
        else:
            return selectpart


    def _log_cursor_messages(self, cursor, messages_source: str|None):
        if cursor.messages:                        
            for nature, message in cursor.messages:
                level, message = self.parse_notice(nature, message)
                logger = logging.getLogger(f'{self._logger.name}:{messages_source}') if messages_source else self._logger
                logger.log(level, message)


    def table_exists(self, table: str|tuple|DbObj = None) -> bool:
        table = self.parse_obj(table)

        if table.name.startswith('#'):
            object_fullname = self.escape_literal(f'tempdb..{self.escape_identifier(table.name)}')
            return self.get_val(f"SELECT CASE WHEN EXISTS(SELECT 1 FROM tempdb.sys.tables WHERE object_id = OBJECT_ID({object_fullname})) THEN 1 ELSE 0 END") == 1
        else:
            return self.get_val("SELECT CASE WHEN EXISTS(SELECT 1 FROM information_schema.tables WHERE table_schema = ? AND table_name = ?) THEN 1 ELSE 0 END", [table.schema or self.default_schema, table.name]) == 1
   
    
    def schema_exists(self, schema: str = None) -> bool:
        if not schema:
            schema = self.schema or self.default_schema

        return self.get_val("SELECT CASE WHEN EXISTS(SELECT 1 FROM information_schema.schemata WHERE schema_name = ?) THEN 1 ELSE 0 END", [schema]) == 1


    def get_type(self, type_info: type|str) -> type|None:
        if isinstance(type_info, int):
            raise TypeError("SqlServer type_info cannot be an integer")
        elif isinstance(type_info, str):
            result = self.type_mapping.get(type_info)
            if result is not None:
                return result
        return super().get_type(type_info)
        

    def _get_headers_data_from_table(self, table: DbObj, *, minimal: bool) -> Iterable[dict[str,Any]]:
        if table.name.startswith('#'):
            object_fullname = self.escape_literal(f'tempdb..{self.escape_identifier(table.name)}')
            sys_schema = 'tempdb.sys'
        else:
            object_fullname = self.escape_literal(table.full_escaped)
            sys_schema = 'sys'

        sql = ""

        if not minimal:
            sql = f"""
WITH primary_key AS (
	SELECT ic.column_id
	FROM {sys_schema}.indexes i
	INNER JOIN {sys_schema}.index_columns ic ON ic.object_id = i.object_id AND ic.index_id = i.index_id
	WHERE i.is_primary_key = 1
	AND i.object_id = OBJECT_ID({object_fullname})
)
,unique_index_detail AS (
	SELECT
		i.index_id
		,c.name AS column_name
		,ic.key_ordinal AS column_order_in_index
		,ic.column_id AS column_order_in_table
	FROM {sys_schema}.indexes i
	INNER JOIN {sys_schema}.index_columns ic ON ic.object_id = i.object_id AND ic.index_id = i.index_id
	INNER JOIN {sys_schema}.columns c ON c.object_id = ic.object_id AND c.column_id = ic.column_id  
	WHERE i.object_id = OBJECT_ID({object_fullname}) AND i.is_unique = 1
)
,unique_index_column AS (
	SELECT
		index_id
		,string_agg(column_name, ',') WITHIN GROUP (ORDER BY column_order_in_index) AS column_names
	FROM unique_index_detail
	GROUP BY
		index_id
)
,unique_index_order AS (
	SELECT
		index_id
		,string_agg(RIGHT('000'+CAST(column_order_in_table AS VARCHAR(3)),3), ',') WITHIN GROUP (ORDER BY column_order_in_table) AS index_order
	FROM unique_index_detail
	GROUP BY
		index_id
)
,unique_index AS (
	SELECT
		i.index_id
		,ic.column_names
		,io.index_order
	FROM (
		SELECT
			i.index_id
		FROM unique_index_detail i
		GROUP BY
			i.index_id
	) i
	INNER JOIN unique_index_column ic ON ic.index_id = i.index_id
	INNER JOIN unique_index_order io ON io.index_id = i.index_id
)
,column_unique AS (
	SELECT
		column_name AS name
		,string_agg(x.column_names, ';') WITHIN GROUP (ORDER BY x.index_order) AS [unique]
	FROM unique_index_detail d
	INNER JOIN unique_index x ON x.index_id = d.index_id
	GROUP BY
		column_name
)
"""

        sql += """
SELECT
	s.*
	,type_info + CASE
		WHEN [precision] IS NOT NULL AND [scale] IS NOT NULL THEN CONCAT('(', [precision],',', [scale], ')')
		WHEN [precision] IS NOT NULL THEN CONCAT('(', [precision], ')')
		ELSE ''
	END AS sql_type
FROM (
	SELECT
		c.column_id AS [ordinal]
		,c.name
	    ,t.name AS type_info
		,CASE WHEN c.collation_name IS NOT NULL THEN concat(' COLLATE ', c.collation_name) ELSE '' END AS sql_type_suffix
	    ,CASE
	        WHEN t.name IN ('char', 'varchar', 'binary', 'varbinary') THEN c.[max_length]
	        WHEN t.name IN ('nchar', 'nvarchar') THEN c.[max_length] / 2
	        WHEN t.name = 'datetime2' THEN c.[scale]
	        WHEN t.name IN ('numeric', 'decimal') THEN c.[precision]
	    END AS [precision]
	    ,CASE
	            WHEN t.name IN ('numeric', 'decimal') THEN c.[scale]
	    END AS [scale]
	    ,CASE WHEN c.is_nullable = 0 THEN 1 ELSE 0 END AS not_null
	    ,c.is_identity AS [identity]
	    ,OBJECT_DEFINITION(c.default_object_id) AS [default]
"""

        if not minimal:
            sql += """
	    ,CASE WHEN c.column_id IN (SELECT column_id FROM primary_key) THEN 1 ELSE 0 END AS [primary_key]
	    ,COALESCE(u.[unique], '') AS [unique]
"""
        
        sql += f"""
    FROM {sys_schema}.columns c
    LEFT OUTER JOIN {sys_schema}.types t ON t.user_type_id = c.system_type_id
"""
        
        if not minimal:
            sql += """
    LEFT OUTER JOIN column_unique u ON u.name = c.name
"""

        sql += f"""
    WHERE c.object_id = OBJECT_ID({object_fullname})
) s
ORDER BY [ordinal]
"""
        return self.get_dicts(sql)
 

    @classmethod
    def parse_notice(cls, nature: str, message: str) -> tuple[int, str]:
        m = re.match(r"^\[Microsoft\]\[[\w\d ]+\]\[SQL Server\](.+)$", message)
        if m:
            message = m[1]

        if nature == '[01000] (0)':
            nature = 'PRINT'
        elif nature == '[01000] (50000)':
            nature = 'RAISERROR'
        elif nature == '[01003] (8153)': # Avertissement : la valeur NULL est éliminée par un agrégat ou par une autre opération SET
            return logging.INFO, message
        
        m = re.match(r'^\[?(?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL)\s?[\]\:](?P<message>.+)$', message, re.DOTALL|re.IGNORECASE)
        if m:
            return getattr(logging, m['level']), m['message'].lstrip()
        
        if nature == 'PRINT':
            return logging.INFO, message
        else:
            return logging.WARNING, message
        
    type_mapping = {
        'bigint': int,
        'binary': bytes,
        'bit': bool,
        'char': str,
        'date': date,
        'datetime': datetime,
        'datetime2': datetime,
        'datetimeoffset': None,
        'decimal': Decimal,
        'float': float,
        'geography': None,
        'geometry': None,
        'hierarchyid': None,
        'image': None,
        'int': int,
        'money': Decimal,
        'nchar': str,
        'ntext': str,
        'numeric': Decimal,
        'nvarchar': str,
        'real': float,
        'smalldatetime': datetime,
        'smallint': int,
        'smallmoney': Decimal,
        'sql_variant': None,
        'sysname': None,
        'text': str,
        'time': time,
        'timestamp': bytearray,
        'tinyint': int,
        'uniqueidentifier': UUID,
        'varbinary': bytes,
        'varchar': str,
        'xml': None,
    }
