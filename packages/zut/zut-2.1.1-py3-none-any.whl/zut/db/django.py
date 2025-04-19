from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Iterable
from django.db import models
from django.contrib.postgresql.field import ArrayField
from zut import Header


def get_headers_from_django_model(model, *, minimal = False) -> Iterable[Header]:
    from django.db import models

    field: models.Field
    
    headers: dict[str,Header] = {}

    for field in model._meta.fields:
        header = Header(field.attname)

        _type = get_django_field_python_type(field)
        if _type:
            header.type = _type
            if isinstance(field, models.DecimalField):
                header.precision = field.max_digits
                header.scale = field.decimal_places
            elif isinstance(field, models.CharField):
                header.precision = field.max_length

        header.not_null = not field.null

        if field.primary_key:
            header.primary_key = True
        if field.unique:
            header.unique = True

        headers[header.name] = header

    if not minimal:
        unique_keys = get_django_model_unique_keys(model)
        for key in unique_keys:
            if len(key) == 1:
                header = headers[key[0]]
                header.unique = True
            else:
                for field in key:
                    header = headers[field]
                    if not headers[field].unique:
                        header.unique = [key]
                    elif not headers[field].unique is True:
                        header.unique.append(key)

    return headers.values()


def get_django_field_python_type(field) -> type|None:
    if isinstance(field, models.BooleanField):
        return bool
    elif isinstance(field, models.IntegerField):
        return int
    elif isinstance(field, models.FloatField):
        return float
    elif isinstance(field, models.DecimalField):
        return Decimal
    elif isinstance(field, models.DateTimeField):
        return datetime
    elif isinstance(field, models.DateField):
        return date
    elif isinstance(field, models.CharField):
        return str
    elif isinstance(field, models.TextField):
        return str
    elif isinstance(field, ArrayField):
        return list
    else:
        return None # we don't want to make false assumptions (e.g. we would probably want 'str' in the context of a load table and 'int' for a foreign key field)


def get_django_model_unique_keys(model) -> list[tuple[str]]:
    """
    Report django model unique keys, based on attnames (column names).
    """
    field_orders: dict[str,int] = {}
    attnames_by_name: dict[str,str] = {}

    class Unique:
        def __init__(self, fields: list[str]|tuple[str]|str):
            if isinstance(fields, str):
                self.fields = [fields]
            elif isinstance(fields, (list,tuple)):
                self.fields: list[str] = []
                for i, name in enumerate(fields):
                    if isinstance(name, str):
                        if not name in field_orders:
                            name = attnames_by_name[name]
                        self.fields.append(name)
                    else:
                        raise TypeError(f"fields[{i}]: {type(name).__name__}")  
            else:
                raise TypeError(f"fields: {type(fields).__name__}")            
            
            self.min_field_order = min(field_orders[field] for field in self.fields)

        def append(self, field: str):
            self.fields.append(field)
            if field_orders[field] < self.min_field_order:
                self.min_field_order = field_orders[field]

    primary_key: Unique = None
    other_keys: list[Unique] = []

    for i, field in enumerate(model._meta.fields):
        field_orders[field.attname] = i
        attnames_by_name[field.name] = field.attname
        
        if field.primary_key:
            if not primary_key:
                primary_key = Unique(field.attname)
            else:
                primary_key.append(field.attname)
        elif field.unique:
            other_keys.append(Unique(field.attname))

    for names in model._meta.unique_together:
        other_keys.append(Unique(names))

    for constraint in model._meta.constraints:
        if isinstance(constraint, models.UniqueConstraint):
            other_keys.append(Unique(constraint.fields))

    results = []
    
    if primary_key:
        results.append(tuple(primary_key.fields))

    for key in sorted(other_keys, key=lambda key: key.min_field_order):
        results.append(tuple(key.fields))

    return results
