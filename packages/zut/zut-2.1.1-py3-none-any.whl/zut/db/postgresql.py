from __future__ import annotations

import logging
import os
import re
from contextlib import contextmanager, nullcontext
from datetime import date, datetime, time
from decimal import Decimal
from io import IOBase
from random import randint
from typing import TYPE_CHECKING, Any, Iterable, TextIO
from urllib.parse import ParseResult
from uuid import UUID

from zut import (Header, build_url, examine_csv_file,
                 get_default_decimal_separator, get_logger, skip_utf8_bom)
from zut.db import Db, DbObj

if TYPE_CHECKING:
    from psycopg import Connection, Cursor

try:
    from psycopg import connect
    from psycopg.errors import Diagnostic
    _missing_dependency = None
except ModuleNotFoundError:
    _missing_dependency = "psycopg"


class PostgreSqlDb(Db[Connection, Cursor] if TYPE_CHECKING else Db):
    """
    Database adapter for PostgreSQL (using `psycopg` (v3) driver).

    This is also the base class for :class:`PostgreSqlOldAdapter` (using `psycopg2` (v2) driver).
    """
    scheme = 'postgresql'
    default_port = 5432
    missing_dependency = _missing_dependency
    

    def _verify_scheme(self, r: ParseResult) -> ParseResult|None:
        # See: https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING
        if r.scheme == 'postgresql':
            return r
        elif r.scheme in {'pg', 'postgres'}:
            return r._replace(scheme='postgresql')
        else:
            return None
    

    @contextmanager
    def _register_cursor_messages_handler(self, cursor: Cursor, messages_source: str|None):
        handler = lambda diag: self._notice_handler(diag, messages_source)
        try:
            cursor.connection.add_notice_handler(handler)
            yield
        finally:
            cursor.connection.remove_notice_handler(handler)


    def _notice_handler(self, diag: Diagnostic, messages_source: str|None = None):
        """
        Handler required by psycopg 3 `connection.add_notice_handler()`.
        """
        # determine level
        level, message = self.parse_message(diag.severity_nonlocalized, diag.message_primary)
        
        # determine logger by parsing context
        if diag.context:
            m = re.match(r"^[\s\w/]+ (\w+)\(", diag.context, re.IGNORECASE)
            if m:
                # English example: "PL/pgSQL function test_callproc(text,integer,smallint) line 3 at RAISE"
                messages_source = m[1] # we replace default messages_source
        logger = get_logger(f'{self._logger.name}:{messages_source}') if messages_source else self._logger

        # write log
        logger.log(level, message)


    @classmethod
    def parse_message(cls, severity: str, message: str) -> tuple[int, str]:
        m = re.match(r'^\[?(?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL)[\]\:](?P<message>.+)$', message, re.DOTALL)
        if m:
            return getattr(logging, m['level']), m['message'].lstrip()

        if severity.startswith('DEBUG'): # not sent to client (by default)
            return logging.DEBUG, message
        elif severity == 'LOG': # not sent to client (by default), written on server log (LOG > ERROR for log_min_messages)
            return logging.DEBUG, message
        elif severity == 'NOTICE': # sent to client (by default) [=client_min_messages]
            return logging.DEBUG, message
        elif severity == 'INFO': # always sent to client
            return logging.INFO, message
        elif severity == 'WARNING': # sent to client (by default) [=log_min_messages]
            return logging.WARNING, message
        elif severity in ['ERROR', 'FATAL']: # sent to client
            return logging.ERROR, message
        elif severity in 'PANIC': # sent to client
            return logging.CRITICAL, message
        else:
            return logging.WARNING, message
    

    def _get_cursor_lastrowid(self, cursor: Cursor):
        cursor.execute("SELECT lastval()")
        return next(iter(cursor))[0]
    

    def _create_connection(self):
        return connect(self._connection_url, autocommit=self._autocommit)
    

    def _create_transaction(self):
        return self.connection.transaction()
    

    def _get_url_from_connection(self):
        with self.cursor() as cursor:
            cursor.execute("SELECT session_user, inet_server_addr(), inet_server_port(), current_database()")
            user, host, port, dbname = next(iter(cursor))
        return build_url(scheme=self.scheme, username=user, hostname=host, port=port, path='/'+dbname)
    

    def table_exists(self, table: str|tuple|DbObj = None) -> bool:
        table = self.parse_obj(table)

        if table.schema in {self.temp_schema, 'temp'}:
            return self.get_val("SELECT EXISTS (SELECT FROM pg_tables WHERE schemaname LIKE 'pg_temp_%%' AND tablename = %s)", [table.name])
        else:
            return self.get_val("SELECT EXISTS (SELECT FROM pg_tables WHERE schemaname = %s AND tablename = %s)", [table.schema or self.default_schema, table.name])
    
    
    def schema_exists(self, schema: str = None) -> bool:
        if not schema:
            schema = self.schema or self.default_schema

        query = "SELECT EXISTS (SELECT FROM pg_namespace WHERE nspname = %s)"
        return self.get_val(query, [schema])


    def get_type(self, type_info: type|int|str) -> type|None:
        if isinstance(type_info, int):
            element = self.type_catalog.get(type_info)
            return element[1] if element else None
        else:
            return super().get_type(type_info)
    

    def _get_headers_data_from_table(self, table: DbObj, *, minimal: bool) -> Iterable[dict[str,Any]]:
        object_fullname = self.escape_literal(table.full_escaped)

        sql = ""

        if not minimal:
            sql = f"""
WITH primary_key AS (
	SELECT i.indkey
	FROM pg_index i
	WHERE i.indisprimary
	AND i.indrelid = {object_fullname}::regclass
)
,unique_index AS (
	SELECT
		index_id
		,array_agg(column_order_in_table ORDER BY column_order_in_table) AS index_order
		,array_agg("column" ORDER BY column_order_in_index) AS column_names
        ,string_agg("column", ',' ORDER BY column_order_in_index) AS column_names_str
	FROM (
		SELECT
			i.indexrelid AS index_id
		    ,k.i AS column_order_in_index
		    ,k.attnum AS column_order_in_table
		    ,a.attname AS "column"
		FROM pg_index i
		CROSS JOIN LATERAL unnest(i.indkey) WITH ORDINALITY AS k(attnum, i)
		INNER JOIN pg_attribute AS a ON a.attrelid = i.indrelid AND a.attnum = k.attnum
		WHERE i.indrelid = {object_fullname}::regclass AND i.indisunique
	) s
	GROUP BY index_id
)
,column_unique AS (
	SELECT
		column_name AS name
        ,string_agg(column_names_str, ';' ORDER BY index_order) AS "unique"
	FROM unique_index i, unnest(i.column_names) AS column_name
	GROUP BY
		column_name
)
"""

        sql += """
SELECT
	attname AS name
    ,format_type(atttypid, atttypmod) AS sql_type
	,atttypid AS type_info
	,CASE
		WHEN atttypmod = -1 THEN null
		WHEN atttypid IN (1042, 1043) THEN atttypmod - 4 -- char, varchar
        WHEN atttypid IN (1560, 1562) THEN atttypmod -- bit, varbit
        WHEN atttypid IN (1083, 1114, 1184, 1266) THEN atttypmod -- time, timestamp, timestamptz, timetz
		WHEN atttypid = 1700 THEN -- numeric (decimal)
			CASE
				WHEN atttypmod = -1 THEN null
	            ELSE ((atttypmod - 4) >> 16) & 65535
	        END
	END AS "precision"
	,CASE
		WHEN atttypmod = -1 THEN null
		WHEN atttypid = 1700 THEN -- numeric (decimal)
	        CASE 
	            WHEN atttypmod = -1 THEN null       
	            ELSE (atttypmod - 4) & 65535  
	        END
	END AS "scale"
	,attnotnull AS not_null
	,a.attidentity != '' AS "identity"
    ,pg_get_expr(d.adbin, d.adrelid) AS "default"
"""

        if not minimal:
            sql += """
    ,COALESCE(a.attnum = ANY((SELECT indkey FROM primary_key)::smallint[]), false) AS "primary_key"
    ,COALESCE(u."unique", '') AS "unique"
"""
        
        sql += f"""
FROM pg_attribute a
LEFT OUTER JOIN pg_attrdef d ON (d.adrelid, d.adnum) = (a.attrelid, a.attnum)
"""
        
        if not minimal:
            sql += """
LEFT OUTER JOIN column_unique u ON u.name = a.attname
"""

        sql += f"""
WHERE a.attnum > 0 AND NOT a.attisdropped AND a.attrelid = {object_fullname}::regclass
ORDER BY attnum
"""
        return self.get_dicts(sql)


    def copy_from_csv(self,
                    csv_file: str|os.PathLike|TextIO,
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
        
        # Prepare table argument
        table = self.parse_obj(table)
            
        # Determine CSV and headers parameters
        if not delimiter or (not headers and not no_headers):
            examined_columns, examined_delimiter, _ = examine_csv_file(csv_file, encoding=encoding, delimiter=delimiter, quotechar=quotechar, force_delimiter=False)
            if not delimiter:
                delimiter = examined_delimiter or get_default_decimal_separator()
            if not headers and not no_headers:
                headers = examined_columns

        if headers:
            headers = [header if isinstance(header, Header) else Header(header) for header in headers]

        # Prepare SQL statement                        
        sql = f"COPY {table.escaped}"

        if headers:
            sql += " ("
            for i, header in enumerate(headers):
                sql += (", " if i > 0 else "") + self.escape_identifier(header.name)
            sql += ")"
            
        sql += f" FROM STDIN (FORMAT csv, ENCODING {self.escape_literal('utf-8' if encoding == 'utf-8-sig' else encoding)}, DELIMITER {self.escape_literal(delimiter)}, QUOTE {self.escape_literal(quotechar)}, ESCAPE {self.escape_literal(quotechar)}"
        if nullval is not None:
            sql += f", NULL {self.escape_literal(nullval)}"
        if not no_headers:
            sql += ", HEADER match"
        sql += ")"
        
        # Execute SQL statement
        with nullcontext(csv_file) if isinstance(csv_file, IOBase) else open(csv_file, "rb") as fp:
            skip_utf8_bom(fp)
            
            with self.cursor() as cursor:
                self._actual_copy_from_csv(cursor, sql, fp, buffer_size)
                return cursor.rowcount
            

    def _actual_copy_from_csv(self, cursor: Cursor, sql: str, fp: TextIO, buffer_size: int):
        with cursor.copy(sql) as copy: # type: ignore
            while True:
                data = fp.read(buffer_size)
                if not data:
                    break
                copy.write(data)


    def enforce_id_seq_offset(self, app_label: str|None = None, *, min_offset: int|None = None, max_offset: int|None = None):
        """
        Ensure the given model (or all models if none is given) have sequence starting with a minimal value.
        This leaves space for custom, programmatically defined values.

        Unless `min_offset` and `max_offset` are specified, the minimal value is randomly chosen between 65537 (after
        max uint16 value) and 262144 (max uint18 value).

        Compatible with postgresql only.
        """
        if min_offset is None and max_offset is None:
            min_offset = 65537
            max_offset = 262144
        elif max_offset is None:
            max_offset = min_offset
        elif min_offset is None:
            min_offset = min(65537, max_offset)

        sql = f"""
    SELECT
        s.schema_name
        ,s.table_name
        ,s.column_names
        ,s.sequence_name
        ,q.seqstart AS sequence_start
    FROM (
        -- List all PKs with their associated sequence name (or NULL if this is not a serial or identity column)
        SELECT
            n.nspname AS schema_name
            ,c.relnamespace AS schema_oid
            ,c.relname AS table_name
            ,array_agg(a.attname) AS column_names
            ,substring(pg_get_serial_sequence(n.nspname || '.' || c.relname, a.attname), length(n.nspname || '.') + 1) AS sequence_name
        FROM pg_index i
        INNER JOIN pg_class c ON c.oid = i.indrelid
        INNER JOIN pg_namespace n ON n.oid = c.relnamespace
        INNER JOIN pg_attribute a ON a.attrelid = c.oid AND a.attnum = any(i.indkey)
        WHERE i.indisprimary
        GROUP BY
            n.nspname
            ,c.relnamespace
            ,c.relname
            ,substring(pg_get_serial_sequence(n.nspname || '.' || c.relname, a.attname), length(n.nspname || '.') + 1)
    ) s
    LEFT OUTER JOIN pg_class c ON c.relnamespace = s.schema_oid AND c.relname = s.sequence_name
    LEFT OUTER JOIN pg_sequence q ON q.seqrelid = c.oid
    WHERE s.schema_name = 'public' AND s.table_name {"LIKE %s" if app_label else "IS NOT NULL"} AND q.seqstart = 1
    ORDER BY schema_name, table_name, column_names
    """
        params = [f'{app_label}_%'] if app_label else None

        seqs = []
        with self.cursor() as cursor:
            for row in cursor.execute(sql, params):
                seqs.append({'schema': row[0], 'table': row[1], 'column': row[2][0], 'name': row[3]})

        with self.cursor() as cursor:
            for seq in seqs:
                sql = f"SELECT MAX({self.escape_identifier(seq['column'])}) FROM {self.escape_identifier(seq['schema'])}.{self.escape_identifier(seq['table'])}"
                cursor.execute(sql)
                max_id = cursor.fetchone()[0] or 0
                
                start_value = max(max_id + 1, randint(min_offset, max_offset))
                self._logger.debug("Set start value of %s to %s", seq['name'], start_value)
                sql = f"ALTER SEQUENCE {self.escape_identifier(seq['name'])} START WITH {start_value} RESTART WITH {start_value}"
                cursor.execute(sql)


    type_catalog = {
        16: ('bool', bool),
        17: ('bytea', bytes),
        18: ('char', str),
        19: ('name', str),
        20: ('int8', int),
        21: ('int2', int),
        23: ('int4', int),
        25: ('text', str),
        26: ('oid', int),
        114: ('json', None),
        650: ('cidr', None),
        700: ('float4', float),
        701: ('float8', float),
        869: ('inet', None),
        1042: ('bpchar', str),
        1043: ('varchar', str),
        1082: ('date', date),
        1083: ('time', time),
        1114: ('timestamp', datetime),
        1184: ('timestamptz', datetime),
        1186: ('interval', None),
        1266: ('timetz', time),
        1700: ('numeric', Decimal),
        2249: ('record', None),
        2950: ('uuid', UUID),
        3802: ('jsonb', None),
        3904: ('int4range', None),
        3906: ('numrange', None),
        3908: ('tsrange', None),
        3910: ('tstzrange', None),
        3912: ('daterange', None),
        3926: ('int8range', None),
        4451: ('int4multirange', None),
        4532: ('nummultirange', None),
        4533: ('tsmultirange', None),
        4534: ('tstzmultirange', None),
        4535: ('datemultirange', None),
        4536: ('int8multirange', None),
    }
