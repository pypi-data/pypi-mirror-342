"""
Infrastructure for db.load_from_csv() and db.merge_table().

ROADMAP: allow compilation to stored procedure.
"""
from __future__ import annotations

import logging
import os
from collections import abc
from contextlib import contextmanager, nullcontext
from datetime import datetime, timedelta
from decimal import Decimal
from io import IOBase
from time import time_ns
from typing import Any, Iterable, Mapping, Sequence, TextIO, Tuple
from uuid import UUID

from zut import (Header, Literal, examine_csv_file, files, cached_property,
                 get_default_csv_delimiter, get_default_decimal_separator,
                 get_tzkey, slugify_snake)

from zut.db import Db, DbObj


class Load:
    csv_files: list[str|os.PathLike|TextIO]
    table: DbObj

    headers: list[Header]|None
    """ CSV headers (or `None` if CSV does not have any header, in this case the table must already exist and have the columns in the same order as the CSV file). """

    header_columns: dict[str,str|None]|None
    """ Associate CSV headers to table column names (or `None` if CSV does not have any header). By default the column name is identical to the CSV header name. """

    table_headers_by_name: dict[str,Header]

    foreign_keys_by_column: dict[str,LoadForeignKey]
    
    key: tuple[str]|None
    init: Literal['create','drop','truncate']|None
    conversions: dict[str,Header]

    _cache: AutoKeyCache|None

    def __init__(self, db: Db,
                    # Main parameters
                    csv_files: str|os.PathLike|TextIO|list[str|os.PathLike|TextIO],
                    table: str|tuple|type|DbObj|None = None,
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
                    create_model: str|tuple|type|DbObj|list[Header] = None,
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
                    **kwargs):
        
        self.db = db

        # Source
        if isinstance(csv_files, (str,os.PathLike,IOBase)):
            csv_files = [csv_files]
        if not csv_files:
            raise ValueError("csv_files cannot be empty")
        for i in range(len(csv_files)):
            if not isinstance(csv_files[i], IOBase):
                if dir is not False:
                    csv_files[i] = files.in_dir(csv_files[i], dir, title=title, **kwargs)
        self.csv_files = csv_files
        
        # Destination
        model = None
        if not table:
            if not self.db.table:
                raise ValueError("No table given")
            self.table = self.db.parse_obj(table)
        elif isinstance(table, (str,tuple)):
            self.table = self.db.parse_obj(table)
        elif isinstance(table, type): # Django split_obj
            model = table
            self.table = self.db.parse_obj(table._meta.db_table)
        else:
            raise TypeError(f"table: {table}")
    
        # Merge action
        self.key = None
        self.init = None
        self._cache = None
        if merge is None or (isinstance(merge, str) and merge in {'auto', 'auto|append', 'auto|truncate', 'auto|recreate'}):
            self._cache = get_auto_key(self.db, model or self.table, headers=headers or self.csv_files[0], columns=columns, encoding=encoding, delimiter=delimiter, quotechar=quotechar)
            if len(self._cache) >= 1:
                self.key = self._cache
            elif 'recreate' in merge:
                self.init = 'drop'
            elif 'truncate' in merge:
                self.init = 'truncate'
        elif isinstance(merge, (list,tuple)):
            self.key = tuple(column.name if isinstance(column, Header) else column for column in merge)            
            for i, column in enumerate(self.key):
                if not isinstance(column, str):
                    raise TypeError(f"merge[{i}]: {type(column).__name__}")
        elif isinstance(merge, str):
            if merge == 'recreate':
                self.init = 'drop'
            elif merge == 'truncate':
                self.init = 'truncate'
            elif merge == 'append':
                self.init = None
            else:
                raise ValueError(f"Invalid merge value: {merge}")
        else:
            raise TypeError(f"merge: {type(merge).__name__}")
        
        # CSV parameters and headers
        if not delimiter:
            if self._cache is not None:
                delimiter = self._cache._delimiter

        if not delimiter or (not headers and not no_headers):
            examined_columns, examined_delimiter, _ = examine_csv_file(self.csv_files[0], encoding=encoding, delimiter=delimiter, quotechar=quotechar, force_delimiter=False)
            if not delimiter:
                delimiter = examined_delimiter or get_default_decimal_separator()
            if not headers and not no_headers:
                headers = examined_columns
                    
        if not decimal_separator:
            decimal_separator = get_default_decimal_separator(csv_delimiter=delimiter)

        if not headers and self._cache is not None:
            headers = self._cache._headers

        if not headers and not no_headers:
            raise ValueError("No headers found")

        self.encoding = encoding
        self.delimiter = delimiter
        self.decimal_separator = decimal_separator
        self.quotechar = quotechar
        self.nullval = nullval

        if headers:
            self.headers = [header if isinstance(header, Header) else Header(header) for header in headers]
            if columns is None:
                self.header_columns = {h.name: h.name for h in self.headers}
            elif columns == 'snake':
                self.header_columns = {h.name: slugify_snake(h.name) for h in self.headers}
            elif isinstance(columns, dict):
                self.header_columns = columns
                for header in self.headers:
                    if not header.name in columns: # defaults
                        self.header_columns[header.name] = header.name
            else:
                raise TypeError(f"columns: {type(columns).__name__}")
        else:
            self.headers = None
            self.header_columns = None

        # Determine if we must (re)create the destination table
        if self._cache is not None and self._cache._target_table_exists is not None and self._cache._target == self.table:
            table_exists = self._cache._target_table_exists
        else:
            table_exists = self.db.table_exists(self.table)

        if not table_exists:
            if create:
                self.init = 'create'
            else:
                raise ValueError(f"Table does not exist: {self.table.unsafe}")
        
        # Determine and format foreign keys
        if foreign_keys is None and self.headers:
            foreign_keys = _get_load_foreign_keys(self.db, model or self.table, self.header_columns.values())

        self.foreign_keys_by_column = {}
        if foreign_keys:
            for foreign_key in foreign_keys:
                for column in foreign_key.origin_columns:
                    self.foreign_keys_by_column[column] = foreign_key
                # Transform the key from source column to destination table, if necessary
                if self.key and all(column for column in foreign_key.origin_columns if column in self.key):
                    new_key = []
                    pk_added = False
                    for column in self.key:
                        if column in foreign_key.origin_columns:
                            if not pk_added:
                                new_key.append(foreign_key.origin_pk)
                                pk_added = True
                        else:
                            new_key.append(column)
                    self.key = new_key
        
        # Determinate destination columns
        if optional:
            if optional == '*':
                optional = True
            elif isinstance(optional, str):
                optional = {optional}
            elif optional is not True:
                optional = set(optional)
        else:
            optional = False
            
        if self.init in {'create', 'drop'}:
            self.prepare_columns_for_new_table(create_model=create_model, create_additional=create_additional, create_pk=create_pk)
        else:
            self.prepare_columns_for_existing_table(optional=optional)

        self.scope = scope
        self.consts = self.select_consts(consts)
        self.insert_consts = self.select_consts(insert_consts)

        if inserted_at_column is True or (inserted_at_column is None and self.headers and 'inserted_at' in self.table_headers_by_name and not 'inserted_at' in self.header_columns.values()):
            inserted_at_column = 'inserted_at'
        self.inserted_at_column = inserted_at_column
        if updated_at_column is True or (updated_at_column is None and self.headers and 'updated_at' in self.table_headers_by_name and not 'updated_at' in self.header_columns.values()):
            updated_at_column = 'updated_at'
        self.updated_at_column = updated_at_column
        if missing_at_column is True or (missing_at_column is None and self.headers and 'missing_at' in self.table_headers_by_name and not 'missing_at' in self.header_columns.values()):
            missing_at_column = 'missing_at'
        self.missing_at_column = missing_at_column
        
        # Determine if we must perform conversions at load time
        self.conversions = {}
        if self.headers:
            for header in self.headers:
                if header.type:
                    column = self.header_columns.get(header.name)
                    if issubclass(header.type, (float,Decimal)) :
                        if decimal_separator != '.':
                            self.conversions[column] = header
                    elif issubclass(header.type, datetime):
                        if self.db.tz:
                            self.conversions[column] = header

        # Title
        self.title = title
        self.interval = interval
        self.src_name = src_name

        # Debugging
        self.debug = debug

    def prepare_columns_for_new_table(self, *,
                    create_model,
                    create_pk,
                    create_additional):
        """
        Set `table_headers_by_name` and `header_columns` when the destination table will be created for us.
        """
        if not self.headers:
            raise ValueError(f"Cannot create table without headers")

        # Prepare `create_model` attributes
        if create_model:
            if isinstance(create_model, (str,tuple,type)):
                create_model = self.db.parse_obj(create_model)
            elif not isinstance(create_model, (DbObj,list)):
                raise TypeError(f"create_model: {type(create_model).__name__}")
            
            if self._cache is not None and self._cache._target_headers_by_name is not None and self._cache._target == create_model:
                create_model_headers_by_name = self._cache._target_headers_by_name
            else:
                create_model_headers_by_name = _get_target_headers_by_name(self.db, create_model)

        # Iterate over CSV headers and columns
        self.table_headers_by_name = {}
        for header in self.headers:
            column = self.header_columns.get(header)
            if not column:
                continue

            # Adapt headers to `create_model`
            if create_model:
                create_model_header = create_model_headers_by_name.get(column)
                if create_model_header:
                    if create_model_header.identity:
                        raise ValueError("Cannot load an identity column")
                    header.merge(create_model_header)
        
            # Ensure a unique key is created for the merge key
            if self.key:
                if column in self.key:
                    if not header.unique:
                        header.unique = [self.key]
                    elif isinstance(header.unique, list):
                        if not self.key in header.unique:
                            header.unique.append(self.key)

            # Determine the column(s) matching the header in the table: this is the column name, except if there is a foreign key translation
            foreign_key = self.foreign_keys_by_column.get(column)
            if foreign_key:
                if foreign_key.origin_pk not in self.table_headers_by_name:
                    self.table_headers_by_name[column] = Header(foreign_key.origin_pk, type=foreign_key.pk_type)
            else:
                self.table_headers_by_name[column] = header

        if create_additional:
            if isinstance(create_additional, dict):
                create_additional: list[Header] = [Header(name, default=default, not_null=default is not None) for (name, default) in create_additional.items()]
            elif isinstance(create_additional, list):
                for i in range(len(create_additional)):
                    if not isinstance(create_additional[i], Header):
                        create_additional[i] = Header(create_additional)
            else:
                raise TypeError(f"create_additional: {type(create_additional).__name__}")

            for column in create_additional:
                if not column.name in self.table_headers_by_name:
                    self.table_headers_by_name[column.name] = column

        if create_pk:
            if create_pk is True:
                create_pk = 'id'
            elif not isinstance(create_pk, str):
                raise TypeError(f"create_pk: {type(create_pk).__name__}")
            pk_found = False

            for header in self.headers:
                if header.primary_key or header.name == create_pk:
                    pk_found = True
                    header.primary_key = True

            if not pk_found:
                pk_column = Header(create_pk, primary_key=True, identity=True, sql_type='bigint')
                self.table_headers_by_name = {pk_column.name: pk_column, **self.table_headers_by_name}
    
    def prepare_columns_for_existing_table(self, *, optional: bool|set[str]):
        """
        Set `table_headers_by_name` and `header_columns` when the destination table exists.

        Also ensure update headers with types from existing destination table.
        """
        if self._cache is not None and self._cache._target_headers_by_name is not None and self._cache._target == self.table:
            self.table_headers_by_name = self._cache._target_headers_by_name
        else:
            self.table_headers_by_name = {column.name: column for column in self.db.get_headers(self.table, minimal=True)}

        # Remove optional columns
        if self.headers:
            for header in self.headers:
                column = self.header_columns.get(header.name)
                if not column:
                    continue # header is explicitly disabled

                table_header = self.table_headers_by_name.get(column)
                if table_header:
                    table_header.unique = None # Not needed and generate an exception if the header names are translated into distinct column names
                    header.merge(table_header)
                else:
                    foreign_key = self.foreign_keys_by_column.get(column)
                    if foreign_key:
                        pass
                    elif optional and (optional is True or header.name in optional):
                        self.header_columns[header.name] = None # column will be discarded

    def select_consts(self, consts: dict[str,Any]):
        """
        Select consts matching destination columns.
        """
        if consts is None:
            return {}
        
        selected_consts = {}
        for name, value in consts.items():
            is_optional = name.endswith('?')
            actual_name = name[:-1] if is_optional else name
            if actual_name in self.header_columns.values():
                raise ValueError(f"Cannot use const '{actual_name}': set from CSV headers")
            if is_optional:
                if not actual_name in self.table_headers_by_name:
                    continue # skip
            else:
                if self.init in {'create', 'drop'}:
                    self.table_headers_by_name[actual_name] = Header(actual_name, type=self.db.get_sql_type(type(value)), not_null=value is not None)
                else:
                    raise ValueError(f"Cannot use const '{actual_name}': missing in destination table")
            selected_consts[actual_name] = value
        return selected_consts
    
    @cached_property
    def reconciliate_table(self):
        """
        Determine if we need to use an intermediate table for reconciliation. If yes, return its schema and name.
        """
        if (self.key and not self.init) or any(column for column in self.header_columns if column is None) or self.conversions or self.consts or self.insert_consts or self.foreign_keys_by_column or self.inserted_at_column or self.updated_at_column or self.missing_at_column:        
            if not self.headers:
                raise ValueError(f"Cannot create reconciliation table if the source has no CSV headers")
            if self.debug:
                self.db.create_schema('debug', if_not_exists=True)
            return self.db.get_new_rand_table_obj('_reconciliate', schema='debug' if self.debug else 'temp')
        else:
            return None

    def execute(self) -> LoadResult:
        self.check_csv_files()

        with self.db.transaction() if not self.debug else nullcontext():
            self.before_title()

            # Initialize destination table if needed
            if self.init == 'create':            
                if self.table.schema:
                    self.db.create_schema(self.table.schema, if_not_exists=True)
                self.db.create_table(self.table, self.table_headers_by_name.values())
            elif self.init == 'drop':
                self.db.drop_table(self.table)
                self.db.create_table(self.table, self.table_headers_by_name.values())
            if self.init == 'truncate':
                self.db.clear_table(self.table, truncate=True)
            
            try:
                # Prepare intermediate table if we're reconciliating
                if self.reconciliate_table:
                    reconciliate_headers = [Header(header.name, sql_type=self.db.str_sql_basetype if header.name in self.conversions else header.sql_type) for header in self.headers]
                    self.db.create_table(self.reconciliate_table, reconciliate_headers)
                
                # Perform actual copy of CSV files
                copy_rowcount = 0
                for csv_file in self.csv_files:
                    if self.reconciliate_table:
                        copy_target = self.reconciliate_table
                    else:
                        copy_target = self.table
                    self.db._logger.debug(f"Load {copy_target.unsafe} from csv file {csv_file}")
                    copy_rowcount += self.db.copy_from_csv(csv_file, copy_target, self.headers, encoding=self.encoding, delimiter=self.delimiter, quotechar=self.quotechar, nullval=self.nullval, no_headers=self.headers is None)

                # Merge from intermediate table to destination table if we're reconciliating
                if self.reconciliate_table:
                    if self.db._logger.isEnabledFor(logging.DEBUG):
                        self.db._logger.debug(f"Merge {self.reconciliate_table.unsafe} to {self.table.unsafe}" + (f" using key {', '.join(self.key)}" if self.key else ''))
                    
                    merge = Merge(self.db,
                                    src_table=self.reconciliate_table,
                                    src_headers=reconciliate_headers,
                                    dst_table=self.table,
                                    columns={header: column for header, column in self.header_columns.items() if column is not None},
                                    key=self.key,
                                    scope=self.scope,
                                    consts=self.consts,
                                    insert_consts=self.insert_consts,
                                    inserted_at_column=self.inserted_at_column,
                                    updated_at_column=self.updated_at_column,
                                    missing_at_column=self.missing_at_column,
                                    foreign_keys=set(self.foreign_keys_by_column.values()),
                                    conversions=self.conversions
                                )
                    result = merge.execute()
                else:
                    result = LoadResult()
                    result.inserted_count = copy_rowcount
            finally:
                if not self.debug:
                    if self.reconciliate_table:
                        self.db.drop_table(self.reconciliate_table, if_exists=True)
        
        self.after_title(result)
        return result

    def check_csv_files(self):
        for csv_file in self.csv_files:
            if isinstance(csv_file, IOBase):
                continue
            if not files.exists(csv_file):
                raise FileNotFoundError(f"Input CSV file does not exist: {csv_file}")

    def before_title(self):
        if self.src_name is None or self.src_name is True:
            if len(self.csv_files) == 1:
                if isinstance(self.csv_files[0], IOBase):
                    self.src_name = False if self.src_name is None else getattr(self.csv_files[0], 'name', f'<{type(self.csv_files[0]).__name__}>')
                else:
                    self.src_name = self.csv_files[0]
            else:
                self.src_name = f"{len(self.csv_files)} files"
                
        if self.interval is None:
            self.interval = False
        elif self.interval is True:
            self.interval = 1.0  #ROADMAP: auto growing from 1.0 to 60.0                       
        self._t0 = time_ns() if self.interval is not False else None
        
        self.db._logger.log(logging.INFO if self.title else logging.DEBUG, f"Load{f' {self.title} to' if self.title and self.title is not True else ''} table {self.table.unsafe}{f' from {self.src_name}' if self.src_name else ''} …")
        
    def after_title(self, result: LoadResult):
        message = f"{result.upserted_count:,}{f' {self.title}' if self.title and self.title is not True else ''} rows loaded{f' from {self.src_name}' if self.src_name else ''}"
        if result.updated_count is not None:
            message += f" (inserted: {result.inserted_count:,} - updated: {result.updated_count:,}"
            if result.missing_count is not None:
                message += f' - missing: {result.missing_count:,}'
            if result.restored_count is not None:
                message += f' - restored: {result.restored_count:,}'
            message += ')'

        if self._t0 is not None:
            seconds = (time_ns() - self._t0) / 1E9
            message += f" in {seconds:,.3f} seconds" if seconds < 60 else f" in {timedelta(seconds=int(seconds))}"

        self.db._logger.log(logging.INFO if self.title else logging.DEBUG, message)


class Merge:
    #region Init
    src_table: DbObj
    dst_table: DbObj

    columns: dict[str,str]
    key: tuple[str]|None
    foreign_key_helpers: list[Merge.ForeignKeyHelper]

    def __init__(self, db: Db, 
            # Main parameters           
            src_table: str|tuple|DbObj,
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
            foreign_keys: Iterable[LoadForeignKey]|None = None,
            conversions: dict[str,str|type|Header] = {},
            # Caching/debugging
            src_headers: list[Header]|None = None,
            debug = False):
        
        self.db = db

        # Prepare table arguments
        self.src_table = self.db.parse_obj(src_table)
        self._src_headers_by_name = {h.name: h for h in src_headers} if src_headers is not None else None

        if not dst_table:
            if not self.db.table:
                raise ValueError("No table given")
            dst_table = self.db.table
        self.dst_table = self.db.parse_obj(dst_table)

        # Prepare columns argument
        if columns:
            if isinstance(columns, abc.Mapping):
                self.columns = {src_column.name if isinstance(src_column, Header) else src_column: dst_column.name if isinstance(dst_column, Header) else dst_column for src_column, dst_column in columns.items()}
            else:
                self.columns = {column.name if isinstance(column, Header) else column: column.name if isinstance(column, Header) else column for column in columns}
        else:
            self.columns = {column: column for column in self.db.get_columns(self.src_table)}

        # Other arguments
        if key and isinstance(key, str):
            key = (key,)
        self.key = key

        if inserted_at_column is True:
            inserted_at_column = 'inserted_at'
        self.inserted_at_column = inserted_at_column        
        if updated_at_column is True:
            updated_at_column = 'updated_at'
        self.updated_at_column = updated_at_column
        if missing_at_column is True:
            missing_at_column = 'missing_at'
        self.missing_at_column = missing_at_column

        foreign_keys_origin_columns = set()
        if foreign_keys:
            self.foreign_key_helpers = []
            for index, fk in enumerate(foreign_keys):
                self.foreign_key_helpers.append(Merge.ForeignKeyHelper(self, index, fk))
                for column in fk.origin_columns:
                    foreign_keys_origin_columns.add(column)
        else:
            self.foreign_key_helpers = []

        self.conversions = conversions
        
        # Prepare main SQL parts and conversions
        self.insert_sql = ""
        self.select_sql = ""
        self.update_sql = ""
        self.update_key_dst_sql = ""
        self.update_key_ret_sql = ""
        self.naive_tzkey = None

        for src_column, dst_column in self.columns.items():
            if not dst_column in foreign_keys_origin_columns:
                self.append_standard_column(src_column, dst_column)
        
        self.append_consts(consts)
        self.append_consts(insert_consts, insert_only=True)
        self.append_consts(scope)
        self.scope = scope # required later (in missing query) contrary to `consts` and `insert_consts`

        for i, helper in enumerate(self.foreign_key_helpers):
            self.append_foreign_key(helper)

        if self.inserted_at_column:            
            self.insert_sql += (", " if self.insert_sql else "") + self.db.escape_identifier(self.inserted_at_column)
            self.select_sql += (", " if self.select_sql else "") + "CURRENT_TIMESTAMP"

        if self.updated_at_column:            
            self.insert_sql += (", " if self.insert_sql else "") + self.db.escape_identifier(self.updated_at_column)
            self.select_sql += (", " if self.select_sql else "") + "CURRENT_TIMESTAMP"
            self.update_sql += (", " if self.update_sql else "") + f"{self.db.escape_identifier(self.updated_at_column)} = CURRENT_TIMESTAMP"       
        
        # Debugging
        self.debug = debug

    #endregion

    #region Returning table

    @cached_property
    def returning_table(self):
        """
        Determine if we need to use an intermediate table for returning inserted/updated values. If yes, return its schema and name.
        """
        if self.key or self.missing_at_column:
            if self.debug:
                self.db.create_schema('debug', if_not_exists=True)
            return self.db.get_new_rand_table_obj('_returning', schema='debug' if self.debug else 'temp')
        else:
            return None
    
    @cached_property
    def returning_key(self):
        """
        Key used to match src table with returning table.
        """
        if not self.returning_table:
            return None
    
        # Find a key that is part of the columns
        if self.key:
            key_headers_by_name = {header.name: header for header in self.db.get_headers(self.dst_table) if header.name in self.key}
            for header in key_headers_by_name.values():
                header.unique = False # a unique constraint might reference columns that are not part of our key
                header.identity = False
                header.primary_key = True
            return list(key_headers_by_name.values())
        else:
            result = []
            for header in self.db.get_headers(self.dst_table):
                if header.primary_key:
                    header.identity = False
                    result.append(header)
            if not result:
                raise ValueError(f"Cannot use `missing_at_column` option: no pk found in {self.dst_table.unsafe}")
            if any(header for header in result if header.name not in self.columns.values()):
                raise NotImplementedError(f"No key given and primary key is not in headers")
            return result
    
    def get_create_returning_table_query(self):
        temp_columns = [*self.returning_key]
        temp_columns.append(Header("_inserted", type=int))
        if self.missing_at_column:
            temp_columns.append(Header("_was_marked_missing", type=int))
        return self.db.get_create_table_query(self.returning_table, temp_columns)

    def clean_returning_table(self):
        if self.debug or not self.returning_table:
            return
        self.db.drop_table(self.returning_table, if_exists=True)

    #endregion
    
    #region SQL helpers

    @property
    def src_headers_by_name(self):
        if self._src_headers_by_name is None:
            self._src_headers_by_name = {h.name: h for h in self.db.get_headers(self.src_table, minimal=True)}
        return self._src_headers_by_name

    def get_conversion_formatter(self, dst_column: str):
        formatter = '{value}'
        conversion = self.conversions.get(dst_column)
        if conversion:
            if isinstance(conversion, Header):
                conversion = self.db.get_sql_type(conversion)
            elif isinstance(conversion, type):
                if issubclass(conversion, Decimal):
                    conversion = self.db.float_sql_basetype # we cannot use decimal because we don't know precision and scale
                else:
                    conversion = self.db.get_sql_type(conversion)
            elif not isinstance(conversion, str):
                raise TypeError(f"conversions[{dst_column}]: {conversion}")
            
            if '{value}' in conversion:
                formatter = conversion
            else:                
                conversion = conversion.lower()
                if conversion.startswith(('float','double','real','decimal','numeric')):
                    formatter = "CAST(replace(replace({value}, ',', '.'), ' ', '') AS "+conversion+")"
                elif conversion == 'timestamptz':
                    if not self.naive_tzkey:
                        if not self.db.tz:
                            raise ValueError("Cannot convert to timestamptz when tz not set")
                        self.naive_tzkey = get_tzkey(self.db.tz)
                    formatter = "CAST(CASE WHEN {value} SIMILAR TO '%[0-9][0-9]:[0-9][0-9]' AND SUBSTRING({value}, length({value})-5, 1) IN ('-', '+') THEN {value}::timestamptz ELSE {value}::timestamp AT TIME ZONE "+self.db.escape_literal(self.naive_tzkey)+" END AS "+conversion+")"
                else:
                    formatter = "CAST({value} AS "+conversion+")"

        return formatter

    def append_standard_column(self, src_column: str, dst_column: str):
        escaped_src_column_name = self.db.escape_identifier(src_column)
        escaped_dst_column_name = self.db.escape_identifier(dst_column)
        src_column_expression = self.get_conversion_formatter(dst_column).format(value=f"src.{escaped_src_column_name}")

        self.insert_sql += (", " if self.insert_sql else "") + escaped_dst_column_name       
        self.select_sql += (", " if self.select_sql else "") + src_column_expression

        if self.key and dst_column in self.key:
            self.update_key_ret_sql += (" AND " if self.update_key_ret_sql else "") + f"ret.{escaped_dst_column_name} = {src_column_expression}"
            self.update_key_dst_sql += (" AND " if self.update_key_dst_sql else "") + f"dst.{escaped_dst_column_name} = {src_column_expression}"
        else:
            self.update_sql += (", " if self.update_sql else "") + f"{escaped_dst_column_name} = {src_column_expression}"

    def append_consts(self, consts: dict[str,Any], *, insert_only = False):
        if not consts:
            return
        
        for column_name, value in consts.items():
            escaped_column_name = self.db.escape_identifier(column_name)
            if value == Header.DEFAULT_NOW:
                escaped_literal = 'CURRENT_TIMESTAMP'
            elif isinstance(value, str) and value.startswith('sql:'):
                escaped_literal = value[len('sql:'):]
            else:
                escaped_literal = self.db.escape_literal(value)

            self.insert_sql += (", " if self.insert_sql else "") + escaped_column_name
            self.select_sql += (", " if self.select_sql else "") + escaped_literal
            if not insert_only:
                self.update_sql += (", " if self.update_sql else "") + f"{escaped_column_name} = {escaped_literal}"

    def append_foreign_key(self, helper: Merge.ForeignKeyHelper):
        origin_column_escaped = self.db.escape_identifier(helper.fk.origin_pk)
        related_pk_escaped = self.db.escape_identifier(helper.fk.related_pk)
        self.insert_sql += (", " if self.insert_sql else "") + origin_column_escaped
        self.select_sql += (", " if self.select_sql else "") + f"tra{helper.num}.{related_pk_escaped}"
        if self.key and helper.fk.origin_pk in self.key:
            self.update_key_ret_sql += (" AND " if self.update_key_ret_sql else "") + f"ret.{origin_column_escaped} = tra{helper.num}.{related_pk_escaped}"
            self.update_key_dst_sql += (" AND " if self.update_key_dst_sql else "") + f"dst.{origin_column_escaped} = tra{helper.num}.{related_pk_escaped}"
        else:
            self.update_sql += (", " if self.update_sql else "") + f"{origin_column_escaped} = tra{helper.num}.{related_pk_escaped}"

    #endregion
    
    #region Insert and update queries
    
    def get_insert_query(self):
        query = f"INSERT INTO {self.dst_table.escaped}"
        query += f" ({self.insert_sql})"
        query += f"\nSELECT {self.select_sql}"
        query += f"\nFROM {self.src_table.escaped} src"
        for helper in self.foreign_key_helpers:
            query += f"\n{helper.get_translate_join_sql()}"
        if self.key:
            query += f"\nON CONFLICT ({', ' .join(self.db.escape_identifier(k) for k in self.key)}) DO NOTHING"
        
        if self.returning_table:
            temp_insert_sql = ', '.join(self.db.escape_identifier(k.name) for k in self.returning_key)
            temp_returning_sql = temp_insert_sql
            temp_select_sql = '*'

            temp_insert_sql += ', _inserted'
            temp_select_sql += ', 1'
            if self.missing_at_column:
                temp_insert_sql += ', _was_marked_missing'
                temp_select_sql += ', 0'

            sub_query = query.replace('\n', '\n\t')
            query = f"WITH sub AS (\n\t{sub_query}\n\tRETURNING {temp_returning_sql}\n)\nINSERT INTO {self.returning_table.escaped} ({temp_insert_sql})\nSELECT {temp_select_sql} FROM sub"

        return query
    
    def get_update_query(self):
        if not self.key:
            return None

        query = f"UPDATE {self.dst_table.escaped} dst"
        query += f"\nSET {self.update_sql}"
        query += f"\nFROM {self.src_table.escaped} src"
        for helper in self.foreign_key_helpers:
            query += f"\n{helper.get_translate_join_sql()}"
        query += f"\nLEFT OUTER JOIN {self.returning_table.escaped} ret ON {self.update_key_ret_sql}" # (join temp table)
        query += f"\nWHERE (ret.{self.db.escape_identifier(self.returning_key[0].name)} IS NULL)" # (exclude inserted rows)
        query += f"\nAND ({self.update_key_dst_sql})" # (match dst and src)

        if self.missing_at_column:
            temp_insert_sql = ', '.join(self.db.escape_identifier(k.name) for k in self.returning_key)
            temp_returning_sql = ', '.join(f'dst.{self.db.escape_identifier(k.name)}' for k in self.returning_key)
            temp_select_sql = '*'

            temp_insert_sql += ', _was_marked_missing'
            temp_returning_sql += f', CASE WHEN dst.{self.db.escape_identifier(self.missing_at_column)} IS NOT NULL THEN 1 ELSE 0 END'
            
            temp_insert_sql += ', _inserted'
            temp_select_sql += ', 0'

            sub_query = query.replace('\n', '\n\t')
            query = f"WITH sub AS (\n\t{sub_query}\n\tRETURNING {temp_returning_sql}\n)\nINSERT INTO {self.returning_table.escaped} ({temp_insert_sql})\nSELECT {temp_select_sql} FROM sub"
        
        return query

    #endregion

    #region Missing and restore queries

    def get_missing_query(self):
        if not self.missing_at_column:
            return None
        
        query = f"UPDATE {self.dst_table.escaped} dst"
        query += f"\nSET {self.db.escape_identifier(self.missing_at_column)} = CURRENT_TIMESTAMP"
        query += f"\nFROM {self.dst_table.escaped} cur"
        query += f"\nLEFT OUTER JOIN {self.returning_table.escaped} ret ON " + ' AND '.join(f"ret.{self.db.escape_identifier(k.name)} = cur.{self.db.escape_identifier(k.name)}" for k in self.returning_key) # (join temp table)
        query += f"\nWHERE (ret.{self.db.escape_identifier(self.returning_key[0].name)} IS NULL AND cur.{self.db.escape_identifier(self.missing_at_column)} IS NULL)" # (exclude inserted and updated rows and rows that are already marked as missing)
        query += f"\nAND ({' AND ' .join(f'dst.{self.db.escape_identifier(k)} = cur.{self.db.escape_identifier(k)}' for k in self.returning_key)})" # (match dst and cur)
        if self.scope:
            query += f"\n AND ({' AND ' .join(f'cur.{self.db.escape_identifier(name)} = {self.db.escape_literal(value)}' for name, value in self.scope.items())})" # (restrict to scope)

        return query

    def get_restore_query(self):
        if not self.missing_at_column:
            return None
        
        query = f"UPDATE {self.dst_table.escaped} dst"
        query += f"\nSET {self.db.escape_identifier(self.missing_at_column)} = null"
        query += f"\nFROM {self.returning_table.escaped} ret"
        query += f"\nWHERE (ret._was_marked_missing = 1)" # (keep only rows that was marked missing)
        query += f"\nAND ({' AND ' .join(f'dst.{self.db.escape_identifier(k)} = ret.{self.db.escape_identifier(k)}' for k in self.returning_key)})" # (match dst and ret)
        
        return query

    #endregion
    
    #region Foreign key utils

    class ForeignKeyHelper:
        def __init__(self, merge: Merge, index: int, foreign_key: LoadForeignKey):
            self.merge = merge
            self.db = merge.db
            self.num = index + 1
            self.fk = foreign_key

        @cached_property
        def translate_table(self):
            if self.merge.debug:
                self.db.create_schema('debug', if_not_exists=True)
            return self.db.get_new_rand_table_obj(f'_translate{self.num}', schema='debug' if self.merge.debug else 'temp')
    
        def find_src_column(self, column):
            for a, b in self.merge.columns.items():
                if column == b:
                    return a
            return column
        
        @cached_property
        def src_columns_escaped(self):
            return [self.db.escape_identifier(self.find_src_column(column)) for column in self.fk.origin_columns]

        @cached_property
        def src_columns_sql(self):
            return ', '.join(f"src.{column}" for column in self.src_columns_escaped)

        def get_notnull_sql(self, op = 'AND'):
            return f' {op} '.join(f"src.{column_escaped} IS NOT NULL" for column_escaped in self.src_columns_escaped)

        def get_translate_join_sql(self, alias = 'tra{num}'):
            alias = alias.format(num=self.num)
            sql = f"LEFT OUTER JOIN {self.translate_table.escaped} {alias} ON "
            for i, column in enumerate(self.fk.origin_columns):
                src_column_escaped = self.src_columns_escaped[i]
                src_column_expression = self.merge.get_conversion_formatter(column).format(value=f"src.{src_column_escaped}")
                sql += (" AND " if i > 0 else "") + f"{alias}.{self.db.escape_identifier(column)} = {src_column_expression}"
            return sql

        def get_related_join_sql(self, alias = 'rel{num}'):
            alias = alias.format(num=self.num)
            sql = f"LEFT OUTER JOIN {self.fk.related_table.escaped} {alias} ON "
            for i, column in enumerate(self.fk.origin_columns):
                src_column_escaped = self.src_columns_escaped[i]
                src_column_expression = self.merge.get_conversion_formatter(column).format(value=f"src.{src_column_escaped}")
                sql += (" AND " if i > 0 else "") + f"{alias}.{self.db.escape_identifier(self.fk.related_columns[i])} = {src_column_expression}"
            return sql

        def get_translate_query(self):
            query = f"INSERT INTO {self.translate_table.escaped}"
            query += f"\nSELECT {self.src_columns_sql}, rel{self.num}.{self.db.escape_identifier(self.fk.related_pk)}"
            query += f"\nFROM ("
            query += f"\n\tSELECT {self.src_columns_sql}"
            query += f"\n\tFROM {self.merge.src_table.escaped} src"
            query += f"\n\tWHERE ({self.get_notnull_sql('AND')})"
            query += f"\n\tGROUP BY {self.src_columns_sql}"
            query += f"\n) src"
            query += f"\n{self.get_related_join_sql()}"
            #ROADMAP: would a src->dst columns translation be required?
            return query
        
        def get_check_query(self):
            if self.fk.optional:
                return None
            
            query = f"SELECT {self.src_columns_sql}"
            query += f"\nFROM {self.merge.src_table.escaped} src"
            query += f"\n{self.get_translate_join_sql()}"
            query += f"\nWHERE ({self.get_notnull_sql('OR')})"
            query += f"\nAND (tra{self.num}.{self.db.escape_identifier(self.fk.related_pk)} IS NULL)"
            query += f"\nGROUP BY {self.src_columns_sql}"
            return query

        def get_create_translate_table_query(self):            
            columns = []
            for column in self.fk.origin_columns:
                src_column = self.find_src_column(column)
                src_header = self.merge.src_headers_by_name.get(src_column)
                sql_type = src_header.sql_type if src_header else None
                columns.append(Header(column, sql_type=sql_type, primary_key=True))
            columns.append(Header(self.fk.related_pk, sql_type=self.db.get_sql_type(self.fk.pk_type)))
            return self.db.get_create_table_query(self.translate_table, columns)

        def clean_translate_table(self):
            if self.merge.debug:
                return
            self.db.drop_table(self.translate_table, if_exists=True)

    #endregion

    def steps(self, op: Operation):
        op.set_count('fk_issue_count', 0)

        for helper in self.foreign_key_helpers:
            op.add_message(f"Create translate table for fk{helper.num}: {helper.fk} …", separator=True)
            op.query(helper.get_create_translate_table_query())

            op.add_message(f"Translate fk{helper.num} …")
            op.query(helper.get_translate_query())
            
            if not helper.fk.optional:
                op.add_message(f"Check fk{helper.num}: {helper.fk} …")
                op.resulting_query(helper.get_check_query(),
                    f"%s key(s) not found for {helper.fk}", 'fk_issue_count', result_increment=True)

        with op.check_step('fk_issue_count', 0, f"%s forein key(s) missing"):
            if self.returning_table:
                msg = f"Create returning table"
                if self.key:
                    msg += f" for key: {self.key}"
                else:
                    msg += f" for {self.missing_at_column}"
                msg += " …"
                op.add_message(msg, separator=True)
                op.query(self.get_create_returning_table_query())
            
            op.add_message(f"Insert new {self.dst_table.unsafe} rows …", separator=True)
            op.query(self.get_insert_query(),
                f"Inserted: %s {self.dst_table.unsafe} rows", 'inserted_count')
                
            if self.key:
                op.add_message(f"Update existing {self.dst_table.unsafe} rows …")
                op.query(self.get_update_query(),
                    f"Updated: %s {self.dst_table.unsafe} rows", 'updated_count')
            
            if self.missing_at_column:
                op.add_message(f"Mark missing {self.dst_table.unsafe} rows …", separator=True)
                op.query(self.get_missing_query(),
                    f"Missing: %s {self.dst_table.unsafe} rows", 'missing_count')

                op.add_message(f"Mark restored {self.dst_table.unsafe} rows …")
                op.query(self.get_restore_query(),
                    f"Restored: %s {self.dst_table.unsafe} rows", 'restored_count')
        
        # ROADMAP: perform clean-up steps
        # self.clean_returning_table()
        # for helper in self.foreign_key_helpers:
        #     helper.clean_translate_table()

    def get_procedure_sql(self, name: str|tuple|DbObj):
        raise NotImplementedError() # This is currently only a preview
        op = Operation(self.db, for_procedure=True)
        self.steps(op)
        return op.get_procedure_sql(name)
    
    def execute(self) -> LoadResult:
        op = Operation(self.db)
        with self.db.transaction() if not self.debug else nullcontext():
            self.steps(op)
            return LoadResult(op)


def get_auto_key(db: Db,
                    target: str|tuple|type|DbObj|list[Header],
                    *,
                    headers: list[str|Header|None]|str|os.PathLike|TextIO|None = None, # headers or CSV file
                    columns: dict[str,str|None]|Literal['snake']|None = None, # translation of headers into column names
                    # For determining headers from `headers` argument if this is actually a file
                    encoding = 'utf-8',
                    delimiter: str = None,
                    quotechar = '"') -> AutoKeyCache:

    delimiter: str|None = None
    target_table_exists: bool = None
    target_headers_by_name: dict[str,Header] = None

    if headers:
        if isinstance(headers, (str,os.PathLike,IOBase)):
            csv_file = headers
            header_names, delimiter, _ = examine_csv_file(csv_file, encoding=encoding, delimiter=delimiter, quotechar=quotechar, force_delimiter=False)                
            actual_headers = [Header(name) for name in header_names] if header_names else None
            if not delimiter:
                delimiter = get_default_csv_delimiter()
        else:
            actual_headers = [header if isinstance(header, Header) else Header(header) for header in headers if headers]
    else:
        actual_headers = None

    if isinstance(target, (str,tuple,type)):
        target = db.parse_obj(target)
    if isinstance(target, DbObj): # This is actually a table                
        target_table_exists = db.table_exists(target)
    
    if target_table_exists is False:
        key = ()
    else:
        target_headers_by_name = _get_target_headers_by_name(db, target)
        key = _select_auto_key(target_headers_by_name.values(), actual_headers=actual_headers, actual_header_columns=columns)

    result = AutoKeyCache(key)
    result._headers = actual_headers
    result._delimiter = delimiter
    result._target = target
    result._target_table_exists = target_table_exists
    result._target_headers_by_name = target_headers_by_name
    return result


class AutoKeyCache(Tuple[str]):
    def __init__(self, *args):
        self._headers: list[Header]|None = None
        self._delimiter: str|None = None
        self._target: DbObj|list[Header]|None = None
        self._target_table_exists: bool = None
        self._target_headers_by_name: dict[str,Header] = None


def _get_target_headers_by_name(db: Db, target: str|tuple|type|DbObj|list[Header]) -> dict[str,Header]:
        """
        Get the headers of the given target model: can be a Django model, the name (or tuple) of a table, or a list of columns.
        """
        if isinstance(target, list):
            by_name = {}
            for column in target:
                if not isinstance(column, Header):
                    column = Header(column)
                by_name[column.name] = column
            return by_name
        else:
            return {header.name: header for header in db.get_headers(target)}


def _select_auto_key(target_headers: Iterable[Header], *, actual_headers: Iterable[Header]|None = None, actual_header_columns: dict[str,str|None]|Literal['snake']|None = None,) -> tuple[str]:
    actual_available_columns: list[str] = []
    if actual_headers:
        for header in actual_headers:
            column = header.name
            if actual_header_columns:
                if isinstance(actual_header_columns, dict):
                    column = actual_header_columns.get(column)
                elif actual_header_columns == 'snake':
                    column = slugify_snake(column)
                else:
                    raise TypeError(f"actual_header_columns: {type(actual_header_columns).__name__}")
            
            if column:
                actual_available_columns.append(column)

    def convert_to_actual_columns(key: tuple[str]):
        if not actual_headers:
            return key
        
        actual_key = []
        for column in key:
            if column in actual_available_columns:
                actual_key.append(column)
            elif column.endswith('_id'):
                base = column[:-len('_id')]
                if base in actual_available_columns:
                    actual_key.append(base)
                else:
                    found = False
                    for name in actual_available_columns:
                        if name.startswith(f'{base}_'):
                            found = True
                            actual_key.append(name)
                    if not found:
                        return None
            else:
                return None
        
        return tuple(actual_key)
    
    # Search primary key
    pk = {header.name for header in target_headers if header.primary_key}
    if pk and all(column in actual_available_columns for column in pk):
        return pk
    
    # Search unique keys
    for header in target_headers:
        if header.unique:
            if header.identity:
                continue

            if header.unique is True:
                keys = [(header.name,)]
            elif header.unique:
                keys = header.unique

            for key in keys:
                actual_key = convert_to_actual_columns(key)
                if actual_key:
                    return actual_key
    
    return ()


def _get_load_foreign_keys(db: Db, load_table: str|type|tuple|DbObj, load_columns: Iterable[str|None]):
    results: list[LoadForeignKey] = []

    if isinstance(load_table, type):
        from django.db.models import Field, ForeignKey

        from zut.db.django import get_django_field_python_type
        field: Field
        for field in load_table._meta.fields:
            if isinstance(field, ForeignKey):
                prefix = f"{field.name}_"
                origin_columns = [column for column in load_columns if column and column.startswith(prefix)]
                if origin_columns:
                    results.append(LoadForeignKey(origin_columns=origin_columns,
                                                related_table=field.related_model,
                                                related_pk=field.related_model._meta.pk.attname,
                                                pk_type=get_django_field_python_type(field.related_model._meta.pk) or str,
                                                origin_pk=field.attname,
                                                nullable=field.null))

    else:
        load_table = db.parse_obj(load_table)

        query = f"""SELECT
    kcu.column_name AS origin_pk
    ,col.is_nullable AS origin_is_nullable
    ,tc.constraint_name AS constraint_name
    ,ccu.table_schema AS related_schema
    ,ccu.table_name AS related_table
    ,ccu.column_name AS related_pk 
    ,col.data_type AS pk_type
FROM information_schema.table_constraints AS tc 
INNER JOIN information_schema.key_column_usage AS kcu ON tc.constraint_name = kcu.constraint_name AND tc.table_schema = kcu.table_schema
INNER JOIN information_schema.columns AS col ON col.table_catalog = kcu.table_catalog AND col.table_schema = kcu.table_schema AND col.table_name = kcu.table_name AND col.column_name = kcu.column_name
INNER JOIN information_schema.constraint_column_usage AS ccu ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_schema = {db.escape_literal(load_table.schema or db.default_schema)} AND tc.table_name = {db.escape_literal(load_table.name)}"""
        
        for row in db.get_rows(query):
            prefix = row['origin_pk'].removesuffix('_id') + '_'
            origin_columns = [column for column in load_columns if column and column.startswith(prefix)]
            if origin_columns:
                results.append(LoadForeignKey(origin_columns=origin_columns,
                                            related_table=DbObj(row['related_table'], row['related_schema'], type(db)),
                                            related_pk=row['related_pk'],
                                            origin_pk=row['origin_pk'],
                                            pk_type=db.get_type(row['pk_type']) or str,
                                            optional=row['origin_is_nullable'] == 'YES'))

        return results


class Operation: #ROADMAP: Load and Merge should inherit from me
    def __init__(self, db: Db, *, for_procedure = False, debug_queries = False):
        self.db = db
        self._procedure_inner_sql = '' if for_procedure else None
        self._counts: dict[str,int|bool] = {}
        self._ignoring_depth = 0

    def get_procedure_sql(self, name: str|tuple|DbObj):
        name = self.db.parse_obj(name)

        sql = f"CREATE OR REPLACE PROCEDURE {name.escaped}() AS $$"
        if self._counts:
            sql += f"\nDECLARE"
            for key in self._counts:
                sql += f"\n\t_{key} bigint;"
        sql += f"\nBEGIN"
        inner_sql = self._procedure_inner_sql.replace('\n', '\n\t')
        sql += f"\n{inner_sql}"
        sql += f"\nEND $$ LANGUAGE plpgsql;"

        return sql
    
    @property
    def for_execute(self):
        return self._procedure_inner_sql is None

    @property
    def for_procedure(self):
        return self._procedure_inner_sql is not None
    
    @property
    def do_for_execute(self):
        return self._procedure_inner_sql is None and self._ignoring_depth == 0
    
    def execute_query(self, sql: str, *, result = False):
        if self.db._logger.isEnabledFor(logging.DEBUG):
            self.db._logger.debug('Execute query:\n\t' + sql.replace('\n', '\n\t'))

        return self.db.execute(sql, result=result)

    def append_procedure_line(self, sql: str):
        inner_sql = '\t' * self._ignoring_depth
        self._procedure_inner_sql += f"\n{inner_sql}{sql}"
    
    def set_count(self, key: str, value: int|str, *, increment = False):
        if self.for_execute:
            if increment:
                value = self._counts.get(key) or 0
            self._counts[key] = value
        elif self.for_procedure:
            self._counts[key] = True
            self.append_procedure_line(f"_{key} := {value}{f' + _{key}' if increment else ''};")

    def get_count(self, key: str):
        if self.for_execute:
            return self._counts.get(key)
        elif self.for_procedure:
            raise ValueError("Cannot use get_count in procedure mode")
    
    def add_message(self, message: str, *keys: int|str, separator = False, if_non_zero: int|str|bool|None = None, level = logging.DEBUG):
        if if_non_zero is True:
            if_non_zero = keys[0]

        if self.do_for_execute:
            if not (isinstance(if_non_zero, int) and if_non_zero == 0):
                self.db._logger.log(level, message, *keys)

        elif self.for_procedure:
            if separator:
                self.append_procedure_line("--------------------------------------------------")
            
            key_sql = ''
            if keys:
                key_holders = []
                for key in keys:
                    key_sql += f', _{key}'
                    key_holders.append('%')
                message = message % key_holders

            if isinstance(if_non_zero, str):
                self.append_procedure_line(f"IF _{if_non_zero} != 0 THEN")
            increment = '\t' if isinstance(if_non_zero, str) else ''
            self.append_procedure_line(f"{increment}RAISE NOTICE {self.db.escape_literal(f'{logging.getLevelName(level)}: {message}')}{key_sql};")
            if isinstance(if_non_zero, str):
                self.append_procedure_line(f"END IF;")

    @contextmanager
    def check_step(self, key: str, expected_value: int, error_title: str|None = None, *, error_level = logging.ERROR):
        if not isinstance(expected_value, int):
            raise TypeError(f'expected_value: {type(expected_value).__name__}')
        
        try:
            if self.do_for_execute:
                value = self.get_count(key)
                if value != expected_value:
                    if error_title:
                        self.add_message(error_title, value, level=error_level)
                    self._ignoring_depth += 1
            elif self.for_procedure:
                self.append_procedure_line(f"\nIF _{key} != {expected_value} THEN")
                if error_title:
                    self.add_message(error_title, 'key', expected_value, level=error_level)
                self.append_procedure_line(f"\nELSE -- _{key} = {expected_value}")
                self._ignoring_depth += 1
            yield
        finally:
            self._ignoring_depth -= 1
            if self.for_procedure:
                self.append_procedure_line(f"\nEND IF -- _{key} = {expected_value}")

    def query(self, query: str, result_title: str|None = None, result_key: str|None = None, result_increment = False, *, result_level = logging.DEBUG):
        if self.do_for_execute:
            affected_count = self.execute_query(query)
            if result_key:
                self.set_count(result_key, affected_count, increment=result_increment)
            if result_title:
                self.add_message(result_title, affected_count, level=result_level)
        
        elif self.for_procedure:
            self.append_procedure_line(f"\n{query}")
            if result_title or result_key:
                self.append_procedure_line(f"\nGET DIAGNOSTICS _affected_count := ROW_COUNT;")
            if result_key:
                self.set_count(result_key, 'affected_count', increment=result_increment)
            if result_title:
                self.add_message(result_title, 'affected_count', level=result_level)
    
    def resulting_query(self, query: str, result_title: str|None = None, result_key: str|None = None, result_increment = False, *, result_level = logging.WARNING):
        if self.do_for_execute:
            with self.execute_query(query, result=True) as result:
                result_count = result.length
                if result_key:                       
                    self.set_count(result_key, result_count, increment=result_increment)
                if result:
                    message = result_title % f'{result_count:,}' + '\n'
                    tab = result.tabulate()
                    message += tab[0:1000] + ('…' if len(tab) > 1000 else '')
                    self.add_message(message, level=result_level)
            
        elif self.for_procedure:
            self._counts['result_count'] = True
            self.append_procedure_line(f"\nSELECT COUNT(*) INTO _result_count FROM ({query})")
            if result_key:
                self.set_count(result_key, 'result_count', increment=result_increment)
            if result_title:
                self.add_message(result_title, 'result_count', if_non_zero=True, level=result_level)


class LoadResult:
    inserted_count: int
    updated_count: int|None
    missing_count: int|None
    restored_count: int|None

    def __init__(self, op: Operation|None = None):
        self.inserted_count = (op.get_count('inserted_count') or 0) if op else 0
        self.updated_count = op.get_count('updated_count') if op else None
        self.missing_count = op.get_count('missing_count') if op else None
        self.restored_count = op.get_count('restored_count') if op else None

    @property
    def upserted_count(self):
        return self.inserted_count + (self.updated_count if self.updated_count is not None else 0)

    def __str__(self):
        if self.updated_count is not None:
            result = f"upserted: {self.upserted_count:,} (inserted: {self.inserted_count:,} - updated: {self.updated_count:,})"

        if self.missing_count is not None:
            result += f' - missing: {self.missing_count:,}'
        if self.restored_count is not None:
            result += f' - restored: {self.restored_count:,}'
        return result


class LoadForeignKey:
    def __init__(self, origin_columns: str|Iterable[str], related_table: str|tuple[str|None,str]|type|DbObj, *, related_columns: str|Iterable[str] = None, related_pk: str = 'id', pk_type = int, origin_pk: str = None, nullable = False, optional = False):
        """
        - `origin_columns`: columns of the merge source (CSV file, potentially snaked-cased).
        - `related_table`: table containing source data used to perform the translation
        - `related_columns`: columns in the related table matching `source_columns`
        - `related_pk`: target column in the related table
        - `origin_pk`: name of the column to use as the remplacement of the origin columns (will contain values found in `related_pk`)

        - `nullable`: origin data may be null, but if it is not null, matching foreign key must exist in the target table
        - `optional`: matching foreign key may not exist in the target table
        """
        if isinstance(origin_columns, str):
            self.origin_columns = (origin_columns,)
        else:
            self.origin_columns = tuple(column for column in origin_columns)

        self.related_table = related_table if isinstance(related_table, DbObj) else DbObj.parse(related_table)
        
        source_prefix = self._find_source_prefix()

        if related_columns:
            if isinstance(related_columns, str):
                self.related_columns = (related_columns,)
            else:
                self.related_columns = tuple(column for column in related_columns)
            if len(self.related_columns) != len(self.origin_columns):
                raise ValueError(f"{len(related_columns)} foreign_columns for {len(origin_columns)} columns")
        else:
            self.related_columns = tuple(column[len(source_prefix):] for column in self.origin_columns)            

        self.related_pk = related_pk
        self.pk_type = pk_type

        if origin_pk:
            self.origin_pk = origin_pk
        elif source_prefix:
            self.origin_pk = f'{source_prefix}{self.related_pk}'
        else:
            self.origin_pk = f'{self.related_table.name}_{self.related_pk}'

        self.nullable = nullable
        self.optional = optional


    def __repr__(self):
        return f"LoadForeignKey({', '.join(self.origin_columns)}) -> {self.origin_pk}: {self.related_table.unsafe}({', '.join(self.related_columns)}) -> {self.related_pk} ({self.pk_type.__name__})" + (f" (nullable)" if self.nullable else "")


    def _find_source_prefix(self):        
        size = len(self.origin_columns)

        # if size is 0, return empty string 
        if (size == 0):
            raise ValueError("Source columns cannot be empty")

        if (size == 1):
            foreign_table_prefix = f"{self.related_table.name}_"
            if self.origin_columns[0].startswith(foreign_table_prefix): # e.g. source_column 'cluster_name', foreign table 'cluster'
                return foreign_table_prefix
            
            pos = self.related_table.name.rfind('_')
            if pos > 0:
                part_prefix = f"{self.related_table.name[pos+1:]}_"
                if self.origin_columns[0].startswith(part_prefix): # e.g. source_column 'cluster_name', foreign table 'vmware_cluster':
                    return part_prefix

            return ''

        # sort the array of strings 
        values = sorted(self.origin_columns)
        
        # find the minimum length from first and last string 
        end = min(len(values[0]), len(values[size - 1]))

        # find the common prefix between  the first and last string 
        i = 0
        while (i < end and values[0][i] == values[size - 1][i]):
            i += 1

        prefix = values[0][0: i]
        return prefix
