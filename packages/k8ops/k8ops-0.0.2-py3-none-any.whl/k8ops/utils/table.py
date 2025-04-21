import logging
from dataclasses import dataclass, fields, is_dataclass
from typing import Any, Callable, Dict, List, Optional, Sequence, Type, TypeVar, Union

from tabulate import tabulate as tabulate_func

T = TypeVar("T")


@dataclass
class ColumnDefinition:
    field_name: str
    column_name: str = ""
    formatter: Optional[Callable[[Any, Any], str]] = None
    default: Any = None


def table_view(cls: Type[T]) -> Type[T]:
    if not is_dataclass(cls):
        raise ValueError("The class must be a dataclass")

    column_dict: Dict[str, ColumnDefinition] = {}
    for f in fields(cls):
        column_name = f.metadata.get("column", f.name)
        column_dict[column_name] = ColumnDefinition(
            field_name=f.name, column_name=column_name, formatter=f.metadata.get("formatter"), default=f.default
        )
    setattr(cls, "__table_columns__", column_dict)
    return cls


def retrieve_columns(cls: Type[Any]) -> Dict[str, ColumnDefinition]:
    """
    Retrieve the column definitions for a table view class.
    """
    if hasattr(cls, "__table_columns__"):
        return getattr(cls, "__table_columns__")
    return {}


@dataclass
class Column:
    name: str
    prefix: str = ""
    suffix: str = ""
    virtual: bool = False
    formatter: Optional[Callable[[Any, Any], str]] = None


def to_row(obj: Any, expected_columns: Sequence[Union[str, Column]]) -> List[str]:
    """
    Convert a table view object to a list of its field values.
    """
    if not obj:
        raise ValueError("Object cannot be None")

    if not expected_columns:
        raise ValueError("Columns list cannot be empty")

    table_columns = retrieve_columns(obj.__class__)
    if not table_columns:
        raise ValueError("Object is not a table view class")

    row: List[str] = []
    for col in expected_columns:
        col_name = col if isinstance(col, str) else col.name
        virtual = False
        formatter: Optional[Callable[[Any, Any], str]] = None
        if isinstance(col, Column):
            virtual = col.virtual
            col_name = col.name
            formatter = col.formatter

        if not virtual:
            if col_name not in table_columns:
                raise ValueError(f"Column '{col_name}' is not defined in the table view class")

            data = getattr(obj, table_columns[col_name].field_name)
            if data is None:
                data = table_columns[col_name].default

            if data is None:
                row.append("")
                continue
            formatter = formatter or table_columns[col_name].formatter
        else:
            data = getattr(obj, col_name, None)

        if formatter:
            try:
                data = formatter(data, obj)
            except Exception as e:
                raise ValueError(f"Formatter error for column '{col_name}': {e}")
        row.append(str(data) if data is not None else "")
    return row


def tabulate(
    headers: Sequence[Union[str, Column]],
    data: List[List[Any]],
    tablefmt: str = "simple",
    lineprefix: str = "",
    showindex: bool = True,
) -> str:
    """
    Format the data into a table using the specified format.
    """
    headers0 = [col.prefix + col.name + col.suffix if isinstance(col, Column) else col for col in headers]
    table = tabulate_func(
        data,
        headers=headers0,
        tablefmt=tablefmt,
        numalign="right",
        stralign="left",
        floatfmt=".2f",
        showindex=showindex,
    )
    if lineprefix:
        table = "\n".join([lineprefix + line for line in table.splitlines()])
    return table


def print_table(
    headers: Sequence[Union[str, Column]],
    data: List[Any],
    format: str = "simple",
    lineprefix: str = "",
):
    """Print the data to the specified format"""
    data = [to_row(item, headers) for item in data]
    logging.info(tabulate(headers, data, tablefmt=format, lineprefix=lineprefix))
